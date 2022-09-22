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
    
    def _sbx(self, x1_i, x2_i, xl, xu):
        beta1 = 1 + 2 * (x1_i - xl) / (x2_i - x1_i)
        beta2 = 1 + 2 * (xu - x2_i) / (x2_i - x1_i)

        alpha1 = 2 - beta1**(-(self.eta+1))
        alpha2 = 2 - beta2**(-(self.eta+1))

        r = np.random.random()
        if r <= 1/alpha1:
            betaq1 = (r*alpha1)**(1/(self.eta+1))
        else:
            betaq1 = (2-r*alpha1)**(-1/(self.eta+1))

        r = np.random.random()
        if r < 1/alpha2:
            betaq2 = (r*alpha2)**(1/(self.eta+1))
        else:
            betaq2 = (2-r*alpha2)**(-1/(self.eta+1))
        
        y1_i = 0.5 * (x1_i + x2_i - betaq1*(x2_i - x1_i))
        y2_i = 0.5 * (x1_i + x2_i + betaq2*(x2_i - x1_i))
        return y1_i, y2_i
    
    def crossover_sbx(self, x1, x2):
        y1 = []
        y2 = []
        for x1_i, x2_i, xl, xu in zip(x1, x2, self.xl, self.xu):
            y1_i, y2_i = self._sbx(x1_i, x2_i, xl, xu)
            y1.append(y1_i)
            y2.append(y2_i)
        
        y1 = np.array(y1)
        y2 = np.array(y2)

        y1 = np.clip(y1, self.xl, self.xu)
        y2 = np.clip(y2, self.xl, self.xu)
        return y1, y2


    def crossover_sbx_old(self, x1, x2):
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
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    x1 = np.array([0.2])
    x2 = np.array([0.8])

    crossover = Crossover(0, 1, 10)
    
    result = []
    for i in range(5000):
        y1, y2 = crossover.crossover_sbx(x1, x2)
        result.append(y1[0])
        result.append(y2[0])
    
    ax.hist(result, bins=200)

    fig, ax = plt.subplots()
    x1 = np.array([0.2])
    x2 = np.array([0.8])

    crossover = Crossover(0, 15, 10)
    
    result = []
    for i in range(5000):
        y1, y2 = crossover.crossover_sbx(x1, x2)
        result.append(y1[0])
        result.append(y2[0])
    
    ax.hist(result, bins=200)

    plt.show()