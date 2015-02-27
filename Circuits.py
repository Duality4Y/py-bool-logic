from baseLogic import *


class HalfAddr(object):
    def __init__(self):
        self.input = (0, 0)

    def setinput(self, input):
        self.input = input

    def getoutput(self):
        sum = Xor(self.input)
        cout = And(self.input)
        return(cout, sum)


class FullAddr(object):
    def __init__(self):
        # the circuit has a cin A and B
        # thus three input.s
        self.input = (0, 0, 0)
        self.h1 = HalfAddr()
        self.h2 = HalfAddr()

    def setinput(self, input):
        self.input = input

    def getoutput(self):
        a, b, cin = self.input

        self.h1.setinput((a, b))
        carryh1, sumh1 = self.h1.getoutput()

        self.h2.setinput((sumh1, cin))
        carryh2, sumh2 = self.h2.getoutput()

        sum = Or((carryh1, carryh2))
        cout = sumh2

        return(cout, sum)


class FourBitAddr(object):
    def __init__(self):
        self.inputa = 0
        self.inputb = 0
        self.cin = 0

        self.addrs = []
        for i in range(0, 4):
            self.addrs.append(FullAddr())

    def setinput(self, inputa, inputb, cin):
        self.inputa = inputa
        self.inputb = inputb
        self.cin = cin

    def getoutput(self):
        sums = [0]
        carry = self.cin
        for i, addr in enumerate(self.addrs):
            signal = (self.inputa[i], self.inputb[i], carry)
            addr.setinput(signal)
            carry, sum = addr.getoutput()
            sums.append(sum)
        sums[0] = carry
        return tuple(sums)
