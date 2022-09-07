from abc import abstractmethod
import numpy as np


class Problem:
    def __init__(self, n_var: int, n_obj: int, n_constr: int, xl: np.ndarray, xu: np.ndarray):
        self.n_var = n_var
        self.n_obj = n_obj
        self.n_constr = n_constr
        self.xl = xl
        self.xu = xu
    
    @abstractmethod
    def _evaluate(self, x, gen, ids):
        pass