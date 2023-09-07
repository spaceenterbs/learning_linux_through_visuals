#!/usr/bin/python3

import signal

# SIGINT 시그널을 무시하도록 설정.
# 첫 번째 인수는 핸들러를 설정할 시그널(여기서는 signal.SIGINT)
# 두 번째 인수에는 시그널 핸들러(여기서는 signal.SIG_IGN)를 지정
signal.signal(signal.SIGINT, signal.SIG_IGN)

while True:
    pass
