# @name: randomizer.py
# @description: Script to generate random synthetic fair data
# @version: 1.0
# @date: 28-02-2021
# @author: Núria Queralt Rosinach
# @email: n.queralt_rosinach@lumc.nl

"""Script to generate synthetic fair data from experimental design 1 ( random numbers of PGE2 on defined conditions ) for twoc"""

import os
from scipy.stats import norm, skewnorm
import csv

# input
N = 5000
S_noticu = N - N*0.02
S_icu = N*0.02

# path to output dir
path = os.getcwd() + "/out"
if not os.path.isdir(path): os.makedirs(path)

# output
out_file = 'out/exp1_random_sdata.csv'
f = open(out_file, 'w')
fieldNames = ['Patient_number', 'S', 'M', 'P']
writer = csv.DictWriter(f, fieldnames=fieldNames)
writer.writeheader()

# algorithm
i = 1
while i <= N:
    # not severe patients (not ICU)
    if i <= S_noticu:
       S = 0
       # on Dexamethasone (prob=0.9)
       if i <= S_noticu*0.9:
          M = 1
       else:
          M = 0
       # PGE2 level: assign random value from normal distribution, [0.0, 1.0] mean=0.5
       P = abs(norm.rvs(loc=0.5, scale=1))
    # severe patients (ICU)
    else:   
       S = 1
       # not on Dexamethasone (prob=0.9)
       if i <= S_noticu + S_icu*0.9:
          M = 0
       else:
          M = 1
       # PGE2 level: assign random value from a negative skew normal distribution, [0.0, 1.0] mean=0.95
       P = abs(skewnorm.rvs(a=0.1, loc=0.95, scale=1))
    
    writer.writerow({'Patient_number': i, 'S': S, 'M': M, 'P': round(P,4)})
    i += 1

f.close()

