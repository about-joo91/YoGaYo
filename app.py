""" 모듈 불러오기 """
from flask_cors import CORS
from flask import Flask
from post.post_bp import post_bp
from user.user_bp import user_bp


app = Flask(__name__)
app.register_blueprint(post_bp)
app.register_blueprint(user_bp)
cors = CORS(app, resources={r"*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
