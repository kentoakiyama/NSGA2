import numpy as np


def lhs(n_dim, n_sample):
    grid_array = np.linspace(0, n_sample-1, n_sample)
    
    def _sample_from_idx(lhs_idx):
        _n_sample = lhs_idx.shape[0]
        lhs_result = np.zeros([_n_sample, n_dim])
        for i in range(_n_sample):
            for j in range(n_dim):
                lhs_result[i, j] = (np.random.rand() + lhs_idx[i, j])/n_sample
        return lhs_result

    # array for storing the index
    lhs_idx = np.zeros([n_sample, n_dim])
    for i in range(n_dim):
        lhs_idx[:, i] = np.random.permutation(grid_array)
    # array for storing values
    lhs_result = _sample_from_idx(lhs_idx)
    return lhs_result