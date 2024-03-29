from typing import List
import numpy as np

from nsga2.individual import Individual
from nsga2.lhs import lhs


class Population:
    def __init__(self, problem, pop_size: int, sampling='lhs'):
        self.problem = problem
        self.pop_size = pop_size

        self.n_var = problem.n_var
        self.n_obj = problem.n_obj
        self.xl = problem.xl
        self.xu = problem.xu
        self.sampling = sampling

        self.history = []

    def create(self, gen: int, x=None) -> List:
        if x is None:
            x = self.x_sampling()
        pop = [Individual(gen, (i+1), x) for i, x in enumerate(x)]
        return pop
    
    def add_history(self, pop: List):
        self.history.extend(pop)

    def x_sampling(self):
        # x = np.random.random([self.pop_size, self.n_var])
        x = lhs(self.n_var, self.pop_size)
        x = x * (self.xu - self.xl) + self.xl
        return x
    
    def sort(self, pop: List) -> List:
        pop = pop.copy()
        self.eval_rank(pop)
        self.calc_crowding_distance(pop)
        pop = sorted(pop, key=lambda ind: ind.cd, reverse=True)
        pop = sorted(pop, key=lambda ind: ind.r)
        return pop
    
    def reduce(self, gen: int, pop1: List, pop2: List) -> List:
        pop = pop1.copy() + pop2.copy()
        pop = self.sort(pop)[:self.pop_size]
        return pop
    
    def write(self, pop: List, filename: str, mode='a'):
        with open(filename, mode) as f:
            for ind in pop:
                string = f'{ind.gen},{ind.ids},{list(ind.x)},{list(ind.f)},{list(ind.g)},{ind.cv},{ind.feasible}\n'
                string = string.replace('[', '').replace(']', '').replace(' ', '')
                f.write(string)
    
    def eval_rank(self, pop: List) -> None:
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
    
    def calc_crowding_distance(self, pop: List) -> None:
        for ind in pop:
            ind.clear_cd()

        rank = 1
        evaluated = 0
        while True:
            tmp_pop = [ind for ind in pop if ind.r == rank]
            if len(tmp_pop) == 0:
                rank += 1
                continue
            if len(tmp_pop) <= 2:
                for ind in tmp_pop:
                    ind.add_cd(10e+10)
            for i in range(self.n_obj):
                tmp_pop = sorted(tmp_pop, key=lambda ind: ind.f[i])
                tmp_pop[0].add_cd(10e+10)
                tmp_pop[-1].add_cd(10e+10)
                
                f_values = [ind.f[i] for ind in tmp_pop]
                scale = max(f_values) - min(f_values)
                if scale == 0: scale = 1
                
                for j in range(1, len(tmp_pop)-1):
                    cd = (tmp_pop[j+1].f[i] - tmp_pop[j-1].f[i]) / scale

                    tmp_pop[j].add_cd(cd)
            
            evaluated += len(tmp_pop)
            if evaluated == len(pop):
                break
            rank += 1


if __name__ == '__main__':
    population = Population()
    pop = population.create()