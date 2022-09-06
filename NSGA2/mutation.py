import numpy as np


class Mutation:
    def __init__(self, xl, xu, eta):
        self.xl = xl
        self.xu = xu
        self.eta = eta
        pass

    def mutation(self, x):
        """
        Mutation function
        """
        delta_1 = (x - self.xl) / (self.xu - self.xl)
        delta_2 = (self.xu - x) / (self.xu - self.xl)
        mut_pow = 1/(self.eta+1)
        r = np.random.random()

        if r <= 0.5:
            xy = 1 - delta_1
            val = 2*r + (1-2*r)*xy**(self.eta+1)
            deltaq = val**mut_pow - 1
        else:
            xy = 1 - delta_2
            val = 2*(1-r) + 2*(r-0.5)*xy**(self.eta+1)
            deltaq = 1 - val**mut_pow

        x = x + deltaq*(self.xu - self.xl)
        x = np.where(x < self.xl, self.xl, x)
        x = np.where(x > self.xu, self.xu, x)
        return x