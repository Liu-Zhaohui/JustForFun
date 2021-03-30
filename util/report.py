#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "liuzhaohui"

import os
import sys
import time
import pandas as pd
base_path = os.getcwd()
sys.path.append(base_path)


class Report:
    def __init__(self):
        self.title = time.strftime("%Y%m%d%H:%M:%S", time.localtime())
        self.report_path = None
        self.keyword = None
        self.description = None
        self.parameter = None
        self.result = True
        self.exception = None

    def create_report(self, title=None):
        """
        生成report名称，包含时间、title
        创建report
        :return:
        """
        if title is not None:
            report_title = str(title) + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xlsx'
        else:
            report_title = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xlsx'
        self.report_path = os.path.join(base_path, '../reports', report_title)
        df = pd.DataFrame(columns=['step', 'keyword', 'param', 'result', 'detail'])
        df.to_excel(self.report_path, index=False)

    def add_report(self, step, keyword, data, result, detail):
        df = pd.read_excel(self.report_path, engine='openpyxl')
        df_rows = df.shape[0]
        print(df_rows)
        step_result = [step, keyword, data, result, detail]
        print(step_result)
        df.loc[df_rows] = step_result
        # ds = pd.DataFrame(step_result)
        # print(ds)
        # df = df.append(ds, ignore_index=True)
        df.to_excel(self.report_path, index=False, header=True)

    # def des(self, description):
    #     # 打印描述
    #     self.description = description
    #
    # def param(self, parameters):
    #     # 打印参数
    #     self.parameter = parameters
    #
    # def success(self):
    #     # 打印执行结果，成功或失败
    #     self.result = 'success'
    #
    # def failed(self):
    #     self.result = 'failed'
    #
    # def detail(self, data):
    #     self.exception = data


if __name__ == '__main__':
    rp = Report()
    rp.create_report('test_title')
    # time.sleep(3)
    rp.add_report('col1', 'col2', 'col3', 'col4')
    rp.add_report('nc1', 'good', 'ok', 'nb')
