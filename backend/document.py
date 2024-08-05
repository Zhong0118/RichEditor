from datetime import datetime

from bson import ObjectId
from flask import jsonify

from db_config import DBConfig

dbconfig = DBConfig()
db = dbconfig.get_db()
document_collection = db['Document']
template_collection = db['Template']


def get_all_document(owner_id):
    documents = document_collection.find({'owner_id': owner_id})
    documents_str_id = []
    for doc in documents:
        doc_str_id = {
            '_id': str(doc['_id']) if '_id' in doc else None,
        }
        doc_str_id.update({k: v for k, v in doc.items() if k != '_id'})
        documents_str_id.append(doc_str_id)
    return jsonify({'documents': documents_str_id}), 200


def update_one_document(did, title, content, tag, update):
    document_collection.update_one({'_id': ObjectId(did)},
                                   {'$set': {'title': title, 'content': content, 'tag': tag, 'updateTime': update}})
    return jsonify({'message': 'ok'}), 200


def rename_one_document(did, title, update):
    document_collection.update_one({'_id': ObjectId(did)}, {'$set': {'title': title, 'updateTime': update}})
    return jsonify({'message': 'ok'}), 200


def retag_one_document(did, tag, update):
    document_collection.update_one({'_id': ObjectId(did)}, {'$set': {'tag': tag, 'updateTime': update}})
    return jsonify({'message': 'ok'}), 200


def create_document(title, content, tag, owner_id, createTime, share_id):
    did = document_collection.insert_one(
        {'title': title, 'content': content, 'tag': tag, 'owner_id': owner_id, 'createTime': createTime,
         'updateTime': createTime, 'share_id': share_id, 'is_shared': False}).inserted_id
    did = str(did)
    return jsonify({'message': 'ok', 'did': did}), 200


def delete_one_document(did):
    document_collection.delete_one({'_id': ObjectId(did)})
    return jsonify({'message': 'ok'}), 200


def save_one_document(did, update, content):
    document_collection.update_one({'_id': ObjectId(did)}, {'$set': {'content': content, 'updateTime': update}})
    return jsonify({'message': 'ok'}), 200


def get_one_content(did):
    content = document_collection.find_one({'_id': ObjectId(did)}, {'content': 1, '_id': 0})
    # print(content)
    return jsonify({'message': 'ok', 'text': content['content']}), 200


def export_one_template(owner_id, title, content):
    template_collection.insert_one({'title': title, 'content': content, 'owner_id': owner_id, 'is_public': False})
    return jsonify({'message': 'ok'}), 200


def get_all_templates(owner_id):
    templates = template_collection.find({'$or': [{'is_public': True}, {'owner_id': owner_id}]})
    templates_str_id = []
    for template in templates:
        template_str_id = {
            '_id': str(template['_id']) if '_id' in template else None,  # 确保_id存在并且转换为字符串
        }
        template_str_id.update({k: v for k, v in template.items() if k != '_id'})
        templates_str_id.append(template_str_id)
    # print(templates_str_id)
    return jsonify({'templates': templates_str_id}), 200


def get_hotmap(uid):
    today = datetime.now()
    year = today.year
    month = today.month
    all_docs = document_collection.find({'owner_id': uid})
    docs = {}
    for doc in all_docs:
        createTime = doc['createTime']
        d_year = createTime[:4]
        d_month = createTime[5:7]
        d_date = createTime[8:10]
        if (d_year == str(year) and d_month <= str(month)) or (d_year == str(year - 1) and int(d_month) >= month):
            date_str = d_year + '-' + d_month + '-' + d_date
            docs[date_str] = docs.get(date_str, 0) + 1
    print(docs)
    return jsonify({'docs': docs}), 200


def changeShare(did, flag):
    document_collection.update_one({'_id': ObjectId(did)}, {'$set': {'is_shared': flag}})
    return jsonify({'message': 'ok'}), 200


def getShare(share_id):
    print(share_id)
    share = document_collection.find_one({'share_id': share_id})
    if share:
        if share['is_shared']:
            doc_str_id = {
                '_id': str(share['_id']) if '_id' in share else None,
            }
            doc_str_id.update({k: v for k, v in share.items() if k != '_id'})
            return jsonify({'doc': doc_str_id}), 200
        else:
            return jsonify({'message': '此文档未共享'}), 201
    else:
        return jsonify({'message': '不存在共享码'}), 202


