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
        ver = "%s"%(1.0)
        path = "/static"+ path + "?ver="+ver
        return UrlManager.buildUrl(path)
