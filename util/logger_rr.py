#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import threading
from logging.handlers import RotatingFileHandler
from conf.logger_config import *
from util.sqldbtool import *
import json,requests,hashlib,base64
import datetime,time
import os


LOG_FORMAT = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"


class Logger:
    _logger = None

    @staticmethod
    def get_logger():
        if not Logger._logger:
            Logger._logger = logging.getLogger("airtest")
            Logger._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(LOG_FORMAT)

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)

            Logger._logger.addHandler(ch)
        return Logger._logger


class Log:
    def __init__(self, path, file_prefix, log_level):
        rotate_handler = RotatingFileHandler((path + file_prefix + '-detail.log'), maxBytes=10 * 1024 * 1024,
                                             backupCount=10)
        formatter = logging.Formatter(
            '[%(asctime)s][%(filename)s][%(funcName)s:%(lineno)d][%(levelname)s][%(message)s]')
        rotate_handler.setFormatter(formatter)
        self.logger = logging.getLogger("ui-autotest")
        self.logger.addHandler(rotate_handler)
        self.logger.setLevel(self._get_log_level(log_level))

    def _get_log_level(self, log_level):
        levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        return levels.get(log_level, logging.WARNING)

    @property
    def debug(self):
        return self.logger.debug

    @property
    def info(self):
        return self.logger.info

    @property
    def warn(self):
        return self.logger.warning

    @property
    def error(self):
        return self.logger.error

    @property
    def critical(self):
        return self.logger.critical


print (os.path.basename(__file__).split(".")[0])

class 日志 ():
    db = MySQLTool(TM_DB_IP, 3306, TM_DB_USER, TM_DB_PASSWD, TM_DB_NAME)
    def __init__(self):
        pass

    @classmethod
    def 开始(self):
        try:
            # 查询数据库最大id 并加1 最为此次之行用例的id
            sql = 'select max(id)+1 from tm_success_ratio'
            logInfo["id"] = 220996
            logInfo["id"] = int(self.db.query(sql)[0][0])
            print(logInfo["id"])

            # 插入本次测试数据 以备后续更新
            logInfo["starttime"] = int(time.time())
            logInfo["datetime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = '''INSERT INTO tm_success_ratio (id,order_id,product_id,tester,env,datetime,order_type,result) VALUES (%d,'%s',%s,'%s','%s','%s','%s','%s')''' % (
                logInfo["id"],logInfo["order_id"], logInfo["product_id"], logInfo["tester"], logInfo["env"], logInfo["datetime"],
                logInfo["order_type"], '开始');
            self.db.insert(sql)
        except BaseException as result:
            print("插入数据库失败")
            print(result)

    @classmethod
    def 记录明细(self,method):
        try:
            exec(method)
        except Exception as result:
            print("%s失败"%logInfo["test_name"])
            logInfo["test_status"] = 'FAIL'
            logInfo["test_message"] = result
            logInfo["result"] = 'FAIL'
            logInfo["endtime"] = int(time.time())
            logInfo["duration"] = (logInfo["endtime"] - logInfo["starttime"])
            logInfo["datetime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql = '''UPDATE tm_success_ratio SET result ='%s' ,duration = %d,datetime='%s' WHERE id = %d ''' % (
                 logInfo["result"], logInfo["duration"], logInfo["datetime"], logInfo["id"])
            self.db.update(sql)

            content = "用例：%s \n 结果：%s\n 执行人：%s\n 执行时间：" \
                      "%s\n 执行时长：%d秒\n" % ( logInfo["test_name"],logInfo["result"],
                                           logInfo["tester"], logInfo["datetime"], logInfo["duration"])
            日志.通知到钉钉群(access_token, conId, content, tele)

        else:
            logInfo["test_status"] = 'PASS'
            logInfo["test_message"] = ''
        finally:
            try:
                sql = '''INSERT INTO tm_success_ratio_log(id,test_name,test_status,test_message) VALUES (%d,'%s','%s','%s')''' \
                      % (logInfo["id"], logInfo["test_name"], logInfo["test_status"], logInfo["test_message"])
                self.db.insert(sql)
            except BaseException as result:
                print("插入日志明细失败")
                print(result)

    @classmethod
    def 结束(self):
        try:
            logInfo["endtime"] = int(time.time())
            logInfo["duration"] = (logInfo["endtime"] - logInfo["starttime"])
            logInfo["datetime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql = '''UPDATE tm_success_ratio SET result ='%s' ,duration = %d,datetime='%s' WHERE id = %d ''' % (
                 logInfo["result"], logInfo["duration"], logInfo["datetime"], logInfo["id"])
            self.db.update(sql)
        except BaseException as result:
            print("插入最终结果失败")
            print(result)
        else:
            print('插入最终结果 成功')
        finally:
            content = "用例：%s \n结果：%s\n执行人：%s\n执行时间：" \
                      "%s\n执行时长：%d秒\n" % (logInfo["test_name"], logInfo["result"],
                                           logInfo["tester"], logInfo["datetime"], logInfo["duration"])
            日志.通知到钉钉群(access_token,conId,content,tele)

    @classmethod
    def 通知到钉钉群(self,access_token, conId, content, tele):
        '''
        钉钉通知
        :param access_token:
        :param conId: 0：艾特所有人 1：艾特个人 2或其他：普通通知
        :param content: 通知内容
        :param tele: conId==1时使用，tele： [13800000000,13800000001]
        :return:
        '''
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + access_token
        judgeList = ['true', 'false']
        if conId == 0 or conId == 1:
            # 0艾特所有人,1艾特个人
            con = {"msgtype": "text", "text": {"content": content},
                   "at": {"isAtAll": judgeList[conId], "atMobiles": tele}}
        else:
            # 普通通知
            con = {"msgtype": "markdown", "markdown": {"title": "通知", "text": content}, }
        data = json.dumps(con)
        headers = {'content-type': 'application/json'}
        r2 = requests.post(url, data=data, headers=headers)
        print(r2.text)

if __name__ == "__main__":
    Logger.get_logger().debug("thread id %d: finish running case..." % threading.get_ident())
