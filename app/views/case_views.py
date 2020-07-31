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
from app.models.models import User, State, Module, Cases, Testcase
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
@case_blueprint.route('/getTestCase/', methods=['GET', 'POST'])
@is_login
def get_test_case():
    """
    获取所有测试用例信息 分页查询
    """
    caselist = ""
    if request.method == 'GET':
        caselist = Testcase.query.filter().all()
        for case in caselist:
            testcase = Testcase.query.filter(Testcase.tc_id == case.tc_link_case).first()
            if testcase is not None:
                case.parent_name = testcase.tc_name
            else:
                case.parent_name = "无"
    if request.method == 'POST':
        testcaseName = request.form.get('testcaseName')
        start = request.form.get('start')
        end = request.form.get('end')
        user = request.form.get('user')
        if testcaseName == "" and start == "" and end == "" and user == "":
            caselist = Testcase.query.filter().all()
            for case in caselist:
                testcase = Testcase.query.filter(Testcase.tc_id == case.tc_link_case).first()
                if testcase is not None:
                    case.parent_name = testcase.tc_name
                else:
                    case.parent_name = "无"
        else:
            filterList = []
            if testcaseName != "":
                filterList.append(Testcase.tc_name.like("%" + testcaseName + "%"))
            if user != "":
                filterList.append(Testcase.tc_create_user_id == user)
            if start != "" and end != "":
                filterList.append(Testcase.tc_create_time.__gt__(start))
                filterList.append(Testcase.tc_create_time.__lt__(end))
            caselist = session.query().filter(*filterList).all()
            for case in caselist:
                testcase = Testcase.query.filter(Testcase.tc_id == case.tc_link_case).first()
                if testcase is not None:
                    case.parent_name = testcase.tc_name
                else:
                    case.parent_name = "无"

    li = []
    for i in range(0, len(caselist)):
        li.append(caselist[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    caselist = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    users = User.query.filter().all()
    return render_template('case-list.html', html=html, caselist=caselist, users=users)


@case_blueprint.route('/addTestCase/', methods=['GET', 'POST'])
@is_login
def add_test_case():
    """
    1、GET  进入添加用例页面
    2、POST 新建用例
    """
    if request.method == 'GET':
        methods = State.query.filter(State.s_item_code == 3).all()
        param_types = State.query.filter(State.s_item_code == 2).all()
        rep_codes = State.query.filter(State.s_item_code == 4).all()
        testcases = Testcase.query.filter().all()
        return render_template('case-add.html', methods=methods, testcases=testcases, param_types=param_types,
                               rep_codes=rep_codes)
    if request.method == 'POST':
        user_id = session.get('user_id')
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = ""
        if data_dict['tc_name'] == "":
            result = {"flag": False, "value": "用例名称不能为空！"}
        elif data_dict['tc_url'] == "":
            result = {"flag": False, "value": "接口地址不能为空！"}
        elif data_dict['tc_param'] == "":
            result = {"flag": False, "value": "请求参数不能为空！"}
        if data_dict['tc_param_type'] == "":
            result = {"flag": False, "value": "参数类型不能为空！"}
        elif data_dict['tc_req_method'] == "":
            result = {"flag": False, "value": "请求方式不能为空！"}
        elif data_dict['tc_status_code'] == "":
            result = {"flag": False, "value": "返回码不能为空！"}
        if data_dict['tc_sql_code'] == "":
            result = {"flag": False, "value": "数据库验证不能为空！"}
        else:
            testcase = Testcase.query.filter_by(tc_name=data_dict['tc_name']).first()
            if testcase:
                result = {"flag": False, "value": "用例“" + data_dict['tc_name'] + "”已经存在！"}
            else:
                testcase = Testcase(tc_name=data_dict['tc_name'],
                                    tc_create_user_id=user_id,
                                    tc_url=data_dict['tc_url'],
                                    tc_param=data_dict['tc_param'],
                                    tc_param_type=data_dict['tc_param_type'],
                                    tc_req_method=data_dict['tc_req_method'],
                                    tc_status_code=data_dict['tc_status_code'],
                                    tc_except=data_dict['tc_except'],
                                    tc_link_case=data_dict['tc_link_case'],
                                    tc_sql_code=data_dict['tc_sql_code'],
                                    tc_sql_data=data_dict['tc_sql_data'],
                                    tc_sql_except=data_dict['tc_sql_except'],
                                    tc_desc=data_dict['tc_desc'],
                                    tc_create_time=datetime.now())
                testcase.save()
                result = {"flag": True, "value": "用例新增成功！"}
        return result


@case_blueprint.route('/delTestCase/', methods=['GET', 'POST'])
@is_login
def del_test_case():
    """
    通过Id删除用例数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        testcase = Testcase.query.filter_by(tc_id=data_dict['tc_id']).first()
        testcase.delete()
        result = {"flag": True}
        return result


@case_blueprint.route('/delTestCases/', methods=['GET', 'POST'])
@is_login
def del_test_cases():
    """
    批量删除用例数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            testcase = Testcase.query.filter_by(tc_id=id).first()
            testcase.delete()
        return result


@case_blueprint.route('/editTestCase/<tc_id>', methods=['GET', 'POST'])
@is_login
def edit_test_case(tc_id):
    """
    进入修改用例页面
    """
    if request.method == "GET":
        testcase = Testcase.query.filter_by(tc_id=tc_id).first()
        methods = State.query.filter(State.s_item_code == 3).all()
        param_types = State.query.filter(State.s_item_code == 2).all()
        rep_codes = State.query.filter(State.s_item_code == 4).all()
        parentcases = Testcase.query.filter().all()
        return render_template('case-edit.html', testcase=testcase, parentcases=parentcases, methods=methods,
                               param_types=param_types, rep_codes=rep_codes)


@case_blueprint.route('/updateTestCase/', methods=['GET', 'POST'])
@is_login
def update_test_case():
    """
    确认进行修改用例
    """
    user_id = session.get('user_id')
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        testcase = Testcase.query.filter_by(tc_id=data_dict['tc_id']).first()
        testcase.tc_name = data_dict['tc_name']
        testcase.tc_create_user_id = user_id
        testcase.tc_url = data_dict['tc_url']
        testcase.tc_param = data_dict['tc_param']
        testcase.tc_param_type = data_dict['tc_param_type']
        testcase.tc_req_method = data_dict['tc_req_method']
        testcase.tc_status_code = data_dict['tc_status_code']
        testcase.tc_except = data_dict['tc_except']
        testcase.tc_link_case = data_dict['tc_link_case']
        testcase.tc_sql_code = data_dict['tc_sql_code']
        testcase.tc_sql_data = data_dict['tc_sql_data']
        testcase.tc_sql_except = data_dict['tc_sql_except'],
        testcase.tc_desc = data_dict['tc_desc'],
        testcase.tc_create_time = datetime.now()
        testcase.save()
        result = {"flag": True, "value": "用例修改成功！"}
        return result
# 用例相关 end
