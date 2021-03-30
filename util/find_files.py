#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "liuzhaohui"

import os
import re


def clear_list(func):
    def wrapper(self, *args, **kwargs):
        self.file_list = []
        self.dir_list = []
        return func(self, *args, **kwargs)
    return wrapper


class FindFiles:
    def __init__(self):
        self.file_list = []
        self.dir_list = []

    def find_files(self, path, name_format, match_tail=True):
        if match_tail is True:
            # self.clear_list()
            name_format = name_format+'$'
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isdir(file):
                if re.match(name_format, file, False):
                    self.dir_list.append(file_path)
                self.find_files(file_path, name_format)
            elif (os.path.isfile(file)) and (re.match(name_format, file)):
                self.file_list.append(file_path)

    @clear_list
    def get_file_list(self, path, name_format, match_tail=True):
        self.find_files(path=path, name_format=name_format, match_tail=match_tail)

    def find_test_file(self, path):
        self.get_file_list(path, 'test.*\.py', match_tail=True)


if __name__ == '__main__':
    # path = 'D:\QA项目\performance\util'
    t_path = os.getcwd()
    target_path = t_path
    f_name = 'test'
    dir_name = '.*st'
    a = FindFiles()
    a.get_file_list(target_path, f_name, False)
    print(a.file_list)
    a.get_file_list(target_path, dir_name)
    print(a.dir_list)
    a.find_test_file(target_path)
    print(a.file_list)
