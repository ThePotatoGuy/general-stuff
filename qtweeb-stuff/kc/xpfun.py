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


def _quadform(lmul, lmod, radmod, xpdiv, xp):
    return (radmod + math.sqrt(abs(lmod + (lmul * xp)))) / xpdiv


def _get_level_piece(piece, start, end, xp):
    amt = c_gl[piece](xp)
    return (amt * c_hfx[start](xp)) - (amt * c_hfx[end](xp))


def get_level(xp):
    return (
        _get_level_piece(0, 0, 1, xp)
        + _get_level_piece(1, 1, 2, xp)
        + _get_level_piece(2, 2, 3, xp)
        + _get_level_piece(3, 3, 4, xp)
        + _get_level_piece(4, 4, 5, xp)
    )


def _xp_diff_start(lvl):
    return (lvl * 100) - 100

def _ymxb(amul, mmul, bmod, lmod, lvl):
    return amul * ( (mmul * (lvl + lmod)) + bmod)
#    return xp_diff(lmod) + (lmul * (lvl + lmod))

def _constant(amt, lvl):
    # hard coded amount since some cases only have single value
    return amt

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
        + _xp_diff_piece(5, 5, 6, lvl)
        + _xp_diff_piece(6, 6, 7, lvl)
        + _xp_diff_piece(7, 7, 8, lvl)
        + _xp_diff_piece(8, 8, 9, lvl)
    )


def _quad(amul, m2, m1, kcon, lvl):
    return amul * ( (m2 * lvl * lvl) + (m1 * lvl) + kcon)

def _quadfact(amul, m1, k1, m2, k2, lvl):
    return amul * ( (m1 * lvl) + k1) * ( (m2 * lvl) + k2)

def _quadfactK(amul, m1, k1, m2, k2, bigK, lvl):
    return bigK + _quadfact(amul, m1, k1, m2, k2, lvl)

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


def unitstep(lmod, lvl):
    return int((lvl - lmod) > 0)


### setup curried functions
c_hf = {
    # number should be level

    0: CurriedFunction(unitstep, 0),
    1: CurriedFunction(unitstep, 51),
    2: CurriedFunction(unitstep, 61),
    3: CurriedFunction(unitstep, 71),
    4: CurriedFunction(unitstep, 81),
    5: CurriedFunction(unitstep, 91),
    6: CurriedFunction(unitstep, 94),
    7: CurriedFunction(unitstep, 95),
    8: CurriedFunction(unitstep, 98),
    9: CurriedFunction(unitstep, 99),
}

c_hfx = {
    # number should be total xp at level

    0: CurriedFunction(unitstep, 0),
    1: CurriedFunction(unitstep, 127500),
    2: CurriedFunction(unitstep, 188500),
    3: CurriedFunction(unitstep, 275000),
    4: CurriedFunction(unitstep, 397000),
    5: CurriedFunction(unitstep, 564500),
}


c_xd = {
    # 100x  100
    # 100 (x - 1)
    0: CurriedFunction(_ymxb, 100, 1, -1, 0),

    # 5000 + 200(x - 51)
    # 200 (x - 26)
    1: CurriedFunction(_ymxb, 200, 1, -26, 0),

    # 7000 + 300(x - 61)
    # 100 (3x - 113)
    2: CurriedFunction(_ymxb, 100, 3, -113, 0),

    # 10000 + 400(x - 71)
    # 400 (x - 46)
    3: CurriedFunction(_ymxb, 400, 1, -46, 0),

    # 14000 + 500(x - 81)
    # 500 (x - 53)
    4: CurriedFunction(_ymxb, 500, 1, -53, 0),

    # 19000 + 500(x - 90)(x - 91)
    5: CurriedFunction(_quadfactK, 500, 1, -90, 1, -91, 19000),

    # 25000 + 5000(x - 94)
    # 5000 ( x - 89)
    # NOTE: only for 1 value
    6: CurriedFunction(_constant, 30000),

    # 30000 + 5000(x - 94)(x - 95)
    7: CurriedFunction(_quadfactK, 5000, 1, -94, 1, -95, 30000),

    # 90000 + 58500(x - 98)
    # 500(117x - 11286)
    # NOTE: only for 1 value
    8: CurriedFunction(_constant, 148500),

}

c_gx = {
    # 50x^2 - 50x
    # (50x)(x - 1)
    0: CurriedFunction(_quadfact, 1, 50, 0, 1, -1),

    # previous + 200(x- 26)
    # previous = 127500
    # 100(x^2 - 51x + 1275)
    1: CurriedFunction(_quad, 100, 1, -51, 1275),

    # previous + 100 (3x - 133)
    # previous = 188500
    # 50(3x^2 - 223x + 6210)
    2: CurriedFunction(_quad, 50, 3, -223, 6210),

    # previous + 400 (x - 46)
    # previous = 275000
    # 200(x^2 - 91x + 2795)
    3: CurriedFunction(_quad, 200, 1, -91, 2795),

    # previous + 500 (x - 53)
    # previous = 397000
    # 250(x^2 - 105x + 3532)
    4: CurriedFunction(_quad, 250, 1, -105, 3532),

    # 564500 + 19000 + 500(x - 90)(x - 91)
    # 500/3 ( (x - 90)^3 + 113(x - 90) + 3273)


    
}

c_gl = {
    # (5 + sqrt( 25 + 2y )) / 10
    0: CurriedFunction(_quadform, 2, 25, 5, 10),

    # (255 + sqrt( y - 62475)) / 10
    1: CurriedFunction(_quadform, 1, -62475, 255, 10),

    # (1115 + sqrt( 6y - 619775)) / 30
    2: CurriedFunction(_quadform, 6, -619775, 1115, 30),

    # (455 + sqrt( y/2 - 72475)) / 10
    3: CurriedFunction(_quadform, 1/2.0, -72475, 455, 10),

    # (525 + sqrt( 2y/5 - 77575)) / 10
    4: CurriedFunction(_quadform, 2/5.0, -77575, 525, 10),
}
