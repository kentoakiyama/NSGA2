import os
import random
import numpy as np
from time import time
import matplotlib.pyplot as plt
from copy import deepcopy

from nsga2.logger import custom_logger
from nsga2.mating import Mating
from nsga2.result import Result
from nsga2.mutation import Mutation
from nsga2.crossover import Crossover
from nsga2.evaluator import Evaluator
from nsga2.selection import Selection
from nsga2.population import Population
from nsga2.save import Save

class NSGA2:
    def __init__(self, problem, pop_size: int, n_gen: int, mutation_prob=0.1, mutation_eta=0.4, crossover_eta=0.4, n_processes=1, sampling='lhs', seed=1, restart=False):
        if pop_size % 4 != 0:
            raise ValueError('"pop_size" must be multiple of 4')

        self.problem = problem()

        self.pop_size = pop_size                         # number of population size (must be multiple of 4)
        self.n_gen = n_gen                               # number of generation
        self.n_var = self.problem.n_var                  # number of variables
        self.n_obj = self.problem.n_obj                  # number of objective function
        self.xl = self.problem.xl                        # lower bound of variables
        self.xu = self.problem.xu                        # upper bound of variables
        self.sampling = sampling
        self.seed = seed
        self.restart = restart

        self.logger = custom_logger(__name__)
        
        self.all_populations = []


        self.population = Population(self.problem, pop_size)
        self.evaluator = Evaluator(self.problem, pop_size, 'solutions_all.csv', n_processes)
        self.crossover = Crossover(self.xl, self.xu, crossover_eta)
        self.mutation = Mutation(mutation_prob, self.xl, self.xu, mutation_eta)
        self.selection = Selection()
        self.mating = Mating(self.n_obj, self.n_var, self.selection, self.crossover, self.mutation)
        self.result = Result()
        self.mating = Mating(self.pop_size, self.n_var, self.selection.selection, self.crossover.crossover_sbx, self.mutation.mutation)
        self.save = Save()

        self.fig, self.ax = plt.subplots()
    
    def set_seed(self):
        random.seed(self.seed)
        np.random.seed(self.seed)
    
    def display(self, gen, pop, ax):
        feas_F = np.array([ind.f for ind in pop if (ind.feasible and ind.r > 1)])
        infeas_F = np.array([ind.f for ind in pop if (not ind.feasible)])
        front_F = np.array([ind.f for ind in pop if ind.r == 1])
        ax.cla()
        if feas_F.size != 0:
            ax.scatter(feas_F[:, 0], feas_F[:, 1], alpha=0.5, c='tab:green', label='feasible')
        if infeas_F.size != 0:
            ax.scatter(infeas_F[:, 0], infeas_F[:, 1], alpha=0.5, c='tab:red', marker='x', label='infeasible')
        if front_F.size != 0:
            ax.scatter(front_F[:, 0], front_F[:, 1], alpha=0.5, c='tab:blue', label='non-dominated')
        ax.legend(loc='upper right')
        ax.set_title(f"Gen: {gen}")
        plt.draw()
        plt.pause(0.01)
    
    def step(self, pop: list) -> list:
        pop = self.evaluator.eval(pop)
        self.population.eval_rank(pop)
        self.population.calc_crowding_distance(pop)
        return pop

    def minimize(self):
        self.set_seed()
        start = time()
        self.logger.info('Start optimization!')

        if self.restart:
            all_populations = self.save.load_pickle()
        else:
            all_populations = []
        
        # 1st generation
        gen = 1
        if len(all_populations) == 0:
            parent_pop = self.population.create(gen)
            self.step(parent_pop)
            self.all_populations.append(deepcopy(parent_pop))
            self.population.write(parent_pop, 'solutions_all.csv', 'w')
            self.save.save_pickle(self.all_populations)
        else:
            self.logger.info('Load data from cache file.')
            parent_pop = all_populations[0]
            self.all_populations.append(deepcopy(parent_pop))

        self.display(gen, parent_pop, self.ax)
        self.logger.info('| Gen | ND_solutions |')
        self.logger.info(f'|{gen: >5}|{len([ind.f for ind in parent_pop if ind.r == 1]): >14}|')
        
        
        for gen in range(2, self.n_gen+1):
            if len(all_populations) < gen:
                child_pop = self.mating.mating(parent_pop, gen)
                self.step(child_pop)
                self.population.write(child_pop, 'solutions_all.csv', 'a')
                self.all_populations.append(deepcopy(child_pop))
                self.save.save_pickle(self.all_populations)

                parent_pop = self.population.reduce(gen, parent_pop, child_pop)
            else:
                self.logger.info('Load data from cache file.')
                parent_pop = all_populations[gen-2]
                child_pop = all_populations[gen-1]
                self.all_populations.append(deepcopy(child_pop))
            self.display(gen, parent_pop, self.ax)
            self.logger.info(f'|{gen: >5}|{len([ind.f for ind in child_pop if ind.r == 1]): >14}|')

        
        self.result.gen = [ind.gen for ind in child_pop]
        self.result.ids = [ind.ids for ind in child_pop]
        self.result.x = [ind.x for ind in child_pop]
        self.result.f = [ind.f for ind in child_pop]
        self.result.g = [ind.g for ind in child_pop]
        self.result.r = [ind.r for ind in child_pop]
        self.result.feasible = [ind.feasible for ind in child_pop]
        self.process_time = time() - start
        self.population.write(child_pop, 'solutions_final.csv', 'w')
        
        # fig, ax = plt.subplots()
        # self.display(gen, child_pop, ax)
        plt.show()
        return self.result



