import numpy as np
from pylfsr import LFSR
## Example 1  ## 5 bit LFSR with x^5 + x^2 + 1
L = LFSR() 
L.info()
L.next()
L.runKCycle(10)
L.runFullCycle()
L.info()
tempseq = L.runKCycle(10000)    # generate 10000 bits from current state

## Example 2  ## 5 bit LFSR with custum state and feedback polynomial
state = np.array([0,0,0,1,0])
fpoly = [5,4,3,2]
L = LFSR(fpoly=fpoly,initstate =state, verbose=True)
L.info()
tempseq = L.runKCycle(10)
tempseq
L.set(fpoly=[5,3])


## Example 3  ## 23 bit LFSR with custum state and feedback polynomial
L = LFSR(fpoly=[23,19],initstate ='ones',verbose=True)
L.info()
L.runKCycle(10)
L.info()
seq = L.seq
L.changeFpoly(newfpoly =[23,21])
seq1 = L.runKCycle(20)














