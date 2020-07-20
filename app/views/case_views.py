#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/2 17:24
# @Author : YvanZheng 
# @File : project_views.py
# @Software: PyCharm
# @Note :cases views 交互层
from flask import Blueprint, render_template, request, session
import json
from datetime import datetime
from app.models.models import Project, User, State, Module, Cases
from app.utils.ch_login import is_login
from app.utils.page_util import Pagination

# from logs.log_util import logger
case_blueprint = Blueprint('cases', __name__)


# 用例集相关 start
@case_blueprint.route('/getCases/', methods=['GET', 'POST'])
@is_login
def get_cases():
    """
    获取所有测试用例集信息 分页查询
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
    return render_template('cases-list.html', html=html, cases=cases, states=states, users=users)


@case_blueprint.route('/addCases/', methods=['GET', 'POST'])
@is_login
def add_cases():
    """
    进入添加用例集，新建用例集
    """
    if request.method == 'GET':
        states = State.query.filter(State.s_item_code == 4).all()
        modules = Module.query.filter(Module.m_state == 3).all()
        return render_template('cases-add.html', states=states, modules=modules)
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


@case_blueprint.route('/delCases/', methods=['GET', 'POST'])
@is_login
def del_cases():
    """
    通过Id删除模块数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        cases = Cases.query.filter_by(cs_id=data_dict['cs_id']).first()
        cases.delete()
        result = {"flag": True}
        return result


@case_blueprint.route('/delAllCases/', methods=['GET', 'POST'])
@is_login
def del_all_cases():
    """
    批量删除模块数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            cases = Cases.query.filter_by(cs_id=id).first()
            cases.delete()
        return result


@case_blueprint.route('/editCases/<cs_id>', methods=['GET', 'POST'])
@is_login
def edit_cases(cs_id):
    """
    进入修改用例集页面
    """
    if request.method == "GET":
        cases = Cases.query.filter_by(cs_id=cs_id).first()
        states = State.query.filter(State.s_item_code == 4).all()
        modules = Module.query.filter(Module.m_state == 3).all()
        return render_template("cases-edit.html", cases=cases, states=states, modules=modules)


@case_blueprint.route('/updateCases/', methods=['GET', 'POST'])
@is_login
def update_cases():
    """
    确认进行修改用例集
    """
    user_id = session.get('user_id')
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        cases = Cases.query.filter_by(cs_id=data_dict['cs_id']).first()
        cases.cs_name = data_dict['cs_name']
        cases.cs_create_user_id = user_id
        cases.cs_remarks = data_dict['cs_remarks']
        cases.cs_in_module_id = data_dict['cs_in_module']
        cases.cs_state = data_dict['cs_state']
        cases.cs_create_time = datetime.now()
        cases.save()
        result = {"flag": True, "value": "用例集修改完成！"}
        return result
# 用例集相关 end


# 用例相关 start
@case_blueprint.route('/getCase/', methods=['GET', 'POST'])
@is_login
def get_case():
    """
    获取所有测试用例信息 分页查询
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
    return render_template('cases-list.html', html=html, cases=cases, states=states, users=users)


@case_blueprint.route('/addCase/', methods=['GET', 'POST'])
@is_login
def add_case():
    """
    进入添加用例集，新建用例集
    """
    if request.method == 'GET':
        states = State.query.filter(State.s_item_code == 4).all()
        modules = Module.query.filter(Module.m_state == 3).all()
        return render_template('cases-add.html', states=states, modules=modules)
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


@case_blueprint.route('/delCase/', methods=['GET', 'POST'])
@is_login
def del_case():
    """
    通过Id删除模块数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        cases = Cases.query.filter_by(cs_id=data_dict['cs_id']).first()
        cases.delete()
        result = {"flag": True}
        return result


@case_blueprint.route('/delAllCase/', methods=['GET', 'POST'])
@is_login
def del_all_case():
    """
    批量删除模块数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            cases = Cases.query.filter_by(cs_id=id).first()
            cases.delete()
        return result


@case_blueprint.route('/editCase/<cs_id>', methods=['GET', 'POST'])
@is_login
def edit_case(cs_id):
    """
    进入修改用例集页面
    """
    if request.method == "GET":
        cases = Cases.query.filter_by(cs_id=cs_id).first()
        states = State.query.filter(State.s_item_code == 4).all()
        modules = Module.query.filter(Module.m_state == 3).all()
        return render_template("cases-edit.html", cases=cases, states=states, modules=modules)


@case_blueprint.route('/updateCase/', methods=['GET', 'POST'])
@is_login
def update_case():
    """
    确认进行修改用例集
    """
    user_id = session.get('user_id')
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        cases = Cases.query.filter_by(cs_id=data_dict['cs_id']).first()
        cases.cs_name = data_dict['cs_name']
        cases.cs_create_user_id = user_id
        cases.cs_remarks = data_dict['cs_remarks']
        cases.cs_in_module_id = data_dict['cs_in_module']
        cases.cs_state = data_dict['cs_state']
        cases.cs_create_time = datetime.now()
        cases.save()
        result = {"flag": True, "value": "用例集修改完成！"}
        return result
# 用例相关 end
