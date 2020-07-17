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
    username = db.Column(db.String(256), nullable=False, comment='用户名')
    password = db.Column(db.String(256), nullable=False, comment='用户密码')
    # type = db.Column(db.Integer, comment='用户类型')
    type = db.Column(db.Enum('0', '1', '2', '3'), server_default='用户类型', nullable=False)

    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.type = type

    def save(self):
        db.session.add(self)
        db.session.commit()


class Item(db.Model):
    __tablename__ = 'item'

    i_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='分类ID')
    i_value = db.Column(db.String(10), comment='分类值')
    i_create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, comment='创建人ID')
    i_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建时间')
    i_desc = db.Column(db.String(256), comment='分类描述')
    to_user = db.relationship('User', backref=db.backref('i_user'))

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

    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='状态ID')
    s_value = db.Column(db.String(10), unique=True, comment='状态值')
    s_item_code = db.Column(db.Integer, db.ForeignKey('item.i_id'), nullable=False, comment='所属分类码')
    s_create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, comment='创建人ID')
    s_desc = db.Column(db.String(256), comment='分类描述')
    s_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建时间')
    to_user = db.relationship('User', backref=db.backref('s_user'))
    to_item = db.relationship('Item', backref=db.backref('s_item'))

    def __init__(self, s_value, s_item_code, s_create_user_id, s_desc, s_create_time):
        self.s_value = s_value
        self.s_item_code = s_item_code
        self.s_create_user_id = s_create_user_id
        self.s_desc = s_desc
        self.s_create_time = s_create_time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Project(db.Model):
    __tablename__ = 'project'

    p_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='项目ID')
    p_create_user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=True, nullable=False, comment='创建人ID')
    p_name = db.Column(db.String(256), unique=True, nullable=False, comment='项目名称')
    p_start_time = db.Column(db.TIMESTAMP, nullable=False, comment='开始时间')
    p_end_time = db.Column(db.TIMESTAMP, nullable=False, comment='截止时间')
    p_remarks = db.Column(db.String(256), unique=True, nullable=False, comment='项目描述')
    p_state = db.Column(db.Integer, db.ForeignKey('state.s_id'), unique=True, nullable=False, comment='项目状态')
    p_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建/修改时间')
    to_user = db.relationship('User', backref=db.backref('p_user'))
    to_state = db.relationship('State', backref=db.backref('p_state'))

    def __init__(self, p_create_user_id, p_name, p_start_time, p_end_time, p_remarks, p_state, p_create_time):
        self.p_create_user_id = p_create_user_id
        self.p_name = p_name
        self.p_start_time = p_start_time
        self.p_end_time = p_end_time
        self.p_remarks = p_remarks
        self.p_state = p_state
        self.p_create_time = p_create_time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Module(db.Model):
    __tablename__ = 'module'

    m_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='模块ID')
    m_create_user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=True, nullable=False, comment='创建人ID')
    m_name = db.Column(db.String(256), unique=True, nullable=False, comment='模块名称')
    m_in_project_id = db.Column(db.Integer, db.ForeignKey('project.p_id'), unique=True, nullable=False, comment='所属项目ID')
    m_remarks = db.Column(db.String(256), unique=True, nullable=False, comment='模块描述')
    m_state = db.Column(db.Integer, db.ForeignKey('state.s_id'), unique=True, nullable=False, comment='模块状态')
    m_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建/修改时间')
    to_user = db.relationship('User', backref=db.backref('m_user'))
    to_state = db.relationship('State', backref=db.backref('m_state'))
    to_project = db.relationship('Project', backref=db.backref('m_project'))

    def __init__(self, m_create_user_id, m_name, m_in_project_id, m_remarks, m_state, m_create_time):
        self.m_create_user_id = m_create_user_id
        self.m_name = m_name
        self.m_in_project_id = m_in_project_id
        self.m_remarks = m_remarks
        self.m_state = m_state
        self.m_create_time = m_create_time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
