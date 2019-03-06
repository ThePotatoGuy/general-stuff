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


def get_level(xp):
    """
    Gets the current level based on total XP gained.

    The returned level includes a fractional (decimal) component that 
    roughly acts as percentage of xp until next level. This is **rough** 
    because some of the functions that calculate this are **non-linear**.

    IN:
        xp - user experience points

    RETURNS: level the user must have if they have the given XP.
    """
    return _applyfunc99(c_gl, xp, c_hfx)


def get_xp(lvl):
    """
    Gets the total amount of XP needed to reach a certain level. This means
    how much the user would have cumulative to reach a level, NOT how much
    more they need.

    IN:
        lvl - user level

    RETURNS: total xp the user must have to reach the given level.
    """
    return _applyfunc99(c_gx, lvl, c_hf)


def xp_diff(lvl):
    """
    Gets the amount of xp needed to reach the next level from the level.
    I.e: if this returns 5000 for level 51, then you need 5000 xp from
        level 51 to reach level 52.

    IN:
        lvl - user level

    RETURNS: xp needed to reach the next level (lvl + 1)
    """
    return _applyfunc99(c_xd, lvl, c_hf)


### Function helpers

def _cube(value):
    return value ** CUBE


def _lineform(ymul, ymod, ydiv, xp):
    # (my + ymod) / ydiv
    return ( (ymul * xp) + ymod ) / ydiv


def _quadform(radmod, amul, lmul, lmod, xpdiv, xp):
    # the negative Boy decided to go the RADical party and Be square, so 
    # he got 4 Asian Chicks. The party was all over at 2 Am.
    return (radmod + math.sqrt(abs(amul * (lmod + (lmul * xp))))) / xpdiv


def _cubeform_s(ymul, ydiv, xmod, aamul, amul, amod, pamul, z1mul, z1div, 
        z1cmul, z1cdiv, z2mul, z2div, z2cmul, z2cdiv, kcon, xp):
    # complicated. 
    a_var = ((ymul * xp) / ydiv) + xmod
    z_var = math.sqrt(abs(aamul * ( (amul * a_var * a_var) + amod))) + (pamul * a_var)
    return (
        (z1mul / z1div) * _cube( (z_var * z1cmul) / z1cdiv )
        + (z2mul / z2div) * _cube( z2cmul / (z_var * z2cdiv) )
        + kcon
    )


def _ymxb(amul, mmul, bmod, lmod, lvl):
    # A( m(x + l) + b)
    return amul * ( (mmul * (lvl + lmod)) + bmod)


def _constant(amt, lvl):
    # hard coded amount since some cases only have single value
    return amt


def _quad(amul, m2, m1, kcon, lvl):
    # A(x^2 + x + K)
    return amul * ( (m2 * lvl * lvl) + (m1 * lvl) + kcon)


def _quadfact(amul, m1, k1, m2, k2, lvl):
    # A(x + k1)(x + k2)
    return amul * ( (m1 * lvl) + k1) * ( (m2 * lvl) + k2)


def _quadfactK(amul, m1, k1, m2, k2, bigK, lvl):
    # K + A(x + k1)(x + k2)
    return bigK + _quadfact(amul, m1, k1, m2, k2, lvl)


def _quadfact_xf(amul, m1, m2, m2mod, kcon, lvl):
    # A( x(x + m) + K)
    return amul * ( (m1 * lvl) * ( (m2 * lvl) + m2mod ) + kcon )


def _cubicsimp(amul, bmul, cxmul, lxmul, lmod, kcon, lvl):
    # (A/B)( (x + m)^3 + b(x + m) + K)
    amt = lvl + lmod
    return (amul * ( (cxmul * amt * amt * amt) + (lxmul * amt) + kcon ) ) / bmul


def unitstep(lmod, lvl):
    return int((lvl - lmod) > 0)


def _unitstep_builder(db, piece, xvar, usdb):
    """
    Implements unit step function logic.
    AKA: calculate the vlaue, then subtract it by itself if its unitstep value
        says it should not exist

    IN:
        db - curried function database to use
        piece - piece to calculate
        xvar - xvar the var to pass into all functions
        usdb - unitstep databse to use
        
    RETURNS a positive value if xvar exists for this piece, 0 otherwise.
    """
    amt = db[piece](xvar)
    return (amt * usdb[piece](xvar)) - (amt * usdb[piece+1](xvar))


def _applyfunc99(db, xvar, usdb):
    """
    Runs unitstep builder for levels 99 and lower

    NOTE: not using looops so we avoid branching
    This is fine since we are never expecting this to change length.

    IN:
        db - curried function database to use
        xvar - xvar to pass into all functions
        usdb - unitstep database to use

    RETURNS: a result of running the unitstep functions
    """
    return (
        _unitstep_builder(db, 0, xvar, usdb)
        + _unitstep_builder(db, 1, xvar, usdb)
        + _unitstep_builder(db, 2, xvar, usdb)
        + _unitstep_builder(db, 3, xvar, usdb)
        + _unitstep_builder(db, 4, xvar, usdb)
        + _unitstep_builder(db, 5, xvar, usdb)
        + _unitstep_builder(db, 6, xvar, usdb)
        + _unitstep_builder(db, 7, xvar, usdb)
        + _unitstep_builder(db, 8, xvar, usdb)
    )


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
    7: CurriedFunction(unitstep, 661500),
    8: CurriedFunction(unitstep, 851500),
    9: CurriedFunction(unitstep, 1000000),
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
    # 100( x(x - 51) + 1275)
    1: CurriedFunction(_quadfact_xf, 100, 1, 1, -51, 1275),

    # previous + 100 (3x - 133)
    # previous = 188500
    # 50(3x^2 - 223x + 6210)
    # 50( x(3x - 223) + 6210)
    2: CurriedFunction(_quadfact_xf, 50, 1, 3, -223, 6210),

    # previous + 400 (x - 46)
    # previous = 275000
    # 200(x^2 - 91x + 2795)
    # 200( x(x - 91) + 2795)
    3: CurriedFunction(_quadfact_xf, 200, 1, 1, -91, 2795),

    # previous + 500 (x - 53)
    # previous = 397000
    # 250(x^2 - 105x + 3532)
    # 250( x(x - 105) + 3532)
    4: CurriedFunction(_quadfact_xf, 250, 1, 1, -105, 3532),

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

    # NOTE: from deriviation:
    # 631500 + 5000(x - 89)
    # 500(5x^2 - 84x - 35021)
    # NOTE: since we only have 1 constant here, we should get a linear function
    #   for this to make the next step way easier
    #   30000n + 631500
    #   1500(20x - 1459)
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

    # NOTE: from derivation
    # 851500 + 500(117x - 11286)
    # 250(117x^2 - 22455x + 1080328)
    # 250( 9x(13x - 2495) + 1080328)
    # NOTE: since we only have 1 constant here, we should get a linear func
    #   for this to make the next step way easier
    #   148500n + 851500
    #   500(297x - 27403)
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

    # NOTE: using derived formula
    # (420 + sqrt( x + 17686900)) /50
    # NOTE: using simple linear from before
    #   (y + 2188500) / 30000
    6: CurriedFunction(_lineform, 1, 2188500, 30000.0),

    # NOTE: this is a cubic root
    # x = (3y) / 500
    # a = x - 3789
    # z = sqrt(3 * (27a^2 + 1965200)) + 9a
    # (z/180)^(1/3) - 17 ( 20 / (3z) )^(1/3) + 94
    7: CurriedFunction(_cubeform_s, 3, 500.0, -3789, 3, 27, 1965200, 9, 1, 1,
        1, 180, -17, 1, 20, 3, 94
    ),

    # NOTE: using derived formula
    # (187125 + sqrt(130y - 94894375)) / 1950
    # (187125 + sqrt(5 (26y - 18 978 875)) / 1950
    # NOTE: using simple linear form
    #   (y + 13701500) / 148500
    8: CurriedFunction(_lineform, 1, 13701500, 148500.0),
}
