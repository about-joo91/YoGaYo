""" 모듈 불러오기 """
import hashlib
import base64
import math
import random
import json
from io import BytesIO
from datetime import datetime, timedelta
from functools import wraps
import certifi
from pymongo import MongoClient
import tensorflow as tf
from PIL import Image
import numpy as np
from bson.objectid import ObjectId
from flask_cors import CORS
import jwt
from flask import jsonify, Flask, render_template, request, abort
from class_name import CLASS_NAME

model = tf.keras.models.load_model('static/model/model.h5')
app = Flask(__name__)
client = MongoClient(
    'mongodb+srv://test:1234567890@cluster0.qwbpf.mongodb.net/?retryWrites=true&w=majority',
 tlsCAFile=certifi.where())
db = client.sparta
cors = CORS(app, resources={r"*": {"origins" : "*"}})

SECRET_KEY = 'YoGaYo'

def authrize(func):
    """토큰 검사 데코레이트 함수"""
    @wraps(func)
    def decorated_function(*args, **kws):
        if not 'mytoken' in request.cookies:
            abort(401)
        user = None
        token = request.cookies['mytoken']
        try:
            user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            abort(401)
        return func(user, *args, **kws)
    return decorated_function



@app.route('/login_page')
def join():
    """ 로그인 화면 """
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def sign_in():
    """ 로그인 정보를 토큰에 담아서 클라이언트로 보냄 """
    data = json.loads(request.data)
    user_email_receive = data.get("user_email_give")
    user_password_receive = data.get("user_password_give")
    hashed_pw = hashlib.sha256(user_password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'email':user_email_receive, 'password': hashed_pw})

    if result:
        payload = {
            'id' : str(result.get('_id')),
            'email':result.get('email'),
            'exp' : datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'result': 'success',
            'token': token,
            'msg': '로그인 성공이셔요'
        })
    return jsonify({
        'result':'fail',
        'msg': '아이디/비밀번호가 기억 안나셔요?'
    })


@app.route('/sign_up_page')
def login():
    """ 회원가입 화면 """
    return render_template('join.html')


@app.route('/sign_up', methods=["POST"])
def check():
    """ 회원가입 정보를 db에 저장 """
    data = json.loads(request.data)
    user_email_receive = data.get("user_email_give")
    nick_name_receive = data.get("nick_name_give")
    user_password_receive = data.get("user_password_give")
    hashed_password = hashlib.sha256(user_password_receive.encode('utf-8')).hexdigest()

    user_check = {
        'email' : user_email_receive
    }
    nick_check = {
        'nick' : nick_name_receive
    }

    check_email = db.user.find_one(user_check)
    check_nick = db.user.find_one(nick_check)
    if check_email:
        return jsonify ({
            "result": "fail",
            'msg': '이메일이 중복이셔요',
            'url' : '/sign_up'
        })

    if check_nick:
        return jsonify ({
            "result": "fail",
            'msg': '닉네임이 중복이셔요',
            'url' : '/sign_up'
        })
    doc = {
        "email" : user_email_receive,
        "nick" : nick_name_receive,
        "password" : hashed_password,
        }
    db.user.insert_one(doc)
    return jsonify({
        "result": "success",
        'msg' : '회원가입 완료셔요',
        'url' : "/login"
    })
@app.route('/')
@authrize
def home(user):
    """ 메인 화면"""
    if user:
        posts = list(db.yoga_post.find({'user_name' : ObjectId(user.get('id'))}))
        recent_thr_pose = [post.get('acting_name') for post in posts[:4]]
        recommend_poses = list(filter(lambda x: x not in recent_thr_pose, CLASS_NAME))
        ran_num = random.randrange(0, len(recommend_poses)-1)
        url = '../static/images/class/'+ recommend_poses[ran_num] + '/img.png'

        doc = {
            'class_name' : recommend_poses[ran_num],
            'url' : url,
        }
        return render_template('main.html', recommend = doc)
    return jsonify({'result' : 'fail', 'msg': '로그인을 하셔요'})


@app.route('/fileupload', methods=['POST'])
@authrize
def file_upload(user):
    """ 파일을 업로드 """
    if user:
        title_receive = request.form['title_give']
        file = request.files['file_give']
        buffered = BytesIO()
        extension = file.filename.split('.')[-1]
        file_format = 'JPEG' if extension.lower() == 'jpg' else extension.upper()

        img = Image.open(file)
        img.save(buffered, file_format)
        image_base64 = base64.b64encode(buffered.getvalue())
        img = img.convert("RGB")

        resize_img = img.resize((224, 224))
        input_arr = tf.keras.preprocessing.image.img_to_array(resize_img)
        prediction = model.predict(np.array([input_arr]))
        class_num = np.argmax(prediction)
        acc = str(math.floor(prediction[0][class_num] * 100))
        class_name = CLASS_NAME[class_num]

        doc = {
            'content': title_receive,
            'yoga_img': image_base64,
            'datetime': datetime.utcnow(),
            'acc': acc,
            'acting_name': class_name,
            'user_name' : ObjectId(user.get('id'))
        }

        db.yoga_post.insert_one(doc)


        return jsonify({'result': 'success', 'msg' : '다이어리에서 당신의 정확도를 확인하세요!!'})
    return jsonify({'result' : 'fail', 'msg': '로그인을 하셔요'})

@app.route("/diary")
@authrize
def diary_page(user):
    """ 다이어리 화면 """
    if user:
        user_name = db.user.find_one({"_id": ObjectId(user.get('id'))},{'password':0})
        posts = list(db.yoga_post.find({"user_name" : ObjectId(user.get('id'))}))
        
        for post in posts:
            post['datetime'] = post['datetime'].strftime("%x")
            post['yoga_img'] = post['yoga_img'].decode('utf-8')
        posts = sorted(posts, key=lambda x:x['datetime'], reverse=True)
        
        return render_template("diary.html",user_name = user_name, posts = posts)
    return jsonify({'result' : 'fail', 'msg': '로그인을 하셔요'})

@app.route("/diary/acc")
@authrize   
def get_acc(user):
    """ 그래프화면에 넣어줄 정확도를 불러옴 """
    if user:
        posts = list(db.yoga_post.find({"user_name" : user.get('_id')}))
        posts = sorted(posts, key=lambda x:x['datetime'], reverse=True)
        posts_acc = [post.get('acc') for post in posts[0:6]]
        return jsonify({"result" : "success", "posts_acc" : posts_acc})
    return jsonify({'result' : 'fail', 'msg': '로그인을 하셔요'})


@app.route("/diary/edit", methods = ["POST"])
@authrize
def edit_post(user):
    """ 포스트를 수정 """
    if user:
        data = json.loads(request.data)
        doc = {
            'content' : data.get('edit_texts_give', None),
        }
        post_id = {
            'post_id' : data.get('post_id_give', None)
        }
        db.yoga_post.update_one({'_id' :ObjectId(post_id.get('post_id')) }, {'$set':doc})
        return jsonify({"result" : "success", "msg" : "수정되었습니다!"})
    return jsonify({'result' : 'fail', 'msg': '로그인을 하셔요'})

@app.route("/diary/delete", methods = ["POST"])
@authrize
def delete_post(user):
    """ 포스트를 지움 """
    if user:
        data = json.loads(request.data)
        post_id = {
            "post_id" : data.get("post_id_give", None)
        }
        db.yoga_post.delete_one({"_id" :ObjectId(post_id.get("post_id"))})
        return jsonify({"result" : "success", "msg" : "삭제되었습니다!"})
    return jsonify({"result" : "fail", "msg": "로그인을 하셔요"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
