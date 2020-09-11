#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/10 10:42
# @Author : YvanZheng 
# @File : soap_util.py
# @Software: PyCharm
# @Note : soap 接口服务
from app.utils.soap_regiest import soap_regiest as soap_reg
from app.utils.ch_login import SimulateUserLoginJson
from app.models.models import Soap
from datetime import datetime
from suds.client import Client

url = "http://10.3.253.194:8383/webservice-api/order_flow_mobile?wsdl"
client = Client(url)


def do_Task(soaps, user_id):
    cust_id = SimulateUserLoginJson("wyz123@dangdang.com", "123123")
    soap_req(soaps, cust_id, user_id)


def soap_req(soaps, custId, userId):
    for soap in soaps:
        method = soap.soap_method
        pmara = update_custId(soap.soap_pmara, custId)
        result = soap_reg.choose(method, pmara)
        soap = Soap.query.filter_by(soap_id=soap.soap_id).first()
        soap.soap_rusult = str(result)
        soap.soap_create_user_id = userId
        soap.soap_create_time = datetime.now()
        soap.save()


def update_custId(data, custId):
    data = data[0:(data.find('<cust_id>')) + 18] + custId + data[data.find('</cust_id>') - 3:]
    return data


def set_method(method):
    print(method)
    file = open("soap_regiest.py", encoding="utf-8", mode="a")
    file.write('        if key == "' + str(method) + '":\n'
               '            result = client.service.' + str(method) + '(pmara)\n'
               '            return result\n')
    file.close()


if __name__ == '__main__':
    set_method(11)
