#!/bin/bash

false &
wait $! # false 프로세스 종료를 기다린다. false 명령어의 PID는 `$!` 변수로 확인
echo "false 명령어가 종료되었습니다: $?" # wait후 false 프로세스 반환값은 `$?` 변수로 확인
