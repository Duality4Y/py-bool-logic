"""
    mainly testing out logic with logic tables.
"""
import baseLogic as logic


def itot(value, bits):
    """ int to binary tuple representation """
    rep = []
    for i in range(bits):
        if(value & (1 << i)):
            rep.append(1)
        else:
            rep.append(0)
    # return a tuple of bits and reverse because it's binary.
    return(tuple(rep))


def ttoi(tuplerep):
    value = 0
    for i, bit in enumerate(tuplerep):
        value |= (tuplerep[i] << i)
    return value


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
    tableCheck(logic.Ior)


def testHalfAddr():
    from Circuits import HalfAddr
    h1 = HalfAddr()
    print("HalfAddr: ")
    print(" A |B |   Co|S ")
    for i in range(0, 4):
        state = itot(i, 2)
        h1.setinput(state)
        print("%s-->%s" % (state, h1.getoutput()))
    print("")


def testFullAddr():
    from Circuits import FullAddr
    f1 = FullAddr()
    print("FullAddr: ")
    print(" A |B |Ci|   Co|S ")
    # create a state and test on it.
    for i in range(0, 8):
        # generate four states
        state = itot(i, 3)
        f1.setinput(state)
        print("%s-->%s" % (state, f1.getoutput()))
    print("")


def testFourBitAddr():
    from Circuits import FourBitAddr
    import random
    addr = FourBitAddr()
    bitlength = 4
    print("FourBitAddr: ")
    for i in range(0, bitlength):
        left, right = (random.randint(0, 2**bitlength),
                       random.randint(0, 2**bitlength))
        state1 = itot(left, bitlength)
        state2 = itot(right, bitlength)
        addr.setinput(state1, state2, 0)
        answer = ttoi(addr.getoutput())
        fmt = (ttoi(state1), ttoi(state2),
               answer, (answer == (left+right)))
        print("%s + %s = %s :check:%s" % fmt)
    print("")


def testXBitAddr():
    from Circuits import XBitAddr
    import random
    bitlength = 8
    addr = XBitAddr(bitlength)
    print("XbitAddr: ")
    for i in range(0, bitlength):
        left, right = (random.randint(0, 2**bitlength),
                       random.randint(0, 2**bitlength))
        state1 = itot(left, bitlength)
        state2 = itot(right, bitlength)
        addr.setinput(state1, state2, 0)
        answer = ttoi(addr.getoutput())
        fmt = (ttoi(state1), ttoi(state2),
               answer, (answer == (left+right)))
        print("%s + %s = %s :check:%s" % fmt)
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


def testPiPaRegister():
    from Circuits import PiPaRegister
    register = PiPaRegister()
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


def testSiPaRegister():
    from Circuits import SiPaRegister
    print("SiPa register: ")
    latch = SiPaRegister()
    data = 0
    enabled = 1
    latch.setinput((data, enabled))
    print(latch.getoutput())
    data = 1
    latch.setinput((data, enabled))
    print(latch.getoutput())
    print("")


def d_latch_vs_dms_latch():
    from getch import getch
    import sys
    from Circuits import DataLatch, MSDataLatch
    latch = DataLatch()
    latch2 = MSDataLatch()
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


def runTests():
    printTestLogic()
    testHalfAddr()
    testFullAddr()
    testFourBitAddr()
    testXBitAddr()


if __name__ == "__main__":
    testFourBitAddr()
    testXBitAddr()
    testPiPaRegister()
    d_latch_vs_dms_latch()
    print("")
