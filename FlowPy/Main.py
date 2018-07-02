# coding: utf-8

import os
import sys
import logging
import argparse
import traceback
from WorkParam import WorkParam
from Flow.Flow import Flow
from Flow.MyArgumentParser import MyArgumentParser
from usertask.MyTask1 import MyTask1
from usertask.MyTaskUnzip import MyTaskUnzip
from usertask.MyTaskDecompile import MyTaskDecompile
from usertask.MyTaskDealDex import MyTaskDealDex
from usertask.MyTaskDealGame import MyTaskDealGame
from usertask.MyTaskDealSo import MyTaskDealSo
from usertask.MyTaskDealH5 import MyTaskDealH5
from usertask.MyTaskDeleteTemps import MyTaskDeleteTemps
import star

'''
使用时需要设置的几点：
1、初始化日志，按下面代码调一下initLog函数即可。
2、创建一个Flow对象，然后往里添加任务即可。最简单的形式可以只调用addWorkTask添加工作任务。
3、任务对象请继承自ITask，请不要实现__init__函数，如需初始化工作可以在onInit函数中进行。
4、参数，创建WorkParam对象，把所需的参数设置为成员，并在具体任务中直接使用。
'''


DEBUG = True

def initLog(logFile = u"log.txt", toFile = False):
    '''
    binPath = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "bin")
    pid = '%d' % (os.getpid())
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=u'%s%swrap_%s.log' % (binPath, os.sep, pid),
            filemode='a')
    #################################################################################################
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #################################################################################################
    '''
    if toFile is False:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)-6s %(filename)20s:%(lineno)-4d  %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            stream=sys.stdout,
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)-6s %(filename)20s:%(lineno)-4d  %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=logFile,
            filemode='a',
        )


def main(params):
    # args = None
    # parser = MyArgumentParser(description="自动打包发布工具参数说明")
    # parser.add_argument('key', help="Redis key where items are stored")
    # parser.add_argument('--file', required=True, help='设置xxx文件路径')
    # parser.add_argument('--ver', help='设置版本号')
    # parser.add_argument('--timeout', type=int, default=5)
    # parser.add_argument('--limit', type=int, default=0)
    # parser.add_argument('--progress_every', type=int, default=100)
    # parser.add_argument('-v', '--verbose', action='store_true')
    # try:
    #     # args = parser.parse_args()
    #     pass
    # except Exception, e:
    #     parser.print_help()
    #     return False
    # file = args.file

    # 初始化log
    initLog(None, not DEBUG)
    flow = Flow()

    # 添加准备任务：步骤1执行完后同时执行步骤2
    flow.addPrePareTask(MyTask1(), u'1')
    flow.addPrePareTask(MyTaskUnzip(), u'2')
    flow.addPrePareTask(MyTaskDecompile(), u'2')

    # 添加工作任务：全部异步
    flow.addWorkTask(MyTaskDealDex(), u'1')
    flow.addWorkTask(MyTaskDealGame(), u'2')
    flow.addWorkTask(MyTaskDealSo(), u'3')
    flow.addWorkTask(MyTaskDealH5(), u'3')

    # 添加收尾任务
    flow.addCleanTask(MyTaskDeleteTemps(), u'1')

    # 执行任务需要的参数
    param = WorkParam()
    param.pathMgr = 'pathmanager'
    # param.args = args

    # 执行准备任务
    flow.prepare(param)

    # 执行工作任务
    flow.work(param)

    # 执行收尾任务
    flow.release(param)

    return True


if __name__ == '__main__':
    ret = False
    try:
        if DEBUG:
            ret = main([__file__, '', ''])
        else:
            ret = main(sys.argv)
        if ret is False:
            print("failed")
    except:
        print(traceback.format_exc())
        os.system('pause')
    if not ret:
        sys.exit(-1)