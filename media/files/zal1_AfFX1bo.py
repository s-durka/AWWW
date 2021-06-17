#!/usr/bin/env python
# coding: utf-8

# **Problem 2c (Squaring the histogram).** In this problem, we again want to sample with known probabilities $p_1,\ldots,p_n$, but this time we make no assumptions on $p_i$. Consider the following algorithm:
#    * Let $V$ be the mean of $p_i$, i.e. $V=\frac{1}{n}$.
#    * Create $n$ buckets, each with volume $V$, put each $p_i$ into a separate bucket.
#    * Until there exists a bucket $A$ that is not full, find a bucket $B$ that overflows, and trasfer probability from $B$ to $A$ until $A$ is exactly full
# 
# Show that:
#    * This algorithm always ends:
#        - the sum of all probabilities is equal to 1, so if there is a bucket $i$ with $p_i < V$, there will be a bucket $j$ with $p_j > V$. 
#        
#    * When it ends, each bucket contains pieces of at most two $p_i$'s.
#        - a bucket will only be 'filled' when its probability is less than V. Once a bucket's probability is less than V, it will be filled to V, taking probability from a bucket with probability > V, and will no longer be modified. 
# 
# How to use the result of this algorithm to sample with probabilities $p_i$. Argue that your algorithm is correct and implement it. The sampling part should be *vectorized*. Use this algorithm to sample birthdates again, and test its efficiency.

# In[54]:


import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fractions import Fraction

get_ipython().run_line_magic('matplotlib', 'inline')

stats = np.loadtxt('../lab1/us_births_69_88.csv', skiprows=1, delimiter=',', dtype=int)

def create_probabilities_list(counts):
    max_count = np.max(counts)
    pref_sums = np.cumsum(counts)
    probabilities = counts/pref_sums[-1]
    return probabilities

def create_buckets(probs):
    # zmieniamy probs tak, żeby na końcu były w nich odpowiednie
    n = probs.size
    V = round(1/n,8)
    buckets = probs.copy()
    aliases = np.zeros(n, dtype=np.int64) #na razie aliases = tablica zer
    while(True):
        i = 0
        while (i < n and buckets[i] >= round(1/n,8)):
            i = i + 1
        if (i == n):
            return aliases
        else:
            j = 0
            #print("ugabuga")
            while (j < n and buckets[j] <= 1/n):
                j = j + 1
            if (j == n):
                print(":(((")
            deficit = 1/n - buckets[i]
            buckets[j] = buckets[j] - deficit
            probs[j] = probs[j] - deficit
            buckets[i] = 1/n
            aliases[i] = j
      

def create_sample_arr(arr_size, aliases, probs):
    n = probs.size
    randoms = np.random.random(arr_size) #losujemy arr_size liczb z [0,1]
    days_rand = np.random.randint(1, n, arr_size) # losujemy arr_size dni z rozkładem jednostajnym
    #formula_bool = (randoms[days_rand-1] <= probs[days_rand-1]*n) #
    formula_bool = (randoms <= probs[days_rand-1]*n)
    #formula_bool = True
    days = np.where(formula_bool, days_rand, aliases[days_rand-1]+1) #jeśli warunek spełniony, to dzień, wpp alias
    return days      

def birthday_paradox(samples):
    ret = []
    count = 0
    s = set()
    for i in np.arange(samples.size):
        if samples[i] in s:
            ret.append(count)
            s.clear()
            count = 0
        else:
            s.add(samples[i])
            count = count + 1
    return ret

probs = create_probabilities_list(stats[:,2])
aliases = create_buckets(probs)
plt.plot()
samples = create_sample_arr(2400000, aliases, probs)
#plt.hist(samples,bins=stats.shape[0])
l = birthday_paradox(samples)
plt.hist(l, bins = np.arange(100))
plt.show()





