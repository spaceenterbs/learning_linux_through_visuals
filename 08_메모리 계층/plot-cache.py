#!/usr/bin/python3

import numpy as np
from PIL import Image
import matplotlib
import os

matplotlib.use('Agg')

import matplotlib.pyplot as plt

plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False

def plot_cache():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x, y = np.loadtxt("out.txt", unpack=True)
    ax.scatter(x,y,s=1)
    ax.set_title("캐시 메모리 효과의 시각화")
    ax.set_xlabel("버퍼 크기[2^x KiB]")
    ax.set_ylabel("접근 속도[접근횟수/나노초]")

    # Ubuntu 20.04의 matplotlib 버그를 회피하기 위해 일단 png 파일로 저장한 후에 jpg로 변환
    # https://bugs.launchpad.net/ubuntu/+source/matplotlib/+bug/1897283?comments=all
    pngfilename = "cache.png"
    jpgfilename = "cache.jpg"
    fig.savefig(pngfilename)
    Image.open(pngfilename).convert("RGB").save(jpgfilename)
    os.remove(pngfilename)

plot_cache()
