#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/26 17:57
# @Author : YvanZheng 
# @File : __init__.py
# @Software: PyCharm
# @Note : Note

import os

import redis
from flask import Flask, Request
from app.views.user_views import user_blueprint
from app.views.project_views import project_blueprint
from app.views.base_views import base_blueprint
from app.views.module_views import module_blueprint
from app.views.case_views import case_blueprint
from app.views.task_views import task_blueprint
from app.views.soap_views import soap_blueprint
from app.models.models import db


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)
    app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024

    # 热部署
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # 注册蓝图
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=base_blueprint, url_prefix='/base')
    app.register_blueprint(blueprint=project_blueprint, url_prefix='/project')
    app.register_blueprint(blueprint=module_blueprint, url_prefix='/module')
    app.register_blueprint(blueprint=case_blueprint, url_prefix='/cases')
    app.register_blueprint(blueprint=task_blueprint, url_prefix='/task')
    app.register_blueprint(blueprint=soap_blueprint, url_prefix='/soap')

    # 数据库连接信息
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/tbug'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 设置session密钥
    app.config['SECRET_KEY'] = 'secret_key'
    # 设置 默认连连接的redis数据库接到本地6379
    app.config['SESSION_TYPE'] = 'redis'
    # 设置远程
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

    db.init_app(app=app)

    return app
