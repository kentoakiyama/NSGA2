import numpy as np


class BNH:
    def __init__(self):
        self.n_var = 2                             # number of variables
        self.n_obj = 2                             # number of objective functions
        self.n_constr = 2                          # number of constraint functions
        self.xl = np.array([0, 0])     # lower bound for variables
        self.xu = np.array([5, 3])  # upper bound for variables
    
    def evaluate(self, x, gen, id):
        x1, x2 = x
        # objective fucntions
        f1 = 4 * x1**2 + 4 * x2**2
        f2 = (x1 - 5)**2 + (x2 - 5)**2

        g1 = (x1 - 5)**2 + x2**2 - 25
        g2 = - (x1 - 8)**2 + (x2 + 3)**2 + 7.7
        return [f1, f2], [g1, g2]