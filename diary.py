# from crypt import methods
import json
from re import template
# from xxlimited import new
from django.shortcuts import render
from flask import Blueprint, jsonify, Flask, render_template, request, Response
import certifi
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask_cors import CORS

client = MongoClient('mongodb+srv://test:sparta@cluster0.alyd7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.sparta

diary = Flask(__name__)
cors = CORS(diary, resources={r"*": {"origins" : "*"}})

# blue_diary = Blueprint("diary",__name__,url_prefix"/diary")

# @blue_diary.route("/diary")

@diary.route('/')
def _home():
    return render_template('index.html')

# @authrize
@diary.route("/diary")

def diary_page():
    user = {'_id' : ObjectId("62887eb015570b9eedb078f6")}
    user_name = db.user.find_one({"_id" : user.get('_id')})
    posts = list(db.yoga_post.find({"user_id" : user.get('_id')}))
    acc_list = []
    for post in enumerate(posts):
        acc_list.append(post)
    return render_template("diary.html",user_name = user_name, posts = posts )

@diary.route("/diary/acc")
def get_acc():
    user = {'_id' : ObjectId("62887eb015570b9eedb078f6")}
    posts = list(db.yoga_post.find({"user_id" : user.get('_id')}))
    posts_acc = []
    for post in posts[0:6]:
        posts_acc.append(post.get('acc'))
    print('posts_acc : ',posts_acc)
    return jsonify({"result" : "success", "posts_acc" : posts_acc})



@diary.route("/diary/edit", methods = ["POST"])
def edit_post():
    user = {'_id' : ObjectId("62887eb015570b9eedb078f6")}
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

@diary.route("/diary/delete", methods = ["POST"])
def delete_post():
    user = {'_id' : ObjectId("62887eb015570b9eedb078f6")}
    posts = list(db.yoga_post.find({"user_id" : user.get('_id')}))
    data = json.loads(request.data)
    post_id = {
        'post_id' : data.get('post_id_give', None)
    }
    print("delete post id : ",ObjectId(post_id.get('post_id')))
    # db.yoga_post.delete({'_id' :ObjectId(post_id.get('post_id')) })
    return jsonify({"result" : "success", "msg" : "삭제되었습니다!"})

if __name__ == '__main__':
    diary.run(host='0.0.0.0', port=8080, debug=True)