
import numpy as np
import requests
import hashlib
import time
import boto
import httpx
import json
from diskcache import Cache
from hamunafs.backends.base import BackendBase

class YaoStorage(BackendBase):
    def __init__(self, cfg):
        self.api_url = 'https://hz-admin.yunvm.com/token-api'
        self.endpoint = 'hz.yunvm.com'
        self.acs_key = cfg['key']
        self.secret = cfg['secret']
        self.domain = 'http://{bucket}.hz.wanyuanyun.com'
        self.token_cache = Cache()

        self.client = boto.connect_s3(
            aws_access_key_id = self.acs_key,
            aws_secret_access_key = self.secret,
            host = self.endpoint,
            is_secure=False,
        )
        self.client.auth_region_name = 'us-west-1'
    
    def geturl(self, entrypoint):
        default_bucket, bucket_name = entrypoint.split('/')
        return '{}/{}'.format(self.domain.format(bucket=default_bucket), bucket_name)

    def __get_upload_token(self, bucket, ttl=86000, tries=0):
        tk_key = 'tk_{}'.format(bucket)
        if tries > 5:
            return False, '超出最大重试次数'

        tk = self.token_cache.get(tk_key)
        if tk is not None:
            return True, {'cloud-api-token':  self.token_cache[tk_key]}

        expire=int(time.time()) + ttl
        data = {
            "key": self.acs_key,
            "bucket": bucket,
            "scope": '*',
            "expire": expire,
            "sign": ""
        }
        toSign = 'key='+data['key']+'&bucket='+data['bucket']+'&expire='+str(data['expire'])+'&scope='+data['scope']+'&secret=' + self.secret
        data['sign'] =  hashlib.sha256(toSign.encode('utf-8')).hexdigest()

        resp = requests.post(self.api_url, data=json.dumps(data))
        try:
            if resp.status_code == 200:
                resp = json.loads(resp.text)
                if resp['rt'] == 0:
                    token = resp['data']['token']
                    
                    self.token_cache.set(tk_key, token, expire=expire - time.time() - 5)
                    
                    return True,  {'cloud-api-token':  token}
                else:
                    return False, resp['error']
            else:
                return self.__get_upload_token(bucket, tries+1)
        except Exception as e:
            return self.__get_upload_token(bucket, tries+1)

    def put(self, file, bucket, bucket_name, tmp=True):
        try:
            if tmp:
                default_bucket = 'tmps'
            else:
                default_bucket = 'others'

            ret, r = self.__get_upload_token(default_bucket)

            b_name = '{}_{}'.format(bucket, bucket_name)
            
            if ret:
                _bucket = self.client.get_bucket(default_bucket, headers=r, validate=False)
                key = _bucket.new_key(b_name)
                key.set_contents_from_filename(file, headers=r, policy='public-read')
                key.set_acl('public-read', r)
                return True, '{}/{}'.format(default_bucket, b_name)

        except Exception as e:
            return False, str(e)

    def get(self, download_path, bucket, bucket_name, tries=0):
        try:
            if tries >= 3:
                return False, '下载出错'
            else:
                ret, r = self.__get_upload_token(bucket)
                if ret:
                    _bucket = self.client.get_bucket(bucket, headers=r, validate=False)
                    key = _bucket.get_key(bucket_name)
                    if key is not None:
                        with open(download_path, 'wb') as f:
                            key.get_file(f)

                        if 'temp' == bucket:
                            self.delete_file(bucket, bucket_name)
                    
                        return True, download_path
                    else:
                        return False, '文件不存在'
                
        except Exception as e:
            if tries >= 3:
                return False, str(e)
            else:
                return self.get(download_path, bucket, bucket_name, tries+1)

    # def get(self, download_path, bucket, bucket_name, tries=0):
    #     try:
    #         if tries >= 3:
    #             return False, '下载出错'
    #         else:
    #             url = '{}/{}'.format(self.domain.format(bucket=bucket), '{}'.format(bucket_name))
    #             print(url)
    #             with open(download_path, mode='wb') as f:
    #                 with httpx.stream('GET', url) as response:
    #                     for chunk in response.iter_bytes():
    #                         f.write(chunk)
    #             return True, download_path
    #     except Exception as e:
    #         if tries >= 3:
    #             return False, str(e)
    #         else:
    #             return self.get(download_path, bucket, bucket_name, tries+1)
            
    def delete_file(self, bucket, bucket_name):
        try:
            ret, r = self.__get_upload_token(bucket)
            
            if ret:
                _bucket = self.client.get_bucket(bucket, headers=r, validate=False)
                _bucket.delete_key(bucket_name)
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    cfg = {
        'key': 'chatupload', 
        'secret': 'w2zxMfpmY1F3mNjNy7qDB6CwX80VcUbkk15E3I3b',

    }
    storage = YaoStorage(cfg)
    
    # ret, e = storage.put('/home/superpigy/文档/Data/pic/images4.jpeg', 'temp', '1.jpg')
    # default_bucket, fname = e.split('/')
    storage.get('./tmp.jpg', 'temp', 'temp_1.jpg')
