#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查端口是否被占用
"""

__author__ = "刘兆辉"

from util.command import AdbCommand, AaptCommand
from util.config_operation import YamlOperation


class DeviceInfo:

    def __init__(self, app, default_port=4723):
        self.flag = True
        self.port = default_port
        self.port_list = []
        self.adb_command = AdbCommand()
        self.aapt_command = AaptCommand(app)
        self.yaml_operation = YamlOperation()

    def write_device_info(self):
        """
        将port_list写入yaml配置文件
        :return:
        """
        self.adb_command.get_devices()
        device_list = self.adb_command.device_list
        device_port_list = []
        self.aapt_command.get_package()
        self.aapt_command.get_activity()
        for i in device_list:
            device_dict = dict()
            device_dict['device'] = i
            device_dict['app'] = self.aapt_command.app
            device_dict['package'] = self.aapt_command.package
            device_dict['activity'] = self.aapt_command.activity
            device_dict['appium_port'] = self.get_port()
            self.port += 1
            device_dict['bootstrap_port'] = self.get_port()
            self.port += 1
            device_port_list.append(device_dict)
        self.yaml_operation.write('../config/device_info.yaml', device_port_list)

    def write_app_info(self, file):
        """
        在配置文件中追加app信息，用于启动driver
        :return:
        """
        pass

    def check_port_used(self, port_num):
        """
        检查端口被占用
        :param port_num:端口号
        :return: 是否被占用
        """
        # command = Command()
        cmd = 'netstat -ano | findstr ' + str(port_num)
        self.adb_command.execute_cmd_result(cmd)

        if len(self.adb_command.result) > 0:
            self.flag = True
        else:
            self.flag = False

    def create_port_list(self, start_port=4723):
        """
        创建端口列表
        :param start_port: 开始端口
        :return: 返回端口列表
        """
        self.adb_command.get_devices()
        device_list = self.adb_command.device_list
        port_list = []
        if device_list is not None:
            while len(port_list) < len(device_list):
                self.check_port_used(start_port)
                if self.flag is False:
                    port_list.append(start_port)
                    start_port += 1
                else:
                    print("当前接口被占用")
                    start_port += 1

        else:
            print("当前设备为空")

        self.port_list = port_list

    def get_port(self):
        # port = default_port
        while self.flag is True:
            self.check_port_used(self.port)
            if self.flag is False:
                self.flag = True
                return self.port
            else:
                self.port += 1

    def write_port_info(self):
        """
        在yaml配置文件中追加port信息，用于启动driver
        :return:
        """
        pass


if __name__ == '__main__':
    device_info = DeviceInfo(default_port=5037, app='D:\反诈项目\云剑反诈\应用备份\云剑反诈apk\\1.0.0.1028\\antifraud-official.apk')
    # port.create_list([1, 2, 3], start_port=5036)
    device_info.write_device_info()
    # print(port.port_list)
