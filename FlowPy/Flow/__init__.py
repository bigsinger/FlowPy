# coding: utf-8

import os
import sys
import traceback

DEBUG = True


def main(params):
    return True


if __name__ == '__main__':
    ret = False
    try:
        if DEBUG:
            ret = main([__file__, '', ''])
        else:
            ret = main(sys.argv)
        if ret is False:
            print "failed"
    except:
        print traceback.format_exc()
        os.system('pause')
    if not ret:
        sys.exit(-1)