import numpy as np


class Individual:
    def __init__(self, gen: int, ids: int, x: np.ndarray):
        self._gen = gen
        self._ids = ids
        self._x = x
    
        self._f = None
        self._g = None
        self._cv = None
        self._r = None
        self._cd = 0

    def set_result(self, f, g):
        self._f = f
        self._g = g
    
    def set_rank(self, r):
        self._r = r
    
    def add_cd(self, cd):
        self._cd += cd

    def clear_cd(self):
        self._cd = 0
    
    def dominate(self, other_individual):
        flag1 = True
        flag2 = False
        for ind1_fi, ind2_fi in zip(self._f, other_individual.f):
            flag1 = flag1 and (ind1_fi <= ind2_fi)
            flag2 = flag2 or (ind1_fi < ind2_fi)
        return flag1 and flag2

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
        self._cv = sum([0 if g < 0 else 1 for g in self._g])
        return self._cv

    @property
    def r(self):
        return self._r
    
    @property
    def feasible(self):
        if self.cv == None:
            self.cv()
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