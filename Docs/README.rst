LFSR -Linear Feedback Shift Register
======================================

* [View on Github Page](http://nikeshbajaj.github.io/Linear_Feedback_Shift_Register/)

* [PyPi - project](https://pypi.org/project/pylfsr/)

----------

**Python**
**Installation**

**Requirement** : *numpy*

**With pip:**

::
  
  pip install pylfsr


**Build from source**

Download the repository or clone it with git, after cd in directory build it from source with

::

  python setup.py install


**Example 1** ## 5 bit LFSR with :x^5 + x^2 + 1:

::
  
  >>>import numpy as np
  >>>from pylfsr import LFSR
  
  >>>L = LFSR() 
  >>>L.info()
  5 bit LFSR with feedback polynomial  :x^5 + x^2 + 1:
  Expected Period (if polynomial is primitive) =  31
  Current :
  State        :  [1 1 1 1 1]
  Count        :  0
  Output bit   :  -1
  feedback bit :  -1


::
  
  >>>L.next()
  >>>L.runKCycle(10)
  >>>L.runFullCycle()
  >>>L.info()

**Example 2** ## 5 bit LFSR with custum state and feedback polynomial

::
  
  >>>state = [0,0,0,1,0]
  >>>fpoly = [5,4,3,2]
  >>>L = LFSR(fpoly=fpoly,initstate =state, verbose=True)
  >>>L.info()
  >>>tempseq = L.runKCycle(10)
  >>>L.set(fpoly=[5,3])


**Example 3**  ## 23 bit LFSR with custum state and feedback polynomial

::
  
  >>>L = LFSR(fpoly=[23,18],initstate ='random',verbose=True)
  >>>L.info()
  >>>L.runKCycle(10)
  >>>L.info()
  >>>seq = L.seq
  

Changing feedback polynomial in between as in Article: **Enhancement of A5/1**

**https://doi.org/10.1109/ETNCC.2011.5958486**

::
  
  >>>L.changeFpoly(newfpoly =[23,14],reset=False)
  >>>seq1 = L.runKCycle(20)

  >>>L.changeFpoly(newfpoly =[23,9],reset=False)
  >>>seq1 = L.runKCycle(20)


**For A5/1 GSM Stream cipher generator (Hint)**

::
  
  # Three LFSRs initialzed with 'ones' though they are intialized with encription key
  R1 = LFSR(fpoly = [19,18,17,14])
  R2 = LFSR(fpoly = [23,22,21,8])
  R3 = LFSR(fpoly = [22,21])

  # clocking bits
  b1 = R1.state[8]
  b2 = R1.state[10]
  b3 = R1.state[10]


Contacts
----------

If any doubt, confusion or feedback please contact me

Nikesh Bajaj
http://nikeshbajaj.in

* `n[dot]bajaj[AT]qmul[dot]ac[dot]uk`
* `bajaj[dot]nikkey[AT]gmail[dot]com`

PhD Student, Queen Mary University of London & University of Genoa
