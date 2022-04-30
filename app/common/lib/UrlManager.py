# -*- coding: utf-8 -*-
# @Time : 2022/4/29 20:52
# @Author : Vincent Vic
# @File : UrlManager.py
# @Software: PyCharm

class UrlManager(object):
    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        path = path + "?ver="+"20220429"
        return UrlManager.buildUrl(path)
