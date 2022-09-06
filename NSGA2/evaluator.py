from multiprocessing import Pool
import numpy as np


class Evaluator:
    def __init__(self, functions, pop_size, n_obj, n_constr, n_proesses=1):
        self.functions = functions
        self.n_obj = n_obj
        self.n_constr = n_constr
        self.pop_size = pop_size
        self.n_proesses = n_proesses

    def _eval_ind(self, ind, gen, ids):
        f_res, g_res = self.functions(ind, gen, ids)
        return f_res, g_res


    def eval(self, gen: int, pop):
        f_results = np.zeros([self.pop_size, self.n_obj])
        g_results = np.zeros([self.pop_size, self.n_constr])
        for ids, ind in enumerate(pop):
            f_results[ids], g_results[ids] = self._eval(ind, gen, ids)
        
        # eval constraints
        cv_results = np.where(g_results <= 0, 0, 1)
        cv_results = np.sum(cv_results, axis=1)[..., np.newaxis]
    
        return f_results, g_results, cv_results