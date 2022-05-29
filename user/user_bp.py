""" 모듈 import """
import json
import hashlib
from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, request
from pymongo import MongoClient
import certifi
import jwt

from config import SECRET_KEY, DB_INFO


user_bp = Blueprint('user_bp', __name__, static_folder='static',
                    template_folder='templates', static_url_path='/user/static')

client = MongoClient(
    f"mongodb+srv://{DB_INFO}@cluster0.qwbpf.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where())
db = client.sparta


@user_bp.route('/login_page')
def join():
    """ 로그인 화면 """
    return render_template('login.html')


@user_bp.route('/login', methods=['POST'])
def sign_in():
    """ 로그인 정보를 토큰에 담아서 클라이언트로 보냄 """
    data = json.loads(request.data)
    user_email_receive = data.get("user_email_give")
    user_password_receive = data.get("user_password_give")
    hashed_pw = hashlib.sha256(
        user_password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one(
        {'email': user_email_receive, 'password': hashed_pw})

    if result:
        payload = {
            'id': str(result.get('_id')),
            'email': result.get('email'),
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'result': 'success',
            'token': token,
            'msg': '로그인 성공이셔요'
        })
    return jsonify({
        'result': 'fail',
        'msg': '아이디/비밀번호가 기억 안나셔요?'
    })


@user_bp.route('/sign_up_page')
def login():
    """ 회원가입 화면 """
    return render_template('join.html')


@user_bp.route('/sign_up', methods=["POST"])
def check():
    """ 회원가입 정보를 db에 저장 """
    data = json.loads(request.data)
    user_email_receive = data.get("user_email_give")
    nick_name_receive = data.get("nick_name_give")
    user_password_receive = data.get("user_password_give")
    hashed_password = hashlib.sha256(
        user_password_receive.encode('utf-8')).hexdigest()

    user_check = {
        'email': user_email_receive
    }
    nick_check = {
        'nick': nick_name_receive
    }

    check_email = db.user.find_one(user_check)
    check_nick = db.user.find_one(nick_check)
    if check_email:
        return jsonify({
            "result": "fail",
            'msg': '이메일이 중복이셔요',
            'url': '/sign_up'
        })

    if check_nick:
        return jsonify({
            "result": "fail",
            'msg': '닉네임이 중복이셔요',
            'url': '/sign_up'
        })
    doc = {
        "email": user_email_receive,
        "nick": nick_name_receive,
        "password": hashed_password,
    }
    db.user.insert_one(doc)
    return jsonify({
        "result": "success",
        'msg': '회원가입 완료셔요',
        'url': "/login"
    })
