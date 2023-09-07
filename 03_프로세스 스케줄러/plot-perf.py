#!/usr/bin/python3

import sys
import plot_sched

def usage():
    print("""사용법: {} <최대 프로세스 개수>
    * cpuperf 프로그램 실행 결과를 저장한 'perf.data' 파일을 가지고 성능 정보를 그래프로 작성합니다.
    * 'avg-tat.jpg' 파일에 평균 턴어라운드 타임 그래프를 저장합니다.
    * 'throughput.jpg' 파일에 스루풋 그래프를 저장합니다.""".format(progname, file=sys.stderr))
    sys.exit(1)

progname = sys.argv[0]

if len(sys.argv) < 2:
    usage()

max_nproc = int(sys.argv[1])
plot_sched.plot_avg_tat(max_nproc)
plot_sched.plot_throughput(max_nproc)
