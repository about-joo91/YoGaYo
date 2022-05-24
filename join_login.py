from pydoc import doc
from flask import Flask, render_template, Blueprint, jsonify, render_template, request, abort
from pymongo import MongoClient
from datetime import date, datetime, timedelta
from flask_cors import CORS
import jwt
import hashlib
import certifi
import json
client = MongoClient('mongodb+srv://test:niSHv7HaIjlNpVdT@cluster0.r6nld.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())

SECRET_KEY = 'YoGaYo'
db = client.yogayo_test
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins":"*"}})

@app.route('/login_page')
def join():
    return render_template('login.html')

@app.route('/sign_up_page')
def login():
    return render_template('join.html')

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


@app.route('/login',methods=['POST'])
def sign_in():
    data = json.loads(request.data)
    user_email_receive = data.get("user_email_give")
    user_password_receive = data.get("user_password_give")
    hashed_pw = hashlib.sha256(user_password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'user_email':user_email_receive, 'user_password': hashed_pw})

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


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)