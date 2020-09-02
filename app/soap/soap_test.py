#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/8/11 18:40
# @Author : YvanZheng 
# @File : soap_test.py
# @Software: PyCharm
# @Note : soap 接口测试案例
import xlrd, os
from app.soap.soap_regiest import soap_regiest as soap_reg
from app.soap import soap_login

data = []


# 获取excel文件数据
def read_xsls(xlsx_path):
    data_xsls = xlrd.open_workbook(xlsx_path)  # 打开此地址下的exl文档
    sheet_name = data_xsls.sheets()[0]  # 进入第一张表
    sheet_name1 = data_xsls.sheet_by_index(0)  # sheet索引从0开始
    count_nrows = sheet_name.nrows  # 获取总行数
    count_nocls = sheet_name.ncols  # 获得总列数
    line_value = sheet_name.row_values(0)  # Excel表头
    for i in range(1, count_nrows):
        data_val = {}
        for j in range(0, count_nocls):
            data_val[line_value[j]] = sheet_name1.cell(i, j).value
        data.append(data_val)
    return data


def get_datas(data):
    method = ""  # 方法名
    pmara = ""  # 参数
    list = []  # 接口数据集合
    for dt in data:
        dict = {}  # 接口 key:value
        for k in dt:
            if k == "接口名":
                method = dt[k]
            if k == "入参示例":
                pmara = dt[k]
            dict[method] = pmara
        list.append(dict)
    return list


def set_method(data):
    li = []  # 接口数据集合
    method = ""
    for dt in data:
        for k in dt:
            if k == "接口名":
                method = dt[k]
        li.append(method)
        li = list(set(li))
    file = open("soap_regiest.py", encoding="utf-8", mode="a")
    for method in li:
        file.write('        if key == "' + method + '":\n'
                   '            result = client.service.' + method + '(pmara)\n'
                   '            print(result)\n'
                   '            return result\n')
    file.close()


def soap_req(data,custId):
    for li in data:
        url = ""
        pmara = ""
        for key in li:
            if key == "接口名":
                url = li[key]
            if key == "入参示例":
                pmara = update_custId(li[key], custId)
        soap_reg.choose(url, pmara)


def update_custId(data, custId):
    data = data[0:(data.find('<cust_id>'))+18]+custId+data[data.find('</cust_id>')-3:]
    print("请求参数：\n"+data)
    return data


if __name__ == '__main__':
    excel_path = os.getcwd() + '/data/soap_test.xlsx'
    data = read_xsls(excel_path)
    # print(data)
    # set_method(data)
    cust_id = soap_login.SimulateUserLogin("18883773158", "123456")
    soap_req(data, cust_id)
