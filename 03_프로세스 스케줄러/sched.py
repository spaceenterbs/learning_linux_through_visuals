#!/usr/bin/python3

import sys
import time
import os
import plot_sched

def usage():
    print("""사용법: {} <프로세스 개수>
        * 논리 CPU0에서 <프로세스 개수>만큼 동시에 100밀리초 동안 CPU 자원을 소비하는 부하 처리 프로세스를 기동하고 모든 프로세스 종료를 기다립니다.
        * 'sched-<프로세스 개수>.jpg' 파일에 실행 결과를 표시한 그래프를 저장합니다.
        * 그래프 x축은 부하 처리 프로세스의 경과 시간[밀리초], y축은 진척도[%]""".format(progname, file=sys.stderr))
    sys.exit(1)

# 실험에 알맞는 부하 정도를 찾기 위한 전처리에 걸리는 부하
# 너무 시간이 걸리면 더 작은 값을 사용
# 너무 빨리 끝나면 더 큰 값을 사용
NLOOP_FOR_ESTIMATION=100000000
nloop_per_msec = None
progname = sys.argv[0]

def estimate_loops_per_msec():
    before = time.perf_counter()
    for _ in  range(NLOOP_FOR_ESTIMATION):
        pass
    after = time.perf_counter()
    return int(NLOOP_FOR_ESTIMATION/(after-before)/1000)

def child_fn(n):
    progress = 100*[None]
    for i in range(100):
        for j in range(nloop_per_msec):
            pass
        progress[i] = time.perf_counter()
    f = open("{}.data".format(n),"w")
    for i in range(100):
        f.write("{}\t{}\n".format((progress[i]-start)*1000,i))
    f.close()
    exit(0)

if len(sys.argv) < 2:
    usage()

concurrency = int(sys.argv[1])

if concurrency < 1:
    print("<동시 실행>은 1이상의 정수를 사용합니다: {}".format(concurrency))
    usage()

# 강제로 논리 CPU0에서 실행
os.sched_setaffinity(0, {0})

nloop_per_msec = estimate_loops_per_msec()

start = time.perf_counter()

for i in range(concurrency):
    pid = os.fork()
    if (pid < 0):
        exit(1)
    elif pid == 0:
        child_fn(i)

for i in range(concurrency):
    os.wait()

plot_sched.plot_sched(concurrency)
