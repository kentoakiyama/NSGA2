import numpy as np


def Binh_functions(x, gen, ids):
    # objective fucntions
    f_1 = 4*x[0]**2 + 4*x[1]**2
    f_2 = (x[0]-5)**2 + (x[1]-5)**2
    # constraint functions
    g_1 = (x[0]-5)**2 + x[1]**2 - 25
    g_2 = -(x[0]-8)**2 - (x[1]+3)**2 + 7.7
    return [f_1, f_2], [g_1, g_2]


def Chankong_functions(x, gen, ids):
    # objective fucntions
    f_1 = 2 + (x[0] - 2)**2 + (x[1] - 1)**2
    f_2 = 9*x[0] - (x[1] - 1)**2
    # constraint functions
    g_1 = x[0]**2 + x[1]**2 - 225.
    g_2 = x[0] - 3*x[1] + 10
    return [f_1, f_2], [g_1, g_2]


def Osyczka_functions(x, gen, ids):
    x1, x2, x3, x4, x5, x6 = x
    # objective fucntions
    f_1 = -25*(x1-2)**2 - (x2-2)**2 - (x3-1)**2 - (x4-4)**2 - (x5-1)**2
    f_2 = x1**2 + x2**2 + x3**2 + x4**2 + x5**2 + x6**2
    # constraint functions
    g_1 = - (x1 + x2 - 2)
    g_2 = - (6 - x1 - x2)
    g_3 = - (2 - x2 + x1)
    g_4 = - (2 - x1 + 3*x2)
    g_5 = - (4 - (x3-3)**2 - x4)
    g_6 = - ((x5 - 3)**2 + x6 - 4)
    return [f_1, f_2], [g_1, g_2, g_3, g_4, g_5, g_6]


def TNK_functions(x, gen, ids):
    # objective fucntions
    f_1 = x[0]
    f_2 = x[1]
    # constraint functions
    g_1 = -x[0]**2 - x[1]**2 + 1 + 0.1*np.cos(16*np.arctan(x[0]/(x[1]+1e-15)))
    g_2 = (x[0]-0.5)**2 + (x[1]-0.5)**2 - 0.5
    return [f_1, f_2], [g_1, g_2]
