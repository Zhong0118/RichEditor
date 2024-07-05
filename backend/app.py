from flask import Flask, request
from flask_cors import CORS

from auth import *
from backend.models import _hash_password

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    password = _hash_password(password)
    return login_verify(username, password)


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('e')
    return register_verify(username, password, email)


@app.route('/api/forget', methods=['POST'])
def forget():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    return forget_verify(username, password, email)


if __name__ == '__main__':
    app.run(debug=True)
