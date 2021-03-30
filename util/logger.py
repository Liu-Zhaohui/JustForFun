#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'liuzhaohui'


import os
import sys
import logging
import time
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from logging.handlers import RotatingFileHandler


class Log:

    def __init__(self):

        # 实例化
        _logger = logging.getLogger(__name__)

        # 输出到标准输出流
        _handler1 = logging.StreamHandler()

        # 输出到文件，这里是以固定大小，备份10份，也可以按照日期进行备份
        _log_path = os.path.join(base_path, 'log', 'log.txt')
        print(_log_path)
        _handler2 = RotatingFileHandler(_log_path, mode='w', maxBytes=10 * 1024 * 1024, backupCount=10)

        # 分别配置控制台和日志文件中的日志级别
        _logger.setLevel(logging.DEBUG)
        _handler1.setLevel(logging.WARNING)
        _handler2.setLevel(logging.DEBUG)

        # 日志的格式
        _formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

        # 格式化日志
        _handler1.setFormatter(_formatter)
        _handler2.setFormatter(_formatter)

        _logger.addHandler(_handler1)
        _logger.addHandler(_handler2)
        self.logger = _logger

    # 未完工，需要写个装饰器，用来打印函数执行的信息
    # def func(function):
    #     def wrapper(*args, **kwargs):
    #         print('开始执行函数:'.format(function.__name__))
    #
    #         # 真正执行的是这行。
    #         function(*args, **kwargs)
    #
    #         print('主人，我执行完啦。')

    # 这个装饰器用得好，直接将这个函数的返回值转化成类的属性
    @property
    def debug(self):
        return self.logger.debug

    @property
    def info(self):
        return self.logger.info

    @property
    def warning(self):
        return self.logger.warning

    @property
    def error(self):
        return self.logger.error

    @property
    def critical(self):
        return self.logger.critical


if __name__ == '__main__':
    log = Log()
    log.info('info')
    log.debug('debug')
    log.warning('warn')
    log.error('error')


