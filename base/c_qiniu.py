from qiniu import Auth, put_file, etag
from qiniu import BucketManager

from base.base_settings import qiniu_access_key, qiniu_secret_key


class QiNiu:
    bucket_name = 'image'
    host = 'https://image.6-79.cn/'
    q = Auth(qiniu_access_key, qiniu_secret_key)

    @staticmethod
    def upload(key, local_file):
        token = QiNiu.q.upload_token(QiNiu.bucket_name, key, 3600)
        ret, info = put_file(token, key, local_file)
        return ret['key'] == key and ret['hash'] == etag(local_file)

    @staticmethod
    def delete(key):
        bucket = BucketManager(QiNiu.q)
        ret, info = bucket.delete(QiNiu.bucket_name, key)
        return ret == {}
