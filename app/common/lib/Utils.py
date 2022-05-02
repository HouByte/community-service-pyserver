# -*- coding: utf-8 -*-
# @Time : 2022/4/30 19:48
# @Author : Vincent Vic
# @File : Utils.py
# @Software: PyCharm
import json
import random


def ObjToJson(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)


seq = "zxcvbnmsadfghjklqwertyuiop12345678901234567890123456789012345678901234567890"
key = []


def getRandomKey(n):
    keyArr = random.sample(seq, n)
    keys = "".join(keyArr)
    return keys
