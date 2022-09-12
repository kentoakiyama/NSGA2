import numpy as np

class Mating:
    def __init__(self, pop_size, n_var, selection, crossover, mutation):
        self.pop_size = pop_size
        self.n_var = n_var

        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
    
    def _mating(self, parent_pop):
        parent_pop1 = np.random.choice(parent_pop, size=self.pop_size, replace=False)
        parent_pop2 = np.random.choice(parent_pop, size=self.pop_size, replace=False)
        children = np.zeros([self.pop_size, self.n_var])
        for i in range(0, self.pop_size, 4):
            # Select parents
            p1 = self.selection(parent_pop1[i+0], parent_pop1[i+1])
            p2 = self.selection(parent_pop1[i+2], parent_pop1[i+3])
            # Generate children
            c1, c2 = self.crossover(p1.x, p2.x)
            children[i] = c1
            children[i+1] = c2
            # Select parents
            p1 = self.selection(parent_pop2[i+0], parent_pop2[i+1])
            p2 = self.selection(parent_pop2[i+2], parent_pop2[i+3])
            # Generate children
            c1, c2 = self.crossover(p1.x, p2.x)
            children[i+2] = c1
            children[i+3] = c2
        return children

    def mating(self, parent_pop):
        children = self._mating(parent_pop)
        self.mutation(children)
        return children