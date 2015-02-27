from baseLogic import *


class LC(object):
    def __init__(self):
        pass

    def setinput(self, input):
        pass

    def getoutput(self):
        pass


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
