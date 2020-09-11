#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/27 12:01
# @Author : YvanZheng 
# @File : ch_login.py
# @Software: PyCharm
# @Note : Note
from flask import url_for, redirect, session
from functools import wraps
import requests, json


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))

    return check_login


def SimulateUserLoginJson(username, password):
    loginUrl = 'http://10.255.255.99:8100/Login.php?username=%s&password=%s&appkey=5000&ip_address=192.168.99.61&watchdog_flg=1' % (
        username, password)
    res = requests.get(loginUrl).text
    data_dict = json.loads(res)
    session_id = data_dict['sessionID']
    custId = data_dict['custid']
    viptype = data_dict['viptype']
    result = {"sessionId": session_id, "custId": custId, "vipType": viptype}
    # return result
    return custId
