# -*- coding: utf-8 -*-
# @Time : 2022/4/30 19:48
# @Author : Vincent Vic
# @File : Utils.py
# @Software: PyCharm
import json
import random
import re


def ObjToJson(obj):
    return json.dumps(obj)


seq = "zxcvbnmsadfghjklqwertyuiop12345678901234567890123456789012345678901234567890"
key = []


def getRandomKey(n):
    keyArr = random.sample(seq, n)
    keys = "".join(keyArr)
    return keys


def isMobile(mobile):
    if mobile is None:
        return False
    ret = re.match(r"^1[35678]\d{9}$", mobile)
    if ret:
        return True
    else:
        return False


def isEmail(email):
    if email is None:
        return False
    ret = re.match(r"^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+", email)
    if ret:
        return True
    else:
        return False


def isUsername(name):
    if name is None:
        return False
    ret = re.match(r"^[-_a-zA-Z0-9]{4,16}$", name)
    if ret:
        return True
    else:
        return False


def isPwd(pwd):
    if pwd is None:
        return False
    ret = re.match(r"^.{6,16}", pwd)
    if ret:
        return True
    else:
        return False
