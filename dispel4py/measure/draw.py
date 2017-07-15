#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
#   Author  :   renyuneyun
#   E-mail  :   renyuneyun@gmail.com
#   Date    :   17/07/10 10:12:36
#   License :   Apache 2.0 (See LICENSE)
#

'''

'''

import matplotlib.pyplot as plt
import numpy as np

from schema import engine, record
from sqlalchemy.sql import select

conn = engine.connect()

def all_platforms():
    s = select([record.c.platform]).distinct()
    results = conn.execute(s)
    for line in results:
        yield line[0]

def all_records_of_platform(platform):
    s = select([record]).where(record.c.platform==platform)
    results = conn.execute(s)
    for line in results:
        yield line[2:]

def all_confs_of_platform(platform):
    targets = [record.c.np_mpi_inc, record.c.max_num_sieve, record.c.max_prime]
    s = select(targets).distinct()
    results = conn.execute(s)
    for line in results:
        yield line

def all_time_of_conf(platform, conf):
    s = select([record.c.num_iter, record.c.mpi_time, record.c.mpi_inc_time]).where(record.c.platform==platform).where(record.c.np_mpi_inc==conf[0]).where(record.c.max_num_sieve==conf[1]).where(record.c.max_prime==conf[2]).order_by(record.c.num_iter)
    results = conn.execute(s)
    num_iters = []
    mpi_times = []
    mpi_inc_times = []
    for line in results:
        num_iter = line[0]
        mpi_time = line[1]
        mpi_inc_time = line[2]
        if num_iters and num_iter == num_iters[-1]:
            mpi_times[-1].append(mpi_time)
            mpi_inc_times[-1].append(mpi_inc_time)
        else:
            num_iters.append(num_iter)
            mpi_times.append([mpi_time])
            mpi_inc_times.append([mpi_inc_time])
    return num_iters, mpi_times, mpi_inc_times

avg = lambda lst: sum(lst) / len(lst)
flatten = lambda l: [item for sub in l for item in sub]
expand = lambda l1, l2: flatten([[item] * len(l2[i]) for i, item in enumerate(l1)])

plt.xlabel('number of iterations')
plt.ylabel('time')
capsize = 5

for platform in all_platforms():
    for conf in all_confs_of_platform(platform):
        num_iters, mpi_times, mpi_inc_times = all_time_of_conf(platform, conf)
        label_old = "old {} {}".format(platform, conf)
        p = plt.errorbar(num_iters, list(map(avg, mpi_times)), yerr=list(map(np.std, mpi_times)), capsize=capsize, linestyle='dashed', label=label_old)
        color = p[0].get_color()
        plt.plot(list(expand(num_iters, mpi_times)), list(flatten(mpi_times)), '.', color=color)
        label_mine = "mine {} {}".format(platform, conf)
        plt.errorbar(num_iters, list(map(avg, mpi_inc_times)), yerr=list(map(np.std, mpi_inc_times)), capsize=capsize, color=color, label=label_mine)
        plt.plot(list(expand(num_iters, mpi_inc_times)), list(flatten(mpi_inc_times)), 'x', color=color)

plt.legend()
plt.show()

