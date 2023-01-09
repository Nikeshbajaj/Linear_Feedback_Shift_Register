**Generators**
==========

**A5/1 GSM Stream cipher generator**
----------

Ref: https://en.wikipedia.org/wiki/A5/1


.. image:: https://upload.wikimedia.org/wikipedia/commons/5/5e/A5-1_GSM_cipher.svg

Image Socuce: https://en.wikipedia.org/wiki/A5/1

::
  
  import numpy as np
  import matplotlib.pyplot as plt
  from pylfsr import A5_1

  A5 = A5_1(key='random')
  print('key: ',A5.key)
  A5.R1.Viz(title='R1')
  A5.R2.Viz(title='R2')
  A5.R3.Viz(title='R3')

  print('key: ',A5.key)
  print()
  print('count \t cbit\t\tclk\t R1_R2_R3\toutbit \t seq')
  print('-'*80)
  for _ in range(15):
      print(A5.count,A5.getCbits(),A5.clock_bit,A5.getLastbits(),A5.outbit,A5.getSeq(),sep='\t')
      A5.next()
  print('-'*80)
  print('Output: ',A5.seq)

  A5.runKCycle(1000)
  A5.getSeq()


**Enhanced A5/1**
----------

Reference Article: **Enhancement of A5/1**: https://doi.org/10.1109/ETNCC.2011.5958486

.. image:: https://raw.githubusercontent.com/nikeshbajaj/Linear_Feedback_Shift_Register/master/images/Enhanced_A51.png
	:width: 70%

::
  
  # Three LFSRs initialzed with 'ones' though they are intialized with encription key
  R1 = LFSR(fpoly = [19,18,17,14])
  R2 = LFSR(fpoly = [23,22,21,8])
  R3 = LFSR(fpoly = [22,21])

  # clocking bits
  b1 = R1.state[8]
  b2 = R3.state[10]
  b3 = R3.state[10]


**Geffe Generator**
----------

Ref: Schneier, Bruce. Applied cryptography: protocols, algorithms, and source code in C. john wiley & sons, 2007.
	Chaper 16 

.. image:: https://raw.githubusercontent.com/nikeshbajaj/Linear_Feedback_Shift_Register/master/images/Geffe_0.jpg

::
  
  import numpy as np
  import matplotlib.pyplot as plt
  from pylfsr import Geffe, LFSR

  kLFSR = [LFSR(initstate='random') for _ in range(8)]  # List of 8 5-bit LFSRs with default feedback polynomial and random initial state 
  cLFSR = LFSR(initstate='random')                      # A 5-bit LFSR with for selecting one of 8 output at a time

  GG = Geffe(kLFSR_list=kLFSR, cLFSR=cLFSR)

  print('key: ',GG.getState())
  print()
  for _ in range(50):
      print(GG.count,GG.m_count,GG.outbit_k,GG.sel_k,GG.outbit,GG.getSeq(),sep='\t')
      GG.next()

  GG.runKCycle(1000)
  GG.getSeq()
  
