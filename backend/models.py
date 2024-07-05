import hashlib


def _hash_password(password):
    # 使用哈希函数加密密码，这里以SHA-256为例
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


class User:
    def __init__(self, uid, username, email, password, is_paid=False, duration=0, start_date=None):
        self.uid = uid  # 用户ID
        self.username = username  # 用户名
        self.password = password  # 密码
        self.email = email  # 邮箱
        self.is_paid = is_paid  # 是否已支付
        self.duration = duration  # 付费持续天数
        self.start_date = start_date  # 付费开始时间


class Document:
    def __init__(self, did, share_id, is_shared, title, content, create_time, finish_time, metadata, owner_id):
        self.did = did  # 文档ID
        self.share_id = share_id  # 文档共享ID
        self.is_shared = is_shared  # 文档是否共享
        self.title = title  # 文档标题
        self.content = content  # 文档内容
        self.create_time = create_time  # 文档初始化时间
        self.finish_time = finish_time  # 文档最后一次编辑结束时间
        self.metadata = metadata  # 文档标签
        self.owner_id = owner_id  # 文档作者id
        self.medias = []  # 文档中媒体文件列表


class Template:
    def __init__(self, tid, title, content, owner_id=None, is_public=False):
        self.tid = tid
        self.title = title
        self.content = content
        self.owner_id = owner_id  # 个人模板的拥有者ID，公共模板此值为None
        self.is_public = is_public  # 标记模板是否为公共模板


class Media:
    def __init__(self, mid, media_type, media_url, caption, doc_id):
        self.mid = mid
        self.media_type = media_type
        self.media_url = media_url
        self.caption = caption
        self.doc_id = doc_id
