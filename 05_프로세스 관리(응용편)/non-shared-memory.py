#!/usr/bin/python3

import os
import sys

data = 1000

print("자식 프로세스 생성전 데이터 값: {}".format(data))
pid = os.fork()
if pid < 0:
    print("fork()에 실패했습니다", file=os.stderr)
elif pid == 0:
    data *= 2
    sys.exit(0)

os.wait()
print("자식 프로세스 종료후 데이터 값: {}".format(data))
