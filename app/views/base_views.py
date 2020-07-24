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

from app.models.models import Item, State
from app.utils.ch_login import is_login
from app.utils.page_util import Pagination

base_blueprint = Blueprint('base', __name__)


@base_blueprint.route('/getItems/', methods=['GET', 'POST'])
@is_login
def get_items():
    """
    获取所有分类信息 分页查询
    """
    itemName = ''
    if request.method == 'POST':
        itemName = request.form.get('itemName')
    items = Item.query.filter(Item.i_value.like("%" + itemName + "%") if itemName is not None else "").all()
    li = []
    for i in range(0, len(items)):
        li.append(items[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    items = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('item-list.html', html=html, items=items)


@base_blueprint.route('/addItem/', methods=['GET', 'POST'])
@is_login
def add_item():
    """
    添加分类页面
    """
    if request.method == 'GET':
        return render_template('item-add.html')
    if request.method == 'POST':
        user_id = session.get('user_id')
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        item = Item.query.filter_by(i_value=data_dict['i_value']).first()
        if item:
            result = {"flag": False, "value": "分类已经存在！"}
            return result
        else:
            item = Item(i_value=data_dict['i_value'], i_create_user_id=user_id,
                        i_desc=data_dict['i_desc'], i_create_time=datetime.now())
            item.save()
            result = {"flag": True, "value": "分类新增成功！"}
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
        item = Item.query.filter_by(i_value=data_dict['i_value']).first()
        if item:
            result = {"flag": False, "value": "分类已经存在！"}
            return result
        else:
            item = Item.query.filter_by(i_id=data_dict['i_id']).first()
            item.i_id = data_dict['i_id']
            item.i_value = data_dict['i_value']
            item.i_desc = data_dict['i_desc']
            item.i_create_user_id = user_id
            item.i_create_time = datetime.now()
            item.save()
            result = {"flag": True, "value": "分类修改成功！"}
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


@base_blueprint.route('/delAllItem/', methods=['GET', 'POST'])
@is_login
def del_all_item():
    """
    删除分类
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        print(data_json)

        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            print(id)
            item = Item.query.filter_by(i_id=id).first()
            item.delete()
        return result


@base_blueprint.route('/getStates/', methods=['GET', 'POST'])
@is_login
def get_states():
    """
    获取所有状态信息 分页查询
    """
    states = ''
    if request.method == 'GET':
        states = State.query.filter().all()
    if request.method == 'POST':
        stateName = request.form.get('stateName')
        itemId = request.form.get('itemName')
        if stateName == "" and itemId == "":
            states = State.query.filter().all()
        else:
            filterList = []
            if stateName != "":
                filterList.append(State.s_value.like("%" + stateName + "%"))
            if itemId != "":
                filterList.append(State.s_item_code == itemId)
            states = State.query.filter(*filterList).all()
    li = []
    for i in range(0, len(states)):
        li.append(states[i])
    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    states = li[pager_obj.start:pager_obj.end]
    items = Item.query.filter().all()
    html = pager_obj.page_html()
    return render_template('state-list.html', html=html, states=states, items=items)


@base_blueprint.route('/addState/', methods=['GET', 'POST'])
@is_login
def add_state():
    """
    进入添加状态页面
    """
    if request.method == 'GET':
        items = Item.query.filter().all()
        return render_template('state-add.html', items=items)
    if request.method == 'POST':
        user_id = session.get('user_id')
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        print(data_dict)
        state = State.query.filter_by(s_value=data_dict['s_value'], s_item_code=data_dict['contrller']).first()
        if state:
            result = {"flag": False, "value": "状态已经存在！"}
            return result
        else:
            state = State(s_value=data_dict['s_value'], s_create_user_id=user_id, s_item_code=data_dict['contrller'],
                          s_desc=data_dict['s_desc'], s_create_time=datetime.now())
            state.save()
            result = {"flag": True, "value": "状态新增成功！"}
            return result


@base_blueprint.route('/delState/', methods=['GET', 'POST'])
@is_login
def del_state():
    """
    删除状态
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        state = State.query.filter_by(s_id=data_dict['state_id']).first()
        state.delete()
        result = {"flag": True}
        return result


@base_blueprint.route('/delAllState/', methods=['GET', 'POST'])
@is_login
def del_all_state():
    """
    删除状态
    """
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        result = {"flag": True}
        for id in data_dict:
            state = State.query.filter_by(s_id=id).first()
            state.delete()
        return result


@base_blueprint.route('/editState/<s_id>', methods=['GET', 'POST'])
@is_login
def edit_state(s_id):
    """
    进入修改状态页面
    """
    if request.method == "GET":
        state = State.query.filter_by(s_id=s_id).first()
        items = Item.query.filter().all()
        return render_template("state-edit.html", state=state, items=items)


@base_blueprint.route('/updateState/', methods=['GET', 'POST'])
@is_login
def update_state():
    """
    确认修改状态
    """
    user_id = session.get('user_id')
    if request.method == 'POST':
        data_json = request.get_data().decode('utf-8')
        data_dict = json.loads(data_json)
        state = State.query.filter_by(s_value=data_dict['s_value'], s_item_code=data_dict['s_item_code']).first()
        if state:
            result = {"flag": False, "value": "状态已经存在！"}
            return result
        else:
            state = State.query.filter_by(s_id=data_dict['s_id']).first()
            state.s_id = data_dict['s_id']
            state.s_item_code = data_dict['s_item_code']
            state.s_value = data_dict['s_value']
            state.s_desc = data_dict['s_desc']
            state.s_create_user_id = user_id
            state.s_create_time = datetime.now()
            state.save()
            result = {"flag": True, "value": "状态修改完成！"}
            return result
