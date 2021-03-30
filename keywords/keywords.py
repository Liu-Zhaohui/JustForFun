#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基础关键字
"""

__author__ = 'liuzhaohui'

import os
import sys
import time
import re
import logging
base_path = os.getcwd()
sys.path.append(base_path)
from driver.create_driver import Driver
from util.server import Server
from appium.webdriver.common.touch_action import TouchAction
from util.command import Command
# from util.report import Report
from util.logger import Log

log = Log()


# 使用函数做装饰器，存报告结果
def result(func):
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
            print('go go go')
            self.result = 'success'
            self.exception = None
        except Exception as ex:
            self.result = 'failed'
            self.exception = ex
            log.warning(ex)
    return wrapper


class KeyWords:

    def __init__(self):
        self.driver = None
        self.command = Command()
        self.flag = None
        # self.report = Report()
        self.result = None
        self.exception = None

    def _success(self):
        # 这些函数废弃，使用result装饰器
        self.result = 'success'
        self.exception = None

    def _failed(self, ex=None):
        # 这些函数废弃，使用result装饰器
        self.result = 'failed'
        self.exception = ex

    def _ignore_ex(self, ex):
        # 这些函数废弃，使用result装饰器
        self.result = 'success'
        self.exception = ex

    def start_appium(self, device, appium_port, bootstrap_port):
        server = Server()
        server.start_appium(device, appium_port, bootstrap_port)
        logging.debug("start_appium"+str(device)+str(appium_port)+str(bootstrap_port))
        self._success()

    def start_driver(self, device, appium_port, app, package, activity):
        driver = Driver()
        self.driver = driver.android_driver(device, appium_port, app, package, activity)
        logging.debug("start_driver"+str(device)+str(appium_port)+str(app+package)+str(activity))
        self._success()

    def find_element(self, method, locator):
        if method == 'id':
            self.driver.find_element_by_id(locator)
        elif method == 'xpath':
            self.driver.find_element_by_xpath(locator)
        elif method == 'class':
            self.driver.find_element_by_class_name(locator)

    # def start_appium(self):
    #     # self.server.start_appium()
    #     self.server.start_server()

    @result
    def click(self, method, locator):
        """
        点击
        :param method: 定位方式
        :param locator: 定位信息
        :return:
        """
        # self.exist(method, locator)
        # if self.result:

        # try:
        self.driver.find_element(method, locator).click()
        time.sleep(1)
        logging.debug("click"+str(method)+str(locator))
        #     self._success()
        # except Exception as ex:
        #     self._failed(ex)
        #     log.info(ex)

    def exist_click(self, method, locator):
        """
        点击
        :param method: 定位方式
        :param locator: 定位信息
        :return:
        """
        try:
            self.driver.find_element(method, locator).click()
            time.sleep(1)
            logging.debug("click"+str(method)+str(locator))
            self._success()
        except Exception as ex:
            self._ignore_ex(ex)

    def input(self, method, locator, value):
        """
        输入
        :param method:定位方式
        :param locator: 定位信息
        :param value: 输入的值
        :return:
        """

        try:
            real_value = self.get_var(value)
            self.driver.find_element(method, locator).send_keys(real_value)
            log.info("input"+str(method)+str(locator+value))
            self._success()
        except Exception as ex:
            self._failed(ex)

    def exist_input(self, method, locator, value):
        """
                输入
                :param method:定位方式
                :param locator: 定位信息
                :param value: 输入的值
                :return:
                """
        try:
            real_value = self.get_var(value)
            self.driver.find_element(method, locator).send_keys(real_value)
            self._success()
        except Exception as ex:
            self._ignore_ex(ex)

    def clear_text(self, method, locator):
        """
        清空文本框文本
        :param method:
        :param locator:
        :return:
        """
        try:
            self.driver.find_element(method, locator).clear()
        except Exception as ex:
            self._failed(ex)

    def long_press(self, method, locator, press_time=2000):
        """
        长按操作
        :param method:
        :param locator:
        :param press_time:
        :return:
        """
        try:
            ele = self.driver.find_element(method, locator)
            TouchAction(self.driver).long_press(ele).wait(press_time).release().perform()
            self._success()
        except Exception as ex:
            self._failed(ex)

    def wait(self, wait_time):
        """
        等待时间
        :param wait_time:等待时间，单位秒
        :return:
        """
        self.driver.implicitly_wait(wait_time)

    def get_text(self, method, locator, var):
        # 要解决如何把输入的当成变量来使用
        """
        获取控件文本
        还可以获取控件属性
        [精]把获取的变量，存到var中
        :param method:定位方式
        :param locator: 定位信息
        :param var:
        :return:
        """
        try:
            ele = self.driver.find_element(method, locator)
            # return ele.text
            globals()[var] = ele.text
        except Exception as ex:
            self._failed(ex)

    # @staticmethod
    def compare(self, value, target, expect=True):
        """
        比较两个值是否相等
        :param value:
        :param target:
        :return:
        """
        try:
            real_value = self.get_var(value)
            real_target = self.get_var(target)
            if real_value == real_target:
                self.flag = True

            else:
                self.flag = False

            if self.flag == expect:
                self._success()
            else:
                self._failed()
        except Exception as ex:
            self._failed(ex)

    def exist(self, method, locator, var, exist=True):
        """
        判断控件是否存在
        还需要对结果可设置
        :return:
        """
        try:
            ele = self.driver.find_element(method, locator)

            # 判断元素是否存在
            if ele.size is not None:
                result = True
            else:
                result = False

            # 判断与预期结果是否一致
            if result == exist:
                self.flag = True
                globals()[var] = True
            else:
                self.flag = False
                globals()[var] = False
        except Exception as ex:
            self.flag = False
            log.info(ex)

    def swipe(self, direction, times=1, size=1.0, duration=1000):
        """
        划动屏幕
        :return:
        """
        try:
            x = self.driver.get_window_size()['width']
            y = self.driver.get_window_size()['height']
            while times > 0:
                if direction == 'up':
                    self.driver.swipe(x * 0.5, y * 0.9 * float(size), x * 0.5, y * 0.1 * float(size), duration)
                elif direction == 'down':
                    self.driver.swipe(x * 0.5, y * 0.1 * float(size), x * 0.5, y * 0.9 * float(size), duration)
                elif direction == 'left':
                    self.driver.swipe(x * 0.9 * float(size), y * 0.5, x * 0.1 * float(size), y * 0.5, duration)
                elif direction == 'right':
                    self.driver.swipe(x * 0.1 * float(size), y * 0.5, x * 0.9 * float(size), y * 0.5, duration)
                times -= 1
            self._success()
        except Exception as ex:
            self._failed(ex)

    def swipe_to(self, direction, method, locator, max_times=10, size=0.5):
        """
        划动屏幕至某一控件
        :param size:
        :param direction:
        :param method:
        :param locator:
        :param max_times: 最大划动次数
        :return:
        """
        try:
            while (self.exist(method, locator) is False) and (max_times>0):
                self.swipe(direction=direction, size=size)
                max_times -= 1
            self._success()
        except Exception as ex:
            self._failed(ex)

    def screenshot(self, path):
        """
        截图
        :param path:截图存放路径
        :return:
        """
        try:
            self.driver.get_screenshot_as_file(path)
            self._success()
        except Exception as ex:
            self._failed(ex)

    def home_button(self):
        try:
            self.driver.keyevent(3)
        except Exception as ex:
            self._failed(ex)

    def volume_up(self):
        self.driver.keyevent(24)

    def volume_down(self):
        self.driver.keyevent(25)

    def set_network(self):
        """
        设置网络状态
        设置网络开关状态，暂时不添加
        :return:
        """
        pass

    def install_app(self, path):
        """
        安装应用
        不可用，有bug
        :return:
        """
        self.driver.install_app(path)

    def uninstall_app(self, package):
        """
        卸载应用
        未调试
        :return:
        """
        self.driver.remove_app(package)

    def reset_app(self, package):
        """
        重置应用（清空应用数据）
        不可用，有bug
        :return:
        """
        self.driver.reset(package)

    def adb_cmd(self, cmd):
        """
        执行adb命令
        :return:
        """
        self.command.execute_cmd(cmd)

    @staticmethod
    def get_var(value):
        """
        这个方法是用来取用户传入的值
        如果用户传入的是实际值，直接返回
        如果用户传入的是用户自己定义的变量，{{xxx}}格式，会判断下取出实际值
        强烈建议，对用户传入值的每一个地方，都是用此方法获取实际值
        :param value:
        :return:
        """
        if re.match('{{.*}}', value):
            var = value.strip('{}')
            real_value = globals()[var]
            return real_value
        else:
            return value


if __name__ == '__main__':
    key = KeyWords()
    # key.start_appium()
    key.start_appium(device='3EP7N19114003487', appium_port=4905, bootstrap_port=4906)
    key.start_driver(device='3EP7N19114003487',
                     appium_port=4905,
                     app='D:\\反诈项目\\云剑反诈\\应用备份\\云剑反诈apk\\1.0.0.1025\\antifraud-official.apk',
                     package='com.trimps.antifraud',
                     activity='com.qihoo360.callsafe.ui.index.AppEnterActivity'
                     )

    time.sleep(10)

    # 获取立即体验文本
    key.get_text(method='id', locator='com.qihoo360.callsafe.entry:id/q', var='lzh')
    print(globals()['lzh'])
    print('11111', '{{lzh}}')
    key.compare('{{lzh}}', '马上体验')
    print(key.result)

    # 判断立即体验控件存在
    # b = key.exist(method='id', locator='com.qihoo360.callsafe.entry:id/q')

    # 点击立即体验
    # key.click(method='id', locator='com.qihoo360.callsafe.entry:id/q')

    # 点击同意
    # key.click(method='id', locator='com.qihoo360.callsafe.entry:id/a2')

    # 输入手机号
    # key.input(method='id', locator='com.qihoo360.mobilesafe.blockmgr:id/er', value='18351922944')

    # key.wait(10)

    # 划动
    # key.swipe('up', times=3, size=0.5)

    # 物理键
    # key.home_button()
    # key.volume_up()
    # key.volume_down()

    # 截图
    # key.wait(10)
    # key.screenshot('.\\test.png')

    # c = key.compare(1, 3)
    # d = key.compare(1, 1)

    # 划动到
    # key.click(method='xpath', locator='//*[@text="马上体验"]')
    # key.click(method='xpath', locator='//*[@text="同意"]')
    # key.swipe_to('up', method='xpath', locator='//*[@text="新疆维吾尔自治区"]')
    # key.wait(1)

    # key.long_press(method='xpath', locator='//*[@text="马上体验"]')

    # key.input(method='id', locator='com.qihoo360.mobilesafe.blockmgr:id/er', value='123456')
    # key.clear_text(method='id', locator='com.qihoo360.mobilesafe.blockmgr:id/er')

    # key.install_app('C:\Users\liuzhaohui\Downloads\\360MobileSafe.apk')
    # key.reset_app('com.trimps.antifraud')

