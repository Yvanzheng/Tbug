#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/23 10:36
# @Author : YvanZheng 
# @File : task_views.py
# @Software: PyCharm
# @Note : task views 交互层

from flask import Blueprint, render_template, request, session
from app.models.models import User, Task, Project, Soap
from app.utils.ch_login import is_login
from app.utils.page_util import Pagination
from app.utils.soap_util import do_Task
import json
from datetime import datetime

# from logs.log_util import logger
task_blueprint = Blueprint('task', __name__)


@task_blueprint.route('/getTask/<tk_type>', methods=['GET', 'POST'])
@is_login
def get_task(tk_type):
    """
    获取所有定时任务信息 分页查询
    """
    tasks = ""
    projects = Project.query.filter().all()
    if request.method == 'GET':
        tasks = Task.query.filter(Task.tk_type == tk_type).all()
    if request.method == 'POST':
        tk_name = request.form.get('tk_name')
        start = request.form.get('start')
        end = request.form.get('end')
        state = request.form.get('state')
        user = request.form.get('user')
        if tk_name == "" and state == "" and start == "" and end == "" and user == "":
            tasks = Task.query.filter().all()
        else:
            filterList = []
            if tk_name != "":
                filterList.append(Task.tk_name.like("%" + tk_name + "%"))
            if user != "":
                filterList.append(Task.tk_create_user_id == user)
            if start != "" and end != "":
                filterList.append(Task.tk_create_time.__gt__(start))
                filterList.append(Task.tk_create_time.__lt__(end))
            filterList.append(Task.tk_type == tk_type)
            tasks = Task.query.filter(*filterList).all()
    li = []
    for i in range(0, len(tasks)):
        li.append(tasks[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    tasks = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    users = User.query.filter().all()
    # logger.info(states)
    return render_template('task-list.html', html=html, tasks=tasks, projects=projects, users=users)


@task_blueprint.route('/addTask/', methods=['GET', 'POST'])
@is_login
def add_task():
    """
    进入添加任务
    """
    if request.method == 'GET':
        projects = Project.query.filter().all()
        soaps = Soap.query.filter().all()
        return render_template('task-add.html', projects=projects, soaps=soaps)
    if request.method == 'POST':
        user_id = session.get('user_id')
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = ""
        if data_dict['tk_name'] == "":
            result = {"flag": False, "value": "任务名称不能为空！"}
        if data_dict['tk_in_project_id'] == "":
            result = {"flag": False, "value": "所属项目不能为空！"}
        if data_dict['tk_type'] == "":
            result = {"flag": False, "value": "项目类型不能为空！"}
        if data_dict['tk_do_tsetcases'] == "":
            result = {"flag": False, "value": "执行用例不能为空！"}
        else:
            task = Task.query.filter_by(tk_name=data_dict['tk_name']).first()
            if task:
                result = {"flag": False, "value": "SOAP任务名:“" + data_dict['tk_name'] + "”已经存在！"}
            else:
                task = Task(tk_name=data_dict['tk_name'], tk_create_user_id=user_id,
                            tk_in_project_id=data_dict['tk_in_project_id'],
                            tk_do_tsetcases=data_dict['tk_do_tsetcases'],
                            tk_desc=data_dict['tk_desc'], tk_type=data_dict['tk_type'],
                            tk_create_time=datetime.now())
                task.save()
                result = {"flag": True, "value": "SOAP任务新增成功！"}
        return result


@task_blueprint.route('/delTask/', methods=['GET', 'POST'])
@is_login
def del_task():
    """
    通过Id删除task请求数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        task = Task.query.filter_by(tk_id=data_dict['tk_id']).first()
        task.delete()
        result = {"flag": True}
        return result


@task_blueprint.route('/delAllTasks/', methods=['GET', 'POST'])
@is_login
def del_all_tasks():
    """
    批量删除task数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            task = Task.query.filter_by(tk_id=id).first()
            task.delete()
        return result


@task_blueprint.route('/editTask/<tk_id>', methods=['GET', 'POST'])
@is_login
def edit_task(tk_id):
    """
    进入修改任务页面
    """
    if request.method == "GET":
        task = Task.query.filter_by(tk_id=tk_id).first()
        projects = Project.query.filter().all()
        soaps = Soap.query.filter().all()
        cases = task.tk_do_tsetcases.split(",")
        return render_template("task-edit.html", task=task, projects=projects, soaps=soaps, cases=cases)


@task_blueprint.route('/updateTask/', methods=['GET', 'POST'])
@is_login
def update_task():
    """
    确认进行修改task数据
    """
    user_id = session.get('user_id')
    result = ""
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        task = Task.query.filter_by(tk_id=data_dict['tk_id']).first()
        task.tk_name = data_dict['tk_name']
        task.tk_in_project_id = data_dict['tk_in_project_id']
        task.tk_do_tsetcases = data_dict['tk_do_tsetcases']
        task.tk_type = data_dict['tk_type']
        task.tk_desc = data_dict['tk_desc']
        task.tk_create_time = datetime.now()
        task.tk_create_user_id = user_id
        task.save()
        result = {"flag": True, "value": "修改成功！"}
    return result


@task_blueprint.route('/detailTask/<tk_id>', methods=['GET', 'POST'])
@is_login
def detail_task(tk_id):
    """
    进入任务详情页面
    """
    if request.method == "GET":
        task = Task.query.filter_by(tk_id=tk_id).first()
        data = task.tk_do_tsetcases.split(",")
        soaps = Soap.query.filter(Soap.soap_id.in_(data)).all()
        return render_template("task-detail.html", tk_name=task.tk_name, soaps=soaps)


@task_blueprint.route('/doTask/', methods=['GET', 'POST'])
@is_login
def do_task():
    """
    执行任务页面
    """
    user_id = session.get('user_id')
    if request.method == "POST":
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        task = Task.query.filter_by(tk_id=data_dict['tk_id']).first()
        data = task.tk_do_tsetcases.split(",")
        soaps = Soap.query.filter(Soap.soap_id.in_(data)).all()
        do_Task(soaps, user_id)
        task.tk_create_time = datetime.now()
        task.tk_create_user_id = user_id
        task.save()
        result = {"flag": True, "value": "执行完成！"}
        return result
