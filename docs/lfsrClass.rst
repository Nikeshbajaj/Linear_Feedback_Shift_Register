
API LFSR
======================================
*class(fpoly=[5,2], initstate='ones', verbose=False)*

*help doc*

**Linear Feedback Shift Register**

**#Parameters** ------------------------------------

* initstate : binary np.array (row vector) or str ='ones' or 'random', optional (default = 'ones')) Initial state of LFSR.		      default ='ones'
	Initial state is intialized with ones and length of register is equal to degree of feedback polynomial
	if state='rand', initial state is intialized with random binary sequence of length equal to degree of feedback polynomial

* fpoly : List, optional (default=[5,2])
	Feedback polynomial, it has to be primitive polynomial of GF(2) field, for valid output of LFSR
	to get the list of feedback polynomials check method 'get_fpolyList'
	or check Refeferece:
	Ref: List of some primitive polynomial over GF(2)can be found at
	http://www.partow.net/programming/polynomials/index.html
	http://www.ams.org/journals/mcom/1962-16-079/S0025-5718-1962-0148256-1/S0025-5718-1962-0148256-1.pdf
	http://poincare.matf.bg.ac.rs/~ezivkovm/publications/primpol1.pdf

* verbose : boolean, optional (default=False)
	if True, state of LFSR will be printed at every cycle(iteration)
	
**#Attributes** ------------------------------------

* count : int
	Count the cycle

* seq   : np.array shape =(count,)
	Output sequence stored in seq since first cycle. 
	If -1, no cycle has been excecuted, count =0

* outbit : binary bit
	Current output bit, Last bit of current state
	if -1, no cycle has been excecuted, count =0

* feedbackbit : binary bit
	If -1, no cycle has been excecuted, count =0

* M : int
      length of LFSR, M-bit LFSR, 
      
* expectedPeriod : int
	Expected period of sequence
	if feedback polynomial is primitive and irreducible (as per reference), period will be 2^M -1

* feedpoly : str
	feedback polynomial
	
**#Methods** ------------------------------------

* next()
	run one cycle on LFSR with given feedback polynomial and
	update the count, state, feedback bit, output bit and seq
	
	return:
	binary bit
	output bit : binary

* runKCycle(k)
	run k cycles and update all the Parameters
	
	return
	tempseq : shape =(k,)
		output binary sequence of k cycles
* runFullCycle()
	run full cycle ( = 2^M-1)
	
	return
	seq : binary output sequence since start: shape = (count,)
	
* set(fpoly,state='ones')
	set feedback polynomial and state
	
	fpoly : list feedback polynomial like [5,4,3,2]
	
	state : np.array, like np.array([1,0,0,1,1]), default ='ones'
	Initial state is intialized with ones and length of register is equal to degree of feedback polynomial
	if state='rand', initial state is intialized with random binary sequence of length equal to degree of feedback polynomial
	
* reset()
	Reseting LFSR to its initial state and count to 0
	
* changeFpoly(newfpoly, reset=False)
	Changing Feedback polynomial
	newfpoly : list like, [5,4,2,1], changing the feedback polynomial
	
	reset : boolean default=False
	if True, reset all the Parameters : count=0, seq=-1..
	if False, leave the LFSR as it is only change the feedback polynomial as used in *'Enhancement of A5/1: Using variable feedback polynomials of LFSR'* ref: 10.1109/ETNCC.2011.5958486

* check()
	check if
	-degree of feedback polynomial <= length of LFSR >=1
	-given intistate of LFSR is correct
	
* info()
	display the information about LFSR with current state of variables
	
* get_fpolyList(m=None)
	Get the list of primitive polynomials as feedback polynomials
	for *m*-bit LFSR
	if *m* is None, list of feedback polynomials for 1 < *m* < 32 is return as a dictionary

* get_Ifpoly(*fpoly*)
	Get the image of primitive polynomial *fpoly*, which is also a valid
	primitive polynomial
