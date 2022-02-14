from eval_functions import Binh_functions, Chankong_functions, Osyczka_functions, TNK_functions
from NSGA2 import NSGA2
import numpy as np


class Problems:
    pass


class Params:
    pass


if __name__ == '__main__':
    params = Params()
    params.n_pop = 500              # populations
    params.n_gen = 50                # generations
    params.crossover_prob = 1.0
    params.crosober_sbx_eta = 10
    params.mutation_prob = 0.1
    params.mutation_eta = 10
    params.n_parallels = 1
    params.seed = None
    # params.plot = True

    prob = Problems()
    prob.n_vars = 6
    prob.n_obj = 2
    prob.n_constr = 6
    prob.range = {}
    prob.range[1] = [0, 10]
    prob.range[2] = [0, 10]
    prob.range[3] = [1, 5]
    prob.range[4] = [0, 6]
    prob.range[5] = [1, 5]
    prob.range[6] = [0, 10]

    nsga2 = NSGA2(Osyczka_functions, params, prob)
    res = nsga2.minimize()
