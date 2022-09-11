import numpy as np


class OsyczkaKundu:
    # Osyczka and Kundu function
    # https://en.wikipedia.org/wiki/Test_functions_for_optimization
    def __init__(self):
        self.n_var = 6                             # number of variables
        self.n_obj = 2                             # number of objective functions
        self.n_constr = 5                          # number of constraint functions
        self.xl = np.array([0, 0, 1, 0, 1, 0])     # lower bound for variables
        self.xu = np.array([10, 10, 5, 6, 5, 10])  # upper bound for variables
    
    def evaluate(self, x, gen, id):
        x1, x2, x3, x4, x5, x6 = x
        # objective fucntions
        f_1 = -25*(x1-2)**2 - (x2-2)**2 - (x3-1)**2 - (x4-4)**2 - (x5-1)**2
        f_2 = x1**2 + x2**2 + x3**2 + x4**2 + x5**2 + x6**2
        # constraint functions
        g_1 = - (x1 + x2 - 2)
        g_2 = - (6 - x1 - x2)
        g_3 = - (2 - x2 + x1)
        g_4 = - (2 - x1 + 3*x2)
        g_5 = - (4 - (x3-3)**2 - x4)
        g_6 = - ((x5 - 3)**2 + x6 - 4)
        return [f_1, f_2], [g_1, g_2, g_3, g_4, g_5, g_6]