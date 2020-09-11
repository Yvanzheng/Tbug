#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/26 18:29
# @Author : YvanZheng 
# @File : user_models.py
# @Software: PyCharm
# @Note : 数据库模型
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
    m_in_project_id = db.Column(db.Integer, db.ForeignKey('project.p_id'), unique=True, nullable=False,
                                comment='所属项目ID')
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


class Testcase(db.Model):
    __tablename__ = 'testcase'

    tc_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='用例ID')
    tc_create_user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=True, nullable=False,
                                  comment='创建人ID')
    tc_name = db.Column(db.String(256), unique=True, nullable=False, comment='用例名称')
    tc_url = db.Column(db.String(256), unique=True, nullable=False, comment='接口地址')
    tc_param = db.Column(db.String(256), unique=True, nullable=False, comment='请求参数')
    tc_in_module_id = db.Column(db.Integer, db.ForeignKey('module.m_id'), unique=True, nullable=False, comment='所属模块')
    tc_param_type = db.Column(db.Integer, db.ForeignKey('state.s_id'), unique=True, nullable=False, comment='参数类型')
    tc_req_method = db.Column(db.Integer, db.ForeignKey('state.s_id'), unique=True, nullable=False, comment='请求方式')
    tc_status_code = db.Column(db.Integer, db.ForeignKey('state.s_id'), unique=True, nullable=False, comment='返回码')
    tc_except = db.Column(db.String(256), unique=True, nullable=False, comment='预期结果')
    tc_link_case = db.Column(db.Integer, unique=True, nullable=False, comment='关联用例')
    tc_sql_code = db.Column(db.Integer, unique=True, nullable=False, comment='数据库判断码')
    tc_sql_data = db.Column(db.String(256), unique=True, nullable=False, comment='数据库查询语句')
    tc_sql_except = db.Column(db.String(256), unique=True, nullable=False, comment='数据库预期结果')
    tc_desc = db.Column(db.String(256), unique=True, nullable=False, comment='用例描述')
    tc_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建/修改时间')
    to_user = db.relationship('User', backref=db.backref('tc_user'))
    to_module = db.relationship('Module', foreign_keys=tc_in_module_id)
    to_state_param = db.relationship('State', foreign_keys=tc_param_type)
    to_state_method = db.relationship('State', foreign_keys=tc_req_method)
    to_state_code = db.relationship('State', foreign_keys=tc_status_code)

    def __init__(self, tc_create_user_id, tc_name, tc_url, tc_param, tc_in_module_id, tc_param_type, tc_req_method,
                 tc_status_code,
                 tc_except, tc_link_case, tc_sql_code, tc_sql_data, tc_sql_except, tc_desc, tc_create_time):
        self.tc_create_user_id = tc_create_user_id
        self.tc_name = tc_name
        self.tc_url = tc_url
        self.tc_param = tc_param
        self.tc_in_module_id = tc_in_module_id
        self.tc_param_type = tc_param_type
        self.tc_req_method = tc_req_method
        self.tc_status_code = tc_status_code
        self.tc_except = tc_except
        self.tc_link_case = tc_link_case
        self.tc_sql_code = tc_sql_code
        self.tc_sql_data = tc_sql_data
        self.tc_sql_except = tc_sql_except
        self.tc_desc = tc_desc
        self.tc_create_time = tc_create_time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Cases(db.Model):
    __tablename__ = 'cases'

    cs_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='用例集ID')
    cs_create_user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=True, nullable=False,
                                  comment='创建人ID')
    cs_name = db.Column(db.String(256), unique=True, nullable=False, comment='用例集名称')
    cs_in_module_id = db.Column(db.Integer, db.ForeignKey('module.m_id'), unique=True, nullable=False, comment='所属模块ID')
    cs_remarks = db.Column(db.String(256), unique=True, nullable=False, comment='用例集描述')
    cs_do_cases = db.Column(db.String(256), unique=True, nullable=False, comment='执行用例')
    cs_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建/修改时间')
    to_user = db.relationship('User', backref=db.backref('cs_user'))
    to_module = db.relationship('Module', backref=db.backref('cs_module'))

    def __init__(self, cs_create_user_id, cs_name, cs_in_module_id, cs_remarks, cs_do_cases, cs_create_time):
        self.cs_create_user_id = cs_create_user_id
        self.cs_name = cs_name
        self.cs_in_module_id = cs_in_module_id
        self.cs_remarks = cs_remarks
        self.cs_do_cases = cs_do_cases
        self.cs_create_time = cs_create_time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Methods(db.Model):
    __tablename__ = 'methods'

    md_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='SOAP服务ID')
    md_create_user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=True, nullable=False,
                                  comment='创建人ID')
    md_name = db.Column(db.String(256), unique=True, nullable=False, comment='SOAP方法名称')
    md_method = db.Column(db.String(256), unique=True, nullable=False, comment='SOAP注册方法')
    md_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建/修改时间')
    to_user = db.relationship('User', backref=db.backref('md_user'))

    def __init__(self, md_create_user_id, md_name, md_method, md_create_time):
        self.md_create_user_id = md_create_user_id
        self.md_name = md_name
        self.md_method = md_method
        self.md_create_time = md_create_time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Soap(db.Model):
    __tablename__ = 'soap'

    soap_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='SOAP服务ID')
    soap_method = db.Column(db.String(256), unique=True, nullable=False, comment='接口名')
    soap_call_timing = db.Column(db.String(256), unique=True, nullable=False, comment='调用时机')
    soap_pmara = db.Column(db.Text, unique=True, nullable=False, comment='入参示例')
    soap_except = db.Column(db.Text, unique=True, nullable=False, comment='响应示例')
    soap_rusult = db.Column(db.Text, unique=True, nullable=False, comment='返回结果')
    soap_create_user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=True, nullable=False,
                                    comment='创建人ID')
    soap_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建/修改时间')
    to_user = db.relationship('User', backref=db.backref('soap_user'))

    def __init__(self, soap_method, soap_call_timing, soap_pmara, soap_except, soap_rusult, soap_create_user_id,
                 soap_create_time):
        self.soap_method = soap_method
        self.soap_call_timing = soap_call_timing
        self.soap_pmara = soap_pmara
        self.soap_except = soap_except
        self.soap_rusult = soap_rusult
        self.soap_create_user_id = soap_create_user_id
        self.soap_create_time = soap_create_time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Task(db.Model):
    __tablename__ = 'task'

    tk_id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment='任务ID')
    tk_name = db.Column(db.String(256), unique=True, nullable=False, comment='任务名称')
    tk_in_project_id = db.Column(db.Integer, db.ForeignKey('project.p_id'), unique=True, nullable=False, comment='所属项目ID')
    tk_do_tsetcases = db.Column(db.String(1024), unique=True, nullable=False, comment='执行用例')
    tk_desc = db.Column(db.String(256), unique=True, nullable=False, comment='任务描述')
    tk_type = db.Column(db.String(256), unique=True, nullable=False, comment='任务类型')
    tk_create_user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=True, nullable=False, comment='创建人ID')
    tk_create_time = db.Column(db.TIMESTAMP, nullable=False, comment='创建/修改时间')
    to_user = db.relationship('User', backref=db.backref('tk_user'))
    to_project = db.relationship('Project', backref=db.backref('tk_project'))

    def __init__(self, tk_name, tk_in_project_id, tk_do_tsetcases, tk_desc, tk_type, tk_create_user_id, tk_create_time):
        self.tk_name = tk_name
        self.tk_in_project_id = tk_in_project_id
        self.tk_do_tsetcases = tk_do_tsetcases
        self.tk_desc = tk_desc
        self.tk_type = tk_type
        self.tk_create_user_id = tk_create_user_id
        self.tk_create_time = tk_create_time

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
