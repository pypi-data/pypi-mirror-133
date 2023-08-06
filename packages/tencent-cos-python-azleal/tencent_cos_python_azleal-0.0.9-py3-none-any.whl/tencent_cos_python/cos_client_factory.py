import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

SPLITTER = "."
PREFIX = SPLITTER.join(["tencent", "cos", ""])


class CosClientFactory(object):

    def __init__(self, env_prefix=PREFIX, env_splitter=SPLITTER):
        self.env_prefix = env_prefix
        self.env_splitter = env_splitter
        self.cos_clients = self.get_cos_clients_from_env()

    def get_cos_clients_from_env(self):
        cos_configs = {}
        cos_clients = {}
        for env in os.environ:
            if env.startswith(self.env_prefix):
                partial_key = env[len(self.env_prefix):]
                bucket, config_key = partial_key.split(self.env_splitter)
                if bucket not in cos_configs:
                    cos_configs[bucket] = {"bucket": bucket}
                cos_configs[bucket][config_key] = os.getenv(env)
        for client_name in cos_configs:
            assert "region" in cos_configs[client_name], "region必须存在"
            assert "secretid" in cos_configs[client_name], "secretid必须存在"
            assert "secretkey" in cos_configs[client_name], "secretkey必须存在"

            config_dict = cos_configs[client_name]
            token = config_dict["token"] if "token" in config_dict else None
            scheme = config_dict["scheme"] if "scheme" in config_dict else "https"

            config = CosConfig(Region=config_dict["region"], SecretId=config_dict["secretid"],
                               SecretKey=config_dict["secretkey"], Token=token, Scheme=scheme)

            bucket_name = cos_configs[client_name]["bucket"]
            cos_clients[bucket_name] = CosS3Client(config)

        return cos_clients

    def get(self, bucket) -> CosS3Client:
        assert bucket in self.cos_clients, "bucket:[%s]不存在" % bucket
        return self.cos_clients[bucket]
