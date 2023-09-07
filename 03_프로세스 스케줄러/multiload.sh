#!/bin/bash

MULTICPU=0
PROGNAME=$0
SCRIPT_DIR=$(cd $(dirname $0) && pwd)

usage() {
    exec >&2
    echo "사용법: $PROGNAME [-m] <프로세스 개수>
    일정 시간 동작하는 부하 처리 프로세스를 <프로세스 개수>로 지정한 만큼 동작시켜서 모두 끝날 때까지 기다립니다.
    각 프로세스 실행에 걸린 시간을 출력합니다.
    기본값은 모든 프로세스가 1개의 논리 CPU에서 동작합니다.

옵션 설명:
    -m: 각 프로세스를 여러 CPU에서 동작시킵니다."
    exit 1
}

while getopts "m" OPT ; do
    case $OPT in
        m)
            MULTICPU=1
            ;;
        \?)
            usage
            ;;
    esac
done

shift $((OPTIND - 1))

if [ $# -lt 1 ] ; then
    usage
fi

CONCURRENCY=$1

if [ $MULTICPU -eq 0 ] ; then
    # 부하 처리를 CPU0에서만 실행시킴
    taskset -p -c 0 $$ >/dev/null
fi

for ((i=0;i<CONCURRENCY;i++)) do
    time "${SCRIPT_DIR}/load.py" &
done

for ((i=0;i<CONCURRENCY;i++)) do
    wait
done
