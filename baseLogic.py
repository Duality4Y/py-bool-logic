"""
    this file implements basic logic operations.
"""


def Not(signal):
    """ return the logic negation of signal """
    return (1-signal)


def Or(signal):
    """ return signal (A or B) """
    return (signal[0] | signal[1])


def And(signal):
    """ return signal (A and B) """
    return (signal[0] & signal[1])


def Xor(signal):
    """ return signal (A xor B) """
    a, b = signal
    left = And((a, Not(b)))
    right = And((b, Not(a)))
    result = Or((left, right))
    return (result)


def Nand(signal):
    """ return negated And """
    return Not(And(signal))


def Nor(signal):
    """ return negated Or """
    return Not(Or(signal))


def Ior(signal):
    """ return signal !(A xor B) (inclusive or) """
    return Not(Xor(signal))
