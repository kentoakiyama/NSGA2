import numpy as np

from nsga2.dominate import Dominate

class Rank:
    def __init__(self, n_obj: int):
        self.dominate = Dominate(n_obj)

    def eval(self, pop):
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