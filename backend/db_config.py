from threading import local

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# 定义一个线程本地变量来存储数据库连接
_thread_locals = local()


class DBConnectionError(Exception):
    pass


class DBConfig:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='richEditorDB'):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        """创建MongoDB客户端并连接到数据库"""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            # 检查连接是否成功
            self.client.admin.command('ping')
        except ConnectionFailure as e:
            raise DBConnectionError(f"MongoDB connection failed: {e}")

    def get_db(self):
        """获取数据库连接"""
        if not hasattr(_thread_locals, 'db'):
            try:
                self.connect()
                _thread_locals.db = self.db
            except DBConnectionError as e:
                print(e)
                raise
        return _thread_locals.db

    def close_connection(self):
        """关闭数据库连接"""
        if self.client:
            self.client.close()


# 上下文管理器
class DBContextManager:
    def __enter__(self):
        self.db_config = DBConfig()
        self.db_config.connect()
        return self.db_config.get_db()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_config.close_connection()


