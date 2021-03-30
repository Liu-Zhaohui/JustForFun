#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建appium driver
"""

__author__ = '刘兆辉'

from appium import webdriver


class Driver:

    @staticmethod
    def android_driver(device, port, app, package, activity):

        capabilities = {
            'platformName': 'Android',
            'deviceName': device,
            'app': app,
            # 'platformVersion': '10',
            'appPackage': package,
            'appActivity': activity,
            'noReset': False,
            'udid': device
        }
        driver = webdriver.Remote('http://127.0.0.1:%s/wd/hub' % port, capabilities)
        return driver


if __name__ == '__main__':

    appium_driver = Driver()
    # a = appium_driver.android_driver(111, 4723)
