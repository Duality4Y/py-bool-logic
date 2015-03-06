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
    value = 0
    for i, bit in enumerate(tuplerep):
        value |= (tuplerep[i] << i)
    return value


def testTupleConversion(amount):
    result = True
    for i in xrange(0, 2**amount):
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
            break


def generateTableFile(numin, numout, tablefile='table.txt'):
    instates = []
    for i in range(0, 2**numin):
        instates.append(itot(i, numin))
    with open(tablefile, 'w') as f:
        head = '|A  |B  |C  |Gi |Ei |Li  |Go  |Eo  |Lo \n'
        f.write(head)
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
