#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
启动appium
"""

__author__ = "刘兆辉"

import os
import sys

base_path = os.getcwd()
sys.path.append(base_path)

from util.command import Command
# from util.port import Port
from util.config_operation import YamlOperation
import threading


class Server:

    def __init__(self):
        self.command = Command()
        self.appium_command = None
        # self.adb = Adb()
        # self.adb.handle_devices()
        # port = Port()
        # port_dic = {}
        # port.create_list(device_list=self.adb.device_list, start_port=4723)
        # port_dic['appium_list'] = port.port_list
        # port.create_list(device_list=self.adb.device_list, start_port=4900)
        # port_dic['bootstrap_list'] = port.port_list
        # print(port_dic)
        self.yaml_operation = YamlOperation()
        self.yaml_operation.read('../config/device_info.yaml')

    def create_command(self, device, appium_port, bootstrap_port):
        # self.yaml_operation.read('../config/device_info.yaml')
        # for i in self.yaml_operation.content:
        #     cmd = 'appium -p %(appium)s -bp %(bootstrap)s -U %(device)s --no-reset --session-over' \
        #           % {'appium': i['appium_port'],
        #              'bootstrap': i['bootstrap_port'],
        #              'device': i['device']
        #              }
        #     self.command_list.append(cmd)

        self.appium_command = 'appium -p %(appium)s -bp %(bootstrap)s -U %(device)s --no-reset --session-over' \
              % {'device': device,
                 'appium': appium_port,
                 'bootstrap': bootstrap_port
                 }
        # self.command_list.append(cmd)

    def start_appium(self, device, appium_port, bootstrap_port):
        # self.create_command()
        # for i in self.command_list:
        #     self.command.execute_cmd(i)
        self.kill_server()
        self.create_command(device, appium_port, bootstrap_port)
        self.command.execute_cmd(self.appium_command)

    # def start_server(self):
    #     self.kill_server()
    #     self.create_command()
    #     for i in self.command_list:
    #         appium_start = threading.Thread(target=self.start_appium, args=(i,))
    #         appium_start.start()

    def kill_server(self):
        self.command.execute_cmd_result('tasklist | findstr node')
        server_list = self.command.result
        if server_list is not None:
            self.command.execute_cmd('taskkill -F -PID node.exe')


if __name__ == '__main__':
    server = Server()
    server.create_command('2344', 4700, 4701)
    server.start_appium()
    # print(server.command_list)
