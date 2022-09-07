from nsga2.mutation import Mutation
from nsga2.crossover import Crossover
from nsga2.evaluator import Evaluator
from nsga2.individual import Individual
from nsga2.rank import Rank
from nsga2.dominate import Dominate
from nsga2.mating import Mating
from nsga2.population import Population
from nsga2.selection import Selection

class NSGA2:
    def __init__(self, functions, n_obj: int, n_constr: int, pop_size: int, n_gen: int, n_var: int, xl, xu, mutation_probs=0.1, mutation_eta=0.4, crossover_eta=0.4, n_processes=1, sampling='lhs'):
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.n_var = n_var
        self.xl = xl
        self.xu = xu
        self.mutation_eta = mutation_eta
        self.crossover_eta = crossover_eta
        self.n_processes = n_processes
        self.sampling = sampling

        self.evaluator = Evaluator(functions, pop_size, n_obj, n_constr, n_processes)
        self.dominate = Dominate(n_obj)
        self.rank = Rank(n_obj)
        self.crossover = Crossover(xl, xu, crossover_eta)
        self.mutation = Mutation(mutation_probs, xl, xu, mutation_eta)
        self.selection = Selection()
        self.mating = Mating(n_obj, n_var, self.selection, self.crossover, self.mutation)

    def minimize(self):
        parents = Population(gen=1, pop_size=self.pop_size)
        import pdb; pdb.set_trace()
        parents_pop = parents.create()
        import pdb; pdb.set_trace()
        self.evaluator.eval(parents_pop)
        import pdb; pdb.set_trace()
        self.rank.eval(parents_pop)
        import pdb; pdb.set_trace()

        for gen in range(1, self.n_gen+1):
            children = self.mating.mating(parents, p_rank_array)
            # f_results, g_results, cv_results = self.evaluator.eval(gen, children)



