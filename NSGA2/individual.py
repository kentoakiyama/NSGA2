import numpy as np


class Individual:
    def __init__(self, pop_size: int, n_var: int, xl, xu, sampling='lhs'):
        self.pop_size = pop_size
        self.n_var = n_var
        self.xl = xl
        self.xu = xu
        self.sampling = sampling
    
    def gen_pop(self):
        pop = np.random.random([self.pop_size, self.n_var])
        pop = pop * (self.xu - self.xl) + self.xl
        return pop


if __name__ == '__main__':
    pop_size = 10
    n_var = 2
    xl = np.array([0, 0.])
    xu = np.array([1., 2.])

    individual = Individual(pop_size, n_var, xl, xu)
    pop = individual.gen_pop()
    import pdb;pdb.set_trace()