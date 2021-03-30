#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
操作配置文件
"""

__author__ = '刘兆辉'

import sys
import os
import configparser
from ruamel import yaml

base_path = os.getcwd()
sys.path.append(base_path)


class IniOperation:
    """
    用于操作ini文件
    """

    __cf =configparser.RawConfigParser()

    def __init__(self):
        self.value = None
        self.section = None

    def read_key(self, file, section, key):
        self.__cf.read(file, encoding='utf-8')
        self.value = self.__cf[section][key]

    def read_section(self, file, section):
        self.__cf.read(file, encoding='utf-8')
        self.section = self.__cf[section]


class YamlOperation:

    def __init__(self):
        self.content = None

    def read(self, path):
        with open(path, 'r', encoding='utf-8') as doc:
            self.content = yaml.load(doc, Loader=yaml.Loader)

    @staticmethod
    def write(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, Dumper=yaml.RoundTripDumper)


if __name__ == '__main__':
    y = YamlOperation()
    y.read('../config/device_info.yaml')
    print(y.content)
    y.write('../config/device_info.yaml', {'p': ['test', 'list'], 'bp': [4723, 4724]})
