#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
执行关键字
"""

__author__ = '刘兆辉'

import pandas as pd
import time
import os
import sys
import math
base_path = os.getcwd()
sys.path.append(base_path)
from keywords.keywords import KeyWords
from util.config_operation import YamlOperation
from util.report import Report

report = Report()


# 使用函数做装饰器，存报告结果
def func_decorator(func):
    def wrapper(self, *args, **kwargs):
        report.result = self.keywords.result
        report.exception = self.keywords.exception
    return wrapper


class Execute:

    def __init__(self):
        self.case = None
        self.keywords = KeyWords()
        # self.yaml_operation = YamlOperation()
        # report.create_report()

    @staticmethod
    def create_report(title=None):
        report.create_report(title)

    def execute(self, device_info, keyword, data, description=None):

        if keyword == 'click':
            # data = eval(self.case.loc[row, 'data'])
            self.keywords.click(method=data['method'], locator=data['locator'])
            report.result = self.keywords.result
            report.exception = self.keywords.exception

        elif keyword == 'input':
            # data = eval(self.case.loc[row, 'data'])
            self.keywords.input(method=data['method'], locator=data['locator'], value=data['value'])
            report.result = self.keywords.result
            report.exception = self.keywords.exception

        elif keyword == 'wait':
            self.keywords.wait(wait_time=data['time'])

        elif keyword == 'screenshot':
            self.keywords.screenshot(path=data['path'])

        elif keyword == 'exit_click':
            self.keywords.exist_click(method=data['method'], locator=data['locator'])
            report.result = self.keywords.result
            report.exception = self.keywords.exception

        elif keyword == 'exit_input':
            self.keywords.exist_input(method=data['method'], locator=data['locator'], value=data['value'])

        elif keyword == 'compare':
            self.keywords.compare(value=data['value'], target=data['target'])

        elif keyword == 'swipe':
            self.keywords.swipe(
                direction=data['direction'],
                times=data['times'],
                size=data['size'],
                duration=data['duration']
            )

        elif keyword == 'swipe_to':
            self.keywords.swipe_to(
                direction=data['direction'],
                method=data['method'],
                locator=data['locator'],
                max_times=data['max_times'],
                size=data['size']
            )

        elif keyword == 'clear_text':
            self.keywords.clear_text(method=data['method'], locator=data['locator'])

        elif keyword == 'long_press':
            self.keywords.long_press(method=data['method'], locator=data['locator'], press_time=data['press_time'])

        elif keyword == 'get_text':
            self.keywords.get_text(method=data['method'], locator=data['locator'])

        elif keyword == 'start-appium':
            self.keywords.start_appium(
                device=device_info['device'],
                appium_port=device_info['appium_port'],
                bootstrap_port=device_info['bootstrap_port']
            )
            time.sleep(10)
            report.result = self.keywords.result
            report.exception = self.keywords.exception
        elif keyword == 'start-driver':
            self.keywords.start_driver(
                device=device_info['device'],
                appium_port=device_info['appium_port'],
                app=device_info['app'],
                package=device_info['package'],
                activity=device_info['activity']
            )
            time.sleep(10)
            report.result = self.keywords.result
            report.exception = self.keywords.exception

        elif keyword == 'home_button':
            self.keywords.home_button()

        elif keyword == 'volume_up':
            self.keywords.volume_up()

        elif keyword == 'volume_down':
            self.keywords.volume_down()

        report.add_report(description, keyword, data, report.result, report.exception)

    def read_file(self):
        # 读取excel中的测试步骤
        file = os.path.join('D:\QA项目\performance\data', 'case.xlsx')
        self.case = pd.read_excel(file, sheet_name='Sheet1', index_col=0, skiprows=0, engine='openpyxl')
        # print(self.case)

    def execute_excel(self, device_info, title=None):
        """
        这里还需要优化，应该把执行动作，和读取excel动作分开
        :param device_info:
        :param title:
        :return:
        """
        self.create_report(title+'_'+device_info['device'])
        print(device_info)
        self.read_file()
        data = None
        for row in self.case.index.values:
            keyword = self.case.loc[row, 'keyword']
            # report.keyword = keyword
            description = self.case.loc[row, 'description']
            # report.parameter = self.case.loc[row, 'data']
            if isinstance(self.case.loc[row, 'data'], str):
                data = eval(self.case.loc[row, 'data'])
            self.execute(device_info, keyword, data, description)


if __name__ == '__main__':
    exe = Execute()
    # exe.read_file()
    a = {'device': '3EP7N19114003487', 'app': 'D:\\反诈项目\\云剑反诈\\应用备份\\云剑反诈apk\\1.0.0.1028\\antifraud-official.apk', 'package': 'com.trimps.antifraud', 'activity': 'com.qihoo360.callsafe.ui.index.AppEnterActivity', 'appium_port': 4723, 'bootstrap_port': 4724}
    exe.execute_excel(a)
