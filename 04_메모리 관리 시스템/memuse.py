#!/usr/bin/python3

import subprocess

# 적당한 양의 데이터를 작성해서 메모리를 사용
# 메모리 용량이 작은 시스템이라면 메모리 부족으로 실패할 가능성이 있으므로
# size값을 줄여서 다시 실행
size = 10000000

print("메모리 사용 전의 전체 시스템 메모리 사용량을 표시합니다.")
subprocess.run("free")

array = [0]*size

print("메모리 사용 후의 전체 시스템 메모리 남은 용량을 표시합니다.")
subprocess.run("free")
