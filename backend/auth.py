from flask import jsonify

from backend.models import _hash_password
from db_config import DBConfig

dbconfig = DBConfig()
db = dbconfig.get_db()
user_collection = db['User']


def login_verify(username, password):
    user = user_collection.find_one({'username': username, 'password': password})
    if user:
        if '_id' in user:
            user['_id'] = str(user['_id'])
        return jsonify({'message': 'yes', 'user': user}), 200
    else:
        return jsonify({'message': '用户名或密码错误'}), 401


def register_verify(username, password, email):
    user = user_collection.find_one({'username': username})
    if user:
        return jsonify({'message': '用户名已经存在了'}), 400
    else:
        password = _hash_password(password)
        uid = user_collection.insert_one({'username': username, 'password': password, 'email': email}).inserted_id
        user = {'_id': str(uid), 'username': username, 'password': password}
        return jsonify({'message': 'ok', 'user': user}), 200


def forget_verify(username, password, email):
    user = user_collection.find_one({'username': username, 'email': email})
    if user:
        password = _hash_password(password)
        user_collection.update_one({'_id': user['_id']}, {'$set': {'password': password}})
        if '_id' in user:
            user['_id'] = str(user['_id'])
        return jsonify({'message': 'ok', 'user': user}), 200
    else:
        return jsonify({'message': '用户名或邮箱错误'}), 400
