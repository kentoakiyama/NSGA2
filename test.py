import numpy as np
import matplotlib.pyplot as plt

from nsga2.nsga2 import NSGA2
from test_functions.osyczkakundu import OsyczkaKundu
from test_functions.zdt import ZDT2, ZDT4


n_gen = 10
pop_size = 8
crossover_eta = 15
mutation_prob = 0.
mutation_eta = 20

nsga2 = NSGA2(ZDT4, pop_size, n_gen, mutation_prob=mutation_prob, mutation_eta=mutation_eta, crossover_eta=crossover_eta)
result = nsga2.minimize()
# import pdb;pdb.set_trace()
# x = np.array(result.x)
# f = np.array(result.f)
# r = np.array(result.r)
# 
# fig, ax = plt.subplots()
# ax.scatter(f[:, 0], f[:, 1], alpha=0.5)
# plt.show()

