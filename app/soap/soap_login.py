#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/8/12 15:39
# @Author : YvanZheng
# @File : soap_login.py
# @Software: PyCharm
# @Note : soap 业务登录util
import requests


# soap登录
def SimulateUserLogin(username, password):
    loginUrl = 'http://10.255.255.99:8100/Login.php?username=%s&password=%s&appkey=5000&ip_address=192.168.99.61&watchdog_flg=1' % (
        username, password)
    res = requests.get(loginUrl)
    resContent = res.text
    session_id = getValueFromResponse(resContent, '<sessionID>')
    custId = getValueFromResponse(resContent, '<custid>')
    viptype = getValueFromResponse(resContent, '<viptype>')
    result = {"sessionId": session_id, "custId": custId, "vipType": viptype}
    # return result
    return custId


def getValueFromResponse(resContent, key):
    listContent = resContent.split('\n')
    for line in listContent:
        if (key in line):
            value = line.strip().split('<![CDATA[')[1][0:-1]
            res = value[:value.index(']]')]
            return res
    return ""


if __name__ == '__main__':
    username = "lichao01@dangdang.com"
    password = "123456"
    print(SimulateUserLogin(username, password))
