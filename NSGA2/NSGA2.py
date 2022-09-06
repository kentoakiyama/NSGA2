from NSGA2.mutation import Mutation
from NSGA2.crossover import Crossover
from NSGA2.evaluator import Evaluator
from NSGA2.individual import Individual


class NSGA2:
    def __init__(self, functions, n_obj, n_constr, pop_size, n_gen, n_var, xl, xu, mutation_eta, crossover_eta, n_processes, sampling='lhs'):
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.n_var = n_var
        self.xl = xl
        self.xu = xu
        self.mutation_eta = mutation_eta
        self.crossover_eta = crossover_eta
        self.n_processes = n_processes
        self.sampling = sampling

        self.individual = Individual(pop_size, n_var, xl, xu)
        self.crossover = Crossover(xl, xu, crossover_eta)
        self.evaluator = Evaluator(functions, pop_size, n_obj, n_constr, n_processes)

    def minimize(self):
        init_pop = self.individual.gen_pop()
        f_results, g_results, cv_results = self.evaluator.eval(1, init_pop)

        for gen in range(self.n_gen):
            pass
