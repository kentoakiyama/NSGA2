import os
import random
import numpy as np
from time import time

from nsga2.logger import custom_logger
from nsga2.rank import Rank
from nsga2.mating import Mating
from nsga2.result import Result
from nsga2.dominate import Dominate
from nsga2.mutation import Mutation
from nsga2.crossover import Crossover
from nsga2.evaluator import Evaluator
from nsga2.selection import Selection
from nsga2.population import Population
from nsga2.individual import Individual


class NSGA2:
    def __init__(self, functions, n_var: int, n_obj: int, n_constr: int, pop_size: int, n_gen: int, xl, xu, mutation_probs=0.1, mutation_eta=0.4, crossover_eta=0.4, n_processes=1, sampling='lhs'):
        if pop_size % 4 != 0:
            raise ValueError('"pop_size" must be multiple of 4')

        self.pop_size = pop_size            # number of population size (must be multiple of 4)
        self.n_gen = n_gen                  # number of generation
        self.n_var = n_var                  # number of variables
        self.n_obj = n_obj                  # number of objective function
        self.n_constr = n_constr            # number of constraint function
        self.xl = xl                        # lower bound of variables
        self.xu = xu                        # upper bound of variables
        self.mutation_eta = mutation_eta
        self.crossover_eta = crossover_eta
        self.n_processes = n_processes
        self.sampling = sampling

        self.logger = custom_logger(__name__)

        seed = 0
        random.seed(seed)
        np.random.seed(seed)

        self.population = Population(pop_size, n_var, n_obj, n_constr, xl, xu)
        self.evaluator = Evaluator(functions, pop_size, n_obj, n_constr, n_processes)
        self.dominate = Dominate(n_obj)
        self.rank = Rank(n_obj, n_constr)
        self.crossover = Crossover(xl, xu, crossover_eta)
        self.mutation = Mutation(mutation_probs, xl, xu, mutation_eta)
        self.selection = Selection()
        self.mating = Mating(n_obj, n_var, self.selection, self.crossover, self.mutation)
        self.result = Result()
    
    def load_history(self):
        if not os.path.exists('solutions.csv'):
            return None
        
        self.logger.info('Load the solution file')
        with open('solutions.csv', 'r') as f:
            lines = f.readlines()
        
        history = []
        for line in lines:
            data = line[:-1].split(',')
            gen = int(data[0])
            ids = int(data[1])
            x = list(map(float, data[2:2+self.n_var]))
            f = list(map(float, data[2+self.n_var:2+self.n_var+self.n_obj]))
            g = list(map(float, data[2+self.n_var+self.n_obj:2+self.n_var+self.n_obj+self.n_constr]))
            individual = Individual(gen, ids, x)
            individual.set_result(f, g)
            history.append(individual)
        # self.population.add_history(history)

    def minimize(self):
        start = time()
        self.logger.info('Start optimization!')
        self.load_history()

        for gen in range(1, self.n_gen+1):
            if gen == 1:
                parent_pop = self.population.create(1)
                self.evaluator.eval(parent_pop)
                self.population.write(parent_pop, 'solutions_all.csv')
                self.rank.eval(parent_pop)
                # self.population.add_history(parent_pop)
            else:
                mating = Mating(self.pop_size, self.n_var, self.selection.selection, self.crossover.crossover_sbx, self.mutation.mutation)
                child_x = mating.mating(parent_pop)
                child_pop = self.population.create(gen, child_x)
                self.evaluator.eval(child_pop)
                self.population.write(child_pop, 'solutions_all.csv')
                # self.population.add_history(child_pop)
                parent_pop = self.population.reduce(parent_pop, child_pop)
            self.logger.info(f'{gen: >4} finished')
        
        self.result.gen = [ind.gen for ind in child_pop]
        self.result.ids = [ind.ids for ind in child_pop]
        self.result.x = [ind.x for ind in child_pop]
        self.result.f = [ind.f for ind in child_pop]
        self.result.g = [ind.g for ind in child_pop]
        self.result.r = [ind.r for ind in child_pop]
        self.result.feasible = [ind.feasible for ind in child_pop]
        self.process_time = time() - start
        self.population.write(child_pop, 'solutions_final.csv')
        return self.result



