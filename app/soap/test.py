#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/8/28 11:40
# @Author : YvanZheng
# @File : soap_regiest.py
# @Software: PyCharm
# @Note : 方法名注册服务方法
from suds.client import Client

url = "http://10.3.253.194:8383/webservice-api/order_flow_mobile?wsdl"
client = Client(url)
method = []


class soap_regiest:
    @classmethod
    def get_order_flow(self, pmara):
        result = client.service.get_order_flow(pmara)
        print(result)
        return result
