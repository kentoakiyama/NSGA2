import numpy as np


class Individual:
    def __init__(self, gen: int, ids: int, x: np.ndarray):
        self._gen = gen
        self._ids = ids
        self._x = x
    
        self._f = None
        self._c = None
        self._cd = 0

    def set_result(self, f, g):
        self._f = f
        self._g = g
    
    def set_rank(self, r):
        self._r = r
    
    def add_cd(self, cd):
        self._cd += cd
    
    @property
    def gen(self):
        return self._gen
    
    @property
    def ids(self):
        return self._ids
    
    @property
    def x(self):
        # input variable
        return self._x

    @property
    def f(self):
        # objective function
        return self._f

    @property
    def g(self):
        # constraint function
        return self._g
    
    @property
    def cv(self):
        # constraint violation
        self._cv = sum([1 if g < 0 else 0 for g in self._g])
        return self._cv

    @property
    def r(self):
        return self._r
    
    @property
    def feasible(self):
        if self._cv == 0:
            return True
        else:
            return False

    @property
    def cd(self):
        return self._cd

if __name__ == '__main__':
    pop_size = 10
    n_var = 2
    xl = np.array([0, 0.])
    xu = np.array([1., 2.])

    individual = Individual(pop_size, n_var, xl, xu)
    pop = individual.gen_pop()
    import pdb;pdb.set_trace()