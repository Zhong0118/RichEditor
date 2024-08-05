import itertools
import os
import shutil
import sys

import cv2
import erniebot
import numpy as np
from flask import Flask, request, Response
from flask_cors import CORS
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from paddleocr import PaddleOCR

# 把backend加入路径中
sys.path.append("E:\\vue_flask\\RichEditor")
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


@app.route('/api/logout', methods=['POST'])
def logout():
    uid = request.json.get('uid')
    images_path = './static/images/' + str(uid)
    libs_path = './static/libs/' + str(uid)
    datas_path = './data/docs_' + str(uid)
    for directory in (images_path, libs_path, datas_path):
        if os.path.exists(directory):
            shutil.rmtree(directory)
    return jsonify({"message": "用户登出成功，相关文件夹已删除"}), 200


@app.route('/api/hotmap', methods=['GET'])
def hotmap():
    uid = request.args.get('uid')
    return get_hotmap(uid)


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


@app.route("/api/share", methods=['POST'])
def set_share():
    data = request.json
    did = data.get('did')
    flag = data.get('flag')
    return changeShare(did, flag)


@app.route("/api/getshare", methods=['GET'])
def get_share():
    shareId = request.args.get('shareId')
    return getShare(shareId)


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
        f"根据'{prompt_text}'的条件，请把相关文本内容：'{content}'进行自动格式排版，优化结构，你需要紧紧贴合给你提供的内容或者依靠条件。我不需要代码块包裹你的答案，我只需要你正常回答我。如果有可能的的话我希望你能自动整理我的主题大意，从而返回更符合我需求的内容。仅仅返回结果即可",
        f"根据'{prompt_text}'的条件，我需要你为我生成markdown格式的表格，请仅仅返回结果，不需要代码块包裹答案，可根据情况自动帮我填充数据。",
        f"根据'{prompt_text}'的条件，以及相关文本内容：'{content}'，我需要你为我生成对应的mermaid语法的代码，请只返回结果，需要代码块包裹答案。",
        f"根据'{prompt_text}'的条件，以及相关文本内容：'{content}'，我需要你先进行数据的提取和分析，我只需要你给我符合Markmap.js语法的结果，请只返回结果，需要代码块包裹答案。",
    ]
    print(prompts[index])
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': prompts[index]}],
        stream=True,
    )
    return Response(generate_stream(response), content_type='text/event-stream')


@app.route('/api/postlib', methods=['POST'])
def postlib():
    uid = request.form.get('uid')  # 获取表单数据中的 ID
    files = request.files.getlist('files')

    file_path = 'static/libs/' + str(uid) + '/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    else:
        shutil.rmtree(file_path)
        os.makedirs(file_path)
    split_docs = []
    for file in files:
        filename = file.filename
        if filename.split('.')[-1] in ['txt', 'pdf', 'xlsx', 'xls', 'docx', 'doc']:
            save_path = os.path.join(file_path, file.filename)
            file.save(save_path)
            if filename.split('.')[-1] in ['xlsx', 'xls']:
                loader = UnstructuredExcelLoader(os.path.join(file_path + filename))
            if filename.split('.')[-1] in ['pdf']:
                loader = PyPDFLoader(os.path.join(file_path + filename))
            if filename.split('.')[-1] in ['txt']:
                loader = UnstructuredFileLoader(os.path.join(file_path + filename))
            if filename.split('.')[-1] in ['docx', 'doc']:
                loader = Docx2txtLoader(os.path.join(file_path + filename))
            try:
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
                data = loader.load()
                print(data)
                split_docs.append(text_splitter.split_documents(data))
            except Exception as e:
                print(e)
    split_docs = list(itertools.chain(*split_docs))
    print(split_docs)  # 将列表元素用空格连接成字符串
    # print("split_docs size:", len(split_docs), type(split_docs))
    # 初始化 hugginFace 的 embeddings 对象
    embeddings = HuggingFaceEmbeddings(model_name="./models/Embeddings/text2vec-base-chinese")
    print("embeddings", embeddings)
    print("embeddings model_name", embeddings.model_name)
    # 初始化加载器，并将向量保存到磁盘
    lib = Chroma.from_documents(split_docs, embeddings, persist_directory="./data/docs_" + str(uid))
    # 持久化
    lib.persist()
    return jsonify({"message": "构建成功"}), 200


@app.route('/api/chat', methods=['POST'])
def talk_chat():
    data = request.get_json()
    uid = data.get('uid')
    content = data.get('content')
    embeddings = HuggingFaceEmbeddings(model_name="./models/Embeddings/text2vec-base-chinese")
    lib = Chroma(persist_directory=f"./data/docs_{uid}", embedding_function=embeddings)
    info = ""
    similarDocs = lib.similarity_search(content, k=4)
    for similardoc in similarDocs:
        info = info + similardoc.page_content
    m = "结合以下信息：" + info + "。回答这个问题：" + content
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': m}],
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
