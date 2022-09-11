import numpy as np


class Crossover:
    def __init__(self, xl, xu, eta):
        self.xl = xl
        self.xu = xu
        self.eta = eta

    def crossover_sbx(self, x1, x2):
        """
        Crossover by using Simulated binary crossover
        Two children are generated from parents.
        """
        r = np.random.random()
        if r <= 0.5:
            beta = (2*r)**(1/(self.eta+1))
        else:
            beta = (1/(2-2*r))**(1/(self.eta+1))
        y1 = 0.5*((1+beta)*x1 + (1-beta)*x2)

        # child 2
        r = np.random.random()
        if r <= 0.5:
            beta = (2*r)**(1/(self.eta+1))
        else:
            beta = (1/(2-2*r))**(1/(self.eta+1))
        y2 = 0.5*((1-beta)*x1 + (1+beta)*x2)

        y1 = np.clip(y1, self.xl, self.xu)
        y2 = np.clip(y2, self.xl, self.xu)
        return y1, y2