#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/8/28 11:40
# @Author : YvanZheng
# @File : soap_regiest.py
# @Software: PyCharm
# @Note : 方法名注册服务方法
from suds.client import Client
import subprocess

url = "http://10.3.253.194:8383/webservice-api/order_flow_mobile?wsdl"
client = Client(url)


# print(client)


class soap_regiest:

    def choose(key, pmara):
        # print("注册服务方法")
        if key == "use_dangdang_money":
            result = client.service.use_dangdang_money(pmara)
            # print("返回结果：" + result)
            return result
        if key == "cancel_coupon_money":
            result = client.service.cancel_coupon_money(pmara)
            # print("返回结果：" + result)
            return result
        if key == "cancel_dangdang_money":
            result = client.service.cancel_dangdang_money(pmara)
            # print("返回结果：" + result)
            return result
        if key == "use_coupon_money":
            result = client.service.use_coupon_money(pmara)
            # print("返回结果：" + result)
            return result
        if key == "use_point_money":
            result = client.service.use_point_money(pmara)
            # print("返回结果：" + result)
            return result
        if key == "submit_order_flow":
            result = client.service.submit_order_flow(pmara)
            # print("返回结果：" + result)
            return result
        if key == "get_order_flow":
            result = client.service.get_order_flow(pmara)
            # print("返回结果：" + result)
            return result
        if key == "cancel_point_money":
            result = client.service.cancel_point_money(pmara)
            # print("返回结果：" + result)
            return result
