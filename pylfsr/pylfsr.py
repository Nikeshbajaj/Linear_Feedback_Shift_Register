'''
Author @ Nikesh Bajaj
Version : 1.0.7
Contact: n.bajaj@qmul.ac.uk
       : n.bajaj@imperial.ac.uk
       : http://nikeshbajaj.in
-----changelog-------------------
first created : Date: 22 Oct 2017
Updated on : 29 Apr 2021 (version:1.0.6)
           : fixed bugs (1) not counting first outbit correctly (2) Exception in info method
		   : added test properties (1) Balance (2) Runlength (3) Autocorrelation
           : improved functionalities
           : added Viz function
           : added A5/1 and Geffe Generator
Updated on : 03 Jan 2023 (version:1.0.7)
           : Added Galois Configuration for LFSR
           : fixed bugs, improved documentation
'''

from __future__ import absolute_import, division, print_function
name = "LFSR "
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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from .utils import deprecated, progbar

class LFSR():
    '''
    Linear Feedback Shift Register

    class LFSR(fpoly=[5,2],initstate='ones',verbose=False)

    Parameters
    ----------

    fpoly : List, optional (default=[5,2])
        Feedback polynomial, it has to be primitive polynomial of GF(2) field, for valid output of LFSR

        Example: for 5-bit LFSR, fpoly=[5,2], [5,3], [5,4,3,2], etc
               : for M-bit LFSR fpoly = [M,...]

        to get the list of feedback polynomials check method 'get_fpolyList'
        or check Refeferece:
        Ref: List of some primitive polynomial over GF(2)can be found at
        http://www.partow.net/programming/polynomials/index.html
        http://www.ams.org/journals/mcom/1962-16-079/S0025-5718-1962-0148256-1/S0025-5718-1962-0148256-1.pdf
        http://poincare.matf.bg.ac.rs/~ezivkovm/publications/primpol1.pdf


    initstate : binary np.array (row vector) or str ='ones' or 'random', optional (default = 'ones'))
        Initial state vector of LFSR. initstate can not be all zeros.

        default ='ones'
            Initial state is intialized with ones and length of register is equal to
            degree of feedback polynomial
        if state='rand' or 'random'
            Initial state is intialized with random binary sequence of length equal to
            degree of feedback polynomial
        if passed as list or numpy array
            initstate = [1,1,0,0,1]

        Theoretically the length initial state vector should be equal to order of polynomial (M), however, it can easily be bigger than that
        which is why all the validation of state vector and fpoly allows bigger length of state vector, however small state vector will raise an error.

    counter_start_zero: bool (default = True), whether to start counter with 0 or 1. If True, initial outbit is
        set to -1, so is feedbackbit, until first .next() clock is excecuted. This initial output is not stacked in
        seq. The output sequence should be same, in anycase, for example if you need run 10 cycles, using runKCycle(10) methed.

    verbose : boolean, optional (default=False)
        if True, state of LFSR will be printed at every cycle(iteration)

    conf: str {'fibonacci', 'galois'}, default conf='fibonacci'
        : configuration mode of LFSR, either fabonacci or galoisi.
        : Example of 16-bit LFSR:
          fibonacci: https://en.wikipedia.org/wiki/Linear-feedback_shift_register#/media/File:LFSR-F16.svg
          Galois: https://en.wikipedia.org/wiki/Linear-feedback_shift_register#/media/File:LFSR-G16.svg

    seq_bit_index: int, index of shift register for output sequence. Default=-1, which means the last register
       : seq_bit_index can varies from -M to M-1,for M-bit LFSR. For example 5-bit LFSR, seq_bit_index=-5,-4,-3,-2,-1, 0, 1, 2, 3, 4
       : seq_bit_index=-1, means output sequence is taken out from last Register, -2, second last,


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


    Methods
    -------

    | Clocking (running LFSR)::
    - next()         : running one cycle
    - runKCycle(k)   : running k cycles
    - runFullPeriod(): running a full period of cylces

    | Deprecated methods::
    - runFullCycle()  :
    - set() : set fpoly and initialstate
    - changeFpoly(newfpoly) : change fpoly
    - change_conf(conf)     : change configuration

    | Setters::
    - reset() :reset to initial settings
    - set_fpoly(fpoly) : change/set fpoly
    - set_conf(conf)   : change/set configuration
    - set_state(state) : change/set state
    - set_seq_bit_index(bit_index) : change/set seq_bit_index

    | Getters::
    - getFullPeriod()    : get a period
    - get_fPoly()        : get feedback polynomial
    - get_initState()    : get initial state
    - get_currentState() : get current state
    - getState()         : get current state as string
    - get_outputSeq()    : get output sequence
    - getSeq()           : get output sequence as string
    - get_period()       : get period
    - get_expectedPeriod() : get expected period
    - get_count()        : get counter

    | Testing Properties
    - test_properties()    : Test all the properties for a valid LFSR
    - balance_property(p)  : Test Balance property for a given sequence p
    - runlength_property(p): Test Runlength property for a given sequence p
    - autocorr_property(p) : Test Autocorrelation property for a given sequence p
    - test_p(p) :Test three properties for a given sequence p

    | Displaying::
    - info(): Display all the attribuates of LFSR
    - Viz() : Display LFSR as a figure with a current state of LSFR with feedback polynomials and given configuration


    Examples::
    ==========
    # For more detailed and updated examples, please check  - https://lfsr.readthedocs.io/
    #-------------------------------------------------------
    >>> import numpy as np
    >>> from pylfsr import LFSR

    ## Example ## 5 bit LFSR with x^5 + x^2 + 1
    >>> L = LFSR()  #default  fpoly=[5,2], initstate='ones'
    >>> L = LFSR(fpoly=[5,2], initstate='ones')

    ### run one cycle
    >>> L.next()
    1

    ### run 10 cycles
    >>> L.runKCycle(10)
    array([1, 1, 1, 1, 0, 0, 1, 1, 0, 1])

    ### run one period of cycles
    #>>> L.runFullCycle()  # Depreciated
    >>> L.runFullPeriod()  # doctest: +NORMALIZE_WHITESPACE
    array([1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0,
       1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1])

    ## Displaying Info
    >>> L.info()
    5 bit LFSR with feedback polynomial  x^5 + x^2 + 1
    Expected Period (if polynomial is primitive) =  31
    Current :
        State        :  [1 1 1 1 1]
        Count        :  0
        Output bit   :  -1
        feedback bit :  -1


    ## Displaying Info with print
    >>>print(L)
    LFSR ( x^5 + x^2 + 1)
    ==================================================
    initstate 	=	[1. 1. 1. 1. 1.]
    fpoly     	=	[5, 2]
    conf      	=	fibonacci
    order     	=	5
    expectedPeriod	=	31
    seq_bit_index	=	-1
    count     	=	1
    state     	=	[0 1 1 1 1]
    outbit    	=	1
    feedbackbit	=	0
    seq       	=	[1]
    counter_start_zero	=	True


    ## Displaying Info with repr
    >>>repr(L)
    "LFSR('fpoly'=[5, 2], 'initstate'=ones,'conf'=fibonacci, 'seq_bit_index'=-1,'verbose'=False, 'counter_start_zero'=True)"


    >>> L.info()  # doctest: +NORMALIZE_WHITESPACE
    5 bit LFSR with feedback polynomial  x^5 + x^2 + 1
    Expected Period (if polynomial is primitive) =  31
    Current :
     State        :  [0 0 1 0 0]
     Count        :  42
     Output bit   :  1
     feedback bit :  0
     Output Sequence 111110011010010000101011101100011111001101


    ## Example  ## 5-bit LFSR with custom state vector and feedback polynomial
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

    ### run 10000 cycles
    >>> tempseq = L.runKCycle(10000)  # generate 10000 bits from current state

    ### verbosity ON
    >>>state = np.array([0,0,0,1,0])
    >>>fpoly = [5,4,3,2]
    >>>L1 = LFSR(fpoly=fpoly,initstate=state, verbose=True)
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


    ## Example ## TO visualize the process with 3-bit LFSR, with default counter_start_zero = True
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

    ## Example ## To visualize the process with 3-bit LFSR, with counter_start_zero = False
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

    ## Example ## To visualize LFSR
    L.Viz(show=False, show_labels=False,title='R1')


    ## Galois Configuration
    L = LFSR(initstate='ones',fpoly=[5,3],conf='galois')
    L.Viz()


    ## Example ## Change/Set conf in between
    >>>L1 = LFSR(initstate='ones',fpoly=[5,3],conf='fibonacci')
    >>>L1.set_fpoly(fpoly=[5,3])
    >>>L1.set_state(state=[1,1,0,0,1])
    >>>L1.set_conf(conf='galois')

    ## Example ## 23 bit LFSR with custum state and feedback polynomial

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

    >>> #L.changeFpoly(newfpoly =[23,21])
    >>> L.set_fpoly(fpoly =[23,21])
    >>> seq1 = L.runKCycle(20)

    ##  Example ## testing the properties
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

    def __init__(self, fpoly=[5, 2], initstate='ones', conf='fibonacci',seq_bit_index=-1,verbose=False,counter_start_zero=True):

        self._initstate = initstate
        if isinstance(initstate, str):
            if initstate == 'ones':
                initstate = np.ones(np.max(fpoly))
            elif initstate == 'random' or initstate == 'rand':
                initstate = np.random.randint(0, 2, np.max(fpoly))
            else:
                raise ValueError('Unknown initial state')
        if isinstance(initstate, list):
            initstate = np.array(initstate)

        self.initstate = initstate
        self.fpoly = fpoly
        self.state = initstate.astype(int)

        # Configuration can be either 'fibonacci' or 'galois'
        self.conf = conf

        # sequence bit: sequence to be taken from, default -1, last bit of LFSR
        self.seq_bit_index = seq_bit_index

        #self.skip_first = skip_first
        self.counter_start_zero = counter_start_zero
        self.count = 0 if counter_start_zero else 1


        self.verbose = verbose
        self.update()
        self.check()
        self.seq =  np.array([-1]) if counter_start_zero else np.array([self.state[self.seq_bit_index]])
        self.outbit = -1 if counter_start_zero else self.state[self.seq_bit_index]
        self.feedbackbit = -1 if counter_start_zero else self.state[self.seq_bit_index]

    def update(self):
        '''
        Updatating order, period and feedpoly string
        '''
        self.fpoly.sort(reverse=True)
        feed = ' '
        for i in range(len(self.fpoly)):
            feed = feed + 'x^' + str(self.fpoly[i]) + ' + '
        feed = feed + '1'
        self.feedpoly = feed

        self.M = np.max(self.fpoly)
        self.order = self.M
        self.expectedPeriod = 2**self.M - 1
        self.T = 2**self.M - 1

    def check(self):
        '''
        Check if
        - degree of feedback polynomial <= length of LFSR >=1
        - given intistate of LFSR is correct
        - configuration is valid
        - output sequence bit index

        '''

        # Check Feedback Polynomial
        # ------------------------
        if np.max(self.fpoly) > self.initstate.shape[0] or np.min(self.fpoly) < 1 or len(self.fpoly) < 2:
            raise ValueError('Invalid feedback polynomial: Order of feedback polynomial can not be less than 2 or greater than length of state vector. \n Polynomial also can not have negative or zeros powers')

        if len(set(self.fpoly))!=len(self.fpoly):
            raise ValueError('Invalid feedback polynomial: feedback polynomial vector should have unique powers')

        # Check Initial State
        # ------------------------
        if len(self.initstate.shape) > 1 and (self.initstate.shape[0] != 1 or self.initstate.shape[1] != 1):
            raise ValueError('Invalid Initial state vector: Size of intial state vector should be one diamensional')
        else:
            self.initstate = np.squeeze(self.initstate)

        if np.sum(self.initstate==1)+np.sum(self.initstate==0) != len(self.initstate):
            raise ValueError('Invalid Initial state vector: Initial state vector should be binary, i.e., 0s and 1s')
        if np.sum(self.initstate==0) == len(self.initstate):
            raise ValueError('Invalid Initial state vector: Initial state vector can not be All Zeros')

        assert np.sum(self.initstate>1) + np.sum(self.initstate<0)==0 # test if initial state is binary, 1s and 0s

        # Check Configuration
        # ------------------------
        # Configuration can be either 'fibonacci' or 'galois'
        if self.conf not in ['fibonacci','galois']:
            raise ValueError('Not valid configuration, "conf" should be either "fibonacci" or "galois"')

        if self.conf=='galois' and np.max(self.fpoly)!=len(self.state):
            raise ValueError('Wrong length of state vector for Galois configuration. For Galois configuration, length of state vector should be same as order of feedback polynomial ')


        # Check Output sequence bit index
        # ------------------------
        if self.seq_bit_index not in list(range(-np.max(self.fpoly), np.max(self.fpoly))):
            raise IndexError('Output sequence can be taken from one of the register only [%d,%d), index = %d provided: Out of bounds index' % (-np.max(self.fpoly), np.max(self.fpoly), self.seq_bit_index))

    def check_state(self):
        '''
        check if current state vector is valid
        '''

        # Check Initial State
        # ------------------------
        if len(self.state.shape) > 1 and (self.state.shape[0] != 1 or self.state.shape[1] != 1):
            raise ValueError('Invalid state vector: Size of state vector should be one diamensional')

        if np.sum(self.state==1)+np.sum(self.state==0) != len(self.state):
            raise ValueError('Invalid state vector: state vector should be binary, i.e., 0s and 1s')

        if np.sum(self.state==0) == len(self.state):
            raise ValueError('Invalid state vector: State vector can not be All Zeros')

        if self.conf=='galois' and np.max(self.fpoly)!=len(self.state):
            raise ValueError('Wrong length of state vector for Galois configuration. For Galois configuration, length of state vector should be same as order of feedback polynomial ')

        assert np.sum(self.state>1) + np.sum(self.state<0)==0 # test if initial state is binary, 1s and 0s

    def info(self):
        '''
        Display the information about LFSR with current state of variables
        '''
        print('%d-bit LFSR with feedback polynomial %s with' % (self.M, self.feedpoly))
        print('Expected Period (if polynomial is primitive) = ', self.expectedPeriod)
        if self.seq_bit_index>-1:
            print('Computing configuration is set to %s with output sequence taken from %d-th register' % (self.conf.capitalize(), self.seq_bit_index+1))
        else:
            print('Computing configuration is set to %s with output sequence taken from %d-th (%d) register' % (self.conf.capitalize(), self.seq_bit_index%self.M +1, self.seq_bit_index))
        print('Current :')
        print(' State        : ', self.state)
        print(' Count        : ', self.count)
        print(' Output bit   : ', self.outbit)
        print(' feedback bit : ', self.feedbackbit)
        if self.count > 0 and self.count < 1000:
            print(' Output Sequence: %s' % (''.join([str(int(x)) for x in self.seq])))

    def __repr__(self):
        fmt = f"LFSR('fpoly'={self.fpoly}, 'initstate'={self._initstate.astype(int).tolist() if isinstance(self._initstate,np.ndarray) else self._initstate}," +\
              f"'conf'={self.conf}, 'seq_bit_index'={self.seq_bit_index},'verbose'={self.verbose}, 'counter_start_zero'={self.counter_start_zero})"
        return fmt

    def __str__(self):
        fmt = f"LFSR ({self.feedpoly})\n"
        fmt = fmt+ f"{'='*50}\n"
        param = ['initstate', 'fpoly', 'conf', 'order', 'expectedPeriod', 'seq_bit_index', ]
        param = param + ['count','state','outbit','feedbackbit','seq','counter_start_zero']

        for key in param:
            if key in self.__dict__:
                fmt = fmt+f"{key}{' '*(10-len(key))}\t=\t{self.__dict__[key]}\n"
        return fmt

    def next(self,verbose=False):
        '''
        Run one cycle on LFSR with given feedback polynomial and
        update the count, state, feedback bit, output bit and seq

        Returns
        -------
        output bit : binary
        '''
        if self.verbose or verbose:
            print('S: ', self.state)

        if self.counter_start_zero:
            self.outbit = self.state[self.seq_bit_index]
            if self.count ==0:
                self.seq = np.array([self.state[self.seq_bit_index]])
            else:
                self.seq  = np.append(self.seq, self.state[self.seq_bit_index])

        if self.conf=='fibonacci':
            b = np.logical_xor(self.state[self.fpoly[0] - 1], self.state[self.fpoly[1] - 1])
            if len(self.fpoly) > 2:
                for i in range(2, len(self.fpoly)):
                    b = np.logical_xor(self.state[self.fpoly[i] - 1], b)

            #self.outbit = self.state[-1]
            self.state = np.roll(self.state, 1)
            self.feedbackbit = b * 1
            self.state[0] = self.feedbackbit
        else:
            #self.conf=='galois':
            self.feedbackbit = self.state[0]
            self.state = np.roll(self.state, -1)
            for k in self.fpoly[1:]:
                self.state[k-1] = np.logical_xor(self.state[k-1], self.feedbackbit)

        if not(self.counter_start_zero):
            self.outbit = self.state[self.seq_bit_index]
            if self.count ==0:
                self.seq = np.array([self.outbit])
            else:
                self.seq  = np.append(self.seq, self.outbit)

        self.count += 1

        return self.outbit

    def runKCycle(self, k, verbose=False):
        '''
        Run k cycles and update all the Parameters

        Parameters
        ----------
        k : int

        Returns
        -------
        tempseq : shape =(k,), output binary sequence of k cycles
        '''
        if verbose:
            self.verbose = False
            tempseq = []
            for i in range(k):
                ProgBar(i,k,title=f' {k}-cycles')
                tempseq.append(self.next())
        else:
            tempseq = [self.next() for _ in range(k)]
        return np.array(tempseq)

    @deprecated('due to misnomer, use "runFullPeriod" instead')
    def runFullCycle(self):
        '''
        NOTE: Will be deprecated in future version due to misnomer, use "runFullPeriod" instead

        Run a full cycle (T = 2^M-1) on LFSR from current state

        Returns
        -------
        seq : binary output sequence since start: shape = (count,)
        '''
        temp = [self.next() for _ in range(self.expectedPeriod)]
        return self.seq

    def runFullPeriod(self,verbose=False):
        '''
        Run a full period of cycles (T = 2^M-1) on LFSR from current state

        Returns
        -------
        seq : binary output sequence since start: shape = (count,)
        '''
        if verbose:
            self.verbose = False
            tempseq = []
            for i in range(self.expectedPeriod):
                ProgBar(i,self.expectedPeriod,title=f' {self.expectedPeriod}-cycles')
                tempseq.append(self.next())
        else:
            temp = [self.next() for _ in range(self.expectedPeriod)]
        return self.seq

    def reset(self):
        '''
        Reseting LFSR to its initial state and count
        '''
        self.__init__(initstate=self.initstate,fpoly=self.fpoly,counter_start_zero=self.counter_start_zero,conf=self.conf,seq_bit_index=self.seq_bit_index)

    @deprecated('Use "set_fpoly" and "set_state" instead')
    def set(self, fpoly, state='ones', enforce=False):
        '''
        NOTE: Will be deprecated in future version, use "set_fpoly" and "set_state" instead

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
        enforce: bool (defaule=False)
            : test if (1) new polynomial is for same LFSR or not (2) state vector is same length or not
            : Setting enforce=True, allows the change of feedback polynomial from M-bit to K-bit LFSR, for example changing from 5-bit to 3-bit etc
              in that case, make sure to change initial state vector accordingly
        '''
        if not enforce:
            # Order of new feedback polynomial should be same as previous
            # if change in size and order was intantional, set enforce=True
            assert np.max(fpoly)==np.max(self.fpoly)
            if not isinstance(state,str):
                # Length of new state vector should be same as previous
                # if change in size and order was intantional, set enforce=True
                assert len(state)==len(self.state)

        self.__init__(fpoly=fpoly, initstate=state,counter_start_zero=self.counter_start_zero,conf=self.conf,seq_bit_index=self.seq_bit_index)

    @deprecated('due to inconsitancy in naming, use "set_fpoly" instead')
    def changeFpoly(self, newfpoly, reset=False,enforce=False):
        '''
        NOTE: Will be deprecated in future version, use "set_fpoly" instead

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
        enforce: bool (defaule=False)
            : test if new polynomial is for same LFSR or not

        '''
        if not enforce:
            # Order of new feedback polynomial should be same as previous
            #if change in size and order was intantional, set enforce=True
            assert np.max(newfpoly)==np.max(self.fpoly)

        newfpoly.sort(reverse=True)
        self.fpoly = newfpoly
        self.update()
        self.check()
        if reset: self.reset()

    @deprecated('due to inconsitancy in naming, use "set_conf" instead')
    def change_conf(self,conf):
        assert conf in ['fibonacci', 'galois']
        self.conf = conf
        self.check()

    def set_fpoly(self, fpoly, reset=False,enforce=False):
        '''
        Set Feedback polynomial
        ------------------------
        Useful to change feedback polynomial in between as in A5/1 stream cipher, to increase the complexity

        Parameters
        ----------
        fpoly : list like, [5,4,2,1], should be same
            changing the feedback polynomial

        reset : boolean default=False
            if True, reset all the Parameters: count and seq etc ....
            if False, leave the LFSR as it is only change the feedback polynomial
            for further use, as used in
            'Enhancement of A5/1: Using variable feedback polynomials of LFSR'
             https://doi.org/10.1109/ETNCC.2011.5958486

        enforce: bool (defaule=False)
            : test if new polynomial is for same LFSR or not
            : Setting enforce=True allows to change feedback polynomial from M-bit to any other bit, given that state vector is changed accordingly.
            : check details of initstate in help(LFSR) doc

        '''
        if not enforce:
            # Order of new feedback polynomial should be same as previous
            #if change in size and order was intantional, set enforce=True
            assert np.max(fpoly)==np.max(self.fpoly)

        fpoly.sort(reverse=True)

        self.fpoly = fpoly
        feed = ' '
        for i in range(len(self.fpoly)):
            feed = feed + 'x^' + str(self.fpoly[i]) + ' + '
        feed = feed + '1'
        self.feedpoly = feed

        self.update()
        self.check()
        if reset: self.reset()

    def set_conf(self,conf, reset=False):
        '''
        Set Configuration
        -----------------
        Change configuration, useful to change configuration in between

        Parameters
        ----------
        conf: str {'fibonacci', 'galois'}, default conf='fibonacci'

        reset : boolean default=False
            if True, reset all the Parameters: count and seq etc ....
            if False, leave the LFSR as it is only change configuration

        '''
        assert conf in ['fibonacci', 'galois']
        self.conf = conf
        self.check()
        if reset: self.reset()

    def set_state(self,state,return_state=False,enforce=False):
        '''
        Set Current state
        -----------------

        Parameters
        ----------
        state: str, list or np.array
             : if str state='ones' or state='random'
             : if list or np.array, it should be binary and length equal to max of polynomial degree
        return_state: bool, if True, return state vector. Useful when state='random' is passed, to keep track of newly inilized state vector
        enforce: bool (defaule=False)
            : test if new state vector has same length as old one
            :

        '''
        if isinstance(state, str):
            if state == 'ones':
                state = np.ones(np.max(self.fpoly))
            elif state == 'random':
                state = np.random.randint(0, 2, np.max(self.fpoly))
            else:
                raise ValueError('Unknown state: only ones or random is allowed')

        if isinstance(state, list):
            state = np.array(state).astype(int)

        if not enforce:
            # Length of new state vector should be same as previous
            # if change in size and order was intantional, set enforce=True
            assert len(state)== len(self.state)
        self.state = state
        self.check_state()
        self.update()
        if return_state: return self.state

    def set_seq_bit_index(self,bit_index):
        '''
        Set Output bit index:  for output sequence as index
        --------------------------------------------------

        seq_bit_index: int in range from -M to M-1

        '''
        if bit_index not in list(range(-np.max(self.fpoly), np.max(self.fpoly))):
            raise IndexError('Output sequence can be taken from one of the register only, index = %d out of bounds' % (bit_index))

        # Index of draw outout sequence should be in bounds to state vector
        self.state[bit_index]

        self.seq_bit_index  = bit_index

    def getFullPeriod(self):
        '''
        Get a seq of a full period from LSFR, by executing next() method T times.
        The current state of LFSR is used to generate T bits.

        Calling this function also update the count, current state and output sequence of main LFSR object

        Returns
        -------
        seq (T bits), binary output sequence of last T bits
        '''
        seq = np.array([self.next() for _ in range(self.expectedPeriod)])
        return seq

    def get_fPoly(self):
        '''get feedback polynomial'''
        return self.fpoly

    def get_initState(self):
        '''get initial state of LFSR'''
        return self.initstate

    def get_currentState(self):
        '''get current state of LFSR'''
        return self.state

    def get_outputSeq(self):
        '''get output sequence as array'''
        return self.seq

    def get_period(self):
        '''get period of sequence'''
        return self.T

    def get_expectedPeriod(self):
        '''get period of sequence'''
        return self.expectedPeriod

    def get_count(self):
        '''get counter value'''
        return self.count

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

    @staticmethod
    def get_Ifpoly(fpoly):
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
        r2, (N1s, N0s)   = self.balance_property(p1.copy())
        r3, runs         = self.runlength_property(p1.copy(),verbose=0)
        r4, (shift, rxx) = self.autocorr_property(p1.copy(),plot=False)

        result = bool(np.prod([r1,r2,r3,r4]))

        if verbose:
            print('1. Periodicity')
            print('------------------')
            print(' - Expected period = 2^M-1 =',self.expectedPeriod)
            print(' - Pass?: ',r1)
            print('')
            print('2. Balance Property')
            print('-------------------')
            print(' - Number of 1s = Number of 0s+1 (in a period)')
            print(' - #1s = ',N1s,'\t#0s = ', N0s, ':=',N1s,'= 1 +',N0s)
            print(' - Pass?: ',r2)
            print('')
            print('3. Runlength Property')
            print('-------------------')
            print(' - Number of Runs of different lengths in a period should be of specific order, e.g. [4,2,1,1], that is 4 runs of length 1, 2 runs of length 2 and so on ..')
            print(' - Runs: ',runs)
            print(' - Pass?: ',r3)
            print('')
            print('4. Autocorrelation Property')
            print('-------------------')
            print(' - Autocorrelation of a period should be noise-like, specifically, 1 at k=0, -1/m everywhere else \n')
            if verbose>1:
                print(' - Rxx(k): ',rxx.round(3))
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
            print(' - Number of 1s = Number of 0s+1 (in a period)')
            print(' - #1s = ',N1s,'\t#0s = ', N0s, ':=',N1s,'= 1 +',N0s)
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
                print(' - Rxx(k): ',rxx.round(3))
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

        if len(set(p))>1:
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

    @staticmethod
    def arr2str(arr):
        return ''.join(arr.copy().astype(str))

    def Viz(self,ax=None,show=True,fs=25,show_labels=False,title='',title_loc='left',box_color='lightblue',alpha=0.5,
            output_arrow_color='C2',output_arrow_style='h',show_outseq=True):

        '''
        Display LFSR
        -------------

        ax: axis to plot, if None, new axis will be created, (default None)
        show: if True, plt.show() will be excecuted, (default True)
        fs:  fontsize (default 25)
        show_label: if true, will display names
        title: str, title of figure, default '',
        title_loc, alignment of title, 'left', 'right', 'center', (default 'left')
        '''
        state = self.state
        fpoly = self.fpoly
        seq = self.getSeq() if show_outseq else ''
        outbit = self.outbit
        feedbit = self.feedbackbit
        conf = self.conf
        out_bit_index = self.seq_bit_index


        dispLFSR(state=state,fpoly=fpoly,conf=conf,seq=seq,out_bit_index=out_bit_index,
             ob=outbit,fb=feedbit,fs=fs,ax=ax,show_labels=show_labels,title=title,
             title_loc=title_loc,box_color=box_color,alpha=alpha,output_arrow_color=output_arrow_color,output_arrow_style=output_arrow_style)
        #PlotLFSR(state,fpoly,seq=seq,ob=outbit,fb=feedbit,fs=fs,ax=ax,show_labels=show_labels,title=title,title_loc=title_loc,
        #         box_color=box_color,alpha=alpha)
        if  show: plt.show()


def drawR(ax,x=0,y=0,s=1,alpha=0.5,color='lightblue',linewidth=1, edgecolor='k',):
    rect = patches.Rectangle((x-s/2, y-s/2), s, s, linewidth=linewidth, edgecolor=edgecolor, facecolor=color,alpha=alpha)
    ax.add_patch(rect)

def PlotLFSR(state,fpoly,conf='fibonacci',seq='',ob=None,fb=None,fs=25,ax=None,show_labels=False,title='',title_loc='left',
             box_color='lightblue',alpha=0.5):
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

    if conf=='fibonacci':
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
    else:
        pass

def dispLFSR(state,fpoly,conf='fibonacci',seq='',out_bit_index=-1,
             ob=None,fb=None,fs=25,ax=None,show_labels=False,title='',
             title_loc='left',box_color='lightblue',alpha=0.5,output_arrow_color='C0',output_arrow_style='h'):

    r'''
    -----  Display LFSR ----

    parameters
    ----------
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

    if conf=='galois': ym +=1
    if ax is None:
        fig, ax = plt.subplots(figsize=(M+5,ym))

    s=1
    xs = 3
    ys = ym-1
    last_x= xs

    #assert out_bit_index!=0
    #assert out_bit_index in range(-M,M+1)
    out_bit_index = np.clip(out_bit_index,-M,M-1)

    #if out_bit_index>-M and out_bit_index<=M:
    out_bit_index=1+(out_bit_index)%M

    #print(out_bit_index)

    output_arr_plot=False

    if conf=='fibonacci':
        for k in range(M):
            x,y = xs+k,ys
            ax.text(x,y,str(state[k]),ha='center',va = 'center',fontsize=fs)

            if k==0:
                x1, y1 = [x-1.5*s, x-s/2], [y, y]
                ax.plot(x1, y1,marker = '>',color='k',markevery=(1,1),ms=10)

            if k+1 in fpoly:
                x1, y1 = [x, x], [y-s/2, y-1.5*s]
                ax.plot(x1, y1,marker = '.',color='k')
                ax.plot(x1[0],y-1*s,marker = 'v',color='k',ms=8,mew=3)

                ax.plot(x,y-1.5*s,marker = '+',color='b',ms=15,mew=3)
                ax.plot(x,y-1.5*s,marker = 'o',color='b',ms=15,mfc='none',mew=2)

                if last_x<x: last_x=x

            if k==out_bit_index-1:
                if out_bit_index!=M or (out_bit_index==M and output_arrow_style=='v'):
                    x1, y1 = [x, x], [y+s/2, y+1*s]
                    ax.plot(x1, y1,marker = '^',color=output_arrow_color,markevery=(1,1),ms=10)
                    output_arr_plot = True
                    #if ob is not None: ax.text(x+1.7*s,y,'ob = '+str(ob),fontsize=fs-7,va = 'bottom')
                    if ob is not None:
                        if show_labels:
                            ax.text(x+0.1*s,y+1*s,'ob = '+str(ob),fontsize=fs-7,va = 'bottom',color=output_arrow_color)
                        else:
                            ax.text(x+0.1*s,y+1*s,str(ob),fontsize=fs,va = 'bottom',color=output_arrow_color)

            drawR(ax,x=x,y=y,s=s,alpha=alpha,color=box_color)

        #if fb is not None: ax.text(xs-1.7*s,y,'fb = '+str(fb),fontsize=fs-7,va = 'bottom')
        if fb is not None:
            if show_labels:
                ax.text(xs-1.7*s,y,'fb = '+str(fb),fontsize=fs-7,va = 'bottom',color='k')
            else:
                ax.text(xs-1.7*s,y,str(fb),fontsize=fs,va = 'bottom',color='k')

        x1, y1 = [last_x,xs-1.5*s ], [y-1.5*s, y-1.5*s]
        ax.plot(x1, y1,marker = '<',color='k',markevery=(1,1),ms=10)

        x2, y2 = [xs-1.5*s,xs-1.5*s], [y-1.5*s,y]
        ax.plot(x2, y2,marker = 'd',color='k',markevery=(1,1))

        if out_bit_index==M and output_arrow_style=='h':
            x1, y1 = [x+s/2, x+1.5*s], [y, y]
            ax.plot(x1, y1,marker = '>',color=output_arrow_color,markevery=(1,1),ms=10)
            if ob is not None:
                if show_labels:
                    ax.text(x+1.7*s,y,'ob = '+str(ob),fontsize=fs-7,va = 'bottom',color=output_arrow_color)
                else:
                    ax.text(x+1.7*s,y,str(ob),fontsize=fs,va = 'top',color=output_arrow_color)

        if len(seq):
            ax.text(0,ym-3.5,'Output seq = '+seq,fontsize=0.7*fs,color='C0',ha='left')
    else:
        #GALOIS LFSR
        #conf=='galois':
        xi = xs
        ds = 1
        for k in range(M):
            xi += 1
            if k in fpoly: xi +=ds
            x,y = xi,ys
            ax.text(x,y,str(state[k]),ha='center',va = 'center',fontsize=fs)

            if k==0:
                #x1, y1 = [x-s/2,x-1.5*s], [y, y]
                #ax.plot(x1, y1,marker = '<',color='k',markevery=(1,1),ms=10)
                x1, y1 = [x, x], [y-s/2, y-1.5*s]
                ax.plot(x1, y1,marker = '.',color='k')

            if k==M-1:
                x1, y1 = [x+1.5*s, x+s/2], [y, y]
                ax.plot(x1, y1,marker = '<',color='k',markevery=(1,1),ms=10)
                last_x = x1[0]

            if k+1 in fpoly[1:]:
                x1, y1 = [x+(1+ds)/2, x+(1+ds)/2], [y, y-1.5*s]
                ax.plot(x1, y1,marker = '.',color='k')
                ax.plot(x1[0],y,marker = '+',color='b',ms=15,mew=3)
                ax.plot(x1[0],y,marker = 'o',color='b',ms=15,mfc='none',mew=2)

                ax.plot(x1[0],y-1*s,marker = '^',color='k',ms=10,mew=3)

                x1, y1 = [x+s/2+ds,x+s/2], [y, y]
                ax.plot(x1, y1,marker = '<',color='k',markevery=(1,1),ms=10)

            if k==out_bit_index-1:
                x1, y1 = [x, x], [y+s/2, y+1*s]
                ax.plot(x1, y1,marker = '^',color=output_arrow_color,markevery=(1,1),ms=10)
                if ob is not None:
                    if show_labels:
                        ax.text(x+0.1*s,y+1*s,'ob = '+str(ob),fontsize=fs-7,va = 'bottom',color=output_arrow_color)
                    else:
                        ax.text(x+0.1*s,y+1*s,str(ob),fontsize=fs,va = 'bottom',color=output_arrow_color)

            drawR(ax,x=x,y=y,s=s,alpha=alpha,color=box_color)

        x1, y1 = [xs+1,last_x], [y-1.5*s, y-1.5*s]
        ax.plot(x1, y1,marker = '>',color='k',markevery=(1,1),ms=10)

        x1, y1 = [last_x,last_x], [y-1.5*s, y]
        ax.plot(x1, y1,marker = '.',color='k',markevery=(1,1),ms=10)

        if fb is not None:
            if show_labels:
                ax.text(last_x+0.1*s,y,'fb = '+str(fb),fontsize=fs-7,va = 'bottom',color='k')
            else:
                ax.text(last_x+0.1*s,y,str(fb),fontsize=fs,va = 'bottom',color='k')

        if len(seq):
            ax.text(2,ym-3.5,'Output seq = '+seq,fontsize=0.7*fs,color='C0',ha='left')

    ax.axis('off')
    if title!='': plt.title(title,fontsize=fs,loc=title_loc)


if __name__ == '__main__':
	import doctest
	doctest.testmod()
