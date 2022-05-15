# -*- coding: utf-8 -*-
# @Time : 2022/5/15 15:19
# @Author : Vincent Vic
# @File : ChartsController.py
# @Software: PyCharm
from flask import Blueprint, jsonify

from web.service.OrderService import OrderService
from web.service.SService import SService

page_charts = Blueprint('charts_page', __name__)

orderService = OrderService()
sService = SService()


@page_charts.get("/order/trading")
def getTradingData():
    resp_data = orderService.getTradingData()
    return jsonify(resp_data)


@page_charts.get("/order/trading/status")
def getTradingStatusData():
    resp_data = orderService.getTradingStatusData()
    return jsonify(resp_data)

@page_charts.get("/service/nature")
def getNatureData():
    resp_data = sService.getNatureData()
    return jsonify(resp_data)

@page_charts.get("/service/type")
def getTypeData():
    resp_data = sService.getTypeData()
    return jsonify(resp_data)
