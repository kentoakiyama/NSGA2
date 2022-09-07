import numpy as np

from nsga2.dominate import Dominate

class Rank:
    def __init__(self, n_obj: int, n_constr: int):
        self.n_constr = n_constr
        self.dominate = Dominate(n_obj)

    def eval(self, pop):
        '''
        get rank for each individual

        input:
        pop: list of individuals
        '''

        feas_sols = [ind for ind in pop if ind.cv == 0]
        infeas_sols = [ind for ind in pop if ind.cv != 0]

        n_inds = len(pop)
        rank_array = np.zeros([n_inds, 1])
        rank = 1
        if len(feas_sols) != 0:
            counts, dominate_list = self.dominate.eval(feas_sols)
            # sorting for feasible solution
            while True:
                # get index of individual that is not dominated
                nd_idx = np.where(counts[:, 1] == 0)[0]
                for i in nd_idx:
                    feas_sols[i].set_rank(rank)
                # rank_idx = feas_idx[nd_idx]
                # rank_array[rank_idx] = rank
                counts[nd_idx, 1] = -1
                for j in nd_idx:
                    counts[dominate_list[j], 1] -= 1
                rank += 1
                if np.all(counts[:, 1] == -1):
                    break

        if len(infeas_sols) != 0:
            cv_sorted_idx = np.argsort([ind.cv for ind in infeas_sols], axis=0)
            for i, idx in enumerate(cv_sorted_idx):
                infeas_sols[idx].set_rank(i + 1 + rank)