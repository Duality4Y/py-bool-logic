from baseLogic import *


class HalfAddr(object):
    def __init__(self):
        self.signal = (0, 0)

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        sum = Xor(self.signal)
        cout = And(self.signal)
        return(cout, sum)


class FullAddr(object):
    def __init__(self):
        # the circuit has a cin A and B
        # thus three input.s
        self.signal = (0, 0, 0)
        self.h1 = HalfAddr()
        self.h2 = HalfAddr()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        a, b, cin = self.signal

        self.h1.setinput((a, b))
        carryh1, sumh1 = self.h1.getoutput()

        self.h2.setinput((sumh1, cin))
        carryh2, sumh2 = self.h2.getoutput()

        sum = Or((carryh1, carryh2))
        cout = sumh2

        return(cout, sum)


class XBitAddr(object):
    def __init__(self, bits):
        self.inputa = 0
        self.inputb = 0
        self.cin = 0

        self.addrs = []
        for i in range(bits):
            self.addrs.append(FullAddr())

    def setinput(self, inputa, inputb, cin):
        self.inputa = inputa
        self.inputb = inputb
        self.cin = cin

    def getoutput(self):
        sums = []
        carry = self.cin

        for i, addr in enumerate(self.addrs):
            signal = (self.inputa[i], self.inputb[i], carry)
            addr.setinput(signal)
            sum, carry = addr.getoutput()
            sums.append(sum)
        sums.append(carry)

        return tuple(sums)


class FourBitAddr(object):
    def __init__(self):
        self.inputa = 0
        self.inputb = 0
        self.cin = 0

        self.addr1 = FullAddr()
        self.addr2 = FullAddr()
        self.addr3 = FullAddr()
        self.addr4 = FullAddr()

    def setinput(self, inputa, inputb, cin):
        self.inputa = inputa
        self.inputb = inputb
        self.cin = cin

    def getoutput(self):
        sums = []
        carry = self.cin

        addr1, addr2, addr3, addr4 = (self.addr1, self.addr2,
                                      self.addr3, self.addr4)

        signal = (self.inputa[0], self.inputb[0], carry)
        self.addr1.setinput(signal)
        sum, carry = addr1.getoutput()
        sums.append(sum)

        signal = (self.inputa[1], self.inputb[1], carry)
        self.addr2.setinput(signal)
        sum, carry = addr2.getoutput()
        sums.append(sum)

        signal = (self.inputa[2], self.inputb[2], carry)
        self.addr3.setinput(signal)
        sum, carry = addr3.getoutput()
        sums.append(sum)

        signal = (self.inputa[3], self.inputb[3], carry)
        self.addr4.setinput(signal)
        sum, carry = addr4.getoutput()
        sums.append(sum)
        sums.append(carry)
        return tuple(sums)


class Latch(object):
    """implementation of sr latch"""
    def __init__(self):
        self.signal = (0, 0)
        self.output = (1, 1)

    def setinput(self, signal):
        self.signal = signal
    """ nand based so set=setnot and reset is reset not."""
    def getoutput(self):
        a, b = self.signal
        q, qn = self.output
        qn = Nor((q, b))
        q = Nor((qn, a))
        qn = Nor((q, b))
        q = Nor((qn, a))
        self.output = (q, qn)
        return(self.output)


class GatedLatch(object):
    """ implementation of a Gated sr latch """
    def __init__(self):
        self.signal = (0, 0, 0)
        self.output = (1, 1)
        self.latch = Latch()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        r, s, e = self.signal
        a = And((r, e))
        b = And((s, e))
        self.latch.setinput((a, b))
        return self.latch.getoutput()


class DataLatch(object):
    """ implementation of a Data latch """
    def __init__(self):
        self.signal = (0, 0)
        self.output = (1, 1)
        self.gatedlatch = GatedLatch()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        data, enabled = self.signal
        r = Not(data)
        s = data
        self.gatedlatch.setinput((r, s, enabled))
        return self.gatedlatch.getoutput()

