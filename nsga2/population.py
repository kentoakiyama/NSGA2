from typing import List
import numpy as np

from nsga2.individual import Individual
from nsga2.lhs import lhs


class Population:
    def __init__(self, pop_size: int, n_var: int, n_obj: int, n_constr: int, xl: np.ndarray, xu: np.ndarray, sampling='lhs'):
        self.pop_size = pop_size
        self.n_var = n_var
        self.n_obj = n_obj
        self.xl = xl
        self.xu = xu
        self.sampling = sampling

        self.history = []

    def create(self, gen: int, x=None):
        if x is None:
            x = self.x_sampling()
        individuals = [Individual(gen, (i+1), x) for i, x in enumerate(x)]
        return individuals
    
    def add_history(self, pop: List):
        self.history.extend(pop)

    def x_sampling(self):
        # x = np.random.random([self.pop_size, self.n_var])
        x = lhs(self.n_var, self.pop_size)
        x = x * (self.xu - self.xl) + self.xl
        return x
    
    def sort(self, pop):
        new_pop = sorted(pop, key=lambda ind: ind.cd, reverse=True)
        new_pop = sorted(new_pop, key=lambda ind: ind.r)
        return new_pop
    
    def reduce(self, pop1, pop2):
        pop = pop1.copy() + pop2.copy()
        self.eval_rank(pop)
        self.calc_crowding_distance(pop)
        pop = self.sort(pop)
        return pop[:self.pop_size]
    
    def write(self, pop, filename):
        with open(filename, 'a') as f:
            for ind in pop:
                string = f'{ind.gen},{ind.ids},{list(ind.x)},{list(ind.f)},{list(ind.g)},{ind.cv},{ind.feasible}\n'
                string = string.replace('[', '').replace(']', '').replace(' ', '')
                f.write(string)
    
    def eval_rank(self, pop):
        '''
        get rank for each individual

        input:
        pop: list of individuals
        '''

        feas_sols = [ind for ind in pop if ind.cv == 0]
        infeas_sols = [ind for ind in pop if ind.cv != 0]

        rank = 1
        if len(feas_sols) != 0:
            front = []
            while len(feas_sols) > 0:
                for individual in feas_sols:
                    nd = True  # non-dominated solution flag
                    for other_individual in feas_sols:
                        nd = nd and (not other_individual.dominate(individual))
                    
                    if nd:
                        individual.set_rank(rank)
                        front.append(individual)
                
                feas_sols = [ind for ind in feas_sols if ind not in front]
                rank += 1

        if len(infeas_sols) != 0:
            cv_sorted_idx = np.argsort([ind.cv for ind in infeas_sols], axis=0)
            for i, idx in enumerate(cv_sorted_idx):
                infeas_sols[idx].set_rank(i + 1 + rank)
    
    def calc_crowding_distance(self, pop):
        for ind in pop:
            ind.clear_cd()

        rank = 1
        evaluated = 0
        while True:
            tmp_pop = [ind for ind in pop if ind.r == rank]
            if len(tmp_pop) == 0:
                rank += 1
                continue

            for i in range(self.n_obj):
                tmp_pop = sorted(tmp_pop, key=lambda ind: ind.f[i])
                tmp_pop[0].add_cd(10e+10)
                tmp_pop[-1].add_cd(10e+10)
                
                f_values = [ind.f[i] for ind in tmp_pop]
                f_i_min = min(f_values)
                f_i_max = max(f_values)
                
                for j in range(1, len(tmp_pop)-1):
                    cd = (tmp_pop[j+1].f[i] - tmp_pop[j-1].f[i]) / (f_i_max - f_i_min)

                    tmp_pop[j].add_cd(cd)
            
            evaluated += len(tmp_pop)
            if evaluated == len(pop):
                break
            rank += 1


if __name__ == '__main__':
    population = Population()
    pop = population.create()