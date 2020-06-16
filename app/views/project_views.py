#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/2 17:24
# @Author : YvanZheng 
# @File : project_views.py
# @Software: PyCharm
# @Note :project views 交互层
from flask import Blueprint, render_template, request
import json

from app.models.models import Project
from app.utils.ch_login import is_login

project_blueprint = Blueprint('project', __name__)


@project_blueprint.route('/getProjects/', methods=['GET'])
@is_login
def getProjects():
    """
    获取全部项目信息
    """
    if request.method == 'GET':
        return render_template('project-list.html')


@project_blueprint.route('/showAddProject/', methods=['GET'])
@is_login
def showAddProject():
    """
    进入添加页面
    """
    if request.method == 'GET':
        return render_template('project-add.html')


@project_blueprint.route('/addProjects/', methods=['GET', 'POST'])
@is_login
def addProject():
    """
    确认新建项目
    """
    if request.method == 'GET':
        return render_template('project-list.html')
    else:
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        print(data_dict['p_name'])
        Project.p_name = data_dict['p_name']
        return render_template('project-list.html')
