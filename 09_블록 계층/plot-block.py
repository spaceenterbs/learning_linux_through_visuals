#!/usr/bin/python3

import numpy as np
from PIL import Image
import matplotlib
import os

matplotlib.use('Agg')

import matplotlib.pyplot as plt

SCHEDULERS = ["mq-deadline", "none"]
plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False

def do_plot(fig, pattern):
    # Ubuntu 20.04의 matplotlib 버그를 회피하기 위해 일단 png 파일로 저장한 후에 jpg로 변환
    # https://bugs.launchpad.net/ubuntu/+source/matplotlib/+bug/1897283?comments=all
    pngfn = pattern + ".png"
    jpgfn = pattern + ".jpg"
    fig.savefig(pngfn)
    Image.open(pngfn).convert("RGB").save(jpgfn)
    os.remove(pngfn)

def plot_iops(type):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for sched in SCHEDULERS:
        x, y, _ = np.loadtxt("{}/randwrite-{}.txt".format(type, sched), unpack=True)
        ax.scatter(x,y,s=3)
    ax.set_title("입출력 스케줄러 유효, 무효시 IOPS")
    ax.set_xlabel("병렬도")
    ax.set_ylabel("IOPS")
    ax.set_ylim(0)
    ax.legend(SCHEDULERS)
    do_plot(fig, type + "-iops")

def plot_iops_compare(type):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x1, y1, _ = np.loadtxt("{}/randwrite-{}.txt".format(type, "mq-deadline"), unpack=True)
    _, y2, _ = np.loadtxt("{}/randwrite-{}.txt".format(type, "none"), unpack=True)
    y3 = (y1 / y2 - 1) * 100
    ax.scatter(x1,y3, s=3)
    ax.set_title("입출력 스케줄러 유효화에 따른 IOPS 변화율[%]")
    ax.set_xlabel("병렬도")
    ax.set_ylabel("IOPS 변화율[%]")
    ax.set_yticks([-20, 0, 20])

    do_plot(fig, type + "-iops-compare")

def plot_latency(type):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for sched in SCHEDULERS:
        x, _, y = np.loadtxt("{}/randwrite-{}.txt".format(type, sched), unpack=True)
        for i in range(len(y)):
            y[i] /= 1000000
        ax.scatter(x,y,s=3)
    ax.set_title("입출력 스케줄러 유효, 무효시 레이턴시")
    ax.set_xlabel("병렬도")
    ax.set_ylabel("레이턴시[밀리초]")
    ax.set_ylim(0)
    ax.legend(SCHEDULERS)

    do_plot(fig, type + "-latency")

def plot_latency_compare(type):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x1, _, y1 = np.loadtxt("{}/randwrite-{}.txt".format(type, "mq-deadline"), unpack=True)
    _, _, y2 = np.loadtxt("{}/randwrite-{}.txt".format(type, "none"), unpack=True)
    y3 = (y1 / y2 - 1) * 100
    ax.scatter(x1,y3, s=3)
    ax.set_title("입출력 스케줄러 유효화에 따른 레이턴시 변화율[%]")
    ax.set_xlabel("병렬도")
    ax.set_ylabel("레이턴시 변화율[%]")
    ax.set_yticks([-20,0,20])

    do_plot(fig, type + "-latency-compare")

for type in ["HDD", "SSD"]:
    plot_iops(type)
    plot_iops_compare(type)
    plot_latency_compare(type)
    plot_latency(type)
