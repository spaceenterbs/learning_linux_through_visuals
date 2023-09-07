#!/usr/bin/python3

import numpy as np
from PIL import Image
import matplotlib
import os

matplotlib.use('Agg')

import matplotlib.pyplot as plt

plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False

def plot_sched(concurrency):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for i in range(concurrency):
        x, y = np.loadtxt("{}.data".format(i), unpack=True)
        ax.scatter(x,y,s=1)
    ax.set_title("타임 슬라이스 가시화(동시 실행={})".format(concurrency))
    ax.set_xlabel("경과 시간[밀리초]")
    ax.set_xlim(0)
    ax.set_ylabel("진척도[%]")
    ax.set_ylim([0,100])
    legend = []
    for i in range(concurrency):
        legend.append("부하 처리"+str(i))
    ax.legend(legend)

    # Ubuntu 20.04의 matplotlib 버그를 회피하기 위해 일단 png 파일로 저장한 후에 jpg로 변환
    # https://bugs.launchpad.net/ubuntu/+source/matplotlib/+bug/1897283?comments=all
    pngfilename = "sched-{}.png".format(concurrency)
    jpgfilename = "sched-{}.jpg".format(concurrency)
    fig.savefig(pngfilename)
    Image.open(pngfilename).convert("RGB").save(jpgfilename)
    os.remove(pngfilename)

def plot_avg_tat(max_nproc):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x, y, _ = np.loadtxt("cpuperf.data", unpack=True)
    ax.scatter(x,y,s=1)
    ax.set_xlim([0, max_nproc+1])
    ax.set_xlabel("프로세스 개수")
    ax.set_ylim(0)
    ax.set_ylabel("평균 턴어라운드 타임[초]")

    # Ubuntu 20.04의 matplotlib 버그를 회피하기 위해 일단 png 파일로 저장한 후에 jpg로 변환
    # https://bugs.launchpad.net/ubuntu/+source/matplotlib/+bug/1897283?comments=all
    pngfilename = "avg-tat.png"
    jpgfilename = "avg-tat.jpg"
    fig.savefig(pngfilename)
    Image.open(pngfilename).convert("RGB").save(jpgfilename)
    os.remove(pngfilename)

def plot_throughput(max_nproc):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x, _, y = np.loadtxt("cpuperf.data", unpack=True)
    ax.scatter(x,y,s=1)
    ax.set_xlim([0, max_nproc+1])
    ax.set_xlabel("프로세스 개수")
    ax.set_ylim(0)
    ax.set_ylabel("스루풋[프로세스/초]")

    # Ubuntu 20.04의 matplotlib 버그를 회피하기 위해 일단 png 파일로 저장한 후에 jpg로 변환
    # https://bugs.launchpad.net/ubuntu/+source/matplotlib/+bug/1897283?comments=all
    pngfilename = "throughput.png"
    jpgfilename = "throughput.jpg"
    fig.savefig(pngfilename)
    Image.open(pngfilename).convert("RGB").save(jpgfilename)
    os.remove(pngfilename)
