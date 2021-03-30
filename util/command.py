#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '刘兆辉'

import os
import sys
import re
base_path = os.getcwd()
sys.path.append(base_path)
from util.logger import Log

log = Log()


class Command:

    def __init__(self):
        self.result = None
        # self.result_list = []

    @staticmethod
    def execute_cmd(command):
        """
        用于在cmd窗口执行命令
        不返回结果
        :param command:命令
        :return: 不返回
        """
        # 这个方式，执行cmd命令后，不会往下执行
        os.system('start '+command)
        log.debug(command)
        # print('command', command)
        # run(command, shell=True)

    def execute_cmd_result(self, command):
        """
        用于在cmd窗口执行dos命令
        并获取执行命令的结果
        :return:命令返回结果
        """
        # result_list = []
        result = os.popen(command).readlines()
        self.result = result

    # def handle_devices(self, result):
    #     """
    #     处理adb devices命令的结果
    #     :param result: cmd窗口返回结果
    #     :return: 结果列表
    #     """
    #     for i in result:
    #         if i == '\n':
    #             continue
    #         self.result_list.append(i.strip('\n'))


class AdbCommand(Command):
    """
    执行adb命令的类
    """

    def __init__(self):
        Command.__init__(self)
        self.device_list = []

    def get_devices(self):
        """
        处理adb devices命令的结果
        :param result: cmd窗口返回结果
        :return: 结果列表
        """
        result_list = []
        self.execute_cmd_result('adb devices')
        for i in self.result:
            if i == '\n':
                continue
            result_list.append(i.strip('\n'))

        self.filter_device(result_list)

    def filter_device(self, result):
        if len(self.result) >= 2:
            for i in result:
                if 'List of devices attached' in i:
                    continue
                device = i.split()
                if device[1] == 'device':
                    self.device_list.append(device[0])
                elif device[1] == 'unauthorized':
                    print('有设备需要授权，请检查手机')


class AaptCommand(Command):
    """
    执行aapt命令的类
    """

    def __init__(self, app):
        Command.__init__(self)
        self.app = app
        self.package = None
        self.activity = None

    def get_package(self):
        try:
            self.execute_cmd_result('aapt d badging %s | findstr package' % self.app)
            self.package = re.search(r"name='\S*'", self.result[0]).group().split("'")[1]
        except Exception as e:
            print(e)
            self.package = None

    def get_activity(self):
        try:
            self.execute_cmd_result('aapt d badging %s | findstr activity' % self.app)
            self.activity = re.search(r"name='\S*'", self.result[0]).group().split("'")[1]
        except Exception as e:
            print(e)
            self.activity = None


if __name__ == '__main__':
    cmd = AdbCommand()
    cmd.get_devices()
    print(cmd.result)
    print(cmd.device_list)
    ######################
    # cmd = AaptCommand('D:\反诈项目\云剑反诈\应用备份\云剑反诈apk\\1.0.0.1028\\antifraud-official.apk')
    # cmd.get_package()
    # cmd.get_activity()
    # print(cmd.package, cmd.activity)
