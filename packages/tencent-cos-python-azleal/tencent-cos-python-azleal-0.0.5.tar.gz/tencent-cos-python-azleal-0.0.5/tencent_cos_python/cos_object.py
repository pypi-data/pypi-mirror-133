# -*- coding: utf-8 -*-
# appid 已在配置中移除,请在参数 Bucket 中带上 appid. Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from os import path

from qcloud_cos import CosS3Client
from urllib3.util import parse_url

from tencent_cos_python.cos_client_factory import CosClientFactory
from logger import Logger
from util import Util

logger = Logger().get()


class CosObject(object):

    def __init__(self, bucket, key):
        assert bucket is not None and len(bucket) > 0, "bucket不能为空"
        assert key is not None and len(key) > 0, "key不能为空"
        self.bucket = bucket
        self.key = key

    def object_exists(self):
        return CosClientFactory.get(self.bucket).object_exists(self.bucket, self.key)

    def get_object(self, local_file=None):
        ext = path.splitext(self.key)[1]
        local_file = local_file if local_file is not None else Util.get_random_path(length=30, non_dot_ext=ext)
        response = CosClientFactory.get(self.bucket).get_object(self.bucket, self.key)
        response['Body'].get_stream_to_file(local_file)
        logger.info(
            u"tencent_cos_python saving bucket:{}, key:{}, to local file{}".format(self.bucket, self.key, local_file))
        return local_file

    def put_object(self, local_file_path):
        with open(local_file_path, 'rb') as fp:
            response = CosClientFactory.get(self.bucket).put_object(
                Bucket=self.bucket,
                Body=fp,
                Key=self.key
            )
        logger.info("put local file path:{}, to tencent_cos_python bucket:{}, with key:{}, got Etag: {}"
                    .format(local_file_path, self.bucket, self.key, response['ETag']))

    def get_cos_client(self) -> CosS3Client:
        return CosClientFactory.get(self.bucket)

    @staticmethod
    def url_2_cos_info(self, url):
        parsed_url = parse_url(url)
        bucket = parsed_url.host.split('.')[0]
        key = parsed_url.request_uri
        return CosObject(bucket, self.normalize_key(key))

    def normalize_key(self, key: str):
        if len(key) > 1 and key.startswith('/'):
            return self.normalize_key(key[1:])
        return key
