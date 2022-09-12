import numpy as np


class Selection:
    def selection(self, individual1, individual2):
        # get better individual from two individuals
        if individual1.r < individual2.r:
            return individual1
        elif individual1.r > individual2.r:
            return individual2
        elif np.random.random() <= 0.5:
            return individual1
        else:
            return individual2