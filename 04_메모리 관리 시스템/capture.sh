#!/bin/bash

<<COMMENT
demand-paging.py 프로세스에 대해 1초 간격으로 메모리 관련 정보를 출력합니다.
각 줄 처음에는 정보를 수집한 시각을 표시합니다. 이후 필드의 의미는 다음과 같습니다.
   1번 필드: 확보한 메모리 영역 크기
   2번 필드: 확보한 물리 메모리 크기
   3번 필드: 메이저 폴트 횟수
   4번 필드: 마이너 폴트 횟수
COMMENT

PID=$(pgrep -f "demand-paging\.py")

if [ -z "${PID}" ]; then
    echo "demand-paging.py 프로세스가 존재하지 않습니다. $0 실행 전에 실행하기 바랍니다." >&2
    exit 1
fi

while true; do
    DATE=$(date | tr -d '\n')
    # -h는 헤더를 출력하지 않는 옵션
    INFO=$(ps -h -o vsz,rss,maj_flt,min_flt -p ${PID})
    if [ $? -ne 0 ]; then
        echo "$DATE: demand-paging.py 프로세스가 종료했습니다." >&2
        exit 1
    fi
    echo "${DATE}: ${INFO}"
    sleep 1
done
