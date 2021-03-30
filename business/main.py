#!/usr/env/bin python3
# -*- coding: utf-8 -*-

"""
执行自动化
"""

__author__ = '刘兆辉'

import os
import sys
import threading
base_path = os.getcwd()
sys.path.append(base_path)
from util.config_operation import YamlOperation
from util.device_info import DeviceInfo
from business.execute import Execute


class Run:
    def __init__(self, app):
        device = DeviceInfo(app=app)
        device.write_device_info()
        yaml_operation = YamlOperation()
        yaml_operation.read(path='../config/device_info.yaml')
        self.device_info = yaml_operation.content
        # self.exe = Execute()

    @staticmethod
    def execute(param, title=None):
        """
        多线程情况下，会造成混乱，导致只有一个手机可以正常执行
        重新写个函数，使用递归锁，完美解决此问题
        :param param:
        :param title:
        :return:
        """

        exe = Execute()
        r_lock = threading.RLock()
        r_lock.acquire()
        exe.execute_excel(param, title=title)
        r_lock.release()

    def run(self, title=None):
        for i in self.device_info:
            start_test = threading.Thread(target=self.execute, args=(i, title,))
            start_test.start()


if __name__ == '__main__':
    run = Run('D:\反诈项目\云剑反诈\应用备份\云剑反诈apk\\1.0.0.1028\\antifraud-official.apk')
    run.run(title='起飞！')
