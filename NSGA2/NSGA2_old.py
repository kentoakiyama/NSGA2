'''
NSGA2 (Non-dominated Sorting Genetic Algorithms-2)
Scripts for multi objective optimization
'''

import os
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool

class Results:
    pass

class NSGA2:
    def __init__(self, functions, params, problem):
        self.functions = functions
        self.params = params
        self.problem = problem
        self.x_min = np.array([problem.range[i][0] for i in problem.range.keys()])
        self.x_max = np.array([problem.range[i][1] for i in problem.range.keys()])
        if self.params.n_pop % 4 != 0:
            raise Exception('Number of poplation must be multiple of 4!')

    def _gen_init_ind(self):
        '''
        generate initial population
        '''
        x_array = np.random.random([self.params.n_pop, self.problem.n_vars])
        for i, key in enumerate(self.problem.range.keys()):
            x_array[:, i] = x_array[:, i]*(self.problem.range[key][1]-self.problem.range[key][0])+self.problem.range[key][0]
        return x_array

    def _eval_inds(self, inds, gen, pool=None):
        '''
        evaluate individuals 
        '''
        # single processing
        if self.params.n_parallels == 1:
            # evaluation for each individual
            f_results = np.zeros([self.params.n_pop, self.problem.n_obj])
            g_results = np.zeros([self.params.n_pop, self.problem.n_constr])

            for i, ind in enumerate(inds):
                ids = i+1
                # evaluate objective functions
                f_results[i], g_results[i] = self.functions(ind, gen, ids)

        # multi processing
        elif self.params.n_parallels > 1:
            # Create argument for multi processing
            multi_args = [(ind, i+1, gen) for i, ind in enumerate(inds)]
            results = pool.starmap(self.functions, multi_args)
            f_results = np.array([result[0] for result in results])
            g_results = np.array([result[1] for result in results])

        cv_results = np.where(g_results <= 0, 0, 1)
        cv_results = np.sum(cv_results, axis=1)[..., np.newaxis]
        return f_results, g_results, cv_results

    def _crossover_sbx(self, x1, x2):
        """
        Crossover by using Simulated binary crossover
        Two children are generated from parents.
        """
        r = np.random.random()
        # u = 0.9
        if r <= 0.5:
            beta = (2*r)**(1/(self.params.crosober_sbx_eta+1))
        else:
            beta = (1/(2-2*r))**(1/(self.params.crosober_sbx_eta+1))
        y1 = 0.5*((1+beta)*x1 + (1-beta)*x2)

        # child 2
        r = np.random.random()
        # u = 0.7
        if r <= 0.5:
            beta = (2*r)**(1/(self.params.crosober_sbx_eta+1))
        else:
            beta = (1/(2-2*r))**(1/(self.params.crosober_sbx_eta+1))
        y2 = 0.5*((1-beta)*x1 + (1+beta)*x2)

        y1 = np.where(y1 < self.x_min, self.x_min, y1)
        y2 = np.where(y2 < self.x_min, self.x_min, y2)
        y1 = np.where(y1 > self.x_max, self.x_max, y1)
        y2 = np.where(y2 > self.x_max, self.x_max, y2)
        return y1, y2

    def _mutation(self, x):
        """
        Mutation function
        """
        delta_1 = (x - self.x_min) / (self.x_max - self.x_min)
        delta_2 = (self.x_max - x) / (self.x_max - self.x_min)
        mut_pow = 1/(self.params.mutation_eta+1)
        r = np.random.random()

        if r <= 0.5:
            xy = 1 - delta_1
            val = 2*r + (1-2*r)*xy**(self.params.mutation_eta+1)
            deltaq = val**mut_pow - 1
        else:
            xy = 1 - delta_2
            val = 2*(1-r) + 2*(r-0.5)*xy**(self.params.mutation_eta+1)
            deltaq = 1 - val**mut_pow

        x = x + deltaq*(self.x_max - self.x_min)
        x = np.where(x < self.x_min, self.x_min, x)
        x = np.where(x > self.x_max, self.x_max, x)
        return x

    def _dominate(self, f_1, f_2):
        '''
        check dominance (x1 to x2)
        '''
        # multi objective
        if self.problem.n_obj >= 2:
            flag1 = 0
            flag2 = 0
            for i in range(self.problem.n_obj):
                f_i_1 = f_1[i]
                f_i_2 = f_2[i]
                if f_i_1 <= f_i_2:
                    flag1 += 1
                if f_i_1 < f_i_2:
                    flag2 += 1
            if (flag1 == self.problem.n_obj) & (flag2 >= 1):
                nd = True  # x1 dominates x2
            else:
                nd = False
            
        # single objective
        elif self.problem.n_obj == 1:
            if f_1 > f_2:
                nd = True
            else:
                nd = False
        return nd

    def _check_nd(self, f_results):
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

    def _sort_inds(self, inds, f_results, g_results, rank_array, cv_results):
        '''
        sorting the individuals 
        '''
        rank = 1
        counts = 0
        sorted_idx = np.zeros([rank_array.size], dtype=np.int32)

        while True:
            rank_idx = np.where(rank_array == rank)[0]
            n_rank = rank_idx.size
            if n_rank == 0:
                break
            if n_rank > 1:
                if counts+n_rank <= self.params.n_pop:
                    sorted_idx[counts:counts+n_rank] = rank_idx
                else:
                    crowd_array = self._calc_crowd(f_results[rank_idx])
                    temp_sorted_idx = np.argsort(crowd_array, axis=0)[:, 0][::-1]
                    sorted_idx[counts:counts+n_rank] = rank_idx[temp_sorted_idx]
            else:
                sorted_idx[counts:counts+n_rank] = rank_idx
            rank += 1
            counts += n_rank

        inds = inds[sorted_idx]
        f_results = f_results[sorted_idx]
        g_results = g_results[sorted_idx]
        rank_array = rank_array[sorted_idx]
        cv_results = cv_results[sorted_idx]
        return inds, f_results, g_results, rank_array, cv_results

    def _get_rank(self, inds, cv_results):
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

    def _tournament(self, rank_array, idx1, idx2):
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

    def _calc_crowd(self, f_results):
        n_inds = f_results.shape[0]
        crowd_array = np.zeros([n_inds, 1])
        for i in range(self.problem.n_obj):
            idxs_i = np.argsort(f_results[:, i])
            crowd_array[idxs_i[0], 0] += 1e+10
            crowd_array[idxs_i[-1], 0] += 1e+10
            f_i_max = np.max(f_results[:, i])
            f_i_min = np.min(f_results[:, i])
            for j in range(1, n_inds-1):
                crowd_array[idxs_i[j], 0] += (f_results[idxs_i[j+1], i] - f_results[idxs_i[j-1], i]) / (f_i_max - f_i_min)
        return crowd_array

    def _gen_children(self, parents, p_rank_array):
        a1 = np.random.permutation(np.array([i for i in range(self.params.n_pop)]))
        a2 = np.random.permutation(np.array([i for i in range(self.params.n_pop)]))
        children = np.zeros([self.params.n_pop, self.problem.n_vars])
        for i in range(0, self.params.n_pop, 4):
            # Select parents
            p1 = self._tournament(p_rank_array, a1[i], a1[i+1])
            p2 = self._tournament(p_rank_array, a1[i+2], a1[i+3])
            # Generate children
            c1, c2 = self._crossover_sbx(parents[p1], parents[p2])
            children[i] = c1
            children[i+1] = c2
            # Select parents
            p1 = self._tournament(p_rank_array, a2[i], a2[i+1])
            p2 = self._tournament(p_rank_array, a2[i+2], a2[i+3])
            # Generate children
            c1, c2 = self._crossover_sbx(parents[p1], parents[p2])
            children[i+2] = c1
            children[i+3] = c2
        for i in range(self.params.n_pop):
            children[i] = self._mutation(children[i])
        return children

    def _plot(self, gen, res, comb):

        feas_idx = np.where(res.CG == 0)[0]  # index for feasible solution
        infeas_idx = np.where(res.CG != 0)[0]  # index for infeasible solution
        nd_idx = np.where(res.Rank == 1)[0]

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        ax.set_title(f'Gen: {gen}')
        ax.scatter(res.F[feas_idx, comb[0]], res.F[feas_idx, comb[1]], label='Feasible', c='blue')
        ax.scatter(res.F[infeas_idx, comb[0]], res.F[infeas_idx, comb[1]], label='Infeasible', c='red')
        ax.scatter(res.F[nd_idx, comb[0]], res.F[nd_idx, comb[1]], label='ND solution', c='green')
        plt.legend()
        plt.pause(0.0001)
        plt.show(block=False)
        return fig

    def _reduce(self, inds, f_results, g_results, rank_array, cv_results):
        inds, f_results, g_results, rank_array, cv_results \
            = self._sort_inds(inds, f_results, g_results, rank_array, cv_results)
        parent = inds[:self.params.n_pop]
        f_results = f_results[:self.params.n_pop]
        g_results = g_results[:self.params.n_pop]
        rank_array = rank_array[:self.params.n_pop]
        cv_results = cv_results[:self.params.n_pop]
        return parent, f_results, g_results, rank_array, cv_results

    def _logger(self, res, gen, file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'w') as w:
            for i in range(self.params.n_pop):
                id = i+1
                string = f'{gen:>3} {id:>3}'
                for j in range(self.problem.n_obj):
                    string += f' {res.F[i, j]}'
                for j in range(self.problem.n_constr):
                    string += f' {res.G[i, j]}'
                for j in range(self.problem.n_vars):
                    string += f' {res.X[i, j]}'
                string += '\n'
                w.write(string)

    def minimize(self):
        print(__file__)
        print(f'Start optimization at {datetime.datetime.now()}')
        print('----------------------------------------------------------')
        print('n_gen |  n_eval  | cv(min) | cv(max) |  cv(ave)  | n_nds |')
        print('----------------------------------------------------------')
        if self.params.seed is not None:
            np.random.seed(seed=self.params.seed)
        # Setting for multi processing
        if self.params.n_parallels == 1:
            pool = None
        elif self.params.n_parallels > 1:
            pool = Pool(self.params.n_parallels)
        start = time.time()
        parents = self._gen_init_ind()
        p_f_results, p_g_results, p_cv_results = self._eval_inds(parents, 1, pool)
        n_eval = self.params.n_pop
        p_rank_array = self._get_rank(p_f_results, p_cv_results)

        for gen in range(self.params.n_gen):
            gen = gen + 1
            children = self._gen_children(parents, p_rank_array)
            c_f_results, c_g_results, c_cv_results = self._eval_inds(children, gen, pool)
            n_eval += self.params.n_pop

            f_indivisuals = np.concatenate([parents, children])
            f_f_results = np.concatenate([p_f_results, c_f_results])
            f_g_results = np.concatenate([p_g_results, c_g_results])
            f_cv_results = np.concatenate([p_cv_results, c_cv_results])
            f_rank_array = self._get_rank(f_f_results, f_cv_results)

            parents, p_f_results, p_g_results, p_rank_array, p_cv_results \
                = self._reduce(f_indivisuals, f_f_results, f_g_results, f_rank_array, f_cv_results)

            res = Results()
            res.X = parents
            res.F = p_f_results
            res.G = p_g_results
            res.CG = p_cv_results
            res.Rank = p_rank_array

            # logger
            file_path = f'History\\all_gen_{gen:3>0}.dat'
            self._logger(res, gen, file_path)

            nd_idx = np.where(p_rank_array == 1)[0]
            print(f'{gen:>5} | {n_eval:>8} | {np.min(p_cv_results):>7} | {np.max(p_cv_results):>7} | {np.average(p_cv_results):.7f} | {len(nd_idx):>6}|')

        res.Time = time.time() - start
        return res
