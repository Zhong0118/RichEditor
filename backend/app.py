import erniebot
from flask import Flask, request, Response
from flask_cors import CORS

from auth import *
from backend.models import _hash_password
from document import *

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

erniebot.api_type = 'aistudio'
erniebot.access_token = '6c12f745fe9aefb5fbc3a5b14bc033b9fbf9d7b2'


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


@app.route('/api/documents/export', methods=['POST'])
def export_template():
    data = request.json
    owner_id = data.get('owner_id')
    title = data.get('title')
    content = data.get('content')
    return export_one_template(owner_id, title, content)


@app.route('/api/gettemplates', methods=['GET'])
def get_templates():
    owner_id = request.args.get('owner_id')
    return get_all_templates(owner_id)


@app.route('/api/applytemplate', methods=['POST'])
def apply_template():
    data = request.json
    doc = data.get('doc')
    owner_id = data.get('owner_id')
    return create_document(doc.get('title'), doc.get('content'), doc.get('tag'), owner_id, doc.get('createTime'),
                           doc.get('share_id'))


def generate_stream(aires):
    try:
        for chunk in aires:
            print(chunk.get_result())
            yield f"{chunk.get_result()}"
    except GeneratorExit:
        print("客户端失连")


@app.route('/api/bubblechat', methods=['POST'])
def bubble_chat():
    data = request.get_json()
    index = int(data.get('type'))
    content = data.get('content')
    prompt_text = data.get('promptText')
    prompts = [
        f"请你帮忙提取这段话的摘要'{content}'，尽可能依据'{prompt_text}'的条件。",
        f"请你帮忙润色这段话'{content}'，使其更有逻辑，同时依据'{prompt_text}'的条件。",
        f"请你根据这段话的大概含义进行续写'{content}'，依据'{prompt_text}'的条件。",
        f"请你帮忙对这段话进行翻译'{content}'，要注意精准度，依据'{prompt_text}'的条件。",
    ]
    print(prompts[index])
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': prompts[index]}],
        stream=True,
    )
    return Response(generate_stream(response), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)
