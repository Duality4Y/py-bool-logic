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
    state1 = logic.Not(0)
    state2 = logic.Not(1)
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


def printTestsLogic():
    print("Not:")
    checkNot(logic)
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
    print(" A |B |   Co|S ")
    for i in range(0, 4):
        state = itot(i, 2)
        h1.setinput(state)
        print("%s-->%s" % (state, h1.getoutput()))
    print("")


def testFullAddr():
    from Circuits import FullAddr
    f1 = FullAddr()
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
    addr = FourBitAddr()
    for i in range(0, 16):
        for y in range(0, 16):
            state1 = itot(i, 4)
            state2 = itot(y, 4)
            addr.setinput(state1, state2, 0)
            fmt = (ttoi(state1), ttoi(state2), ttoi(addr.getoutput()))
            print("%s + %s = %s" % fmt)


def testXBitAddr():
    from Circuits import XBitAddr
    bitlength = 8
    addr = XBitAddr(bitlength)
    for i in range(0, (2**bitlength)+1):
        state1 = itot(1, bitlength)
        state2 = itot(i, bitlength)
        addr.setinput(state1, state2, 0)
        fmt = (ttoi(state1), ttoi(state2), ttoi(addr.getoutput()))
        print("%s + %s = %s" % fmt)


def testLatch():
    from Circuits import Latch
    latch = Latch()
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

if __name__ == "__main__":
    testXBitAddr()
