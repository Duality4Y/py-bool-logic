
import baseLogic as logic
from LogicUtils import itot
from LogicUtils import ttoi
from LogicUtils import getRandomInts
from LogicUtils import invertTuple
from LogicUtils import states


def checkNot(logic):
    state1 = logic(0)
    state2 = logic(1)
    print("0 : %d" % (state1))
    print("1 : %d" % (state2))
    print("")


def tableCheck(gate):
    # table to check against two input signal.
    table = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for state in table:
        state1, state2 = state
        output = gate(state)
        print("%d %d : %d" % (state1, state2, output))
    print("")


def printTestLogic():
    print("Not:")
    checkNot(logic.Not)
    print("Or: ")
    tableCheck(logic.Or)
    print("And: ")
    tableCheck(logic.And)
    print("Xor: ")
    tableCheck(logic.Xor)
    print("Nor: ")
    tableCheck(logic.Nor)
    print("Nand: ")
    tableCheck(logic.Nand)
    print("Ior: ")
    tableCheck(logic.Xnor)


def testMultiInputLogic():
    length = 2
    print("Input:\t      Or:    And:    Nor:   Nand:  Xored: Xnored:")
    for i in range(0, 2**length):
        state = itot(i, length)
        ored = logic.Or(state)
        anded = logic.And(state)
        nored = logic.Nor(state)
        nanded = logic.Nand(state)
        Xored = logic.Xor(state)
        Xnored = logic.Xnor(state)
        fmt = (state, ored, anded, nored, nanded, Xored, Xnored)
        fmtstr = ("%s:\t\t%s\t%s\t%s\t%s\t%s\t%s" % fmt)
        print(fmtstr)
    length = 4
    print("Input:        Or:    And:    Nor:   Nand:  Xored: Xnored:")
    for i in range(0, 2**length):
        state = itot(i, length)
        ored = logic.Or(state)
        anded = logic.And(state)
        nored = logic.Nor(state)
        nanded = logic.Nand(state)
        Xored = logic.Xor(state)
        Xnored = logic.Xnor(state)
        fmt = (state, ored, anded, nored, nanded, Xored, Xnored)
        fmtstr = ("%s:\t%s\t%s\t%s\t%s\t%s\t%s" % fmt)
        print(fmtstr)


def testHalfAdder():
    from Circuits import HalfAdder
    h1 = HalfAdder()
    print("Halfadder: ")
    print(" A |B |   Co|S ")
    for i in range(0, 4):
        state = itot(i, 2)
        h1.setinput(state)
        print("%s-->%s" % (state, h1.getoutput()))
    print("")


def testFullAdder():
    from Circuits import FullAdder
    f1 = FullAdder()
    print("Fulladder: ")
    print(" A |B |Ci|   Co|S ")
    # create a state and test on it.
    for i in range(0, 8):
        # generate four states
        state = itot(i, 3)
        f1.setinput(state)
        print("%s-->%s" % (state, f1.getoutput()))
    print("")


def testFourBitAdder():
    from Circuits import FourBitAdder
    adder = FourBitAdder()
    bitlength = 4
    print("FourBitadder: Addition")
    for i in range(0, bitlength):
        left, right = getRandomInts(bitlength)
        state1 = itot(left, bitlength)
        state2 = itot(right, bitlength)
        adder.setinput(state1, state2, 0)
        output = adder.getoutput()
        if output[1]:
            overflow = True
        else:
            overflow = False
        answer = ttoi(output[0])
        check = (answer == (left+right))
        fmt = (ttoi(state1), ttoi(state2),
               answer, check)
        if overflow:
            fmtstr = "%s + %s = %s :check:%s number overflow"
        else:
            fmtstr = "%s + %s = %s :check:%s"
        print(fmtstr % fmt)
    print("")


def testXBitAdder():
    from Circuits import XBitAdder
    bitlength = 8
    print("max integer size: %d" % (bitlength))
    adder = XBitAdder(bitlength)
    print("Xbitadder: ")
    # run 20 tests
    for i in range(0, 6):
        left, right = getRandomInts(bitlength)
        state1 = itot(left, bitlength)
        state2 = itot(right, bitlength)
        adder.setinput(state1, state2, 0)
        answer = ttoi(adder.getoutput()[0])
        fmt = (ttoi(state1), ttoi(state2),
               answer, (answer == (left+right)))
        if adder.getoutput()[1]:
            print("%s + %s = %s :check:%s integer overflow" % fmt)
        else:
            print("%s + %s = %s :check:%s" % fmt)
    print("")


def testXBitSubtractor():
    from Circuits import XBitSubtractor
    bitlength = 8
    print("integer size: %s" % bitlength)
    subtractor = XBitSubtractor(bitlength)
    print("XBitSubtractor unsigned: ")
    for i in range(0, 6):
        left, right = getRandomInts(bitlength)
        state1 = itot(left, bitlength)
        state2 = itot(right, bitlength)
        subtractor.setinput(state1, state2, 0)
        answer = ttoi(subtractor.getoutput()[0])
        fmt = (ttoi(state1), ttoi(state2), answer)
        print("%s - %s = %s" % fmt)
    print("signed: ")
    for i in range(0, 6):
        left, right = getRandomInts(bitlength)
        state1 = itot(left, bitlength)
        state2 = itot(right, bitlength)
        subtractor.setinput(state1, state2, 0)
        output = subtractor.getoutput()
        if output[1]:
            answer = -(ttoi(invertTuple(output[0]))+1)
        else:
            answer = ttoi(output[0])
        fmt = (ttoi(state1), ttoi(state2), answer)
        print("%s - %s = %s " % fmt)
    print("")


def testSubtractor():
    import Circuits as cir
    subtractor = cir.FourBitSubtractor()
    bitlength = 4
    print("FourBitSubtractor: ")
    print("printing signed representation:")
    for i in range(0, 5):
        left, right = getRandomInts(bitlength)
        state1 = itot(left, bitlength)
        state2 = itot(right, bitlength)
        subtractor.setinput(state1, state2, 0)
        output = subtractor.getoutput()
        # check signednes
        if output[1]:
            # if signed do this for the right negative number
            # because if you don't you get to deal with unsigned number.
            # and thus have overflow, and thus not really good to check for
            # human readers, unless you like to think about it ofcourse .
            answer = -(ttoi(invertTuple(output[0]))+1)
        else:
            answer = (ttoi(output[0]))
        fmt = (left, right, answer)
        fmtstr = "%s - %s = %s" % fmt
        print(fmtstr)
    print("printing unsigned representation: ")
    for i in range(0, 5):
        left, right = getRandomInts(bitlength)
        state1 = itot(left, bitlength)
        state2 = itot(right, bitlength)
        subtractor.setinput(state1, state2, 0)
        output = subtractor.getoutput()
        answer = ttoi(output[0])
        fmt = (left, right, answer)
        fmtstr = "%s - %s = %s" % fmt
        print(fmtstr)
    print("")


def testLatch():
    from Circuits import Latch
    latch = Latch()
    print("s-r latch: ")
    while(True):
        answer = raw_input("Input (S)et (R)eset (Q)uit:\n").lower()
        if answer == "q":
            break
        elif answer == "s":
            latch.setinput((1, 0))
            print(latch.getoutput())
        elif answer == "r":
            latch.setinput((0, 1))
            print(latch.getoutput())


def testGatedLatch():
    from Circuits import GatedLatch
    latch = GatedLatch()
    enabled = 0
    print("gated s-r latch: ")
    while(True):
        answer = raw_input("Input (S)et (R)eset (E)nable (Q)uit: \n").lower()
        if answer == "q":
            break
        elif answer == "s":
            latch.setinput((1, 0, enabled))
            print(latch.getoutput())
        elif answer == "r":
            latch.setinput((0, 1, enabled))
            print(latch.getoutput())
        elif answer == "e":
            enabled = logic.Not(enabled)


def testDataLatch():
    from Circuits import DataLatch
    latch = DataLatch()
    enabled = 0
    data = 0
    print("Data latch: ")
    while(True):
        answer = raw_input("input (D)ata (E)nable (Q)uit: \n").lower()
        if answer == "q":
            break
        elif answer == "d":
            answer = raw_input("input 1 or 0 for data: \n").lower()
            data = eval(answer)
            latch.setinput((data, enabled))
            print(latch.getoutput())
            data = logic.Not(data)
        elif answer == "e":
            enabled = logic.Not(enabled)


def testPiPoRegister():
    from Circuits import PiPoRegister
    register = PiPoRegister()
    print("Paralel in paralel out register.")
    enabled = 0
    # once and zero's alternating
    data = 170

    print("data:%s disabled:" % (itot(data, register.length),))
    signal = (itot(data, register.length), enabled)
    register.setinput(signal)
    print(register.getoutput())

    enabled = 1
    print("data:%s enabled:" % (itot(data, register.length),))
    signal = (itot(data, register.length), enabled)
    register.setinput(signal)
    print(register.getoutput())

    enabled = 0
    data = 0xF0
    print("data:%s disabled: " % (itot(data, register.length),))
    signal = (itot(data, register.length), enabled)
    register.setinput(signal)
    print(register.getoutput())

    print("data:%s enabled:" % (itot(data, register.length),))
    enabled = 1
    signal = (itot(data, register.length), enabled)
    register.setinput(signal)
    print(register.getoutput())
    print("")


def testXBitPiPoRegister():
    from Circuits import XBitPiPoRegister
    from getch import getch
    import time
    import sys
    bitlength = 4
    register = XBitPiPoRegister(length=bitlength)
    print("\nvariable length parallel in parallel out register:")
    data = itot(0, bitlength)
    clock = 0
    char = ''
    while(char != u'q'):
        if char >= u'0' and char <= u'9':
            intdata = ttoi(data)
            shifted = (ord(char) - ord(u'0') - 1)
            intdata ^= (1 << shifted)
            data = itot(intdata, bitlength)
        elif char == u'c':
            clock = logic.Not(clock)
        signal = (data, clock)
        register.setinput(signal)
        output = register.getoutput()
        fmt = (clock, data, output, time.time())
        fmtstr = "Clock:%s Input:%s Output:%s %s\r" % fmt
        sys.stdout.write(fmtstr)
        char = getch()


def d_latch_vs_dms_latch():
    from getch import getch
    import sys
    from Circuits import DataLatch, MSDataLatch
    latch = DataLatch()
    latch2 = MSDataLatch()
    print("\ndifference between latch, and flipflop")
    data, enabled = 1, 0
    char = ' '
    while(char != u'q'):
        if char == u'2':
            enabled = logic.Not(enabled)
        elif char == u'1':
            data = logic.Not(data)
        latch.setinput((data, enabled))
        latch2.setinput((data, enabled))
        fmt = (data, enabled, latch.getoutput(), latch2.getoutput())
        fmtstr = "\rdata:%s enabled:%s D-Latch:%s MSD-Latch:%s"
        sys.stdout.write(fmtstr % fmt)
        char = getch()


def testJKFlipflop():
    from Circuits import JKFlipFlop
    from getch import getch
    import sys
    flipflop = JKFlipFlop()
    j, k, clock = 0, 0, 0
    print("\nJK-flipflop")
    print("")
    char = ""
    while(char != u'q'):
        if(char == u'j'):
            j = logic.Not(j)
        elif(char == u'k'):
            k = logic.Not(k)
        elif(char == u'c'):
            clock = logic.Not(clock)
        signal = (j, k, clock)
        flipflop.setinput(signal)
        q, qn, = flipflop.getoutput()
        fmt = (j, k, clock, q, qn)
        fmtstr = "\rJ:%s K:%s clock:%s Q:%s Qn:%s"
        sys.stdout.write(fmtstr % fmt)
        char = getch()


def testTFlipflop():
    from Circuits import TFlipFlop
    from getch import getch
    import sys
    flipflop = TFlipFlop()
    t, clock = 0, 0
    print("\nToggle FlipFlop")
    print("")
    char = ""
    while(char != u'q'):
        if(char == u't'):
            t = logic.Not(t)
        elif(char == u'c'):
            clock = logic.Not(clock)
        signal = (t, clock)
        flipflop.setinput(signal)
        q, qn, = flipflop.getoutput()
        fmt = (t, clock, q, qn)
        fmtstr = "\rT:%s clock:%s q:%s qn:%s"
        sys.stdout.write(fmtstr % fmt)
        char = getch()


def testCounter():
    from Circuits import Counter
    from getch import getch
    import sys
    counter = Counter(length=8)
    print("\ncounter:")
    print("")
    clock = 0
    enabled = 1
    char = ""
    while(char != u'q'):
        if(char == u'e'):
            enabled = logic.Not(enabled)
        elif(char == u'c'):
            clock = logic.Not(clock)
        signal = (clock, enabled)
        counter.setinput(signal)
        count = counter.getoutput()
        fmt = (enabled, clock, count)
        fmtstr = "\rEnabled:%s Clock:%s Count:%s"
        sys.stdout.write(fmtstr % fmt)
        char = getch()


def testXBitSiPoRegister():
    from Circuits import XBitSiPoRegister
    from getch import getch
    import sys
    register = XBitSiPoRegister(length=4)

    print("XBit SiPo register:")
    clock = 0
    data = 0
    char = ""
    while(char != u'q'):
        if(char == u'c'):
            clock = logic.Not(clock)
        elif(char == u'd'):
            data = logic.Not(data)
        signal = (data, clock)
        register.setinput(signal)
        output = register.getoutput()
        fmt = (clock, data, output)
        fmtstr = "\rClock:%s Data:%s Output:%s"
        sys.stdout.write(fmtstr % fmt)
        char = getch()


def sipoTesting():
    from Circuits import SiPoRegister
    register = SiPoRegister()
    print("serial in parallel out")
    print("")
    data, clock = 1, 1
    register.setinput((data, clock))
    register.getoutput()
    clock = 0
    register.setinput((data, clock))
    print(register.getoutput())

    data, clock = 0, 1
    register.setinput((data, clock))
    register.getoutput()
    clock = 0
    register.setinput((data, clock))
    print(register.getoutput())

    data, clock = 1, 1
    register.setinput((data, clock))
    register.getoutput()
    clock = 0
    register.setinput((data, clock))
    print(register.getoutput())

    data, clock = 0, 1
    register.setinput((data, clock))
    register.getoutput()
    clock = 0
    register.setinput((data, clock))
    print(register.getoutput())


def testOneBitMagnitudeComparator():
    from Circuits import OneBitMagnitudeComparator as comp
    comparator = comp()
    length = 2
    print("magnitude comparator test:")
    print(" Ai|Bi  Go|Eo|Lo")
    for i in range(2**length):
        state = itot(i, length)
        comparator.setinput(state)
        output = comparator.getoutput()
        fmt = (state, output)
        fmtstr = "%s %s" % fmt
        print(fmtstr)


def testCascadeMagnitudeComparator():
    from Circuits import CascadeOneBitMagnitudeComparator as comp
    comparator = comp()
    length = 5
    print("cascade magnitude comparator:")
    print(" Ai|Bi|Gi|Ei|Li  Go|Eo|Lo")
    for state in states(length):
        comparator.setinput(state)
        output = comparator.getoutput()
        fmt = (state, output)
        fmtstr = "%s %s" % fmt
        print(fmtstr)


def testFourBitMagnitudeComparator():
    from Circuits import FourBitMagnitudeComparator as comp
    comparator = comp()
    length = 4
    print("Four bit magnitude comparator:")
    for i in range(0, length*10):
        left, right = getRandomInts(4)
        state1 = itot(left, 4)
        state2 = itot(right, 4)

        comparator.setinput(state1, state2, (0, 0, 0))
        output = comparator.getoutput()
        print(left, right, output)
    print("")


def testEncoder8to3():
    from Circuits import Encoder8to3
    encoder = Encoder8to3()
    inputs = 8
    print("Encoder: ")
    for i in range(0, inputs):
        inputed = (1 << i)
        state = itot(inputed, inputs)
        encoder.setinput(state)
        output = encoder.getoutput()
        fmt = (state, output)
        fmtstr = "%s : %s" % fmt
        print(fmtstr)
    print("")


def testDecoder2to4():
    from Circuits import Decoder2to4
    decoder = Decoder2to4()
    # 2 plus enable
    inputs = 3
    print("Decoder2to4: ")
    for state in states(inputs):
        decoder.setinput(state)
        output = decoder.getoutput()
        fmt = (state, output)
        fmtstr = "%s : %s" % fmt
        print(fmtstr)
    print("")


def testDecoder3to8():
    from Circuits import Decoder3to8
    decoder = Decoder3to8()
    # 3 inputs plus enable
    inputs = 4
    print("Decoder3to8: ")
    for state in states(inputs):
        decoder.setinput(state)
        output = decoder.getoutput()
        fmt = (state, output)
        fmtstr = "%s : %s" % fmt
        print(fmtstr)
    print("")


def testDecoder4to16():
    from Circuits import Decoder4to16
    decoder = Decoder4to16()
    # 4 inputs plus enable
    inputs = 5
    print("Decoder4to16: ")
    for state in states(inputs):
        decoder.setinput(state)
        output = decoder.getoutput()
        fmt = (state, output)
        fmtstr = "%s : %s" % fmt
        print(fmtstr)
    print("")


def testDecoder5to32():
    from Circuits import Decoder5to32
    decoder = Decoder5to32()
    # 5 inputs plus enabled
    inputs = 6
    print("Decoder5to32: ")
    for state in states(inputs):
        decoder.setinput(state)
        output = decoder.getoutput()
        fmt = (state, output)
        fmtstr = "%s : %s" % fmt
        print(fmtstr)
    print("")


def testDecoder6to64():
    from Circuits import Decoder6to64


def runTests():
    printTestLogic()
    testHalfAdder()
    testFullAdder()
    testFourBitAdder()
    testXBitAdder()
    testPiPoRegister()
    sipoTesting()
    d_latch_vs_dms_latch()
    testJKFlipflop()
    testTFlipflop()
    testCounter()
    testOneBitMagnitudeComparator()
    testCascadeMagnitudeComparator()
    testFourBitMagnitudeComparator()
