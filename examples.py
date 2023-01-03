import numpy as np
from pylfsr import LFSR
## Example 1  ## 5 bit LFSR with x^5 + x^2 + 1
L = LFSR()
L.info()
L.next()
L.runKCycle(10)
#L.runFullCycle()
L.runFullPeriod()
L.info()
tempseq = L.runKCycle(10000)    # generate 10000 bits from current state

## Example 2  ## 5 bit LFSR with custum state and feedback polynomial
state = [0,0,0,1,0]
fpoly = [5,4,3,2]
L1 = LFSR(fpoly=fpoly,initstate =state, verbose=True)
L1.info()
tempseq = L1.runKCycle(10)
tempseq
L1.set_fpoly(fpoly=[5,3])

## Example 3 ## TO visualize the process with 3-bit LFSR, with default counter_start_zero = True
state = [1,1,1]
fpoly = [3,2]
L = LFSR(initstate=state,fpoly=fpoly)
print('count \t state \t\toutbit \t seq')
print('-'*50)
for _ in range(15):
    print(L.count,L.state,'',L.outbit,L.seq,sep='\t')
    L.next()
print('-'*50)
print('Output: ',L.seq)

## Example 4 ## TO visualize the process with 3-bit LFSR, with default counter_start_zero = False
state = [1,1,1]
fpoly = [3,2]
L = LFSR(initstate=state,fpoly=fpoly,counter_start_zero=False)
print('count \t state \t\toutbit \t seq')
print('-'*50)
for _ in range(15):
    print(L.count,L.state,'',L.outbit,L.seq,sep='\t')
    L.next()
print('-'*50)
print('Output: ',L.seq)


## Example 5  ## 23 bit LFSR with custum state and feedback polynomial
L = LFSR(fpoly=[23,19],initstate ='ones',verbose=True)
L.info()
L.runKCycle(10)
L.info()
seq = L.seq
#L.changeFpoly(newfpoly =[23,21])
L.set_fpoly(fpoly =[23,21])
seq1 = L.runKCycle(20)

##  Example 6 ## testing the properties
state = [1,1,1,1,0]
fpoly = [5,3]
L = LFSR(initstate=state,fpoly=fpoly)
L.info()
result  = L.test_properties(verbose=1)


##  Example 7 ## testing the properties  for non-primitive polynomial
state = [1,1,1,1,0]
fpoly = [5,1]
L = LFSR(initstate=state,fpoly=fpoly)
L.info()
result  = L.test_properties(verbose=1)
