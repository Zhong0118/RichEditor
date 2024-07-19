import os

import cv2
import erniebot
import numpy as np
from flask import Flask, request, Response
from flask_cors import CORS
from paddleocr import PaddleOCR

from auth import *
from backend.models import _hash_password
from document import *

# from paddlespeech.cli.asr.infer import ASRExecutor

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

erniebot.api_type = 'aistudio'
erniebot.access_token = '6c12f745fe9aefb5fbc3a5b14bc033b9fbf9d7b2'
ocr = PaddleOCR(use_angle_cls=True, lang="ch")


# asr = ASRExecutor()


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


@app.route('/api/setvip', methods=['POST'])
def vip():
    data = request.json
    uid = data.get('uid')
    set_vip(uid)
    return jsonify({'message': 'VIP status updated'}), 200


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
        f"根据'{prompt_text}'的条件，请把这段HTML内容：'{content}'进行自动格式排版，优化结构，你需要紧紧贴合给你提供的内容或者依靠条件，返回markdown格式文本，如果有可能的的话我希望你能自动整理我的主题大意，从而返回更符合我需求的内容。",
    ]
    print(prompts[index])
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': prompts[index]}],
        stream=True,
    )
    return Response(generate_stream(response), content_type='text/event-stream')


@app.route('/api/chat', methods=['POST'])
def talk_chat():
    data = request.get_json()
    content = data.get('content')
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': content}],
        stream=True,
    )
    return Response(generate_stream(response), content_type='text/event-stream')


def generate_ocr(aires):
    try:
        for chunk in aires:
            print(chunk[1][0])
            yield f"{chunk[1][0]}"
    except GeneratorExit:
        print("客户端失连")


@app.route('/api/imageOCR', methods=['POST'])
def image_ocr():
    uid = request.form.get('uid')
    img = request.files['file']
    picname = img.filename
    file = img.read()
    file = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)  # 解码为ndarray
    imgfile1_path = "./static/images/" + uid + "/"
    if not os.path.exists(imgfile1_path):
        os.makedirs(imgfile1_path)
    img1_path = os.path.join(imgfile1_path, picname)
    cv2.imwrite(filename=img1_path, img=file)
    img_path = imgfile1_path + picname
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        return Response(generate_ocr(res), content_type='text/event-stream')


@app.route('/api/asr', methods=['POST'])
def asr_api():
    # uid = request.form.get('uid')
    # audio = request.files['audio']
    # current_time = datetime.now()
    # timestr = current_time.strftime('%Y_%m_%d_%H_%M_%S')
    # audio_name = timestr + ".wav"  # 使用时间戳作为文件名
    # audio_path = "./static/voice/" + uid + "/"
    # if not os.path.exists(audio_path):
    #     os.makedirs(audio_path)
    # audio_full_path = os.path.join(audio_path, audio_name)
    # with open(audio_full_path, 'wb') as f:
    #     f.write(audio.read())
    # result = asr(audio_file=audio_full_path)
    # print(result)  # 假设这是你的语音识别结果处理函数
    result = '你好，我很高兴参加比赛，希望取得好名次。'

    # 返回语音识别结果
    return Response(result, content_type='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
