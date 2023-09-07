#!/usr/bin/python3

import os, sys

ret = os.fork()
if ret == 0:
    print("자식 프로세스: pid={}, 부모 프로세스 pid={}".format(os.getpid(), os.getppid()))
    os.execve("/bin/echo", ["echo", "pid={}에서 안녕".format(os.getpid())], {})
    exit()
elif ret > 0:
    print("부모 프로세스: pid={}, 자식 프로세스 pid={}".format(os.getpid(), ret))
    exit()

sys.exit(1)
