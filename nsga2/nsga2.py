import os
import random
import numpy as np
from time import time
import matplotlib.pyplot as plt

from nsga2.logger import custom_logger
from nsga2.mating import Mating
from nsga2.result import Result
from nsga2.mutation import Mutation
from nsga2.crossover import Crossover
from nsga2.evaluator import Evaluator
from nsga2.selection import Selection
from nsga2.population import Population
from nsga2.individual import Individual


class NSGA2:
    def __init__(self, problem, pop_size: int, n_gen: int, mutation_prob=0.1, mutation_eta=0.4, crossover_eta=0.4, n_processes=1, sampling='lhs', seed=1):
        if pop_size % 4 != 0:
            raise ValueError('"pop_size" must be multiple of 4')

        self.problem = problem()

        self.pop_size = pop_size                         # number of population size (must be multiple of 4)
        self.n_gen = n_gen                               # number of generation
        self.n_var = self.problem.n_var                  # number of variables
        self.n_obj = self.problem.n_obj                  # number of objective function
        self.n_constr = self.problem.n_constr            # number of constraint function
        self.xl = self.problem.xl                        # lower bound of variables
        self.xu = self.problem.xu                        # upper bound of variables
        self.mutation_prob = mutation_prob
        self.mutation_eta = mutation_eta
        self.crossover_eta = crossover_eta
        self.n_processes = n_processes
        self.sampling = sampling

        self.logger = custom_logger(__name__)

        random.seed(seed)
        np.random.seed(seed)

        self.population = Population(self.problem, pop_size)
        self.evaluator = Evaluator(self.problem, pop_size, n_processes)
        self.crossover = Crossover(self.xl, self.xu, crossover_eta)
        self.mutation = Mutation(self.mutation_prob, self.xl, self.xu, mutation_eta)
        self.selection = Selection()
        self.mating = Mating(self.n_obj, self.n_var, self.selection, self.crossover, self.mutation)
        self.result = Result()
        self.mating = Mating(self.pop_size, self.n_var, self.selection.selection, self.crossover.crossover_sbx, self.mutation.mutation)

        self.fig, self.ax = plt.subplots()
    
    def display(self, gen, pop, ax):
        feas_F = np.array([ind.f for ind in pop])
        r = np.array([ind.r for ind in pop])
        infeas_F = np.array([ind.f for ind in pop if (not ind.feasible and ind.r > 1)])
        front_F = np.array([ind.f for ind in pop if ind.r == 1])
        ax.cla()
        ax.scatter(feas_F[:, 0], feas_F[:, 1], alpha=0.5, c=r, cmap='jet', label='feasible')
        # self.fig, self.ax = plt.subplots()
        # if feas_F.size != 0:
        #     ax.scatter(feas_F[:, 0], feas_F[:, 1], alpha=0.5, c='tab:green', label='feasible')
        # if infeas_F.size != 0:
        #     ax.scatter(infeas_F[:, 0], infeas_F[:, 1], alpha=0.5, c='tab:red', marker='x', label='infeasible')
        # if front_F.size != 0:
        #     ax.scatter(front_F[:, 0], front_F[:, 1], alpha=0.5, c='tab:blue', label='non-dominated')
        plt.draw()
        plt.pause(0.2)
        # plt.show()
        # import pdb;pdb.set_trace()
    
    def step(self, gen, parent_pop, child_pop):
        parent_pop = self.population.reduce(parent_pop, child_pop)

    def minimize(self):
        start = time()
        self.logger.info('Start optimization!')
        
        # 1st generation
        gen = 1
        parent_pop = self.population.create(gen)
        self.evaluator.eval(parent_pop)
        self.population.write(parent_pop, 'solutions_all.csv')
        parent_pop = self.population.sort(parent_pop)
        self.display(gen, parent_pop, self.ax)
        self.logger.info(f'{gen: >4} finished')
        
        # 2nd generation
        gen = 2
        child_pop = self.mating.mating(parent_pop, gen)
        self.evaluator.eval(child_pop)
        # self.population.write(child_pop, 'solutions_all.csv')
        child_pop = self.population.sort(child_pop)
        self.display(gen, child_pop, self.ax)
        self.logger.info(f'{gen: >4} finished')

        for gen in range(3, self.n_gen+1):
            parent_pop = self.population.sort(parent_pop+child_pop)[:self.pop_size]
            child_pop = self.mating.mating(parent_pop, gen)
            self.evaluator.eval(child_pop)
            # self.population.write(child_pop, 'solutions_all.csv')
            child_pop = self.population.sort(child_pop)
            self.display(gen, child_pop, self.ax)
            self.logger.info(f'{gen: >4} finished')
            # import pdb;pdb.set_trace()
        
        self.result.gen = [ind.gen for ind in child_pop]
        self.result.ids = [ind.ids for ind in child_pop]
        self.result.x = [ind.x for ind in child_pop]
        self.result.f = [ind.f for ind in child_pop]
        self.result.g = [ind.g for ind in child_pop]
        self.result.r = [ind.r for ind in child_pop]
        self.result.feasible = [ind.feasible for ind in child_pop]
        self.process_time = time() - start
        self.population.write(child_pop, 'solutions_final.csv')
        import pdb;pdb.set_trace()
        
        fig, ax = plt.subplots()
        self.display(gen, child_pop, ax)
        plt.show()
        return self.result



