#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/26 17:57
# @Author : YvanZheng
# @File : manage.py
# @Software: PyCharm
# @Note : 项目入口
from flask_script import Manager
from app import create_app

app = create_app()
manage = Manager(app)

if __name__ == '__main__':
    manage.run()
