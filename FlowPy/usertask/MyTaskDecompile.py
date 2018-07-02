# coding: utf-8

import os
import sys
import time
import traceback
from Flow.ITask import ITask


class MyTaskDecompile(ITask):
    def getName(self):
        return "MyTaskDecompile"

    def onInit(self):
        pass

    def onBeforeWork(self, param):
        pass

    def onWork(self, param):
        print(param.pathMgr)
        time.sleep(2)
        pass

    def onAfterWork(self, param):
        pass

    def onRelease(self):
        pass