"""
    this file implements basic logic operations.
"""


def Not(signal):
    """ return the logic negation of signal """
    return (1-signal)


def Or(signal):
    """ return signal allinputs orred. """
    output = 0
    for bit in signal:
        output |= bit
    return (output)


def And(signal):
    """ return signal (A and B) """
    output = 1
    for bit in signal:
        output &= bit
    return (output)


def Xor(signal):
    """ return signal (A xor B) """
    output = 0
    for bit in signal:
        left = And((output, Not(bit)))
        right = And((Not(output), bit))
        output = Or((left, right))
    return (output)


def Nand(signal):
    """ return negated And """
    return Not(And(signal))


def Nor(signal):
    """ return negated Or """
    return Not(Or(signal))


def Xnor(signal):
    """ return signal !(A xor B) (inclusive or) """
    return Not(Xor(signal))
