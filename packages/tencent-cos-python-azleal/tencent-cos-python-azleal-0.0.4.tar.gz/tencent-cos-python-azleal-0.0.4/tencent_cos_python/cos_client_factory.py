import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

PREFIX = "tencent.tencent_cos_python."
SPLITTER = "."


def get_cos_clients_from_env():
    cos_configs = {}
    cos_clients = {}
    for env in os.environ:
        if env.startswith(PREFIX):
            partial_key = env[len(PREFIX):]
            bucket, config_key = partial_key.split(SPLITTER)
            if bucket not in cos_configs:
                cos_configs[bucket] = {"bucket": bucket}
            cos_configs[bucket][config_key] = os.getenv(env)
    for bucket_name in cos_configs:
        assert "region" in cos_configs[bucket_name], "region必须存在"
        assert "secret_id" in cos_configs[bucket_name], "secret_id必须存在"
        assert "secret_key" in cos_configs[bucket_name], "secret_key必须存在"

        config_dict = cos_configs[bucket_name]
        token = config_dict["token"] if "token" in config_dict else None
        scheme = config_dict["scheme"] if "scheme" in config_dict else "https"

        config = CosConfig(Region=config_dict["region"], SecretId=config_dict["secret_id"],
                           SecretKey=config_dict["secret_key"], Token=token, Scheme=scheme)

        cos_clients[bucket_name] = CosS3Client(config)

    return cos_clients


cos_clients = get_cos_clients_from_env()


class CosClientFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def get(bucket) -> CosS3Client:
        assert bucket in cos_clients, "bucket:[%s]不存在" % bucket
        return cos_clients[bucket]
