import numpy as np


class Mutation:
    def __init__(self, mutation_prob, xl, xu, eta):
        self.mutation_prob = mutation_prob
        self.xl = xl
        self.xu = xu
        self.eta = eta

    def _mutation(self, x):
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
        x = np.clip(x, self.xl, self.xu)
        return x
    
    def mutation(self, pop):
        for i in range(len(pop)):
            if np.random.random() < self.mutation_prob:
                self._mutation(pop[i])