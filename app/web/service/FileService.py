# -*- coding: utf-8 -*-
# @Time : 2022/5/4 18:35
# @Author : Vincent Vic
# @File : CategoryService.py
# @Software: PyCharm
import datetime
import uuid

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging


# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
from common.lib.APIException import APIUpdateFail

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在CosConfig中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
secret_id = 'AKIDlLfiU0GFxOZT6RVJq65nEOHuHNDl34oG'     # 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
secret_key = 'D9oBI8gxxhAMGuGL9hyyg7IBn8E3brsc'   # 替换为用户的 SecretKey，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
region = 'ap-guangzhou'      # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

class FileService:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            # 如果__instance还没有值，就给__instance变量赋值
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            # 如果__instance有值，则直接返回。
            return cls.__instance

    def uploadFile(self, file,ext):
        file_path = datetime.datetime.now().strftime('/%Y/%m/%d/')
        uid = str(uuid.uuid4())
        filename = file_path + ''.join(uid.split('-')) + "." + ext
        # 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        client = CosS3Client(config)
        response = client.put_object(
            Bucket='flowboot-1301252068',  # Bucket 由 BucketName-APPID 组成
            Body=file,
            Key=filename,
            StorageClass='STANDARD',
            ContentType='image/png'
        )

        if not response['ETag']:
            raise APIUpdateFail
        return filename


