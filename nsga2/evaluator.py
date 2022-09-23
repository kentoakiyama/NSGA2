from typing import List
import numpy as np
import joblib
from time import time

class Evaluator:
    def __init__(self, problem, pop_size, filename, n_processes=1):
        self.problem = problem
        self.pop_size = pop_size
        self.filename = filename
        self.n_processes = n_processes

        self.history = []

    def _eval_ind(self, individual):
        f, g = self.problem.evaluate(individual.x, individual.gen, individual.ids)
        self.history.append(individual)
        individual.set_result(f, g)
        with open(self.filename, 'a') as f:
            string = f'{individual.gen},{individual.ids},{list(individual.x)},{list(individual.f)},{list(individual.g)},{individual.cv},{individual.feasible}\n'
            string = string.replace('[', '').replace(']', '').replace(' ', '')
            f.write(string)
        return individual

    def eval(self, pop: List) -> List:
        if self.n_processes == 1:
            for individual in pop:
                _ = self._eval_ind(individual)
        elif self.n_processes >= 2:
            pop = joblib.Parallel(n_jobs=self.n_processes)(
                joblib.delayed(self._eval_ind)(ind) for ind in pop
            )
        return pop