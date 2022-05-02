# -*- coding: utf-8 -*-
# @Time : 2022/5/2 10:08
# @Author : Vincent Vic
# @File : Helper.py
# @Software: PyCharm
# 统一渲染方法

from flask import g, render_template


def ops_render(template, context={}):
    if 'current_user' in g:
        context['current_user'] = g.current_user
    return render_template(template, **context)
