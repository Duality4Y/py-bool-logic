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
        self.signal = (0, 1)
        self.output = (1, 1)

    def setinput(self, signal):
        self.signal = signal
    """ nand based so set=setnot and reset is reset not."""
    def getoutput(self):
        a, b = self.signal
        q, qn = self.output
        q = Nor((qn, a))
        qn = Nor((q, b))
        q = Nor((qn, a))
        qn = Nor((q, b))
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
        self.output = self.latch.getoutput()
        return self.output


class DataLatch(object):
    """ implementation of a data latch """
    def __init__(self):
        self.signal = (0, 0)
        self.output = (1, 1)
        self.latch = Latch()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        data, enabled = self.signal
        r = Not(data)
        s = data
        signal = (r, s)
        self.latch.setinput(signal)
        self.output = self.latch.getoutput()
        return self.output


class GatedDataLatch(object):
    """ implementation of a Gated Data latch """
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
        self.output = self.gatedlatch.getoutput()
        return self.output


class MSDataLatch(object):
    """ implemenation of a master slave data latch """
    def __init__(self):
        self.signal = (0, 0)
        self.output = []
        self.master = GatedDataLatch()
        self.slave = GatedDataLatch()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        data, clock = self.signal
        self.master.setinput(self.signal)
        data, qn = self.master.getoutput()
        clock = Not(clock)
        signal = (data, clock)
        self.slave.setinput(signal)
        self.output = self.slave.getoutput()
        return self.output


class JKFlipFlop(object):
    """
    implementation of a j-k flipflop.
    url: "https://electrosome.com/wp-content/uploads/2013/05/
          JK-Flip-Flop-using-D-Flip-Flop-Logic-Diagram.jpg"
    """
    def __init__(self):
        self.signal = (0, 0)
        self.output = (1, 1)
        self.flipflop = MSDataLatch()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        j, k, clock = self.signal
        q, qn = self.output
        k = Not(k)
        orA = And((j, qn))
        orB = And((k, q))
        d = Or((orA, orB))
        signal = (d, clock)
        self.flipflop.setinput(signal)
        self.output = self.flipflop.getoutput()
        return tuple(self.output)


class TFlipFlop(object):
    """
    implemenation of a toggle flipflop based on
    a j-k flipflop
    """
    def __init__(self):
        self.signal = (0, 0)
        self.output = (1, 1)
        self.flipflop = JKFlipFlop()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        t, clock = self.signal
        signal = (t, t, clock)
        self.flipflop.setinput(signal)
        self.output = self.flipflop.getoutput()
        return tuple(self.output)


class Counter(object):
    """
    implementation of a counter with toggle flipflops
    """
    def __init__(self, length=4):
        self.signal = (0, 0)
        self.output = []
        self.flipflops = []
        self.length = length
        for i in range(0, self.length):
            self.flipflops.append(TFlipFlop())

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        self.output = []
        clock, enabled = self.signal

        for flipflop in self.flipflops:
            signal = (enabled, clock)
            flipflop.setinput(signal)
            q, qn = flipflop.getoutput()
            clock = qn
            # replace qn with q for backward counting.
            self.output.append(qn)

        return tuple(self.output)


class PiPoRegister(object):
    """
    8 bit paralel in paralel out register.
    with optional register length select.
    """
    def __init__(self, length=8):
        self.length = length
        self.signal = ()
        self.output = []

        self.latches = []
        for i in range(0, self.length):
            self.latches.append(GatedDataLatch())

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        output = []
        data, enabled = self.signal

        for i, latch in enumerate(self.latches):
            latch.setinput((data[i], enabled))
            # get the Q bit
            output.append(latch.getoutput()[0])
        self.output = output
        return tuple(self.output)


class SiPoRegister(object):
    """
    implementation of a serial in paralel out register.
    """
    def __init__(self, length=4):
        self.length = length
        self.signal = ()
        self.output = []

        self.latch1 = MSDataLatch()
        self.latch2 = MSDataLatch()
        self.latch3 = MSDataLatch()
        self.latch4 = MSDataLatch()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        output = []
        data, clock = self.signal

        self.latch1.setinput(self.signal)
        q, qn = self.latch1.getoutput()
        output.append(q)
        self.latch2.setinput((q, clock))
        q, qn = self.latch2.getoutput()
        output.append(q)
        self.latch3.setinput((q, clock))
        q, qn = self.latch3.getoutput()
        output.append(q)
        self.latch4.setinput((q, clock))
        q, qn = self.latch4.getoutput()
        output.append(q)

        return tuple(output)


class OneBitDigComp(object):
    """
    implemenatation of a 1 bit magnitude comparator.
    """
    def __init__(self):
        self.signal = (0, 0)
        self.output = []

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        a, b = self.signal
        c = And((Not(a), b))
        d = Not(Or((And((Not(a), b)), And((a, Not(b))))))
        e = And((a, Not(b)))
        self.output = (c, d, e)
        return tuple(self.output)


class CascadeBitDigComp(object):
    """
    implementation of a x bit cascadeable
    digital magnitude comparator.
    """
    def __init__(self):
        pass

    def setinput(self):
        pass

    def getoutput(self):
        pass


class OneBitEquComp(object):
    """
    implementation of a cascadable 1 bit equ comparator.
    http://web.stcloudstate.edu/pkjha/CSCI220/MagnitudeComparator.pdf
    """
    def __init__(self):
        self.signal = ()
        self.output = ()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        Ai, Bi, Ei = self.signal
        signal = (Ai, Bi)
        A = Xnor(signal)
        B = Ei
        signal = (A, B)
        out = And(signal)
        self.output = out
        return self.output
