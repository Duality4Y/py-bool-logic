import random


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
    """ binary tuple representation to int"""
    value = 0
    for i, bit in enumerate(tuplerep):
        value |= (tuplerep[i] << i)
    return value


def invertTuple(tuplerep):
    rep = []
    for value in tuplerep:
        if value:
            rep.append(0)
        else:
            rep.append(1)
    return tuple(rep)


def appendTuple(*tupleReps):
    newrep = []
    for rep in tupleReps:
        for bit in rep:
            newrep.append(bit)
    return tuple(newrep)


def paddedTuple(size, pat=1):
    rep = []
    for i in range(size):
        if pat:
            rep.append(i % 2)
        else:
            rep.append(1 - (i % 2))
    return tuple(rep)


def testPaddedTuple(size=32):
    import baseLogic
    print("padded test: ")
    state1 = paddedTuple(size, 0)
    state2 = paddedTuple(size, 1)
    print(state1)
    print(state2)
    print(baseLogic.Xor(state1))
    print(baseLogic.Xor(state2))
    print(baseLogic.Xnor(state1))
    print(baseLogic.Xnor(state2))


def testTupleConversion(amount):
    result = True
    for i in range(0, 2**amount):
        it = itot(i, amount)
        ti = ttoi(it)
        if ti != i:
            result = False
            break
        else:
            result = True
    return result


def testConversion(start=0):
    testing = True
    iteration = start
    while(testing):
        testing = testTupleConversion(iteration)
        iteration += 1
        print("iteration: %d" % iteration)
        if(iteration == 21):
            print("got through test")
            return


def states(length=2):
    for intrep in range(0, 2**length):
        yield itot(intrep, length)


def testStatesGenerator():
    for i in range(1, 4):
        for rep in states(i+1):
            print(rep)


def testTupleAppending():
    output = (1, 0, 1, 0)
    for state in states(4):
        output = appendTuple(state, state)
        print(output)


def generateTableFile(numin, numout, head=None, tablefile='table.txt'):
    instates = []
    for i in range(0, 2**numin):
        instates.append(itot(i, numin)[::-1])
    with open(tablefile, 'w') as f:
        if head:
            # head = '|A  |B  |Gi |Ei |Li  |Go  |Eo  |Lo \n'
            f.write(head+'\n')
        for state in instates:
            f.write(str(state).replace(' ', '  ')+' '+str((' ', )*numout)+'\n')


def getRandomInts(length, amount=2):
    """ return <amount> random ints with <length> """
    randomints = []
    for i in range(0, amount):
        randomints.append(random.randint(0, (2**length)-1))
    if amount == 1:
        return randomints[0]
    else:
        return randomints
