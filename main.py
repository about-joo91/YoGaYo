from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from pymongo import MongoClient
import gridfs
import codecs
import tensorflow as tf
import torch
import torchvision.transforms as T
import torchvision
from PIL import Image
import numpy as np
from flask_cors import CORS
import math


model = tf.keras.models.load_model('static/model/model.h5')
seg_model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
seg_model.eval()
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
cors = CORS(app, resources={r"*": {"origins": "*"}})
client = MongoClient(
    'mongodb+srv://test:dkssudgktpdy@cluster0.qwbpf.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta_plus_week4
fs = gridfs.GridFS(db)


def black_colour_masks(image):
    colours = [[0, 0, 0]]
    r = np.zeros_like(image.astype(np.uint8))
    g = np.zeros_like(image.astype(np.uint8))
    b = np.zeros_like(image.astype(np.uint8))
    r[image == 1], g[image == 1], b[image == 1] = colours[0]
    coloured_mask = np.stack([r, g, b], axis=2)
    return coloured_mask

#################################
##  HTML을 주는 부분             ##
#################################


@app.route('/')
def home():
    return render_template('test.html')

# 방식2 : DB에 이미지 파일 자체를 올리는 방식


@app.route('/fileupload', methods=['POST'])
def file_upload():
    title_receive = request.form['title_give']
    file = request.files['file_give']
    # gridfs 활용해서 이미지 분할 저장
    fs_image_id = fs.put(file)
    img = Image.open(file)
    resize_img = img.resize((224, 224))
    input_arr = tf.keras.preprocessing.image.img_to_array(resize_img)
    prediction = model.predict(np.array([input_arr]))
    class_num = np.argmax(prediction)
    acc = str(math.floor(prediction[0][class_num] * 100))
    # acc = round(prediction[0][class_num], 3)
    class_name = class_name_list[class_num]
    # db 추가
    doc = {
        'content': title_receive,
        'yoga_img': fs_image_id,
        'datetime': datetime.utcnow(),
        'acc': acc,
        'acting_name': class_name
    }
    db.camp2.insert_one(doc)

    return jsonify({'result': 'success'})

# 주소에다가 /fileshow/이미지타이틀 입력하면 그 이미지타이틀을 title이라는 변수로 받아옴


@ app.route('/fileshow/<title>')
def file_show(title):
    # title은 현재 이미지타이틀이므로, 그것을 이용해서 db에서 이미지 '파일'을 가지고 옴
    img_info = db.camp2.find_one({'title': title})
    img_binary = fs.get(img_info['img'])
    # html 파일로 넘겨줄 수 있도록, base64 형태의 데이터로 변환
    base64_data = codecs.encode(img_binary.read(), 'base64')
    image = base64_data.decode('utf-8')
    # 해당 이미지의 데이터를 jinja 형식으로 사용하기 위해 넘김
    return render_template('showimg.html', img=image)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
