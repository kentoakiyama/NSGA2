import numpy as np


class Crossover:
    def __init__(self, xl, xu, eta):
        self.xl = xl
        self.xu = xu
        self.eta = eta
    
    def _get_beta(self):
        r = np.random.random()
        if r <= 0.5:
            beta = (2*r)**(1/(self.eta+1))
        else:
            beta = (1/(2-2*r))**(1/(self.eta+1))
        return beta

    def crossover_sbx(self, x1, x2):
        """
        Crossover by using Simulated binary crossover
        Two children are generated from parents.
        """
        beta = self._get_beta()
        y1 = 0.5*((1+beta)*x1 + (1-beta)*x2)
        y1 = np.clip(y1, self.xl, self.xu)

        # child 2
        beta = self._get_beta()
        y2 = 0.5*((1-beta)*x1 + (1+beta)*x2)
        y2 = np.clip(y2, self.xl, self.xu)
        return y1, y2