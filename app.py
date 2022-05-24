from flask import jsonify, Flask, render_template, request, Response, abort
from datetime import datetime, timedelta
from pymongo import MongoClient
import codecs
import tensorflow as tf
import json
from PIL import Image
import numpy as np
from bson.objectid import ObjectId
from flask_cors import CORS
import base64
import jwt
import hashlib
import math
import certifi
import random
from io import BytesIO
from functools import wraps
import os


model = tf.keras.models.load_model('static/model/model.h5')
class_name_list = ['adho mukha svanasana', 'adho mukha vriksasana',
                   'ananda balasana', 'anantasana', 'anjaneyasana',
                   'ardha chandrasana', 'ardha matsyendrasana', 'ardha pincha mayurasana',
                   'ardha uttanasana', 'astavakrasana', 'baddha konasana', 'bakasana',
                   'balasana', 'bhujangasana', 'bhujapidasana', 'bitilasana', 'camatkarasana',
                   'chaturanga dandasana', 'dandasana', 'dhanurasana', 'dwi pada viparita dandasana',
                   'eka pada koundinyanasana', 'eka pada rajakapotasana', 'garudasana', 'gomukhasana',
                   'halasana', 'janu sirsasana', 'kapotasana', 'krounchasana', 'kurmasana',
                   'malasana', 'marjaryasana', 'matsyasana', 'mayurasana', 'natarajasana',
                   'parighasana', 'paripurna navasana', 'parivrtta janu sirsasana', 'parivrtta parsvakonasana',
                   'parivrtta trikonasana', 'parsva bakasana', 'parsvottanasana', 'paschimottanasana',
                   'pincha mayurasana', 'prasarita padottanasana', 'purvottanasana', 'salabhasana',
                   'salamba sarvangasana', 'salamba sirsasana', 'savasana', 'setu bandha sarvangasana',
                   'supta padangusthasana', 'supta virasana', 'tittibhasana', 'tolasana', 'upavistha konasana',
                   'urdhva prasarita eka padasana', 'ustrasana', 'utkatasana', 'uttana shishosana', 'uttanasana',
                   'utthita hasta padangustasana', 'vajrasana', 'vasisthasana', 'viparita karani', 'virabhadrasana i',
                   'virabhadrasana ii', 'virabhadrasana iii', 'vriksasana', 'vrischikasana', 'yoganidrasana']


app = Flask(__name__)
client = MongoClient('mongodb+srv://test:dkssudgktpdy@cluster0.qwbpf.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where()) 
db = client.sparta
cors = CORS(app, resources={r"*": {"origins" : "*"}})

SECRET_KEY = 'YoGaYo'

#토오큰
def authrize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'mytoken' in request.cookies:
            abort(401)
        user = None
        token = request.cookies['mytoken']
        try:
            user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            abort(401)
        return f(user, *args, **kws)
    return decorated_function

#이미지 처리
def black_colour_masks(image):
    colours = [[0, 0, 0]]
    r = np.zeros_like(image.astype(np.uint8))
    g = np.zeros_like(image.astype(np.uint8))
    b = np.zeros_like(image.astype(np.uint8))
    r[image == 1], g[image == 1], b[image == 1] = colours[0]
    coloured_mask = np.stack([r, g, b], axis=2)
    return coloured_mask


#로그인 화면
@app.route('/login_page')
def join():
    return render_template('login.html')

#로그인 정보가 담기는 곳
@app.route('/login',methods=['POST'])
def sign_in():
    data = json.loads(request.data)
    user_email_receive = data.get("user_email_give")
    user_password_receive = data.get("user_password_give")
    hashed_pw = hashlib.sha256(user_password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'email':user_email_receive, 'password': hashed_pw})

    if result is not None:
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
    
    else:
        return jsonify({
            'result':'fail', 
            'msg': '아이디/비밀번호가 기억 안나셔요?'
        })



#회원가입 화면

@app.route('/sign_up_page')
def login():
    return render_template('join.html')

#회원가입 정보가 담기는 곳
@app.route('/sign_up', methods=["POST"])
def check():
    data = json.loads(request.data)
    user_email_receive = data.get("user_email_give")
    nick_name_receive = data.get("nick_name_give")
    user_password_receive = data.get("user_password_give")
    hashed_password = hashlib.sha256(user_password_receive.encode('utf-8')).hexdigest()

    doc1 = {
        'email' : user_email_receive
    }
    doc2 = {
        'nick' : nick_name_receive
    }

    check_email = db.user.find_one(doc1)
    check_nick = db.user.find_one(doc2)

    if check_email is None and check_nick is None:
        
        doc3 = {
        "email" : user_email_receive,  
        "nick" : nick_name_receive,
        "password" : hashed_password,  
        }
                
        db.user.insert_one(doc3)
        return jsonify({
            "result": "success",
            'msg' : '회원가입 완료셔요',
            'url' : "/login"
        })

    elif check_email is not None:
        return jsonify ({
            "result": "fail", 
            'msg': '이메일이 중복이셔요', 
            'url' : '/sign_up'
        })
    
    elif check_nick is not None:
        return jsonify ({
            "result": "fail", 
            'msg': '닉네임이 중복이셔요', 
            'url' : '/sign_up'
        })

#메인 화면
@app.route('/')
@authrize
def home(user):
    if user is not None:
        posts = list(db.yoga_post.find({'user_name' : ObjectId(user.get('id'))}))
        recent_thr_pose = []
        for post in posts[:4]:
            recent_thr_pose.append(post.get('acting_name'))
        recommend_poses = list(filter(lambda x: x not in recent_thr_pose, class_name_list))
        ran_num = random.randrange(0, len(recommend_poses)-1)
        url = '../static/images/class/'+ recommend_poses[ran_num] + '/img.png'
        doc = {
            'class_name' : recommend_poses[ran_num],
            'url' : url,
        }
        return render_template('main.html', recommend = doc)

#메인 화면에서 데이터를 담는 곳

@app.route('/fileupload', methods=['POST'])
@authrize
def file_upload(user):
    if user is not None:
        title_receive = request.form['title_give']
        file = request.files['file_give']
        # gridfs 활용해서 이미지 분할 저장
        buffered = BytesIO()
        extension = file.filename.split('.')[-1]
        format = 'JPEG' if extension.lower() == 'jpg' else extension.upper()

        img = Image.open(file)
        img.save(buffered, format)
        image_base64 = base64.b64encode(buffered.getvalue())
        img = img.convert("RGB")

        resize_img = img.resize((224, 224))
        input_arr = tf.keras.preprocessing.image.img_to_array(resize_img)
        prediction = model.predict(np.array([input_arr]))
        class_num = np.argmax(prediction)
        acc = str(math.floor(prediction[0][class_num] * 100))
        class_name = class_name_list[class_num]

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


# 주소에다가 /fileshow/이미지타이틀 입력하면 그 이미지타이틀을 title이라는 변수로 받아옴
@app.route('/fileshow/<title>')
@authrize
def file_show(user):
    if user is not None:
        # title은 현재 이미지타이틀이므로, 그것을 이용해서 db에서 이미지 '파일'을 가지고 옴
        img_info = db.yoga_post.find_one({'title': title})
        img_binary = fs.get(img_info['img'])
        # html 파일로 넘겨줄 수 있도록, base64 형태의 데이터로 변환
        base64_data = codecs.encode(img_binary.read(), 'base64')
        image = base64_data.decode('utf-8')
        # 해당 이미지의 데이터를 jinja 형식으로 사용하기 위해 넘김
        return render_template('showimg.html', img=image)

#다이어리 화면
@app.route("/diary")
@authrize
def diary_page(user):
    if user is not None:
        # user = {'_id' : ObjectId("62887eb015570b9eedb078f6")}
        user_name = db.user.find_one({"_id": ObjectId(user.get('id'))},{'password':0})
        posts = list(db.yoga_post.find({"user_id" : ObjectId(user.get('id'))}))
        for post in posts:
            post['datetime'] = post['datetime'].strftime("%x")
            post['yoga_img'] = post['yoga_img'].decode('utf-8')
        posts = sorted(posts, key=lambda x:x['datetime'])
        return render_template("diary.html",user_name = user_name, posts = posts)

#다이어리 화면의 차트 구성에 필요한 acc 데이터를 받아오는 곳
@app.route("/diary/acc")
@authrize
def get_acc(user):
    if user is not None:
        # user = {'_id' : ObjectId("62887eb015570b9eedb078f6")}
        posts = list(db.yoga_post.find({"user_id" : user.get('_id')}))
        posts_acc = []
        for post in posts[0:6]:
            posts_acc.append(post.get('acc'))
        return jsonify({"result" : "success", "posts_acc" : posts_acc})


#다리어리 화면의 edit할 데이터를 담는 곳
@app.route("/diary/edit", methods = ["POST"])
@authrize
def edit_post(user):
    if user is not None:
        # user = {'_id' : ObjectId("62887eb015570b9eedb078f6")}
        posts = list(db.yoga_post.find({"user_id" : user.get('_id')}))
        
        data = json.loads(request.data)
        doc = {
            'content' : data.get('edit_texts_give', None),
        }
        post_id = {
            'post_id' : data.get('post_id_give', None)
        }
        db.yoga_post.update_one({'_id' :ObjectId(post_id.get('post_id')) }, {'$set':doc})
        return jsonify({"result" : "success", "msg" : "수정되었습니다!"})

#다리어리 화면의 delete할 데이터를 담는 곳
@app.route("/diary/delete", methods = ["POST"])
@authrize
def delete_post(user):
    if user is not None:
        # user = {'_id' : ObjectId("62887eb015570b9eedb078f6")}
        # posts = list(db.yoga_post.find({"user_id" : user.get('_id')}))
        data = json.loads(request.data)
        post_id = {
            'post_id' : data.get('post_id_give', None)
        }
        db.yoga_post.delete_one({'_id' :ObjectId(post_id.get('post_id'))})

        return jsonify({"result" : "success", "msg" : "삭제되었습니다!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)