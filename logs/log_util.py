# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time : 2020/7/7 10:26
# # @Author : YvanZheng
# # @File : log_util.py
# # @Software: PyCharm
# # @Note : 日志基础配置类
# import logging
# from logging import handlers
# import os
# import configparser
#
# # 1.获取根目录
# root_path = os.path.split(os.path.realpath(__file__))[0]
# # 2. 设置日志解析实例
# cf = configparser.ConfigParser()
# # 3.读取日志文件
# cf.read(root_path + "/logs/log.conf")
#
#
# class Mylogger(object):
#     def __init__(self, log_name):
#         # 1.指明日志记录到哪个文件 "/logs/" + "info.log"
#         logfile = root_path + log_name
#         # 2.配置日志操作器
#         handler = handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
#         # 3.设置日志格式
#         fmt = "%(levelname)s-%(asctime)s-%(module)s-%(lineno)d-%(message)s"
#         # 4. 配置格式实例
#         formatter = logging.Formatter(fmt)
#         # 5.操作器加载格式实例
#         handler.setFormatter(formatter)
#         # 6.创建logger实例
#         self.logger = logging.getLogger()
#         # 7.给实例增加日志操作器
#         self.logger.addHandler(handler)
#         # 8.给实例增加日志输出登记
#         self.logger.setLevel(logging.DEBUG)
#
#     # 设置方法返回looger实例
#     def get_logger(self):
#         return self.logger
#
#
# # 4. 创建自定义日志类的实例对象
# logger = Mylogger("/info.log").get_logger()
