import math

CUBE = (1.0 / 3.0)
# cube root

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


def _quadform(radmod, amul, lmul, lmod, xpdiv, xp):
    return (radmod + math.sqrt(abs(amul * (lmod + (lmul * xp))))) / xpdiv


def _cubeform_s(ymul, ydiv, xmod, aamul, amul, amod, pamul, z1mul, z1div, 
        z1cmul, z1cdiv, z2mul, z2div, z2cmul, z2cdiv, kcon, xp):
    a_var = ((ymul * xp) / ydiv) + xmod
    z_var = math.sqrt(abs(aamul * ( (amul * a_var * a_var) + amod))) + (pamul * a_var)
    return (
        (z1mul / z1div) * ( ( (z_var * z1cmul) / z1cdiv) ** CUBE)
        + (z2mul / z2div) * ( ( z2cmul / (z_var * z2cdiv)) ** CUBE)
        + kcon
    )


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
        + _get_level_piece(5, 5, 6, xp)
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

def _cubicsimp(amul, bmul, cxmul, lxmul, lmod, kcon, lvl):
    amt = lvl + lmod
    return (amul * ( (cxmul * amt * amt * amt) + (lxmul * amt) + kcon ) ) / bmul

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
        + _get_xp_piece(5, 5, 6, lvl)
        + _get_xp_piece(6, 6, 7, lvl)
        + _get_xp_piece(7, 7, 8, lvl)
        + _get_xp_piece(8, 8, 9, lvl)

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
    6: CurriedFunction(unitstep, 631500),
}


# difference in xp for each level 
# AKA: how much xp needed to gain to reach next level
# This is our base function, since it can be easily modeled as linaer or
# quadratic
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

    # 1000(x - 91) -- diff formula
    # 19000 + 500(x - 90)(x - 91)
    5: CurriedFunction(_quadfactK, 500, 1, -90, 1, -91, 19000),

    # 25000 + 5000(x - 94)
    # 5000 ( x - 89)
    # NOTE: only for 1 value
    6: CurriedFunction(_constant, 30000),

    # 10000(x - 95) -- diff formula
    # 30000 + 5000(x - 94)(x - 95)
    7: CurriedFunction(_quadfactK, 5000, 1, -94, 1, -95, 30000),

    # 90000 + 58500(x - 98)
    # 500(117x - 11286)
    # NOTE: only for 1 value
    8: CurriedFunction(_constant, 148500),

}

# total xp gained to reach a certain level
# this is basically how much xp you should have at minmum for a level
# To get this, do a summation on the xp diff formulas using the
# partial sum / natural numbers sum function
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

    # 564500 + (double summation of diff formula using substitution)
    # NOTE: we are starting with the growth of diff instead of diff itself,
    #   which is why we need double summation
    # n = x - 91
    # K = 19000 (add to first summation)
    #
    # 1: 1000n 
    #
    # 2: 500n^2 + 500n + 19000 
    #   with sub: (500/3)(x - 91)(x^2 - 179x + 8124)
    #
    # Then add 564500 and simplify:
    # 3: (1/3)(500n^3 + 1500n + 58000n + 1693500)
    #   (500/3)(n^3 + 3n^2 + 116n + 3387)
    #   (500/3)(x^3 - 270x^2 + 24413x - 735897)
    #
    # 500/3 ( (x - 90)^3 + 113(x - 90) + 3273)
    5: CurriedFunction(_cubicsimp, 500, 3, 1, 113, -90, 3273),

    # 631500 + 5000(x - 89)
    # 500(5x^2 - 885x + 40273)
    # NOTE: only for 1 value
    6: CurriedFunction(_constant, 661500),

    # 661500 + (double summation of diff formula using sub)
    # n = x - 95
    # K = 30000 (add to first summation)
    #
    # 1: 10000n 
    # 2: 5000n^2 + 5000n + 30000 
    #   with sub: (5000/3)(x - 95)(x^2 - 187x + 8760)
    #
    # then add 661500 and simplify
    # 3: (1/3)(5000n^3 + 15000n^2 + 100000n + 1984500)
    #
    # (500/3)(10(x - 94)^3 + 170(x - 94) + 3789
    7: CurriedFunction(_cubicsimp, 500, 3, 10, 170, -94, 3789),

    # 851500 + 500(117x - 11286)
    # 250(117x^2 - 22455x + 1080328)
    # 250( 9x(13x - 2495) + 1080328)
    # NOTE: only for 1 value
    8: CurriedFunction(_constant, 1000000),

    
}

# current level based on xp.
# to get this, inverse the get_xp functions.
# This is very hard to do.
# For quadratics, its a matter of using substitution:
#   1. move the constant and factors over to the other side (where y is)
#   2. substitute that with Z (a variable)
#   3. move that Z over to the other side again, and use quadratic formula
#   4. Replace Z in the quadratic formula with the substitution
#   5. simplify
#
# For cubics, use the "cubic formula" to 
# help solve. By default, wolfram alpha puts cubic functions in
# the cubic formula -> x^3 + Ax = B
# NOTE: actually, just using wolfram to get inverse. Then we take that and
#   simplify down to a standard set that limits the number of weird math 
#   equations
c_gl = {
    # (5 + sqrt( 2y + 25 )) / 10
    0: CurriedFunction(_quadform, 5, 1, 2, 25, 10),

    # (255 + sqrt( y - 62475)) / 10
    1: CurriedFunction(_quadform, 255, 1, 1, -62475, 10),

    # (1115 + sqrt( 6y - 619775)) / 30
    2: CurriedFunction(_quadform, 1115, 1, 6,  -619775, 30),

    # (455 + sqrt( y/2 - 72475)) / 10
    # (910 + sqrt( 2 (y - 144950) )) / 20
    3: CurriedFunction(_quadform, 910, 2, 1, -144950, 20),

    # (525 + sqrt( 2y/5 - 77575)) / 10
    # (2625 + sqrt( 5 (2y - 387875) )) / 50
    4: CurriedFunction(_quadform, 2625, 5, 2, -387875, 50),

    # NOTE: this is a cubic root
    # x = (3 * y) / 500
    # a = x - 3273
    # z = sqrt(3 * (27a^2 + 5771588)) + 9a
    # (z/18)^(1/3) - 113 ( 2 / (3z) )^(1/3) + 90
    5: CurriedFunction(_cubeform_s, 3, 500.0, -3273, 3, 27, 5771588, 9, 1, 1, 
        1, 18, -113, 1, 2, 3, 90
    ),

    # test

    # NOTE: this is a cubic root

    # last
}
