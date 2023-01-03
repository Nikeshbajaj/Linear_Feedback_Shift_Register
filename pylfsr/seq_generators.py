'''
Sequence Generators based on LFSR
---------------------------
Author @ Nikesh Bajaj
Date: 03 Jan 2023
Version : 1.0.7
Github :  https://github.com/Nikeshbajaj/Linear_Feedback_Shift_Register
Contact: n.bajaj@qmul.ac.uk
'''

from __future__ import absolute_import, division, print_function
name = "LFSR | Generators"
import sys

if sys.version_info[:2] < (3, 3):
    old_print = print
    def print(*args, **kwargs):
        flush = kwargs.pop('flush', False)
        old_print(*args, **kwargs)
        if flush:
            file = kwargs.get('file', sys.stdout)
            # Why might file=None? IDK, but it works for print(i, file=None)
            file.flush() if file is not None else sys.stdout.flush()


from .pylfsr import LFSR
from .pylfsr import *
from .utils import deprecated, progbar

class A5_1():
	'''
	A5/1 GSM Stream Cipher
	----------------------
	#TODO
		1.doc
		2.check the output sequence
	Ref:  https://en.wikipedia.org/wiki/A5/1

	Example
	--------

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

	'''
	def __init__(self,key='random',k1='ones',k2='random',k3='ones',counter_start_zero=True):

	    self.M1,self.M2,self.M3 =19,22,23
	    self.M = self.M1+self.M2+self.M3
	    self.counter_start_zero = counter_start_zero


	    if key is not None:
	        key = self.key_frmt(self.M,key)
	        assert len(key)==self.M
	        #key should be of length = 19+22+23 for three LFSRs

	        self.k1 = key[:self.M1]
	        self.k2 = key[self.M1:self.M1+self.M2]
	        self.k3 = key[self.M1+self.M2:]

	        assert len(self.k1)==self.M1 and len(self.k2)==self.M2 and len(self.k3)==self.M3
	        self.key = ''.join(key.copy().astype(str))

	    else:
	        self.k1 = self.key_frmt(n=self.M1,ktype=k1)
	        self.k2 = self.key_frmt(n=self.M2,ktype=k2)
	        self.k3 = self.key_frmt(n=self.M3,ktype=k3)
	        assert len(self.k1)==self.M1 and len(self.k2)==self.M2 and len(self.k3)==self.M3

	        self.key = ''.join([''.join(k.copy().astype(str)) for k in [self.k1, self.k2, self.k3]])


	    self.R1 = LFSR(initstate=self.k1, fpoly = [19,18,17,14],counter_start_zero=counter_start_zero)
	    self.R2 = LFSR(initstate=self.k2, fpoly = [22,21],counter_start_zero=counter_start_zero)
	    self.R3 = LFSR(initstate=self.k3, fpoly = [23,22,21,8],counter_start_zero=counter_start_zero)
	    self.state = np.r_[self.R1.state, self.R2.state,self.R3.state]

	    # clocking bits
	    self.c1 = self.R1.state[8]
	    self.c2 = self.R2.state[10]
	    self.c3 = self.R3.state[10]

	    self.count = 0
	    self.seq = np.array([])
	    self.outbit = -1
	    self.clock_bit = -1



	def key_frmt(self,n,ktype):
		if isinstance(ktype, str):
		    if ktype == 'ones':
		        ikey = np.ones(n).astype(int)
		    elif ktype == 'random' or ktype == 'rand':
		        ikey = np.random.randint(0, 2,n).astype(int)
		    elif len(ktype)==n:
		        ikey = np.array([int(b) for b in ktype]).astype(int)
		    else: raise Exception('Unknown initial state')
		    return ikey
		elif isinstance(ktype,list):
		    return np.array(ktype)
		elif isinstance(ktype,np.ndarray):
		    return ktype
		else:
		    raise Exception('Unknown key type one of [binary string, list, np.array]')

	def next(self):
		'''
		#TODO check the output sequence
		'''
		# clocking bits

		if self.count:
			if self.c1==self.clock_bit: self.R1.next()
			if self.c2==self.clock_bit: self.R2.next()
			if self.c3==self.clock_bit: self.R3.next()

		self.state = np.r_[self.R1.state, self.R2.state,self.R3.state]
		self.outbit = np.logical_xor(np.logical_xor(self.R1.state[-1],self.R2.state[-1]),self.R3.state[-1])*1

		self.seq  = np.append(self.seq, self.outbit).astype(int)

		self.count+=1

		self.c1 = self.R1.state[8]
		self.c2 = self.R2.state[10]
		self.c3 = self.R3.state[10]
		self.clock_bit = (self.c1+self.c2+self.c3 > 1)*1
		return self.outbit

	def getLastbits(self):
	    return [self.R1.state[-1],self.R2.state[-1],self.R3.state[-1]]
	def getCbits(self):
	    return [self.R1.state[8],self.R2.state[10],self.R3.state[10]]
	def getSeq(self):
	    return ''.join(self.seq.copy().astype(str))
	def getState(self):
	    return ''.join(self.state.copy().astype(str))
	def arr2str(self,arr):
		return ''.join(arr.copy().astype(str))
	def runKCycle(self, k):
	    '''
	    Run k cycles and update all the Parameters

	    Parameters
	    ----------
	    k : int

	    Returns
	    -------
	    tempseq : shape =(k,), output binary sequence of k cycles
	    '''
	    tempseq = [self.next() for i in range(k)]
	    return np.array(tempseq)

class Geffe():
	'''
	Geffe Generator
	---------------
	Combining K LFSR in non-linear manner
	linear complexity

	Parameters
	----------
	K+1 LFSRs

	kLFSR_list: list of K LFSR, output of one of these is choosen at any time, depending on cLFSR
	cLFSR: clocking LFSR

	K should be power of 2. 2,4,8,... 128

	Ref: Schneier, Bruce. Applied cryptography: protocols, algorithms, and source code in C. john wiley & sons, 2007.
	Chaper 16


	Example
	--------

	import numpy as np
	import matplotlib.pyplot as plt
	from pylfsr import Geffe, LFSR

	kLFSR = [LFSR(initstate='random') for _ in range(8)]
	cLFSR = LFSR(initstate='random')

	GG = Geffe(kLFSR_list=kLFSR, cLFSR=cLFSR)

	print('key: ',GG.getState())
	print()
	for _ in range(50):
	    print(GG.count,GG.m_count,GG.outbit_k,GG.sel_k,GG.outbit,GG.getSeq(),sep='\t')
	    GG.next()

	GG.runKCycle(1000)
	GG.getSeq()
	'''
	def __init__(self,kLFSR_list,cLFSR):

	    self.K = len(kLFSR_list)
	    assert isinstance(cLFSR,LFSR)
	    assert [isinstance(Rk,LFSR) for Rk in kLFSR_list]
	    assert self.K>1
	    assert (self.K & (self.K-1) == 0) and self.K != 0
	    #K (list of LFSR) should be power of 2

	    self.m = np.log2(self.K).astype(int)

	    self.kLFSR_list = kLFSR_list
	    self.cLFSR = cLFSR

	    self.count=0
	    self.m_count =0
	    self.seq =np.array([])
	    self.outbit = -1
	    self.sel_k = -1
	    self.outbit_k = [Rk.state[-1] for Rk in self.kLFSR_list]
	    self.state = np.hstack([R.state for R in self.kLFSR_list+[self.cLFSR]])
	    self.state_k = np.hstack([R.state for R in self.kLFSR_list])
	    self.state_c = self.cLFSR.state


	def getSel(self):
	    sel =  self.cLFSR.runKCycle(self.m)
	    self.m_count+=self.m
	    sel = ''.join(sel.astype(str))
	    return int(sel, 2)
	def next(self):
	    if self.count:
	        _ = [Rk.next() for Rk in self.kLFSR_list]

	    self.outbit_k = [Rk.state[-1] for Rk in self.kLFSR_list]
	    self.sel_k = self.getSel()
	    self.outbit = self.outbit_k[self.sel_k]

	    self.seq = np.append(self.seq,self.outbit).astype(int)

	    self.state = np.hstack([R.state for R in self.kLFSR_list+[self.cLFSR]])
	    self.state_k = np.hstack([R.state for R in self.kLFSR_list])
	    self.state_c = self.cLFSR.state

	    self.count+=1
	    return self.outbit

	def getSeq(self):
	    return ''.join(self.seq.copy().astype(str))
	def getState(self):
	    return ''.join(self.state.copy().astype(str))
	def arr2str(self,arr):
		return ''.join(arr.copy().astype(str))

	def runKCycle(self, k):
	    '''
	    Run k cycles and update all the Parameters

	    Parameters
	    ----------
	    k : int

	    Returns
	    -------
	    tempseq : shape =(k,), output binary sequence of k cycles
	    '''
	    tempseq = [self.next() for i in range(k)]
	    return np.array(tempseq)

class Geffe3():
    '''
    Geffe Generator
    ---------------
    Combining three LFSR in non-linear manner
    linear complexity: If the LFSRs have lengths n1, n2, and n3, respectively, then the linear
    complexity of the generator is  = (n1 + 1)n2 + n1n3

    output bit at any time is

    b = (r1 ^ r2) • ((¬ r1) ^ r3)

    where r1,r2,r3 are the outbit of three LFSRs respectively

    Ref: Schneier, Bruce. Applied cryptography: protocols, algorithms, and source code in C. john wiley & sons, 2007.
    Chaper 16

    '''
    def __init__(self,R1,R2,R3):

        assert isinstance(R1,LFSR)
        assert isinstance(R2,LFSR)
        assert isinstance(R3,LFSR)

        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.count=0
        self.seq =[]
        self.state = np.r_[self.R1.state, self.R2.state,self.R3.state]
        self.next()

    def next(self):
        if self.count:
            self.R1.next()
            self.R2.next()
            self.R3.next()
        self.r1 = self.R1.state[-1]
        self.r2 = self.R2.state[-1]
        self.r3 = self.R3.state[-1]

        b1 = np.logical_and(self.r1,self.r2)
        b2 = np.logical_and(not(self.r1),self.r2)
        self.outbit = np.logical_xor(b1,b2)*1

        self.seq = np.append(self.seq,self.outbit).astype(int)

        self.state = np.r_[self.R1.state, self.R2.state,self.R3.state]
        self.count+=1
        return self.outbit
    def getSeq(self):
        return ''.join(self.seq.copy().astype(str))
    def getState(self):
        return ''.join(self.state.copy().astype(str))
    def arr2str(self,arr):
    	return ''.join(arr.copy().astype(str))

    def runKCycle(self, k):
        '''
        Run k cycles and update all the Parameters

        Parameters
        ----------
        k : int

        Returns
        -------
        tempseq : shape =(k,), output binary sequence of k cycles
        '''
        tempseq = [self.next() for i in range(k)]
        return np.array(tempseq)

if __name__ == '__main__':
	import doctest
	doctest.testmod()
