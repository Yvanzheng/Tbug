#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/30 18:39
# @Author : YvanZheng 
# @File : sql_util.py
# @Software: PyCharm
# @Note : 原生态执行sql 方法
from app.models.models import db
from flask import flash
import traceback


def do_sql(sql):
    cursor = db.cursor()
    try:
        results = cursor.execute(sql)
        db.commit()
        flash("查询成功")
        db.close()
        return results
    except:
        traceback.print_exc()
        db.rollback()
        return '查询失败'
