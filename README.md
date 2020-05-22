# LFSR -Linear Feedback Shift Register

**[Documentation](https://lfsr.readthedocs.io/)**

[![Documentation Status](https://readthedocs.org/projects/linear-feedback-shift-register/badge/?version=latest)](https://linear-feedback-shift-register.readthedocs.io/en/latest/?badge=latest)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  [![DOI](https://zenodo.org/badge/31331840.svg)](https://zenodo.org/badge/latestdoi/31331840)
[![PyPI version fury.io](https://badge.fury.io/py/pylfsr.svg)](https://pypi.python.org/pypi/pylfsr/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pylfsr.svg)](https://pypi.python.org/pypi/pylfsr/)
[![GitHub release](https://img.shields.io/github/release/nikeshbajaj/Linear_Feedback_Shift_Register.svg)](https://github.com/Nikeshbajaj/Linear_Feedback_Shift_Register/releases/)
[![PyPI format](https://img.shields.io/pypi/format/pylfsr.svg)](https://pypi.python.org/pypi/pylfsr/)
[![PyPI implementation](https://img.shields.io/pypi/implementation/pylfsr.svg)](https://pypi.python.org/pypi/pylfsr/)
[![HitCount](http://hits.dwyl.io/nikeshbajaj/Linear_Feedback_Shift_Register.svg)](http://hits.dwyl.io/nikeshbajaj/Linear_Feedback_Shift_Register)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/nikeshbajaj/Linear_Feedback_Shift_Register.svg)](http://isitmaintained.com/project/nikeshbajaj/Linear_Feedback_Shift_Register "Percentage of issues still open")
[![PyPI download month](https://img.shields.io/pypi/dm/pylfsr.svg)](https://pypi.org/project/pylfsr/)
[![PyPI download week](https://img.shields.io/pypi/dw/pylfsr.svg)](https://pypi.org/project/pylfsr/)


[![Generic badge](https://img.shields.io/badge/pip%20install-pylfsr-blue.svg)](https://pypi.org/project/pylfsr/)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](mailto:n.bajaj@qmul.ac.uk)


![PyPI - Downloads](https://img.shields.io/pypi/dm/pylfsr?style=social)
![GitHub stars](https://img.shields.io/github/stars/nikeshbajaj/Linear_Feedback_Shift_Register?style=social)
![GitHub forks](https://img.shields.io/github/forks/nikeshbajaj/Linear_Feedback_Shift_Register?style=social)

### **[Github Page](http://nikeshbajaj.github.io/Linear_Feedback_Shift_Register/)**
### **[PyPi - project](https://pypi.org/project/pylfsr/)**
### **[Documentation](https://linear-feedback-shift-register.readthedocs.io/en/latest/index.html)** 


<p align="center">
  <img src="https://raw.githubusercontent.com/nikeshbajaj/Linear_Feedback_Shift_Register/master/images/LFSR.jpg" width="500"/>
</p>


# Python


### Requirement : *numpy*

## Installation

### with pip

```
pip install pylfsr
```

### Build from the source
Download the repository or clone it with git, after cd in directory build it from source with

```
python setup.py install
```

## Examples
### **Example 1**: 5-bit LFSR with feedback polynomial *x^5 + x^2 + 1*

```
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
```


```
L.next()
L.runKCycle(10)
L.runFullCycle()
L.info()
```

### Example 2**: 5-bit LFSR with custom state and feedback polynomial

```
state = [0,0,0,1,0]
fpoly = [5,4,3,2]
L = LFSR(fpoly=fpoly,initstate =state, verbose=True)
L.info()
tempseq = L.runKCycle(10)
L.set(fpoly=[5,3])
```

### Example 3**: 23-bit LFSR with custom state and feedback polynomial

```
L = LFSR(fpoly=[23,18],initstate ='random',verbose=True)
L.info()
L.runKCycle(10)
L.info()
seq = L.seq
```

### Example 4**: Get the feedback polynomial or list
Reference : http://www.partow.net/programming/polynomials/index.html

```
L = LFSR()
# list of 5-bit feedback polynomials
fpoly = L.get_fpolyList(m=5)

# list of all feedback polynomials as a dictionary
fpolyDict = L.get_fpolyList()
```


### Changing feedback polynomial in between 
```
L.changeFpoly(newfpoly =[23,14],reset=False)
seq1 = L.runKCycle(20)

# Change after 20 clocks
L.changeFpoly(newfpoly =[23,9],reset=False)
seq2 = L.runKCycle(20)
```

### For A5/1 GSM Stream cipher generator
Reference Article: **Enhancement of A5/1**: https://doi.org/10.1109/ETNCC.2011.5958486

```
# Three LFSRs initialzed with 'ones' though they are intialized with encription key
R1 = LFSR(fpoly = [19,18,17,14])
R2 = LFSR(fpoly = [23,22,21,8])
R3 = LFSR(fpoly = [22,21])

# clocking bits
b1 = R1.state[8]
b2 = R1.state[10]
b3 = R1.state[10]

```
_______________________________________________________________________________________________

# MATLAB

Folder : https://github.com/Nikeshbajaj/Linear_Feedback_Shift_Register/tree/master/matlabfiles

**Description**
Genrate randon binary sequence using LFSR for any given feedback taps (polynomial), 
This will also check Three fundamental Property of LFSR 
1. Balance Property 
2. Runlength Property 
3. Autocorrelation Property

**This MATLAB Code work for any length of LFSR with given taps (feedback polynomial) -Universal, There are three files LFSRv1.m an LFSRv2.m, LFSRv3.m**

### LFSRv1
This function will return all the states of LFSR and will check Three fundamental Property of LFSR 
(1) Balance Property (2) Runlength Property (3) Autocorrelation Property

#### EXAMPLE
```
s=[1 1 0 0 1] 
t=[5 2]
[seq c] =LFSRv1(s,t)
```

### LFSRv2
This function will return only generated sequence will all the states of LFSR, no verification of properties are done
here. Use this function to avoid verification each time you execute the program.
#### EXAMPLE
```
s=[1 1 0 0 1] 
t=[5 2]
[seq c] =LFSRv2(s,t)
```

### LFSRv3 (faster)
*seq = LFSRv3(s,t,N)*
this function generates N bit sequence only. This is faster then other two functions, as this does not gives each state of LFSR

#### EXAMPLE
```
s=[1 1 0 0 1]  
t=[5 2]
seq =LFSRv3(s,t,50)
```



## Tips
* If you want to use this function in middle of any program, use LFSRv2 or LFSRv1 with verification =0. 
* If you want to make it fast for long length of LFSR,use LFSRv3.m 

______________________________________

# Contacts:

If any doubt, confusion or feedback please contact me
* **Nikesh Bajaj**
* http://nikeshbajaj.in
* n.bajaj@qmul.ac.uk
* bajaj[dot]nikkey [AT]gmail[dot]com
### PhD Student: Queen Mary University of London & University of Genoa
______________________________________

