import numpy as np


class Dominate:
    def __init__(self, n_obj: int):
        self.n_obj = n_obj
        pass

    def _dominate(self, f_1, f_2):
        '''
        check dominance (f1 to f2)
        '''
        # multi objective
        if self.n_obj >= 2:
            flag1 = 0
            flag2 = 0
            for i in range(self.n_obj):
                f_i_1 = f_1[i]
                f_i_2 = f_2[i]
                if f_i_1 <= f_i_2:
                    flag1 += 1
                if f_i_1 < f_i_2:
                    flag2 += 1
            if (flag1 == self.n_obj) & (flag2 >= 1):
                nd = True  # x1 dominates x2
            else:
                nd = False
            
        # single objective
        elif self.n_obj == 1:
            if f_1 > f_2:
                nd = True
            else:
                nd = False
        return nd

    def eval(self, f_results):
        '''
        counting the number of dominate and dominated solutions
        '''
        n_inds = f_results.shape[0]
        counts = np.zeros([n_inds, 2])  # [number of dominate, number of dominated]
        dominate_list = [[] for _ in range(n_inds)]
        for i in range(n_inds):
            for j in range(n_inds):
                nd = self._dominate(f_results[i], f_results[j])
                if nd:
                    counts[i, 0] += 1
                    counts[j, 1] += 1
                    dominate_list[i].append(j)
        return counts, dominate_list


if __name__ == '__main__':
    n_obj = 2
    dominate = Dominate(n_obj)

    f1 = np.array([1., 1.])
    f2 = np.array([0.9, 0.8])
    print(dominate._dominate(f1, f2))

    f1 = np.array([1., 1.])
    f2 = np.array([1., 0.8])
    print(dominate._dominate(f1, f2))

    f1 = np.array([1., 1.])
    f2 = np.array([1., 1.])
    print(dominate._dominate(f1, f2))

    f1 = np.array([1., 1.])
    f2 = np.array([1., 4.])
    print(dominate._dominate(f1, f2))
