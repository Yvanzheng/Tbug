#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/6/2 17:24
# @Author : YvanZheng
# @File : base_views.py
# @Software: PyCharm
# @Note :基础 views 交互层
from flask import Blueprint, render_template, request, session
import json
from datetime import datetime

from app.models.models import Item, User
from app.utils.ch_login import is_login
from app.utils.page_util import Pagination

base_blueprint = Blueprint('base', __name__)


@base_blueprint.route('/getItems/', methods=['GET', 'POST'])
@is_login
def get_items():
    """
    获取所有分类信息 分页查询
    """
    if request.method == 'GET':
        items = Item.query.all()
        li = []
        for i in range(0, len(items)):
            li.append(items[i])
        pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
        items = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render_template('item-list.html', html=html, items=items)


@base_blueprint.route('/showItem/', methods=['GET'])
@is_login
def show_item():
    """
    进入添加分类页面
    """
    if request.method == 'GET':
        return render_template('item-add.html')


@base_blueprint.route('/addItem/', methods=['GET', 'POST'])
@is_login
def add_item():
    """
    确认添加分类
    """
    user_id = session.get('user_id')
    if request.method == 'GET':
        return render_template('item-list.html')
    else:
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        item = Item.query.filter_by(i_value=data_dict['i_value']).first()
        if item:
            print('分类已经存在！')
            result = {"flag": False}
            return result
        else:
            print('分类不存在，请添加！')
            item = Item(i_value=data_dict['i_value'], i_create_user_id=user_id,
                        i_desc=data_dict['i_desc'], i_create_time=datetime.now())
            item.save()
            result = {"flag": True}
            return result


@base_blueprint.route('/editItem/<i_id>', methods=['GET', 'POST'])
@is_login
def edit_item(i_id):
    """
    进入修改分类页面
    """
    if request.method == "GET":
        item = Item.query.filter_by(i_id=i_id).first()
        return render_template("item-edit.html", item=item)


@base_blueprint.route('/updateItem/', methods=['GET', 'POST'])
@is_login
def update_item():
    """
    确认修改分类
    """
    user_id = session.get('user_id')
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        item = Item.query.filter_by(i_id=data_dict['i_id']).first()
        item.i_id = data_dict['i_id']
        item.i_value = data_dict['i_value']
        item.i_desc = data_dict['i_desc']
        item.i_create_user_id = user_id
        item.save()
        result = {"flag": True}
        return result


@base_blueprint.route('/delItem/', methods=['GET', 'POST'])
@is_login
def del_item():
    """
    删除分类
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        item = Item.query.filter_by(i_id=data_dict['item_id']).first()
        item.delete()
        result = {"flag": True}
        return result


@base_blueprint.route('/getStates/', methods=['GET'])
@is_login
def getStates():
    """
    获取状态信息
    """
    if request.method == 'GET':
        return render_template('state_list.html')


@base_blueprint.route('/showAddState/', methods=['GET'])
@is_login
def showAddState():
    """
    进入添加分类页面
    """
    if request.method == 'GET':
        return render_template('state-add.html')
