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
        # y1 = (x1+x2)/2 + beta * abs(x1 - x2/2)
        y1 = np.clip(y1, self.xl, self.xu)

        y2 = 0.5*((1-beta)*x1 + (1+beta)*x2)
        # y2 = (x1+x2)/2 - beta * abs(x1 - x2/2)
        y2 = np.clip(y2, self.xl, self.xu)
        return y1, y2


if __name__ == '__main__':
    x1 = np.array([0.2])
    x2 = np.array([0.8])

    crossover = Crossover(0, 1, 10)
    
    result = []
    for i in range(5000):
        y1, y2 = crossover.crossover_sbx(x1, x2)
        result.append(y1[0])
        result.append(y2[0])
    
    # import pdb;pdb.set_trace()

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.hist(result, bins=200)
    plt.show()