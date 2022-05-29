""" 모듈 import """
import math
import os
import random
import base64
import json
from datetime import datetime
import certifi
import tensorflow as tf
import numpy as np
from io import BytesIO
from PIL import Image
from functools import wraps
from flask import Blueprint, render_template, abort, jsonify, request
from bson import ObjectId
from pymongo import MongoClient
import jwt

from config import SECRET_KEY, DB_INFO, CLASS_NAME

post_bp = Blueprint('post_bp', __name__, static_folder='static',
                    template_folder='templates', static_url_path='/post/static')

client = MongoClient(
    f"mongodb+srv://{DB_INFO}@cluster0.qwbpf.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where())
db = client.sparta

model = tf.keras.models.load_model(
    os.path.join(post_bp.static_folder, 'model/model.h5'))


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


@post_bp.route('/')
@authrize
def home(user):
    """ 메인 화면"""
    if user:
        posts = list(db.yoga_post.find(
            {'user_name': ObjectId(user.get('id'))}))
        recent_thr_pose = [post.get('acting_name') for post in posts[:4]]
        recommend_poses = list(
            filter(lambda x: x not in recent_thr_pose, CLASS_NAME))
        ran_num = random.randrange(0, len(recommend_poses)-1)
        url = recommend_poses[ran_num]
        print(url)
        doc = {
            'class_name': recommend_poses[ran_num],
            'url': url,
        }
        return render_template('main.html', recommend=doc)
    return jsonify({'result': 'fail', 'msg': '로그인을 하셔요'})


@post_bp.route('/fileupload', methods=['POST'])
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
            'user_name': ObjectId(user.get('id'))
        }

        db.yoga_post.insert_one(doc)

        return jsonify({'result': 'success', 'msg': '다이어리에서 당신의 정확도를 확인하세요!!'})
    return jsonify({'result': 'fail', 'msg': '로그인을 하셔요'})


@post_bp.route("/diary")
@authrize
def diary_page(user):
    """ 다이어리 화면 """
    if user:
        user_name = db.user.find_one(
            {"_id": ObjectId(user.get('id'))}, {'password': 0})
        posts = list(db.yoga_post.find(
            {"user_name": ObjectId(user.get('id'))}))

        for post in posts:
            post['datetime'] = post['datetime'].strftime("%x")
            post['yoga_img'] = post['yoga_img'].decode('utf-8')
        posts = sorted(posts, key=lambda x: x['datetime'], reverse=True)

        return render_template("diary.html", user_name=user_name, posts=posts)
    return jsonify({'result': 'fail', 'msg': '로그인을 하셔요'})


@post_bp.route("/diary/acc")
@authrize
def get_acc(user):
    """ 그래프화면에 넣어줄 정확도를 불러옴 """
    if user:
        posts = list(db.yoga_post.find({"user_name": user.get('_id')}))
        posts = sorted(posts, key=lambda x: x['datetime'], reverse=True)
        posts_acc = [post.get('acc') for post in posts[0:6]]
        return jsonify({"result": "success", "posts_acc": posts_acc})
    return jsonify({'result': 'fail', 'msg': '로그인을 하셔요'})


@post_bp.route("/diary/edit", methods=["POST"])
@authrize
def edit_post(user):
    """ 포스트를 수정 """
    if user:
        data = json.loads(request.data)
        doc = {
            'content': data.get('edit_texts_give', None),
        }
        post_id = {
            'post_id': data.get('post_id_give', None)
        }
        db.yoga_post.update_one(
            {'_id': ObjectId(post_id.get('post_id'))}, {'$set': doc})
        return jsonify({"result": "success", "msg": "수정되었습니다!"})
    return jsonify({'result': 'fail', 'msg': '로그인을 하셔요'})


@post_bp.route("/diary/delete", methods=["POST"])
@authrize
def delete_post(user):
    """ 포스트를 지움 """
    if user:
        data = json.loads(request.data)
        post_id = {
            "post_id": data.get("post_id_give", None)
        }
        db.yoga_post.delete_one({"_id": ObjectId(post_id.get("post_id"))})
        return jsonify({"result": "success", "msg": "삭제되었습니다!"})
    return jsonify({"result": "fail", "msg": "로그인을 하셔요"})
