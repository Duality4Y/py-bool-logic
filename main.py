#!/usr/bin/env python2.7
"""
    mainly testing out logic with logic tables.
"""

import LogicTests as test

if __name__ == "__main__":
    # runTests()
    test.testFourBitadder()
    test.testXBitadder()
    from Circuits import FullSubtractor, HalfSubtractor
    from LogicUtils import itot
    subtractor = HalfSubtractor()
    for i in range(2**2):
        state = itot(i, 2)[::-1]
        subtractor.setinput(state)
        print(state, subtractor.getoutput())
    print("")
    subtractor = FullSubtractor()
    for i in range(2**3):
        state = itot(i, 3)[::-1]
        subtractor.setinput(state)
        print(state, subtractor.getoutput())
    # test.testFourBitEquComp()
    # test.testEquComparator()
    print("")
