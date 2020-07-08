#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/27 11:55
# @Author : YvanZheng 
# @File : user_views.py
# @Software: PyCharm
# @Note : user views 交互层
from flask import Blueprint, render_template, request, session

from app.models.models import User
from app.utils.ch_login import is_login

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/home/<userid>', methods=['GET'])
@is_login
def home(userid):
    """
    首页
    """
    if request.method == 'GET':
        user = User.query.filter_by(id=userid).first()
        return render_template('index.html', user=user)


@user_blueprint.route('/welcome/', methods=['GET'])
@is_login
def welcome():
    """
    首页Welcome
    """
    if request.method == 'GET':
        return render_template('welcome.html')


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登录
    """
    session.clear()
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 判断用户名和密码是否填写
        if not all([username, password]):
            result = {"msg": '* 请填写好完整的信息'}
            return result
        # 核对用户名和密码是否一致
        user = User.query.filter_by(username=username, password=password).first()
        # 如果用户名和密码一致
        if user:
            # 向session中写入相应的数据
            session['user_id'] = user.id
            session['username'] = user.username
            return render_template('index.html', user=user)
        # 如果用户名和密码不一致返回登录页面,并给提示信息
        else:
            result = {"msg": '* 用户名或者密码不一致'}
            return result
