#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/23 10:36
# @Author : YvanZheng 
# @File : task_views.py
# @Software: PyCharm
# @Note : task views 交互层

from flask import Blueprint, render_template, request, session
import json
from datetime import datetime
from app.models.models import Project, User, State, Module, Cases
from app.utils.ch_login import is_login
from app.utils.page_util import Pagination

# from logs.log_util import logger
task_blueprint = Blueprint('task', __name__)


# 任务相关 start
@task_blueprint.route('/getTask/', methods=['GET', 'POST'])
@is_login
def get_task():
    """
    获取所有任务信息 分页查询
    """
    cases = ""
    if request.method == 'GET':
        cases = Cases.query.filter().all()
    if request.method == 'POST':
        casesName = request.form.get('casesName')
        start = request.form.get('start')
        end = request.form.get('end')
        state = request.form.get('state')
        user = request.form.get('user')
        if casesName == "" and state == "" and start == "" and end == "" and user == "":
            cases = Cases.query.filter().all()
        else:
            filterList = []
            if casesName != "":
                filterList.append(Module.m_name.like("%" + casesName + "%"))
            if user != "":
                filterList.append(Module.m_create_user_id == user)
            if state != "":
                filterList.append(Module.m_state == state)
            if start != "" and end != "":
                filterList.append(Module.m_create_time.__gt__(start))
                filterList.append(Module.m_create_time.__lt__(end))
            cases = Cases.query.filter(*filterList).all()
    li = []
    for i in range(0, len(cases)):
        li.append(cases[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    tasks = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    projects = Project.query.filter().all()
    users = User.query.filter().all()
    states = State.query.filter(State.s_item_code==5).all()
    # logger.info(states)
    return render_template('task-list.html', html=html, tasks=tasks, projects=projects, states=states, users=users)


@task_blueprint.route('/addTask/', methods=['GET', 'POST'])
@is_login
def add_task():
    """
    进入添加任务，新建执行任务
    """
    if request.method == 'GET':
        states = State.query.filter(State.s_item_code == 4).all()
        modules = Module.query.filter(Module.m_state == 3).all()
        return render_template('task-add.html', states=states, modules=modules)
    if request.method == 'POST':
        user_id = session.get('user_id')
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = ""
        if data_dict['cs_name'] == "":
            result = {"flag": False, "value": "用例集名称不能为空！"}
        if data_dict['cs_in_module'] == "":
            result = {"flag": False, "value": "所属模块不能为空！"}
        if data_dict['cs_state'] == "":
            result = {"flag": False, "value": "用例集状态不能为空！"}
        else:
            cases = Cases.query.filter_by(cs_name=data_dict['cs_name']).first()
            if cases:
                result = {"flag": False, "value": "用例集“" + data_dict['cs_name'] + "”已经存在！"}
            else:
                cases = Cases(cs_name=data_dict['cs_name'], cs_create_user_id=user_id,
                              cs_remarks=data_dict['cs_remarks'], cs_state=data_dict['cs_state'],
                              cs_in_module_id=data_dict['cs_in_module'],
                              cs_create_time=datetime.now())
                cases.save()
                result = {"flag": True, "value": "用例集新增成功！"}
        return result

# 任务相关 end


# 定时任务相关 start
@task_blueprint.route('/getQuartz/', methods=['GET', 'POST'])
@is_login
def get_quartz():
    """
    获取所有定时任务信息 分页查询
    """
    cases = ""
    if request.method == 'GET':
        cases = Cases.query.filter().all()
    if request.method == 'POST':
        casesName = request.form.get('casesName')
        start = request.form.get('start')
        end = request.form.get('end')
        state = request.form.get('state')
        user = request.form.get('user')
        if casesName == "" and state == "" and start == "" and end == "" and user == "":
            cases = Cases.query.filter().all()
        else:
            filterList = []
            if casesName != "":
                filterList.append(Module.m_name.like("%" + casesName + "%"))
            if user != "":
                filterList.append(Module.m_create_user_id == user)
            if state != "":
                filterList.append(Module.m_state == state)
            if start != "" and end != "":
                filterList.append(Module.m_create_time.__gt__(start))
                filterList.append(Module.m_create_time.__lt__(end))
            cases = Cases.query.filter(*filterList).all()
    li = []
    for i in range(0, len(cases)):
        li.append(cases[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    cases = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    states = State.query.filter(State.s_item_code == 4).all()
    users = User.query.filter().all()
    # logger.info(states)
    return render_template('task-list.html', html=html, cases=cases, states=states, users=users)
# 定时任务相关 end
