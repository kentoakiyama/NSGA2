from multiprocessing import Pool
import numpy as np


class Evaluator:
    def __init__(self, functions, pop_size, n_obj, n_constr, n_proesses=1):
        self.functions = functions
        self.n_obj = n_obj
        self.n_constr = n_constr
        self.pop_size = pop_size
        self.n_proesses = n_proesses

    def _eval_ind(self, individual):
        f, g = self.functions(individual.x, individual.gen, individual.ids)
        individual.set_result(f, g)


    def eval(self, pop):
        # f_results = np.zeros([self.pop_size, self.n_obj])
        # g_results = np.zeros([self.pop_size, self.n_constr])
        for individual in pop:
            self._eval_ind(individual)
        return pop