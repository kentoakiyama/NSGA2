import numpy as np


class Selection:
    def selection(self, rank_array, idx1, idx2):
        # get better individual from two individuals
        if rank_array[idx1] < rank_array[idx2]:
            idx = idx1
        elif rank_array[idx1] > rank_array[idx2]:
            idx = idx2
        elif np.random.random() <= 0.5:
            idx = idx1
        else:
            idx = idx2
        return idx