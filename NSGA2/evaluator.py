from multiprocessing import Pool
from typing import List
import numpy as np

from time import time

class Evaluator:
    def __init__(self, functions, pop_size, n_obj, n_constr, n_processes=1):
        self.functions = functions
        self.n_obj = n_obj
        self.n_constr = n_constr
        self.pop_size = pop_size
        self.n_processes = n_processes

        self.history = []

    def _eval_ind(self, individual):
        f, g = self.functions(individual.x, individual.gen, individual.ids)
        self.history.append(individual)
        individual.set_result(f, g)

    def eval(self, pop):
        start = time()
        if self.n_processes == 1:
            for individual in pop:
                self._eval_ind(individual)
        elif self.n_processes >= 2:
            with Pool(self.n_processes) as pool:
                pool.starmap(self._eval_ind, pop)
        # print(time() - start)
        return pop