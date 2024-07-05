from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
client = MongoClient('mongodb://localhost:27017/')
db = client['richEditorDB']
user_collection = db['User']
document_collection = db['Document']
template_collection = db['Template']
media_collection = db['Media']


@app.route('/api/login', methods=['POST'])
def login():
    return 'Hello World!'


@app.route('/api/register', methods=['POST'])
def register():
    return 'Hello World!'


@app.route('/api/forget', methods=['POST'])
def forget():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
