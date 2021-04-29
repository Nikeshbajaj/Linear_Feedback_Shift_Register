import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
'''
Author @ Nikesh Bajaj
first created : Date: 22 Oct 2017
Updated on : 29 Apr 2021
           : fixed bugs (1) not counting first outbit correctly (2) Exception in info method
		   : added test properties (1) Balance (2) Runlength (3) Autocorrelation
           : improved functionalities
           : added Viz function
           : added A5/1 and Geffe Generator
Version : 1.0.6
Contact: n.bajaj@qmul.ac.uk
       : http://nikeshbajaj.in
'''

class LFSR():
	'''
	Linear Feedback Shift Register

	class LFSR(fpoly=[5,2],initstate='ones',verbose=False)

	Parameters
	----------
	initstate : binary np.array (row vector) or str ='ones' or 'random', optional (default = 'ones'))
		Initial state of LFSR. initstate can not be all zeros.
		default ='ones'
			Initial state is intialized with ones and length of register is equal to
			degree of feedback polynomial
		if state='rand'
			Initial state is intialized with random binary sequence of length equal to
			degree of feedback polynomial

	fpoly : List, optional (default=[5,2])
		Feedback polynomial, it has to be primitive polynomial of GF(2) field, for valid output of LFSR
		to get the list of feedback polynomials check method 'get_fpolyList'
		or check Refeferece:
		Ref: List of some primitive polynomial over GF(2)can be found at
		http://www.partow.net/programming/polynomials/index.html
		http://www.ams.org/journals/mcom/1962-16-079/S0025-5718-1962-0148256-1/S0025-5718-1962-0148256-1.pdf
		http://poincare.matf.bg.ac.rs/~ezivkovm/publications/primpol1.pdf
	counter_start_zero: bool (default = True), whether to start counter with 0 or 1. If True, initial outbit is
	    set to -1, so is feedbackbit, until first .next() clock is excecuted. This initial output is not stacked in
		seq. The output sequence should be same, in anycase, for example if you need run 10 cycles, using runKCycle(10) methed.
	Verbose : boolean, optional (default=False)
		if True, state of LFSR will be printed at every cycle(iteration)

	Attributes
	----------
	count : int
		Count the cycle, starts with 0 if counter_start_zero True, else starts with 1
	seq   : np.array shape =(count,)
		Output sequence stored in seq since first cycle
		if -1, no cycle has been excecuted, count=0 when counter_start_zero is True
		else last bit of initial state

	outbit : binary bit
		Current output bit,
		Last bit of current state
		if -1, no cycle has been excecuted, count =0,  when counter_start_zero is True

	feedbackbit : binary bit
		if -1, no cycle has been excecuted, count =0,  when counter_start_zero is True
	M : int
		length of LFSR, M-bit LFSR

	expectedPeriod : int (also saved as T)
		Expected period of sequence
		if feedback polynomial is primitive and irreducible (as per reference)
		period will be 2^M -1
	T : int (also saved as expectedPeriod)
		Expected period of sequence
		if feedback polynomial is primitive and irreducible (as per reference)
		period will be 2^M -1
	feedpoly : str
		feedback polynomial


	Examples
	--------
	>>> import numpy as np
	>>> from pylfsr import LFSR

	## Example 1  ## 5 bit LFSR with x^5 + x^2 + 1
	>>> L = LFSR()
	>>> L.info()
	5 bit LFSR with feedback polynomial  x^5 + x^2 + 1
	Expected Period (if polynomial is primitive) =  31
	Current :
		State        :  [1 1 1 1 1]
		Count        :  0
		Output bit   :  -1
		feedback bit :  -1

	>>> L.next()
	1

	>>> L.runKCycle(10)
	array([1, 1, 1, 1, 0, 0, 1, 1, 0, 1])

	>>> L.runFullCycle()  # doctest: +NORMALIZE_WHITESPACE
	array([1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0,
       1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1])

	>>> L.info()  # doctest: +NORMALIZE_WHITESPACE
	5 bit LFSR with feedback polynomial  x^5 + x^2 + 1
	Expected Period (if polynomial is primitive) =  31
	Current :
	 State        :  [0 0 1 0 0]
	 Count        :  42
	 Output bit   :  1
	 feedback bit :  0
	 Output Sequence 111110011010010000101011101100011111001101

	>>> tempseq = L.runKCycle(10000)  # generate 10000 bits from current state

	## Example 2  ## 5 bit LFSR with custum state and feedback polynomial
	>>> state = np.array([0,0,0,1,0])
	>>> fpoly = [5,4,3,2]
	>>> L1 = LFSR(fpoly=fpoly,initstate =state, verbose=True)
	>>> L1.info()  # doctest: +NORMALIZE_WHITESPACE
	5 bit LFSR with feedback polynomial  x^5 + x^4 + x^3 + x^2 + 1
	Expected Period (if polynomial is primitive) =  31
	Current :
		State        :  [0 0 0 1 0]
		Count        :  0
		Output bit   :  -1
		feedback bit :  -1
	>>> tempseq = L1.runKCycle(10)
	S:  [0 0 0 1 0]
	S:  [1 0 0 0 1]
	S:  [1 1 0 0 0]
	S:  [1 1 1 0 0]
	S:  [0 1 1 1 0]
	S:  [1 0 1 1 1]
	S:  [1 1 0 1 1]
	S:  [1 1 1 0 1]
	S:  [1 1 1 1 0]
	S:  [1 1 1 1 1]
	>>> tempseq
	array([0, 1, 0, 0, 0, 1, 1, 1, 0, 1])

	>>>L1.set(fpoly=[5,3])

	## Example 3 ## TO visualize the process with 3-bit LFSR, with default counter_start_zero = True
	>>> state = [1,1,1]
	>>> fpoly = [3,2]
	>>> L = LFSR(initstate=state,fpoly=fpoly,counter_start_zero=True)
	>>> print('count \t state \t\toutbit \t seq')
	>>> print('-'*50)
	>>> for _ in range(15):
	>>>    print(L.count,L.state,'',L.outbit,L.seq,sep='\t')
	>>>    L.next()
	>>> print('-'*50)
	>>> print('Output: ',L.seq)
	count 	 state 		outbit 	 seq
	--------------------------------------------------
	0		[1 1 1]		-1	[-1]
	1		[0 1 1]		1	[1]
	2		[0 0 1]		1	[1 1]
	3		[1 0 0]		1	[1 1 1]
	4		[0 1 0]		0	[1 1 1 0]
	5		[1 0 1]		0	[1 1 1 0 0]
	6		[1 1 0]		1	[1 1 1 0 0 1]
	7		[1 1 1]		0	[1 1 1 0 0 1 0]
	8		[0 1 1]		1	[1 1 1 0 0 1 0 1]
	9		[0 0 1]		1	[1 1 1 0 0 1 0 1 1]
	10		[1 0 0]		1	[1 1 1 0 0 1 0 1 1 1]
	11		[0 1 0]		0	[1 1 1 0 0 1 0 1 1 1 0]
	12		[1 0 1]		0	[1 1 1 0 0 1 0 1 1 1 0 0]
	13		[1 1 0]		1	[1 1 1 0 0 1 0 1 1 1 0 0 1]
	14		[1 1 1]		0	[1 1 1 0 0 1 0 1 1 1 0 0 1 0]
	--------------------------------------------------
	Output:  [1 1 1 0 0 1 0 1 1 1 0 0 1 0 1]

	## Example 4.1 ## To visualize the process with 3-bit LFSR, with counter_start_zero = False
	>>> state = [1,1,1]
	>>> fpoly = [3,2]
	>>> L = LFSR(initstate=state,fpoly=fpoly,counter_start_zero=False)
	>>> print('count \t state \t\toutbit \t seq')
	>>> print('-'*50)
	>>> for _ in range(15):
	>>>    print(L.count,L.state,'',L.outbit,L.seq,sep='\t')
	>>>    L.next()
	>>> print('-'*50)
	>>> print('Output: ',L.seq)
	count 	 state 		outbit 	 seq
	--------------------------------------------------
	1	[1 1 1]		1	[1]
	2	[0 1 1]		1	[1 1]
	3	[0 0 1]		1	[1 1 1]
	4	[1 0 0]		0	[1 1 1 0]
	5	[0 1 0]		0	[1 1 1 0 0]
	6	[1 0 1]		1	[1 1 1 0 0 1]
	7	[1 1 0]		0	[1 1 1 0 0 1 0]
	8	[1 1 1]		1	[1 1 1 0 0 1 0 1]
	9	[0 1 1]		1	[1 1 1 0 0 1 0 1 1]
	10	[0 0 1]		1	[1 1 1 0 0 1 0 1 1 1]
	11	[1 0 0]		0	[1 1 1 0 0 1 0 1 1 1 0]
	12	[0 1 0]		0	[1 1 1 0 0 1 0 1 1 1 0 0]
	13	[1 0 1]		1	[1 1 1 0 0 1 0 1 1 1 0 0 1]
	14	[1 1 0]		0	[1 1 1 0 0 1 0 1 1 1 0 0 1 0]
	--------------------------------------------------
	Output:  [1 1 1 0 0 1 0 1 1 1 0 0 1 0 1]

	## Example 4.2 ## To visualize LFSR
	L.Viz(show=False, show_labels=False,title='R1')

	## Example 5  ## 23 bit LFSR with custum state and feedback polynomial

	>>> fpoly = [23,19]
	>>> L1 = LFSR(fpoly=fpoly,initstate ='ones', verbose=False)
	>>> L1.info()
	23 bit LFSR with feedback polynomial  x^23 + x^19 + 1
	Expected Period (if polynomial is primitive) =  8388607
	Current :
	 State        :  [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]
	 Count        :  0
	 Output bit   :  -1
	 feedback bit :  -1

	>>> seq = L1.runKCycle(100)
	>>> seq
	array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
       1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
       1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
       1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1])

	>>> L.changeFpoly(newfpoly =[23,21])
	>>> seq1 = L.runKCycle(20)

	##  Example 6 ## testing the properties
	>>> state = [1,1,1,1,0]
	>>> fpoly = [5,3]
	>>> L = LFSR(initstate=state,fpoly=fpoly)
	>>> L.info()
	5 bit LFSR with feedback polynomial  x^5 + x^3 + 1
	Expected Period (if polynomial is primitive) =  31
	Current :
	 State        :  [1 1 1 1 0]
	 Count        :  0
	 Output bit   :  -1
	 feedback bit :  -1

	>>>result  = L.test_properties(verbose=1)
	1. Periodicity
	------------------
	 - Expected period = 2^M-1 = 31
	 - Pass?:  True

	2. Balance Property
	-------------------
	 - Number of 1s = Number of 0s+1 (in a period): (N1s,N0s) =  (16, 15)
	 - Pass?:  True

	3. Runlength Property
	-------------------
	 - Number of Runs in a period should be of specific order, e.g. [4,2,1,1]
	 - Runs:  [8 4 2 1 1]
	 - Pass?:  True

	4. Autocorrelation Property
	-------------------
	 - Autocorrelation of a period should be noise-like, specifically, 1 at k=0, -1/m everywhere else
	 - Pass?:  True

	==================
	Passed all the tests
	==================


	>>> p = L.getFullPeriod()
	>>> p
	array([0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0,
       0, 1, 0, 0, 1, 0, 1, 1, 0])

	>>> L.balance_property(p.copy())
	(True, (16, 15))

	>>> L.runlength_property(p.copy())
	(True, array([8, 4, 2, 1, 1]))

	>>> L.autocorr_property(p.copy())[0]
	True

	##  Example 7 ## testing the properties for non-primitive polynomial
	>>> state = [1,1,1,1,0]
	>>> fpoly = [5,1]
	>>> L = LFSR(initstate=state,fpoly=fpoly)
	>>> result = L.test_properties(verbose=1)
	1. Periodicity
	------------------
	 - Expected period = 2^M-1 = 31
	 - Pass?:  False

	2. Balance Property
	-------------------
	 - Number of 1s = Number of 0s+1 (in a period): (N1s,N0s) =  (17, 14)
	 - Pass?:  False

	3. Runlength Property
	-------------------
	 - Number of Runs in a period should be of specific order, e.g. [4,2,1,1]
	 - Runs:  [10  2  1  1  2]
	 - Pass?:  False

	4. Autocorrelation Property
	-------------------
	 - Autocorrelation of a period should be noise-like, specifically, 1 at k=0, -1/m everywhere else
	 - Pass?:  False

	==================
	Failed one or more tests, check if feedback polynomial is primitive polynomial
	==================
	'''

	def __init__(self, fpoly=[5, 2], initstate='ones', verbose=False,counter_start_zero=True):
		if isinstance(initstate, str):
			if initstate == 'ones':
				initstate = np.ones(np.max(fpoly))
			elif initstate == 'random':
				initstate = np.random.randint(0, 2, np.max(fpoly))
			else:
				raise Exception('Unknown intial state')
		if isinstance(initstate, list):
			initstate = np.array(initstate)

		self.initstate = initstate
		self.fpoly = fpoly
		self.state = initstate.astype(int)
		#self.skip_first = skip_first
		self.counter_start_zero = counter_start_zero
		self.count = 0 if counter_start_zero else 1
		self.seq =  np.array([-1]) if counter_start_zero else np.array([self.state[-1]])
		self.outbit = -1 if counter_start_zero else self.state[-1]
		self.feedbackbit = -1 if counter_start_zero else self.state[-1]
		self.verbose = verbose
		self.M = self.initstate.shape[0]
		self.expectedPeriod = 2**self.M - 1
		self.T = 2**self.M - 1
		self.fpoly.sort(reverse=True)
		feed = ' '
		for i in range(len(self.fpoly)):
			feed = feed + 'x^' + str(self.fpoly[i]) + ' + '
		feed = feed + '1'
		self.feedpoly = feed

		self.check()

	def info(self):
		'''
		Display the information about LFSR with current state of variables
		'''
		print('%d bit LFSR with feedback polynomial %s' % (self.M, self.feedpoly))
		print('Expected Period (if polynomial is primitive) = ', self.expectedPeriod)
		print('Current :')
		print(' State        : ', self.state)
		print(' Count        : ', self.count)
		print(' Output bit   : ', self.outbit)
		print(' feedback bit : ', self.feedbackbit)
		if self.count > 0 and self.count < 1000:
			print(' Output Sequence %s' % (''.join([str(int(x)) for x in self.seq])))

	def check(self):
		'''
		Check if
		- degree of feedback polynomial <= length of LFSR >=1
		- given intistate of LFSR is correct
		'''
		if np.max(self.fpoly) > self.initstate.shape[0] or np.min(self.fpoly) < 1 or len(self.fpoly) < 2:
			raise ValueError('Wrong feedback polynomial')
		if len(self.initstate.shape) > 1 and (self.initstate.shape[0] != 1 or self.initstate.shape[1] != 1):
			raise ValueError('Size of intial state vector should be one diamensional')
		else:
			self.initstate = np.squeeze(self.initstate)
		assert np.sum(self.initstate>1) + np.sum(self.initstate<0)==0 # test if initial state is binary, 1s and 0s

	def set(self, fpoly, state='ones'):
		'''
		Set feedback polynomial and state

		Parameters
		----------
		fpoly : list
			feedback polynomial like [5,4,3,2]

		state : np.array, like np.array([1,0,0,1,1])
			default ='ones'
				Initial state is intialized with ones and length of register is equal to
				degree of feedback polynomial
			if state='rand'
				Initial state is intialized with random binary sequence of length equal to
				degree of feedback polynomial
		'''
		self.__init__(fpoly=fpoly, initstate=state)

	def reset(self):
		'''
		Reseting LFSR to its initial state and count
		'''
		self.__init__(initstate=self.initstate, fpoly=self.fpoly,counter_start_zero=self.counter_start_zero )

	def changeFpoly(self, newfpoly, reset=False):
		'''
		Changing Feedback polynomial :  Useful to change feedback polynomial in between as in A5/1 stream cipher

		Parameters
		----------
		newfpoly : list like, [5,4,2,1]
			changing the feedback polynomial

		reset : boolean default=False
			if True, reset all the Parameters: count and seq etc ....
			if False, leave the LFSR as it is only change the feedback polynomial
			for further use, as used in
			'Enhancement of A5/1: Using variable feedback polynomials of LFSR'
			 https://doi.org/10.1109/ETNCC.2011.5958486
		'''
		newfpoly.sort(reverse=True)
		self.fpoly = newfpoly
		feed = ' '
		for i in range(len(self.fpoly)):
			feed = feed + 'x^' + str(self.fpoly[i]) + ' + '
		feed = feed + '1'
		self.feedpoly = feed

		self.check()
		if reset:
			self.reset()

	def next(self):
		'''
		Run one cycle on LFSR with given feedback polynomial and
		update the count, state, feedback bit, output bit and seq

		Returns
		-------
		output bit : binary
		'''
		if self.verbose:
			print('S: ', self.state)
		if self.counter_start_zero:
			self.outbit = self.state[-1]
			if self.count ==0:
				self.seq = np.array([self.state[-1]])
			else:
				self.seq  = np.append(self.seq, self.state[-1])

		b = np.logical_xor(self.state[self.fpoly[0] - 1], self.state[self.fpoly[1] - 1])
		if len(self.fpoly) > 2:
			for i in range(2, len(self.fpoly)):
				b = np.logical_xor(self.state[self.fpoly[i] - 1], b)

		#self.outbit = self.state[-1]
		self.state = np.roll(self.state, 1)
		self.feedbackbit = b * 1
		self.state[0] = self.feedbackbit

		if not(self.counter_start_zero):
			self.outbit = self.state[-1]
			if self.count ==0:
				self.seq = np.array([self.state[-1]])
			else:
				self.seq  = np.append(self.seq, self.state[-1])

		self.count += 1

		return self.outbit

	def runFullCycle(self):
		'''
		Run a full cycle (T = 2^M-1) on LFSR from current state

		Returns
		-------
		seq : binary output sequence since start: shape = (count,)
		'''
		temp = [self.next() for i in range(self.expectedPeriod)]
		return self.seq

	def getFullPeriod(self):
		'''
		Get a seq of a full period from LSFR, by executing next() method T times.
		The current state of LFSR is used to generate T bits.

		Returns
		-------
		seq (T bits), binary output sequence of last T bits
		'''
		seq = np.array([self.next() for i in range(self.expectedPeriod)])
		return seq

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

	def _loadFpolyList(self):
		import os
		fname = 'primitive_polynomials_GF2_dict.txt'
		fname = os.path.join(os.path.dirname(__file__), fname)
		try:
			f = open(fname, "rb")
			lines = f.readlines()
			f.close()
			self.fpolyList = eval(lines[0].decode())
		except:
			raise Exception("File named:'{}' Not Found!!! \n try again, after downloading file from github save it in lfsr directory".format(fname))

	def get_fpolyList(self,m=None):
		'''
		Get the list of primitive polynomials as feedback polynomials for m-bit LFSR.
		Only list of primary primitive polynomials are retuned, not full list (half list), since for each primary primitive polynomial
		an image polymial can be computed using 'get_Ifpoly' method

		Parameters
		----------
		m: 1<int<32, if None, list of feedback polynomials for 1 < m < 32 is return as a dictionary

		Returns
		-------
		fpoly_list: list of polynomial if m is not None else a dictionary

		'''
		self._loadFpolyList()
		if m is None:
			return self.fpolyList
		elif type(m)== int and m > 1 and m < 32:
			return self.fpolyList[m]
		else:
			print('Wrong input m. m should be int 1 < m < 32 or None')

	def get_Ifpoly(self,fpoly):
		'''
		Get image of feebback polynomial
		Get the image of primitive polynomial
		Parameters
		----------
		fpoly: polynomial as list e.g. [5,2] for x^5 + x^2 + 1
		     : should be a valid primitive polynomial

		Returns
		-------
		ifpoly: polynomial as list e.g. [5,3] for x^5 + x^3 + 1

		'''
		if isinstance(fpoly, list) or (isinstance(fpoly, numpy.ndarray) and len(fpoly.shape)==1):
			fpoly = list(fpoly)
			fpoly.sort(reverse=True)
			ifpoly = [fpoly[0]] +[fpoly[0]-ff for ff in fpoly[1:]]
			ifpoly.sort(reverse=True)
			return ifpoly
		else:
			print('Not a valid form of feedback polynomial')

	def test_properties(self,verbose=1):
		p1 = self.getFullPeriod()
		p2 = self.getFullPeriod()
		r1 = np.mean(p1==p2)==1

		r2, (N1s,N0s) = self.balance_property(p1.copy())

		r3,runs = self.runlength_property(p1.copy(),verbose=0)

		r4,(shift,rxx) = self.autocorr_property(p1.copy(),plot=False)

		result = bool(np.prod([r1,r2,r3,r4]))

		if verbose:
			print('1. Periodicity')
			print('------------------')
			print(' - Expected period = 2^M-1 =',self.expectedPeriod)
			print(' - Pass?: ',r1)
			print('')
			print('2. Balance Property')
			print('-------------------')
			print(' - Number of 1s = Number of 0s+1 (in a period): (N1s,N0s) = ',(N1s, N0s))
			print(' - Pass?: ',r2)
			print('')
			print('3. Runlength Property')
			print('-------------------')
			print(' - Number of Runs in a period should be of specific order, e.g. [4,2,1,1]')
			print(' - Runs: ',runs)
			print(' - Pass?: ',r3)
			print('')
			print('4. Autocorrelation Property')
			print('-------------------')
			print(' - Autocorrelation of a period should be noise-like, specifically, 1 at k=0, -1/m everywhere else')
			if verbose>1:
			    print(' - Rxx(k): ',rxx)
			    try:
			        import matplotlib.pyplot as plt
			    except:
			        raise('Error loading matplotlib, either install it or set verbose<2')
			    plt.plot(shift,rxx)
			    plt.xlabel('shift (k)')
			    plt.ylabel(r'$R_{xx}(k)$')
			    plt.axhline(y=0,color='k',ls=':',lw=0.5)
			    plt.xlim(shift[0],shift[-1])
			    plt.title('Autocorrelation')
			    plt.grid(alpha=0.4)
			    plt.show()
			print(' - Pass?: ',r4)
			print('\n\n')
			print('==================')
			if result:
				print('Passed all the tests')
			else:
				print('Failed one or more tests, check if feedback polynomial is primitive polynomial')
			print('==================')
		return result

	def test_p(self,p,verbose=1):
		'''
		Test all the three properties for seq p :
			(1) Balance Property
			(2) Runlegth Property
			(3) Autocorrelation Property


		Parameters
		----------
		p :  array-like, a sequence of a period from LFSR
		verbose = 0 : no printing details
		        = 1 : print details
				= 2 : print and plot more details
		Returns
		-------
		result: bool,  True if all three are satisfied else False
		'''
		r1,(N1s,N0s) = self.balance_property(p.copy())
		r2,runs = self.runlength_property(p.copy(),verbose=0)
		r3,(shift,rxx) = self.autocorr_property(p.copy(),plot=False)
		result = bool(np.prod([r1,r2,r3]))
		if verbose:
			print('1. Balance Property')
			print('-------------------')
			print(' - Number of 1s = Number of 0s+1 (in a period): (N1s,N0s) = ',(N1s, N0s))
			print(' - Pass?: ',r1)
			print('')
			print('2. Runlength Property')
			print('-------------------')
			print(' - Number of Runs in a period should be of specific order, e.g. [4,2,1,1]')
			print(' - Runs: ',runs)
			print(' - Pass?: ',r2)
			print('')
			print('3. Autocorrelation Property')
			print('-------------------')
			print(' - Autocorrelation of a period should be noise-like, specifically, 1 at k=0, -1/m everywhere else')
			if verbose>1:
				print(' - Rxx(k): ',rxx)
				try:
					import matplotlib.pyplot as plt
				except:
					raise('Error loading matplotlib, either install it or set verbose<2')
				plt.plot(shift,rxx)
				plt.xlabel('shift (k)')
				plt.ylabel(r'$R_{xx}(k)$')
				plt.axhline(y=0,color='k',ls=':',lw=0.5)
				plt.xlim(shift[0],shift[-1])
				plt.title('Autocorrelation')
				plt.grid(alpha=0.4)
				plt.show()
			print(' - Pass?: ',r3)
			print('\n\n')
			print('==================')
			if result:
				print('Passed all three tests')
			else:
				print('Failed one or more tests')
			print('==================')

		return result

	def balance_property(self,p):
		'''
		Balance Property: In a period of LFSR with a valid feedback polynomial,
		the number of 1s should be equal to number of 0s +1
							''     N1s == N0s + 1   ''
		Test balance property for a given full period of seq, p.

		Parameters
		----------
		p:  array-like, a sequence of a period from LFSR


		Returns
		-------
		result: bool, True if seq p satisfies Balance Property else False
		(N1s, N0s): tuple, number of 1s and number of 0s
		'''
		N1s = np.sum(p==1)
		N0s = np.sum(p==0)
		result = N1s == N0s+1
		return result, (N1s,N0s)

	def runlength_property(self,p,verbose=0):
		'''
		Run Length Property: In a period of LSFR with valid feedback polynomial,
		the number of runs of different length are in specific order.
			''
			number of (M-k) bit runs  =  ⌈ 2^(k-1) ⌉  , for k = 0 to M-1
			''
		where ⌈ ⌉ is a ceiling function
		That is, for M bit LFSR,
		    - number of M bit runs     : 1
			- number of (M-1) bit runs : 1
			- number of (M-2) bit runs : 2
			- number of (M-3) bit runs : 4
			...
			so on

		Parameters
		----------
		p:  array-like, a sequence of a period from LFSR

		Returns
		-------
		result:  bool, True if seq p satisfies Run Length Property else False
		runs: list, list of runs
		'''
		T = len(p)
		if verbose>1: print(p)
		while p[0]==p[-1]: p = np.roll(p,1)

		if verbose>1: print(p)
		if p[-1]==0:
		    p = np.append(p,1)
		else:
		    p = np.append(p,0)
		if verbose>1: print(p)

		i=0
		runs = np.zeros(T).astype(int)
		for k in range(T):
		    if p[k]==p[k+1]:
		        i=i+1
		    else:
		        runs[i]=runs[i]+1
		        i=0
		if verbose>1: print(runs)
		runs = runs[:max(np.where(runs)[0])+1]
		if verbose: print('Runs : ',runs)

		l = len(runs)
		pp=0
		for k in range(len(runs)-2):
		    if runs[k]==2*runs[k+1]:
		        pp=pp+1
		if runs[-2]==runs[-1]: pp=pp+1

		result = False

		if pp==len(runs)-1: result = True
		if verbose>1:
		    if result: print('Pass')
		    else: print('Fail')
		return result, runs

	def autocorr_property(self,p,plot=False):
		'''
		Autocorrelation Property: For sequence of period T of LSFR with valid feedback polynomial,
		the autocorrelation is a noise like, that is, 1 with zero (or T) lag (shift), -1/T (almost zero) else.

		unlike usual, for binary, the correlation value between two sequence of same length bx, by is computed as follow;
		match    = sum(bx == by) (number of mataches)
		mismatch = sum(bx!= by) (number of mismatches)
		''
		rxy =  (match - mismatch)/ length(bx)
		''

		Parameters
		----------
		p:  array-like, a sequence of a period from LFSR

		plot: bool (default False), if True, it will plot the autocorrelation function,
		    which will require matplotlib library. Turn it of if matplotlib is not installed

		Returns
		-------
		result: bool, True if seq p satisfies Autocorrelation Property else False
		(shift, rxx): tuple of sequence of shift corresponding autocorrelation values
		'''
		T = len(p)
		px = p.copy()
		rxx = np.zeros(2*T+1)
		for k in range(2*T+1):
		    py = np.roll(p.copy(),k)
		    r = px==py
		    rxx[k] = (np.sum(r==1) - np.sum(r==0))/T

		result = False
		if np.prod(np.isclose(rxx[1:T],-1/T)):
		    result = True

		shift = np.arange(-T,T+1)
		if plot:
		    try:
		        import matplotlib.pyplot as plt
		    except:
		        raise('Error loading matplotlib, either install it or set plot=False')
		    plt.plot(shift,rxx)
		    plt.xlabel('shift (k)')
		    plt.ylabel(r'$R_{xx}(k)$')
		    plt.axhline(y=0,color='k',ls=':',lw=0.5)
		    plt.xlim(shift[0],shift[-1])
		    plt.title('Autocorrelation')
		    plt.grid(alpha=0.4)
		    plt.show()
		return result, (shift,rxx)

	def getSeq(self):
		return ''.join(self.seq.copy().astype(str))
	def getState(self):
	    return ''.join(self.state.copy().astype(str))
	def arr2str(self,arr):
		return ''.join(arr.copy().astype(str))
	def Viz(self,ax=None,show=True,fs=25,show_labels=False,title='',title_loc='left',box_color='lightblue',alpha=0.5):
		'''
		ax: axis to plot, if None, new axis will be created, (default None)
		show: if True, plt.show() will be excecuted, (default True)
		fs:  fontsize (default 25)
		show_label: if true, will display names
		title: str, title of figure, default '',
		title_loc, alignment of title, 'left', 'right', 'center', (default 'left')
		'''
		state = self.state
		fpoly = self.fpoly
		seq = self.getSeq()
		outbit = self.outbit
		feedbit = self.feedbackbit
		PlotLFSR(state,fpoly,seq=seq,ob=outbit,fb=feedbit,fs=fs,ax=ax,show_labels=show_labels,title=title,title_loc=title_loc,box_color=box_color,alpha=alpha)
		if  show: plt.show()



def drawR(ax,x=0,y=0,s=1,alpha=0.5,color='lightblue'):
    rect = patches.Rectangle((x-s/2, y-s/2), s, s, linewidth=1, edgecolor='k', facecolor=color,alpha=alpha)
    ax.add_patch(rect)
def PlotLFSR(state,fpoly,seq='',ob=None,fb=None,fs=25,ax=None,show_labels=False,title='',title_loc='left',box_color='lightblue',alpha=0.5):
	'''
    -----  Plot LFSR ----
    state: current state of LFSR
    fpoly:  feedback polynomial of LFSR
    seq: str, output sequence
    ob: output bit
    fb: feedback bit
    ax: axis to plot, if None, new axis will be created, (default None)

	show: if True, plt.show() will be excecuted, (default True)
	fs:  fontsize (default 25)
	show_label: if true, will display names
	title: str, title of figure, default '',
	title_loc, alignment of title, 'left', 'right', 'center', (default 'left')
	box_color: color of register box, default='lightblue'
	'''
	M = len(state)
	ym = 3.5
	if ax is None:
	    fig, ax = plt.subplots(figsize=(M+5,ym))

	s=1
	xs = 3
	ys = ym-1
	last_x= xs

	for k in range(M):
	    x,y = xs+k,ys
	    ax.text(x,y,str(state[k]),ha='center',va = 'center',fontsize=fs)

	    if k==0:
	        x1, y1 = [x-1.5*s, x-s/2], [y, y]
	        ax.plot(x1, y1,marker = '>',color='k',markevery=(1,1),ms=10)

	    if k+1 in fpoly:
	        x1, y1 = [x, x], [y-s/2, y-1.5*s]
	        ax.plot(x1, y1,marker = '.',color='k')
	        ax.plot(x,y-1.5*s,marker = '+',color='b',ms=15,mew=3)
	        ax.plot(x,y-1.5*s,marker = 'o',color='b',ms=15,mfc='none',mew=2)
	        if last_x<x: last_x=x
	    drawR(ax,x=x,y=y,s=s,alpha=alpha,color=box_color)

    #if fb is not None: ax.text(xs-1.7*s,y,'fb = '+str(fb),fontsize=fs-7,va = 'bottom')
	if fb is not None:
	    if show_labels:
	        ax.text(xs-1.7*s,y,'fb = '+str(fb),fontsize=fs-7,va = 'bottom')
	    else:
	        ax.text(xs-1.7*s,y,str(fb),fontsize=fs,va = 'bottom',color='b')

	x1, y1 = [last_x,xs-1.5*s ], [y-1.5*s, y-1.5*s]
	ax.plot(x1, y1,marker = '<',color='k',markevery=(1,1),ms=10)

	x2, y2 = [xs-1.5*s,xs-1.5*s], [y-1.5*s,y]
	ax.plot(x2, y2,marker = 'd',color='k',markevery=(1,1))

	x1, y1 = [x+s/2, x+1.5*s], [y, y]
	ax.plot(x1, y1,marker = '>',color='k',markevery=(1,1),ms=10)
	#if ob is not None: ax.text(x+1.7*s,y,'ob = '+str(ob),fontsize=fs-7,va = 'bottom')
	if ob is not None:
	    if show_labels:
	        ax.text(x+1.7*s,y,'ob = '+str(ob),fontsize=fs-7,va = 'bottom')
	    else:
	        ax.text(x+1.7*s,y,str(ob),fontsize=fs,va = 'bottom',color='b')

	if len(seq):
	    ax.text(0,0,'Output seq = '+seq,fontsize=0.7*fs,color='b',ha='left')
	ax.axis('off')
	if title!='': plt.title(title,fontsize=fs,loc=title_loc)

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
		    elif ktype == 'random':
		        ikey = np.random.randint(0, 2,n).astype(int)
		    elif len(ktype)==n:
		        ikey = np.array([int(b) for b in ktype]).astype(int)
		    else: raise Exception('Unknown intial state')
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
