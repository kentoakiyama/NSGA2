from urllib.parse import ParseResultBytes

import numpy as np

class Rank:
    def __init__(self):
        pass
    def eval(self, inds, cv_results):
        '''
        get rank for each individual
        '''
        feas_idx = np.where(cv_results == 0)[0]  # index for feasible solution
        infeas_idx = np.where(cv_results != 0)[0]  # index for infeasible solution
        feas_inds = inds[feas_idx]

        n_inds = inds.shape[0]
        rank_array = np.zeros([n_inds, 1])
        rank = 1
        if feas_idx.size != 0:
            counts, dominate_list = self._check_nd(feas_inds)
            # sorting for feasible solution
            while True:
                # get index of individual that is not dominated
                nd_idx = np.where(counts[:, 1] == 0)[0]
                rank_idx = feas_idx[nd_idx]
                rank_array[rank_idx] = rank
                counts[nd_idx, 1] = -1
                for j in nd_idx:
                    counts[dominate_list[j], 1] -= 1
                rank += 1
                if np.all(counts[:, 1] == -1):
                    break 
        if infeas_idx.size != 0:
            cv_rank = np.argsort(cv_results[infeas_idx], axis=0) + rank
            rank_array[infeas_idx] = cv_rank
        return rank_array