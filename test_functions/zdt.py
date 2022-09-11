import numpy as np


class ZDT2:
    def __init__(self):
        self.n_var = 2                             # number of variables
        self.n_obj = 2                             # number of objective functions
        self.n_constr = 0                          # number of constraint functions
        self.xl = np.array([0, 0])     # lower bound for variables
        self.xu = np.array([1, 1])  # upper bound for variables
    
    def evaluate(self, x, gen, id):
        x1, x2 = x
        # objective fucntions
        f1 = x1
        g = 1 + 9 * x2 / (self.n_var - 1)
        f2 = g * (1 - (f1 / g)**2)
        return [f1, f2], []
    

class ZDT4:
    def __init__(self):
        self.n_var = 10                             # number of variables
        self.n_obj = 2                             # number of objective functions
        self.n_constr = 0                          # number of constraint functions
        self.xl = np.array([0, -5, -5, -5, -5, -5, -5, -5, -5, -5])     # lower bound for variables
        self.xu = np.array([1, 5, 5, 5, 5, 5, 5, 5, 5, 5])  # upper bound for variables
    
    def evaluate(self, x, gen, id):
        # objective fucntions
        f1 = x[0]
        g = 91 + np.sum(x[1:]**2 - 10 * np.cos(4*np.pi*x[1:]))
        f2 = g * (1 - np.sqrt(f1 / g))
        return [f1, f2], []