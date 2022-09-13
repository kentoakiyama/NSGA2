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


if __name__ == '__main__':
    x = np.array([1.89119994e-02, -5.07731326e-01, 7.14824730e-03, -4.82485340e-01, -4.15367224e-03,
                  1.23603788e-02, -8.30132133e-03, -1.00023650e+00, 4.92809536e-01, -4.97535518e-01])

    zdt4 = ZDT4()
    print(zdt4.evaluate(x, 0, 0))