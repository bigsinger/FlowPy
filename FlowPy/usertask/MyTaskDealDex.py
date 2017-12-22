# coding: utf-8

import os
import sys
import time
import traceback
from Flow.ITask import ITask


class MyTaskDealDex(ITask):
    def getName(self):
        return "MyTaskDealDex"

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