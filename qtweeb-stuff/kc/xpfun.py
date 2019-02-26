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

def _xp_diff_help(amul, mmul, bmod, lmod, lvl):
    return amul * ( (mmul * (lvl + lmod)) + bmod)
#    return xp_diff(lmod) + (lmul * (lvl + lmod))

def _xp_diff_piece(piece, start, end, lvl):
    amt = c_xd[piece](lvl)
    return (amt * c_hf[start](lvl)) - (amt * c_hf[end](lvl))


def xp_diff(lvl):
    """
    Xp diff calcs:
    First 50 levels follows formula: 100x - 100
    From there to level 91, add a 100x - 100 term every 10 levels.
    """
    return (
        _xp_diff_piece(0, 0, 1, lvl)
        + _xp_diff_piece(1, 1, 2, lvl)
        + _xp_diff_piece(2, 2, 3, lvl)
        + _xp_diff_piece(3, 3, 4, lvl)
        + _xp_diff_piece(4, 4, 5, lvl)
    )
#    amt = 0
#    for i in range(5):
#        amt += (c_xd[i](lvl) * c_hf[i](lvl))
#    return amt

#    return curried_xp_diff.get(lvl_state(lvl), bad_result)(lvl)


def _get_xp_quad(amul, m2, m1, kcon, lvl):
    return amul * ( (m2 * lvl * lvl) + (m1 * lvl) + kcon)

def _get_xp_quadf(amul, m1, k1, m2, k2, lvl):
    return amul * ( (m1 * lvl) + k1) * ( (m2 * lvl) + k2)

def _get_xp_help(amul, mmul, bmod, lmod, prev, lvl):
    return (amul * lvl * ( (mmul * (lvl + lmod)) + bmod)) + get_xp
#    return amul * lvl * ( (mmul * (lvl + lmod)) + bmod)


def _get_xp_piece(piece, start, end, lvl):
    amt = c_gx[piece](lvl)
    return (amt * c_hf[start](lvl)) - (amt * c_hf[end](lvl))


def get_xp(lvl):
    return (
        _get_xp_piece(0, 0, 1, lvl)
        + _get_xp_piece(1, 1, 2, lvl)
        + _get_xp_piece(2, 2, 3, lvl)
        + _get_xp_piece(3, 3, 4, lvl)
        + _get_xp_piece(4, 4, 5, lvl)
    )

#    return curried_get_exp.get(lvl_state(lvl), bad_result)(lvl)


def bad_result(lvl):
    return -1


def heaviside(lmod, lvl):
    if lvl - lmod <= 0:
        return 0
    return 1


### setup curried functions
c_hf = {
    0: CurriedFunction(heaviside, 0),
    1: CurriedFunction(heaviside, 51),
    2: CurriedFunction(heaviside, 61),
    3: CurriedFunction(heaviside, 71),
    4: CurriedFunction(heaviside, 81),
    5: CurriedFunction(heaviside, 91)
}

c_xd = {
    # 100x  100
    # 100 (x - 1)
    0: CurriedFunction(_xp_diff_help, 100, 1, -1, 0),

    # prevouis + 200(x - 51)
    # 200 (x - 26)
    1: CurriedFunction(_xp_diff_help, 200, 1, -26, 0),
    # 300x - 10 300 = 100(3x - 103)
#    1: CurriedFunction(_xp_diff_help, 200, 1, -51),
#    1: CurriedFunction(_xp_diff_help, 100, 3, -103),
#    1: CurriedFunction(_xp_diff_help, 1, 100, -100, -50),

    # previous + 300(x - 61)
    # 100 (3x - 113)
    2: CurriedFunction(_xp_diff_help, 100, 3, -113, 0),
    # 600x - 28 600 = 200(3x - 143)
#    2: CurriedFunction(_xp_diff_help, 300, 1, -61),
#    2: CurriedFunction(_xp_diff_help, 200, 3, -143),
#    2: CurriedFunction(_xp_diff_help, 1, 100, -100, -60),

    # previous + 400(x - 71)
    # 400 (x - 46)
    3: CurriedFunction(_xp_diff_help, 400, 1, -46, 0),
    # 1000x - 57 000 = 1000(x - 57)
#    3: CurriedFunction(_xp_diff_help, 400, 1, -71),
#    3: CurriedFunction(_xp_diff_help, 1000, 1, -57),
#    3: CurriedFunction(_xp_diff_help, 1, 100, -100, -70),

    # previous + 500(x - 81)
    # 500 (x - 53)
    4: CurriedFunction(_xp_diff_help, 500, 1, -53, 0),
    # 1500x - 97 500 = 1500(x - 65)
#    4: CurriedFunction(_xp_diff_help, 500, 1, -81)
#    4: CurriedFunction(_xp_diff_help, 1500, 1, -65),
#    4: CurriedFunction(_xp_diff_help, 1, 100, -100, -80),

}

c_gx = {
    # 50x^2 - 50x
    # (50x)(x - 1)
    0: CurriedFunction(_get_xp_quadf, 1, 50, 0, 1, -1),

    # previous + 200(x- 26)
    # previous = 127500
    # 100(x^2 - 51x + 1275)
    1: CurriedFunction(_get_xp_quad, 100, 1, -51, 1275),
    # 150n^2 - 10150n + K (previous)
    # 150x^2 - 5150x
    # 50x(3x - 103)
#    1: CurriedFunction(_get_xp_help, 50, 3, -103, 0),
    # 150x^2 - 25450x
    # 50x(3x - 509)
#    1: CurriedFunction(_get_xp_help, 50, 3, -509, 0),

    # previous + 100 (3x - 133)
    # previous = 188500
    # 50(3x - 145)(n -26)
    2: CurriedFunction(_get_xp_quadf, 50, 3, -145, 1, -26),
    # 300n^2 - 28300n
    # 300x^2 - 8300x
    # 100x(3x - 83)
#    2: CurriedFunction(_get_xp_help, 50, 3, -83, 0),
    # 300x^2 - 64900x
    # 100x(3x - 649)
#    2: CurriedFunction(_get_xp_help, 100, 3, -649, 0),

    # previous + 400 (x - 46)
    # previous = 275000
    # 200(x^2 - 91x + 1375)
    3: CurriedFunction(_get_xp_quad, 200, 1, -91, 1375),
    # 500n^2 - 56500n
    # 500x^2 - 14500x
    # 500x(x - 29)
#    3: CurriedFunction(_get_xp_help, 500, 1, -29, 0),
    # 500x^2 - 127500x
    # 500x(x - 255)
#    3: CurriedFunction(_get_xp_help, 500, 1, -255, 0),

    # previous + 500 (x - 53)
    # previous = 397000
    # 250(x^2 - 105x + 1588)
    4: CurriedFunction(_get_xp_quad, 250, 1, -105, 1588),
    # 750n^2 - 96750n
    # 750x^2 - 24750x
    # 750x(x - 33)
#    4: CurriedFunction(_get_xp_help, 750, 1, -33, 0),
    # 750x^2 - 218250x
    # 750x(x - 291)
#    4: CurriedFunction(_get_xp_help, 750, 1, -291, 0)
    
}
