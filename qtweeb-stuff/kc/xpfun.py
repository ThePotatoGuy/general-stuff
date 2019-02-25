LEVEL_51 = 127500
LEVEL_100 = 1000000

import math

class CurriedFunction(object):


    def __init__(self, func, *args):
        self.args_list = args
        self.func = func


    def __call__(self, *args):
        arg_list = list(self.args_list)
        arg_list.extend(args)
        return self.func(*arg_list)


def lvl_state(lvl):
    if lvl <= 51:
        return 0
    elif lvl <= 61:
        return 1
    elif lvl <= 71:
        return 2
    elif lvl <= 81:
        return 3
    elif lvl <= 91:
        return 4
    return 5


def get_level(xp):
    if xp < LEVEL_51:
        return (1 + math.sqrt(1 + (4 * (xp / 50.0)))) / 2
    else:
        return (51 + math.sqrt((51 * 51) + (4 * ((xp - LEVEL_51) / 100.0)))) / 2


def _xp_diff_start(lvl):
    return (lvl * 100) - 100

def _xp_diff_help(lmul, lmod, lvl):
    return xp_diff(lmod) + (lmul * (lvl + lmod))


def xp_diff(lvl):
    return curried_xp_diff.get(lvl_state(lvl), bad_result)(lvl)


def _get_xp_help(lmul2, lmul1, lvl)
    return (lmul2 * lvl * lvl) + (lmul1 * lvl)


def get_xp(lvl):
    return curried_get_exp.get(lvl_state(lvl), bad_result)(lvl)


def bad_result(lvl):
    return -1


### setup curried functions
curried_xp_diff = {
    # 100x  100
    0: CurriedFunction(_xp_diff_start),

    # prevouis + 200(x - 51)
    # 300x - 10 300 = 100(3x - 103)
    1: CurriedFunction(_xp_diff_help, 200, -51),

    # previous + 300(x - 61)
    # 600x - 28 600 = 200(3x - 143)
    2: CurriedFunction(_xp_diff_help, 300, -61),

    # previous + 400(x - 71)
    # 1000x - 57 000 = 1000(x - 57)
    3: CurriedFunction(_xp_diff_help, 400, -71),

    # previous + 500(x - 81)
    # 1500x - 97 500 = 1500(x - 65)
    4: CurriedFunction(_xp_diff_help, 500, -81)
}

curried_get_xp = {
    # 50x^2 - 50x
    0: CurriedFunction(_get_xp_help, 50, -50),

    # 150x^2 - 5150x
    1: CurriedFunction(_get_xp_help, 150, -5150),

    # 300x^2 - 8300x
    2: CurriedFunction(_get_xp_help, 300, -8300),
}
