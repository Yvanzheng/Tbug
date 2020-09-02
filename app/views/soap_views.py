#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/23 10:36
# @Author : YvanZheng 
# @File : soap_views.py
# @Software: PyCharm
# @Note : soap views 交互层

from flask import Blueprint, render_template, request, session
import json
from datetime import datetime
from app.models.models import User, Methods, Soap
from app.utils.ch_login import is_login
from app.utils.page_util import Pagination

soap_blueprint = Blueprint('soap', __name__)


# soap注册方法相关 start
@soap_blueprint.route('/shows/', methods=['GET', 'POST'])
@is_login
def shows():
    """
    获取所有注册服务 分页查询
    """
    methods = ""
    if request.method == 'GET':
        methods = Methods.query.filter().all()
    if request.method == 'POST':
        methodName = request.form.get('methodName')
        start = request.form.get('start')
        end = request.form.get('end')
        user = request.form.get('user')
        if methodName == "" and start == "" and end == "" and user == "":
            methods = Methods.query.filter().all()
        else:
            filterList = []
            if methodName != "":
                filterList.append(Methods.md_method.like("%" + methodName + "%"))
            if user != "":
                filterList.append(Methods.md_create_user_id == user)
            if start != "" and end != "":
                filterList.append(Methods.md_create_time.__gt__(start))
                filterList.append(Methods.md_create_time.__lt__(end))
            methods = Methods.query.filter(*filterList).all()
    li = []
    for i in range(0, len(methods)):
        li.append(methods[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    methods = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    users = User.query.filter().all()
    return render_template('method-regiest.html', html=html, methods=methods, users=users)


@soap_blueprint.route('/addMethod/', methods=['GET', 'POST'])
@is_login
def add_method():
    """
    进入添加soap注册方法
    """
    if request.method == 'GET':
        return render_template('method-add.html')
    if request.method == 'POST':
        user_id = session.get('user_id')
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = ""
        if data_dict['md_name'] == "":
            result = {"flag": False, "value": "方法名称不能为空！"}
        if data_dict['md_method'] == "":
            result = {"flag": False, "value": "方法值不能为空！"}
        else:
            method = Methods.query.filter_by(md_name=data_dict['md_name']).first()
            if method:
                result = {"flag": False, "value": "soap注册方法名:“" + data_dict['md_name'] + "”已经存在！"}
            method = Methods.query.filter_by(md_method=data_dict['md_method']).first()
            if method:
                result = {"flag": False, "value": "soap注册方法:“" + data_dict['md_method'] + "”已经存在！"}
            else:
                method = Methods(md_name=data_dict['md_name'], md_create_user_id=user_id,
                                 md_method=data_dict['md_method'], md_create_time=datetime.now())
                method.save()
                result = {"flag": True, "value": "soap注册方法新增成功！"}
        return result


@soap_blueprint.route('/delMethod/', methods=['GET', 'POST'])
@is_login
def del_method():
    """
    通过Id删除soap注册方法数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        method = Methods.query.filter_by(md_id=data_dict['md_id']).first()
        method.delete()
        result = {"flag": True}
        return result


@soap_blueprint.route('/delAllMethods/', methods=['GET', 'POST'])
@is_login
def del_all_methods():
    """
    批量删除soap注册方法数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            method = Methods.query.filter_by(md_id=id).first()
            method.delete()
        return result


@soap_blueprint.route('/editMethod/<md_id>', methods=['GET', 'POST'])
@is_login
def edit_cases(md_id):
    """
    进入修改soap注册页面
    """
    if request.method == "GET":
        method = Methods.query.filter_by(md_id=md_id).first()
        return render_template("method-edit.html", method=method)


@soap_blueprint.route('/updateMethod/', methods=['GET', 'POST'])
@is_login
def update_Method():
    """
    确认进行修改soap注册方法
    """
    user_id = session.get('user_id')
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        method = Methods.query.filter_by(md_method=data_dict['md_method']).first()
        print(method)
        if method:
            result = {"flag": False, "value": "Soap注册方法：" + data_dict['md_method'] + "存在！"}
        else:
            method = Methods.query.filter_by(md_id=data_dict['md_id']).first()
            method.md_name = data_dict['md_name']
            method.md_method = data_dict['md_method']
            method.md_create_user_id = user_id
            method.md_create_time = datetime.now()
            method.save()
            result = {"flag": True, "value": "修改成功！"}
        return result


# soap执行相关 start
@soap_blueprint.route('/soaps/', methods=['GET', 'POST'])
@is_login
def soaps():
    """
    获取所有soap执行任务服务 分页查询
    """
    soaps = ""
    if request.method == 'GET':
        soaps = Soap.query.filter().all()
    if request.method == 'POST':
        soap_method = request.form.get('soap_method')
        soap_call_timing = request.form.get('soap_call_timing')
        start = request.form.get('start')
        end = request.form.get('end')
        user = request.form.get('user')
        if soap_method == "" and soap_call_timing == "" and start == "" and end == "" and user == "":
            soaps = Soap.query.filter().all()
        else:
            filterList = []
            if soap_method != "":
                filterList.append(Soap.soap_method.like("%" + soap_method + "%"))
            if soap_call_timing != "":
                filterList.append(Soap.soap_call_timing.like("%" + soap_call_timing + "%"))
            if user != "":
                filterList.append(Soap.soap_create_user_id == user)
            if start != "" and end != "":
                filterList.append(Soap.soap_create_time.__gt__(start))
                filterList.append(Soap.soap_create_time.__lt__(end))
            soaps = Soap.query.filter(*filterList).all()
    li = []
    for i in range(0, len(soaps)):
        li.append(soaps[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    soaps = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    users = User.query.filter().all()
    return render_template('soap-list.html', html=html, soaps=soaps, users=users)


@soap_blueprint.route('/addSoap/', methods=['GET', 'POST'])
@is_login
def add_soap():
    """
    进入添加soap注册方法
    """
    if request.method == 'GET':
        return render_template('soap-add.html')
    if request.method == 'POST':
        user_id = session.get('user_id')
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = ""
        if data_dict['soap_method'] == "":
            result = {"flag": False, "value": "接口名不能为空！"}
        if data_dict['soap_call_timing'] == "":
            result = {"flag": False, "value": "调用时机不能为空！"}
        if data_dict['soap_pmara'] == "":
            result = {"flag": False, "value": "入参示例不能为空！"}
        if data_dict['soap_except'] == "":
            result = {"flag": False, "value": "响应示例不能为空！"}
        else:
            soap = Soap.query.filter_by(soap_method=data_dict['soap_method']).first()
            if soap:
                result = {"flag": False, "value": "soap方法名:“" + data_dict['soap_method'] + "”已经存在！"}
            else:
                soap = Soap(soap_method=data_dict['soap_method'], soap_create_user_id=user_id,
                            soap_call_timing=data_dict['soap_call_timing'], soap_pmara=data_dict['soap_pmara'],
                            soap_except=data_dict['soap_except'], soap_rusult='', soap_create_time=datetime.now())
                soap.save()
                result = {"flag": True, "value": "soap测试数据新增成功！"}
        return result


@soap_blueprint.route('/delSoap/', methods=['GET', 'POST'])
@is_login
def del_soap():
    """
    通过Id删除soap请求数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        soap = Soap.query.filter_by(soap_id=data_dict['soap_id']).first()
        soap.delete()
        result = {"flag": True}
        return result


@soap_blueprint.route('/delAllSoaps/', methods=['GET', 'POST'])
@is_login
def del_all_soaps():
    """
    批量删除soap数据
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            soap = Soap.query.filter_by(soap_id=id).first()
            soap.delete()
        return result


@soap_blueprint.route('/editSoap/<soap_id>', methods=['GET', 'POST'])
@is_login
def edit_soap(soap_id):
    """
    进入修改soap注册页面
    """
    if request.method == "GET":
        soap = Soap.query.filter_by(soap_id=soap_id).first()
        return render_template("soap-edit.html", soap=soap)


@soap_blueprint.route('/updateSoap/', methods=['GET', 'POST'])
@is_login
def update_soap():
    """
    确认进行修改soap数据
    """
    user_id = session.get('user_id')
    result = ""
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        soap = Soap.query.filter_by(soap_id=data_dict['soap_id']).first()
        soap.soap_method = data_dict['soap_method']
        soap.soap_call_timing = data_dict['soap_call_timing']
        soap.soap_pmara = data_dict['soap_pmara']
        soap.soap_except = data_dict['soap_except']
        soap.soap_create_time = datetime.now()
        soap.soap_create_user_id = user_id
        soap.save()
        result = {"flag": True, "value": "修改成功！"}
    return result
