import numpy as np

class Mating:
    def __init__(self, pop_size, n_var, selection, crossover, mutation):
        self.pop_size = pop_size
        self.n_var = n_var

        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
    
    def _mating(self, parent_pop):
        rank_array = np.array([ind.r for ind in parent_pop])
        a1 = np.random.permutation(np.array([i for i in range(self.pop_size)]))
        a2 = np.random.permutation(np.array([i for i in range(self.pop_size)]))
        children = np.zeros([self.pop_size, self.n_var])
        for i in range(0, self.pop_size, 4):
            # Select parents
            p1 = self.selection(rank_array, a1[i], a1[i+1])
            p2 = self.selection(rank_array, a1[i+2], a1[i+3])
            # Generate children
            c1, c2 = self.crossover(parent_pop[p1].x, parent_pop[p2].x)
            children[i] = c1
            children[i+1] = c2
            # Select parents
            p1 = self.selection(rank_array, a2[i], a2[i+1])
            p2 = self.selection(rank_array, a2[i+2], a2[i+3])
            # Generate children
            c1, c2 = self.crossover(parent_pop[p1].x, parent_pop[p2].x)
            children[i+2] = c1
            children[i+3] = c2
        return children

    def mating(self, parent_pop):
        children = self._mating(parent_pop)
        self.mutation(children)
        return children