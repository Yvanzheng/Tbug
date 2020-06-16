#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/26 18:29
# @Author : YvanZheng 
# @File : user_models.py
# @Software: PyCharm
# @Note : user数据库模型
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='用户密码')
    type = db.Column(db.Integer, comment='用户类型')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()


class Item(db.Model):
    __tablename__ = 'item'

    i_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='分类ID')
    i_value = db.Column(db.String(255), comment='分类值')
    i_create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, comment='创建人ID')
    i_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建时间')
    i_desc = db.Column(db.String(255), comment='分类描述')
    to_user = db.relationship('User', backref=db.backref('items'))

    def __init__(self, i_value, i_create_user_id, i_create_time, i_desc):
        self.i_value = i_value
        self.i_create_user_id = i_create_user_id
        self.i_create_time = i_create_time
        self.i_desc = i_desc

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class State(db.Model):
    __tablename__ = 'state'

    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_value = db.Column(db.String(255), unique=True)
    s_item_code = db.Column(db.Integer)

    def __init__(self, s_id, s_value, s_item_code):
        self.s_id = s_id
        self.s_value = s_value
        self.s_item_code = s_item_code

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Project(db.Model):
    p_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='项目ID')
    p_create_user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=True, nullable=False, comment='创建人ID')
    p_name = db.Column(db.String(256), unique=True, nullable=False, comment='项目名称')
    p_start_time = db.Column(db.TIMESTAMP, nullable=False, comment='开始时间')
    p_end_time = db.Column(db.TIMESTAMP, nullable=False, comment='截止时间')
    p_remarks = db.Column(db.String(256), unique=True, nullable=False, comment='项目描述')
    p_state = db.Column(db.Integer, unique=True, nullable=False, comment='项目类型')
    p_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建/修改时间')

    __tablename__ = 'project'

    def __repr__(self):
        return '<Project %r>' % self.p_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()