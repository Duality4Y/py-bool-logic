from baseLogic import *
from LogicUtils import *


class HalfAdder(object):
    def __init__(self):
        self.signal = (0, 0)

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        sum = Xor(self.signal)
        cout = And(self.signal)
        return(cout, sum)


class HalfSubtractor(object):
    """
    Subtractor series based on:
    http://www.vidyarthiplus.in/2012/01/digital-logic-circuitshalf-and-full.html#.VP9lI59jPJ8
    """
    def __init__(self):
        self.signal = ()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        # Bwi borrow in.
        a, b = self.signal
        D = Xor((a, b))
        B = And((Not(a), b))
        return (B, D)


class FullAdder(object):
    def __init__(self):
        # the circuit has a cin A and B
        # thus three input.s
        self.signal = (0, 0, 0)
        self.h1 = HalfAdder()
        self.h2 = HalfAdder()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        a, b, cin = self.signal
        sp = Xor((a, b))
        sum = Xor((sp, cin))
        cp1 = And((a, b))
        cp2 = And((sp, cin))
        cout = Or((cp1, cp2))

        return (cout, sum)


class FullSubtractor(object):
    def __init__(self):
        self.signal = (0, 0, 0)
        self.sub1 = HalfSubtractor()
        self.sub2 = HalfSubtractor()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        a, b, bwin = self.signal
        d = Xor((Xor((a, b)), bwin))
        bpa = And((bwin, b))
        bpb = And((b, Not(a)))
        bpc = And((bwin, Not(a)))
        bout = Or((Or((bpa, bpb)), bpc))
        return(bout, d)


class FourBitSubtractor(object):
    def __init__(self):
        self.inputa = 0
        self.inputb = 0
        self.Bin = 0
        self.sub1 = FullSubtractor()
        self.sub2 = FullSubtractor()
        self.sub3 = FullSubtractor()
        self.sub4 = FullSubtractor()

    def setinput(self, a, b, bwin):
        self.inputa = a
        self.inputb = b
        self.bwin = bwin

    def getoutput(self):
        sub1, sub2, sub3, sub4 = self.sub1, self.sub2, self.sub3, self.sub4
        sums = []
        a, b = self.inputa, self.inputb

        signal = (a[0], b[0], self.bwin)
        sub1.setinput(signal)
        bwin, sum = sub1.getoutput()
        sums.append(sum)

        signal = (a[1], b[1], bwin)
        sub2.setinput(signal)
        bwin, sum = sub2.getoutput()
        sums.append(sum)

        signal = (a[2], b[2], bwin)
        sub3.setinput(signal)
        bwin, sum = sub3.getoutput()
        sums.append(sum)

        signal = (a[3], b[3], bwin)
        sub4.setinput(signal)
        bwin, sum = sub4.getoutput()
        sums.append(sum)

        output = tuple(sums)
        return(output, bwin,)


class XBitSubtractor(object):
    def __init__(self, bits):
        self.inputa = 0
        self.inputb = 0
        self.bin = 0
        self.length = bits
        self.subtractors = []
        for i in range(bits):
            self.subtractors.append(FullSubtractor())

    def setinput(self, inputa, inputb, bin):
        self.inputa = inputa
        self.inputb = inputb
        self.bin = bin

    def getoutput(self):
        sums = []
        borrow = self.bin

        for i, subtractor in enumerate(self.subtractors):
            signal = (self.inputa[i], self.inputb[i], borrow)
            subtractor.setinput(signal)
            borrow, sum = subtractor.getoutput()
            sums.append(sum)

        return tuple(sums), borrow


class XBitAdder(object):
    def __init__(self, bits):
        self.inputa = 0
        self.inputb = 0
        self.cin = 0
        self.length = bits

        self.adders = []
        for i in range(bits):
            self.adders.append(FullAdder())

    def setinput(self, inputa, inputb, cin):
        self.inputa = inputa
        self.inputb = inputb
        self.cin = cin

    def getoutput(self):
        sums = []
        carry = self.cin

        for i, adder in enumerate(self.adders):
            signal = (self.inputa[i], self.inputb[i], carry)
            adder.setinput(signal)
            carry, sum = adder.getoutput()
            sums.append(sum)

        return tuple(sums), carry


class FourBitAdder(object):
    def __init__(self):
        self.inputa = 0
        self.inputb = 0
        self.cin = 0

        self.adder1 = FullAdder()
        self.adder2 = FullAdder()
        self.adder3 = FullAdder()
        self.adder4 = FullAdder()

    def setinput(self, inputa, inputb, cin):
        self.inputa = inputa
        self.inputb = inputb
        self.cin = cin

    def getoutput(self):
        sums = []

        adder1, adder2, adder3, adder4 = (self.adder1, self.adder2,
                                          self.adder3, self.adder4)
        self.inputa = list(self.inputa)
        for i, bit in enumerate(self.inputa):
            self.inputa[i] = Xor((bit, self.cin))

        signal = (self.inputa[0], self.inputb[0], self.cin)
        self.adder1.setinput(signal)
        carry, sum = adder1.getoutput()
        sums.append(sum)

        signal = (self.inputa[1], self.inputb[1], carry)
        self.adder2.setinput(signal)
        carry, sum = adder2.getoutput()
        sums.append(sum)

        signal = (self.inputa[2], self.inputb[2], carry)
        self.adder3.setinput(signal)
        carry, sum = adder3.getoutput()
        sums.append(sum)

        signal = (self.inputa[3], self.inputb[3], carry)
        self.adder4.setinput(signal)
        carry, sum = adder4.getoutput()
        sums.append(sum)

        output = tuple(sums)
        return(output, carry,)


class Latch(object):
    """implementation of sr latch"""
    def __init__(self):
        self.signal = (0, 1)
        self.output = (1, 1)

    def setinput(self, signal):
        self.signal = signal
    """ Or based so 1 for set and 1 for reset. """
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


class FourBitEquComp(object):
    """
    implementation of a 4 bit equality comparator.
    """
    def __init__(self):
        self.signal = ()
        self.output = ()

        self.length = 4
        self.comparators = []
        for i in range(0, self.length):
            self.comparators.append(OneBitEquComp())

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        A, B, Ei = self.signal
        for i, comparator in enumerate(self.comparators):
            signal = (A[i], B[i], Ei)
            comparator.setinput(signal)
            Ei = comparator.getoutput()
        self.output = Ei
        return self.output


"""
implementation of cascadable magnitude comparator logic.
"""


class EquComparator(object):
    """
    1 bit cascadable equality comparator.
    """
    def __init__(self):
        self.signal = ()
        self.output = ()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        Ai, Bi, Gi = self.signal
        A = And((Ai, Not(Bi)))
        B = And((Ai, Gi))
        C = And((Bi, Not(Gi)))
        AB = Or((A, B))
        output = Or((AB, C))
        self.output = output
        return (self.output)
