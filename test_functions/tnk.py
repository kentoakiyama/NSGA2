import numpy as np


class TNK:
    def __init__(self):
        self.n_var = 2                             # number of variables
        self.n_obj = 2                             # number of objective functions
        self.n_constr = 2                          # number of constraint functions
        self.xl = np.array([0, 0])     # lower bound for variables
        self.xu = np.array([np.pi, np.pi])  # upper bound for variables
    
    def evaluate(self, x, gen, id):
        x1, x2 = x
        # objective fucntions
        f1 = x1
        f2 = x2

        g1 = - (x1**2 + x2**2 -1 - 0.1*np.cos(16*np.arctan(x1/(x2+1e-8))))
        g2 = (x1**2 - 0.5)**2 + (x2 - 0.5)**2 - 0.5
        return [f1, f2], [g1, g2]