# coding: utf-8

import os
import sys
import time
import traceback
from Flow.ITask import ITask


class MyTaskDealSo(ITask):
    def getName(self):
        return "MyTaskDealSo"

    def onInit(self):
        pass

    def onBeforeWork(self, param):
        pass

    def onWork(self, param):
        time.sleep(3)
        pass

    def onAfterWork(self, param):
        pass

    def onRelease(self):
        pass