# coding: utf-8

import os
import sys
import time
import traceback
import logging
import threading
import collections

'''
各个任务为顺序字典，按照添加的顺序执行任务
'''


# 参数为ITask类型对象
def WorkThread(task, param):
    try:
        task.work(param)
    except Exception, e:
        logging.error(u"执行任务：%s 时发生异常", task.getName())
        logging.error(u"\n" + traceback.format_exc())


class Flow:
    def __init__(self):
        self._prePareTasks = collections.OrderedDict()
        self._workTasks = collections.OrderedDict()
        self._cleanTasks = collections.OrderedDict()

    def prepare(self, param):
        logging.info(u"-------------------------------")
        logging.info(u"prepare Begin")
        logging.info(u"执行准备任务...")
        if self._prePareTasks:
            start_time = time.time()
            self.runTask(self._prePareTasks, param)
            end_time = time.time()
            logging.info(u"准备任务完成, 耗时: %.2f s", end_time - start_time)
        else:
            logging.info(u"当前工作没有准备任务.")
        logging.info(u"prepare OK")
        logging.info(u"-------------------------------\n")

    def work(self, param):
        logging.info(u"-------------------------------")
        logging.info(u"work Begin")
        logging.info(u"执行工作任务...")
        if self._workTasks:
            start_time = time.time()
            self.runTask(self._workTasks, param)
            end_time = time.time()
            logging.info(u"工作任务完成, 耗时: %.2f s", end_time - start_time)
        else:
            logging.info(u"当前工作没有工作任务.")
        logging.info(u"work OK")
        logging.info(u"-------------------------------\n")

    def release(self, param):
        logging.info(u"-------------------------------")
        logging.info(u"release Begin")
        logging.info(u"执行收尾任务...")
        if self._cleanTasks:
            start_time = time.time()
            self.runTask(self._cleanTasks, param)
            end_time = time.time()
            logging.info(u"收尾任务完成, 耗时: %.2f s", end_time - start_time)
        else:
            logging.info(u"当前工作没有收尾任务.")
        logging.info(u"release OK")
        logging.info(u"-------------------------------\n")

        # 释放
        logging.info(u"清除准备任务...")
        self.delTask(self._prePareTasks)
        logging.info(u"清除工作任务...")
        self.delTask(self._workTasks)
        logging.info(u"清除收尾任务...")
        self.delTask(self._cleanTasks)
        logging.info(u"所有工作执行完成!")

    def addPrePareTask(self, task, step_name):
        tasks = self._prePareTasks.get(step_name)
        if tasks is None:
            tasks = []
            self._prePareTasks[step_name] = tasks
        tasks.append(task)
        pass

    def addCleanTask(self, task, step_name):
        tasks = self._cleanTasks.get(step_name)
        if tasks is None:
            tasks = []
            self._cleanTasks[step_name] = tasks
        tasks.append(task)

    def addWorkTask(self, task, step_name):
        tasks = self._workTasks.get(step_name)
        if tasks is None:
            tasks = []
            self._workTasks[step_name] = tasks
        tasks.append(task)

    # 执行任务
    def runTask(self, taskDic, param):
        for step_name in taskDic:
            start_time = time.time()
            logging.info(u"步骤: %s 的任务执行开始", step_name)
            tasks = taskDic.get(step_name)

            # 这里创建线程调用，因为步骤一样，异步调用
            threads = []
            for task in tasks:
                t = threading.Thread(target=WorkThread, args=(task, param))
                threads.append(t)
                t.start()

            # 这里要等所有线程结束才能开始下一步骤的任务
            for t in threads:
                t.join()
                del t

            end_time = time.time()
            logging.info(u"步骤: %s 的任务执行完成, 耗时: %.2f s\n", step_name, end_time - start_time)

    def delTask(self, taskDic):
        for step_name in taskDic:
            tasks = taskDic.get(step_name)
            for task in tasks:
                task.release()
                del task
        taskDic = None