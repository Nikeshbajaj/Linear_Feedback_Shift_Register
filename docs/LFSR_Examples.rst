**Examples**
=========

**Basic Examples:**
=========

5-bit LFSR with feedback polynomial: x\ :sup:`5`\ + x\ :sup:`2`\ +1
----------

Default feedback polynomial is p(x) = x\ :sup:`5`\ + x\ :sup:`2`\ + 1

::
  
  # import LFSR
  import numpy as np
  from pylfsr import LFSR
  
  L = LFSR()
  
  # print the info
  L.info()
  
  5 bit LFSR with feedback polynomial  x^5 + x^2 + 1
  Expected Period (if polynomial is primitive) =  31
  Current :
  State        :  [1 1 1 1 1]
  Count        :  0
  Output bit   : -1
  feedback bit : -1


Execute cycles (run LFSR by clock)
----------

::
  
  # one cycle
  L.next()
  
  # K cycles
  k=10
  seq  = L.runKCycle(k)
  
  #Cycles of a full period, #cycles = expected period of LFSR
  
  # L.runFullCycle()  # Depreciated
  seq = L.runFullPeriod()
  
  

5-bit LFSR with custom state and feedback polynomial
----------

::
  
  state = [0,0,0,1,0]
  fpoly = [5,4,3,2]
  L = LFSR(fpoly=fpoly,initstate =state, verbose=True)
  L.info()
  tempseq = L.runKCycle(10)
  L.set(fpoly=[5,3])


Fibonacci LFSR
----------
By deault, LFSR is in Fibonacci configuration mode, but it can be implicitly set to Fibonacci conf

::
  
  L = LFSR(fpoly = [5,4,3,2], conf='fibonacci') 
  L.Viz(show_outseq=False)


Galois LFSR
----------
To construct LSFR with Galois configuration , pass conf = 'galois'

::
  
  L = LFSR(fpoly = [5,4,3,2], conf='galois') 
  L.Viz(show_outseq=False)




23-bit LFSR: x\ :sup:`23`\ + x\ :sup:`18`\ +1
----------

::
  
  L = LFSR(fpoly=[23,18],initstate ='random',verbose=True)
  L.info()
  L.runKCycle(10)
  L.info()
  seq = L.seq


23-bit LFSR: x\ :sup:`23`\ + x\ :sup:`5`\ +1
----------

::
  
  fpoly = [23,5]
  L1 = LFSR(fpoly=fpoly,initstate ='ones', verbose=False)
  L1.info()
  
  
::
  
  23 bit LFSR with feedback polynomial  x^23 + x^5 + 1
  Expected Period (if polynomial is primitive) =  8388607
  Current :
   State        :  [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]
   Count        :  0
   Output bit   :  -1
   feedback bit :  -1
