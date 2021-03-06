from baseLogic import Not, And, Or, Nor, Xor, Nand
from LogicUtils import appendTuple


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
        d = Xor((a, b))
        b = And((Not(a), b))
        return (b, d)


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
    """ implemenation of a master slave data flipflop """
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

DataFlipFlop = MSDataLatch


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
        ora = And((j, qn))
        orb = And((k, q))
        signal = (ora, orb)
        d = Or(signal)
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
            self.latches.append(DataFlipFlop())

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


class XBitPiPoRegister(PiPoRegister):
    """
    variable length pipo register.
    """
    def __init__(self, length=8):
        PiPoRegister.__init__(self, length)

    def setinput(self, signal):
        PiPoRegister.setinput(self, signal)

    def getoutput(self):
        return PiPoRegister.getoutput(self)


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

        self.output = output
        return tuple(self.output)


class XBitSiPoRegister(object):
    """
    implementation of a serial in paralel out register.
    with variable bit length
    """
    def __init__(self, length=4):
        self.length = length
        self.signal = ()
        self.output = ()

        self.flipflops = []
        for i in range(0, length):
            self.flipflops.append(MSDataLatch())

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        output = []
        data, clock = self.signal

        for flipflop in self.flipflops:
            signal = (data, clock)
            flipflop.setinput(signal)
            data, qn = flipflop.getoutput()
            output.append(data)

        self.output = tuple(output)
        return self.output


class OneBitMagnitudeComparator(object):
    """
    1 bit magnitude comparator.
    """
    def __init__(self):
        self.signal = ()
        self.output = ()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        Ai, Bi = self.signal
        ab = And((Ai, Not(Bi)))
        ba = And((Not(Ai), Bi))
        signal = (ab, ba)
        aisb = Nor(signal)
        self.output = (ab, aisb, ba)
        return self.output


class CascadeOneBitMagnitudeComparator(object):
    """
    cascadable 1 bit magnitude comparator.
    """
    def __init__(self):
        self.signal = ()
        self.output = ()
        self.comparator = OneBitMagnitudeComparator()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        Ai, Bi, Gi, Ei, Li = self.signal
        signal = (Ai, Bi)
        self.comparator.setinput(signal)
        g, e, l = self.comparator.getoutput()

        go = Or((And((Gi, e)), g))
        lo = Or((And((Li, e)), l))
        eo = And((e, Ei))

        self.output = (go, eo, lo)
        return self.output


class FourBitMagnitudeComparator(object):
    """
    4 bit magnitude comparator.
    """
    def __init__(self):
        self.Ai = ()
        self.Bi = ()
        self.previous = ()
        self.output = ()
        self.comp1 = CascadeOneBitMagnitudeComparator()
        self.comp2 = CascadeOneBitMagnitudeComparator()
        self.comp3 = CascadeOneBitMagnitudeComparator()
        self.comp4 = CascadeOneBitMagnitudeComparator()

    def setinput(self, ai, bi, previous):
        self.Ai = ai
        self.Bi = bi
        self.previous = previous

    def getoutput(self):
        ai = self.Ai
        bi = self.Bi

        Gi, Ei, Li = self.previous
        previous = (Gi, Not(Ei), Li)

        signal = (appendTuple((ai[0], bi[0]), previous))
        self.comp1.setinput(signal)
        previous = self.comp1.getoutput()

        signal = (appendTuple((ai[1], bi[1]), previous))
        self.comp2.setinput(signal)
        previous = self.comp2.getoutput()

        signal = (appendTuple((ai[2], bi[2]), previous))
        self.comp3.setinput(signal)
        previous = self.comp3.getoutput()

        signal = (appendTuple((ai[3], bi[3]), previous))
        self.comp4.setinput(signal)
        output = self.comp4.getoutput()
        self.output = output
        return self.output


class Encoder4to2(object):
    """
    4 to 2 encoder
    """
    def __init__(self):
        self.signal = ()
        self.output = ()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        signal = self.signal
        xout = Or((signal[1], signal[3]))
        yout = Or((signal[2], signal[3]))
        self.output = (xout, yout)
        return self.output


class Encoder8to3(object):
    """
    8 to 3 encoder
    """
    def __init__(self):
        self.signal = ()
        self.output = ()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        signal = self.signal
        xout = Or((signal[1], signal[3], signal[5], signal[7]))
        yout = Or((signal[2], signal[3], signal[6], signal[7]))
        zout = Or((signal[4], signal[5], signal[6], signal[7]))
        self.output = (xout, yout, zout)
        return self.output


class Encoder(object):
    """
    implementation based on the 74xx148
    8 to 3 encoder with cascade inputs.
    """
    def __init__(self):
        self.signal = ()
        self.output = ()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        ei, d0, d1, d2, d3, d4, d5, d6, d7 = self.signal
        output = []

        signal = (d0, d1, d2, d3, d4, d5, d6, d7, Not(ei))
        eo = Nand(signal)
        signal = (Not(eo), ei)
        g5 = Or(signal)

        # doing the inputs for A0
        signal = (Not(d1), d2, d4, d6, Not(ei))
        a = And(signal)
        signal = (Not(d3), d4, d6, Not(ei))
        b = And(signal)
        signal = (Not(d5), d6, Not(ei))
        c = And(signal)
        signal = (Not(d7), Not(ei))
        d = And(signal)

        signal = (a, b, c, d)
        a0 = Nor(signal)

        # doing the inputs for A1
        signal = (Not(d2), d4, d5, Not(ei))
        a = And(signal)
        signal = (Not(d3), d4, d2, Not(ei))
        b = And(signal)
        signal = (Not(d6), Not(ei))
        c = And(signal)
        signal = (Not(d7), Not(ei))
        d = And(signal)

        signal = (a, b, c, d)
        a1 = Nor(signal)

        # doint the inputs for A2
        signal = (Not(d4), Not(ei))
        a = And(signal)
        signal = (Not(d5), Not(ei))
        b = And(signal)
        signal = (Not(d6), Not(ei))
        c = And(signal)
        signal = (Not(d7), Not(ei))
        d = And(signal)

        signal = (a, b, c, d)
        a2 = Nor(signal)

        output = (a0, a1, a2, g5, eo)
        self.output = output
        return self.output


class Decoder2to4(object):
    """
    2 to 4 decoder
    """
    def __init__(self):
        self.signal = ()
        self.output = ()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        a, b, Enable = self.signal
        output = []

        signal = (Not(a), Not(b), Enable)
        d0 = And(signal)
        output.append(d0)

        signal = (a, Not(b), Enable)
        d1 = And(signal)
        output.append(d1)

        signal = (Not(a), b, Enable)
        d2 = And(signal)
        output.append(d2)

        signal = (a, b, Enable)
        d3 = And(signal)
        output.append(d3)

        self.output = tuple(output)
        return self.output


class Decoder3to8(object):
    """
    3 to 8 decoder
    """
    def __init__(self):
        self.signal = ()
        self.output = ()
        self.decoder1 = Decoder2to4()
        self.decoder2 = Decoder2to4()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        a, b, ca, Enable = self.signal
        output = []

        # last one first because of order enabled.
        signal = (a, b, Not(ca))
        self.decoder2.setinput(signal)
        output += self.decoder2.getoutput()

        signal = (a, b, ca)
        self.decoder1.setinput(signal)
        output += self.decoder1.getoutput()

        # output if enabled
        for i, bit in enumerate(output):
            output[i] = And((bit, Enable))
        self.output = tuple(output)

        return(self.output)


class Decoder4to16(object):
    """
    4 to 16 decoder
    """
    def __init__(self):
        self.signal = ()
        self.output = ()
        self.length = 4
        self.selector = Decoder2to4()
        self.decoders = {}
        for i in range(0, self.length):
            self.decoders[i] = Decoder2to4()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        a, b, c, d, Enable = self.signal
        output = []

        # C, D input select the decoder.
        signal = (c, d, Enable)
        self.selector.setinput(signal)
        selected = self.selector.getoutput()

        for decoder in self.decoders:
            signal = (a, b, selected[decoder])
            self.decoders[decoder].setinput(signal)
            output += self.decoders[decoder].getoutput()

        self.output = tuple(output)
        return self.output


class Decoder5to32(object):
    """
    5 to 32 decoder
    """
    def __init__(self):
        self.signal = ()
        self.output = ()
        self.length = 8
        self.selector = Decoder3to8()
        self.decoders = {}
        for i in range(0, self.length):
            self.decoders[i] = Decoder2to4()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        a, b, c, d, e, Enable = self.signal
        output = []

        # C, D, E input select decoder
        signal = (c, d, e, Enable)
        self.selector.setinput(signal)
        selected = self.selector.getoutput()

        for decoder in self.decoders:
            signal = (a, b, selected[decoder])
            self.decoders[decoder].setinput(signal)
            output += self.decoders[decoder].getoutput()

        self.output = tuple(output)
        return self.output


class Decoder6to64(object):
    """
    6 to 64 decoder
    """
    def __init__(self):
        self.signal = ()
        self.output = ()
        self.length = 16
        self.selector = Decoder4to16()
        self.decoders = {}
        for i in range(0, self.length):
            self.decoders[i] = Decoder2to4()

    def setinput(self, signal):
        self.signal = signal

    def getoutput(self):
        a, b, c, d, e, f, Enable = self.signal
        output = []

        # C, D, E, F input select decoder
        signal = (c, d, e, f, Enable)
        self.selector.setinput(signal)
        selected = self.selector.getoutput()

        for decoder in self.decoders:
            signal = (a, b, selected[decoder])
            self.decoders[decoder].setinput(signal)
            output += self.decoders[decoder].getoutput()

        self.output = tuple(output)
        return self.output
