from flask import Flask, request
from flask_cors import CORS

from auth import *
from backend.models import _hash_password
from document import *

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


@app.route('/api/getdocuments', methods=['GET'])
def get_all_documents():
    owner_id = request.args.get('owner_id')
    return get_all_document(owner_id)


@app.route('/api/createdocument', methods=['POST'])
def create_one_document():
    data = request.json
    owner_id = data.get('owner_id')
    doc = data.get('doc')
    return create_document(doc.get('title'), '', doc.get('tag'), owner_id, doc.get('createTime'), doc.get('share_id'))


@app.route('/api/rename', methods=['PUT'])
def rename_one():
    data = request.json
    did = data.get('did')
    title = data.get('title')
    update = data.get('update')
    return rename_one_document(did, title, update)


@app.route('/api/retag', methods=['PUT'])
def retag_one():
    data = request.json
    did = data.get('did')
    tag = data.get('tag')
    update = data.get('update')
    return retag_one_document(did, tag, update)


@app.route('/api/delete', methods=['DELETE'])
def delete_one():
    data = request.json
    did = data.get('did')
    return delete_one_document(did)


@app.route('/api/documents/update', methods=['POST'])
def save_one():
    data = request.json
    did = data.get('did')
    update = data.get('update')
    content = data.get('content')
    return save_one_document(did, update, content)


@app.route('/api/documents/content', methods=['GET'])
def get_doc_content():
    did = request.args.get('did')
    return get_one_content(did)


if __name__ == '__main__':
    app.run(debug=True)
