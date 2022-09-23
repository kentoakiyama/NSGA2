import numpy as np
import matplotlib.pyplot as plt

from nsga2.nsga2 import NSGA2
from test_functions.get_problem import get_problem

problem = get_problem('TNK')

n_processes = 4
n_gen = 100
seed = 6
pop_size = 100
crossover_eta = 15
mutation_prob = 0.
mutation_eta = 20
restart = False

nsga2 = NSGA2(problem, pop_size, n_gen, mutation_prob=mutation_prob, mutation_eta=mutation_eta, crossover_eta=crossover_eta, n_processes=n_processes, seed=seed, restart=restart)
result = nsga2.minimize()


