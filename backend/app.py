from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 可以添加具体参数调整，例如 origins 来限制访问源


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api', methods=['GET'])  # 修改为处理 POST 请求
def post_data():
    return jsonify({'message': 'Received POST request with data: {}'})


if __name__ == '__main__':
    app.run(debug=True)
