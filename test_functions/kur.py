import numpy as np


class KUR:
    def __init__(self):
        self.n_var = 100                             # number of variables
        self.n_obj = 2                             # number of objective functions
        self.n_constr = 1                          # number of constraint functions
        self.xl = np.ones([self.n_var]) * (-5)     # lower bound for variables
        self.xu = np.ones([self.n_var]) * 5  # upper bound for variables
    
    def evaluate(self, x, gen, id):
        # objective fucntions

        f1 = -10 * np.sum(np.exp(-0.2 * np.sqrt(x[:-1]**2 + x[1:]**2)))
        f2 = np.sum(np.abs(x)**0.8 + 5 * (np.sin(x))**2)
        return [f1, f2], [-1]