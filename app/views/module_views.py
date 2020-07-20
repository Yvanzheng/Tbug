#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/2 17:24
# @Author : YvanZheng 
# @File : project_views.py
# @Software: PyCharm
# @Note :module views 交互层
from flask import Blueprint, render_template, request, session
import json
from datetime import datetime
from app.models.models import Project, User, State, Module
from app.utils.ch_login import is_login
from app.utils.page_util import Pagination

# from logs.log_util import logger
module_blueprint = Blueprint('module', __name__)


@module_blueprint.route('/getModules/', methods=['GET', 'POST'])
@is_login
def get_modules():
    """
    获取所有模块信息 分页查询
    """
    modules = ""
    if request.method == 'GET':
        modules = Module.query.filter().all()
    if request.method == 'POST':
        moduleName = request.form.get('moduleName')
        start = request.form.get('start')
        end = request.form.get('end')
        moduleState = request.form.get('module_state')
        user = request.form.get('user')
        if moduleName == "" and moduleState == "" and start == "" and end == "" and user == "":
            modules = Module.query.filter().all()
        else:
            filterList = []
            if moduleName != "":
                filterList.append(Module.m_name.like("%" + moduleName + "%"))
            if user != "":
                filterList.append(Module.m_create_user_id == user)
            if moduleState != "":
                filterList.append(Module.m_state == moduleState)
            if start != "" and end != "":
                filterList.append(Module.m_create_time.__gt__(start))
                filterList.append(Module.m_create_time.__lt__(end))
            modules = Module.query.filter(*filterList).all()
    li = []
    for i in range(0, len(modules)):
        li.append(modules[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    modules = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    states = State.query.filter(State.s_item_code == 2).all()
    users = User.query.filter().all()
    # logger.info(states)
    return render_template('module-list.html', html=html, modules=modules, states=states, users=users)


@module_blueprint.route('/addModule/', methods=['GET', 'POST'])
@is_login
def add_module():
    """
    进入添加模块，新建模块
    """
    if request.method == 'GET':
        states = State.query.filter(State.s_item_code == 2).all()
        projects = Project.query.filter(Project.p_state == 1).all()
        return render_template('module-add.html', states=states, projects=projects)
    if request.method == 'POST':
        user_id = session.get('user_id')
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = ""
        if data_dict['m_name'] == "":
            result = {"flag": False, "value": "模块名称不能为空！"}
        if data_dict['m_in_project'] == "":
            result = {"flag": False, "value": "所属项目不能为空！"}
        if data_dict['m_state'] == "":
            result = {"flag": False, "value": "模块状态不能为空！"}
        else:
            module = Module.query.filter_by(m_name=data_dict['m_name']).first()
            if module:
                result = {"flag": False, "value": "模块“" + data_dict['m_name'] + "”已经存在！"}
            else:
                module = Module(m_name=data_dict['m_name'], m_create_user_id=user_id,
                                m_remarks=data_dict['m_remarks'], m_state=data_dict['m_state'],
                                m_in_project_id=data_dict['m_in_project'],
                                m_create_time=datetime.now())
                module.save()
                result = {"flag": True, "value": "模块新增成功！"}
        return result


@module_blueprint.route('/delModule/', methods=['GET', 'POST'])
@is_login
def del_module():
    """
    通过Id删除模块数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        module = Module.query.filter_by(m_id=data_dict['m_id']).first()
        module.delete()
        result = {"flag": True}
        return result


@module_blueprint.route('/delAllModule/', methods=['GET', 'POST'])
@is_login
def del_all_module():
    """
    批量删除模块数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            module = Module.query.filter_by(m_id=id).first()
            module.delete()
        return result


@module_blueprint.route('/editModule/<m_id>', methods=['GET', 'POST'])
@is_login
def edit_module(m_id):
    """
    进入修改项目页面
    """
    if request.method == "GET":
        module = Module.query.filter_by(m_id=m_id).first()
        states = State.query.filter(State.s_item_code == 2).all()
        projects = Project.query.filter(Project.p_state == 1).all()
        return render_template("module-edit.html", module=module, states=states, projects=projects)


@module_blueprint.route('/updateModule/', methods=['GET', 'POST'])
@is_login
def update_module():
    """
    确认进行修改模块
    """
    user_id = session.get('user_id')
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        module = Module.query.filter_by(m_name=data_dict['m_name']).first()
        module.m_name = data_dict['m_name']
        module.m_create_user_id = user_id
        module.m_remarks = data_dict['m_remarks']
        module.m_in_project_id = data_dict['m_in_project']
        module.m_state = data_dict['m_state']
        module.m_create_time = datetime.now()
        module.save()
        result = {"flag": True, "value": "模块修改完成！"}
        return result
