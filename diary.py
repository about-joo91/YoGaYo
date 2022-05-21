# from crypt import methods
from re import template
from django.shortcuts import render
from flask import Blueprint, jsonify, Flask, render_template, request
import certifi
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.alyd7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.sparta

diary = Flask(__name__)

# blue_diary = Blueprint("diary",__name__,url_prefix"/diary")

# @blue_diary.route("/diary")

@diary.route('/')
def _home():
    return render_template('index.html')

# @authrize
@diary.route("/diary")

def diary_page():
    user = {'_id' : ObjectId("62887eb015570b9eedb078f6")}
    print(user.get('_id'))
    user_name = db.user.find_one({"_id" : user.get('_id')})
    print(user.get('_id'))
    posts = list(db.yoga_post.find({"user_id" : user.get('_id')}))
    print("posts : ",posts)
    return render_template('diary.html', user_name = user_name, posts = posts)

# @blue_diary.route("/post", methods = ["POST"])
@diary.route("/diary/edit", methods = ["POST"])
# @authreize
def edit_post():
    # if user is not None:
        user_name = db.user.find_one({'_id': ObjectId(user.get('id'))})
        post = db.yoga_post.find({'user_id' : user.get("id")})

if __name__ == '__main__':
    diary.run(host='0.0.0.0', port=8080, debug=True)