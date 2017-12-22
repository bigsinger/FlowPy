
# coding: utf-8

import os
import sys
import time
import inspect
import logging
import traceback


def get_current_function_name():
    return inspect.stack()[1][3]


class ITask:
    def __init__(self):
        self.onInit()
        pass

    def __del__(self):
        # logging.info(u"释放资源：" + self.getName())
        pass

    def getName(self):
        logging.error(self.getName() + u'派生类未实现函数' + get_current_function_name())
        assert None

    def onInit(self):
        logging.error(self.getName() + u'派生类未实现函数' + get_current_function_name())
        assert None

    def work(self, param):
        start_time = time.time()
        logging.info(u"开始执行: [%s]", self.getName())
        self.onBeforeWork(param)
        self.onWork(param)
        self.onAfterWork(param)
        end_time = time.time()
        logging.info(u"执行完成: [%s] 耗时: %.2f s", self.getName(), end_time -  start_time)

    def release(self):
        self.onRelease()

    def onBeforeWork(self, param):
        logging.error(self.getName() + u'派生类未实现函数' + get_current_function_name())
        assert None

    def onWork(self, param):
        logging.error(self.getName() + u'派生类未实现函数' + get_current_function_name())
        assert None

    def onAfterWork(self, param):
        logging.error(self.getName() + u'派生类未实现函数' + get_current_function_name())
        assert None

    def onRelease(self):
        logging.error(self.getName() + u'派生类未实现函数' + get_current_function_name())
        assert None

