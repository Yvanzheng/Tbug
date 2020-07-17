#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/2 17:24
# @Author : YvanZheng 
# @File : project_views.py
# @Software: PyCharm
# @Note :project views 交互层
from flask import Blueprint, render_template, request, session
import json
from datetime import datetime
from app.models.models import Project, User, State
from app.utils.ch_login import is_login
from app.utils.page_util import Pagination
# from logs.log_util import logger
project_blueprint = Blueprint('project', __name__)


@project_blueprint.route('/getProjects/', methods=['GET', 'POST'])
@is_login
def get_projects():
    """
    获取所有项目信息 分页查询
    """
    projects = ""
    if request.method == 'GET':
        projects = Project.query.filter().all()
    if request.method == 'POST':
        projectName = request.form.get('projectName')
        start = request.form.get('start')
        end = request.form.get('end')
        projectState = request.form.get('project_state')
        user = request.form.get('user')
        if projectName == "" and projectState == "" and start == "" and end == "" and user == "":
            projects = Project.query.filter().all()
        else:
            filterList = []
            if projectName != "":
                filterList.append(Project.p_name.like("%" + projectName + "%"))
            if user != "":
                filterList.append(Project.p_create_user_id == user)
            if projectState != "":
                filterList.append(Project.p_state == projectState)
            if start != "" and end != "":
                filterList.append(Project.p_create_time.__gt__(start))
                filterList.append(Project.p_create_time.__lt__(end))
            projects = Project.query.filter(*filterList).all()
    li = []
    for i in range(0, len(projects)):
        li.append(projects[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    projects = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    states = State.query.filter(State.s_item_code == 1).all()
    users = User.query.filter().all()
    # logger.info(states)
    return render_template('project-list.html', html=html, projects=projects, states=states, users=users)


@project_blueprint.route('/addProject/', methods=['GET', 'POST'])
@is_login
def add_project():
    """
    进入添加页面，新建项目
    """
    if request.method == 'GET':
        states = State.query.filter(State.s_item_code == 1).all()
        return render_template('project-add.html', states=states)
    if request.method == 'POST':
        user_id = session.get('user_id')
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = ""
        if data_dict['p_name'] == "":
            result = {"flag": False, "value": "项目名称不能为空！"}
        if data_dict['start'] == "":
            result = {"flag": False, "value": "项目开始时间不能为空！"}
        if data_dict['end'] == "":
            result = {"flag": False, "value": "项目截止时间不能为空！"}
        if data_dict['p_state'] == "":
            result = {"flag": False, "value": "项目状态不能为空！"}
        else:
            project = Project.query.filter_by(p_name=data_dict['p_name']).first()
            if project:
                result = {"flag": False, "value": "项目“" + data_dict['p_name'] + "”已经存在！"}
            else:
                project = Project(p_name=data_dict['p_name'], p_create_user_id=user_id,
                                  p_start_time=data_dict['start'], p_end_time=data_dict['end'],
                                  p_remarks=data_dict['p_remarks'], p_state=data_dict['p_state'],
                                  p_create_time=datetime.now())
                project.save()
                result = {"flag": True, "value": "项目新增成功！"}
        return result


@project_blueprint.route('/delProject/', methods=['GET', 'POST'])
@is_login
def del_project():
    """
    删除项目
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        project = Project.query.filter_by(p_id=data_dict['project_id']).first()
        project.delete()
        result = {"flag": True}
        return result


@project_blueprint.route('/delAllProject/', methods=['GET', 'POST'])
@is_login
def del_all_project():
    """
    删除状态
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            project = Project.query.filter_by(p_id=id).first()
            project.delete()
        return result


@project_blueprint.route('/editProject/<p_id>', methods=['GET', 'POST'])
@is_login
def edit_project(p_id):
    """
    进入修改项目页面
    """
    if request.method == "GET":
        project = Project.query.filter_by(p_id=p_id).first()
        states = State.query.filter(State.s_item_code == 1).all()
        return render_template("project-edit.html", project=project, states=states)


@project_blueprint.route('/updateProject/', methods=['GET', 'POST'])
@is_login
def update_project():
    """
    确认进行修改项目
    """
    user_id = session.get('user_id')
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        projects = Project.query.filter(Project.p_name == data_dict['p_name'], Project.p_state == data_dict['p_state'],
                                       Project.p_id != data_dict['p_id']).all()
        if len(projects) > 0:
            result = {"flag": False, "value": "项目已经存在！"}
            return result
        else:
            project = Project.query.filter_by(p_name=data_dict['p_name']).first()
            project.p_name = data_dict['p_name']
            project.p_create_user_id = user_id
            project.p_start_time = data_dict['start']
            project.p_end_time = data_dict['end']
            project.p_remarks = data_dict['p_remarks']
            project.p_state = data_dict['p_state']
            project.p_create_time = datetime.now()
            project.save()
            result = {"flag": True, "value": "项目修改完成！"}
            return result
