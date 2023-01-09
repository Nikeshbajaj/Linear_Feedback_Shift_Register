API: LFSR Class
=========
Linear Feedback Shift Register

Python implementation of LFSR


::
  
  class pylfsr.LFSR(fpoly=[5, 2], initstate='ones', conf='fibonacci', seq_bit_index=-1, 
                     verbose=False, counter_start_zero=True)
  

Parameters:
----------


fpoly : list, optional (default=[5,2]):
    Feedback polynomial, it has to be primitive polynomial of GF(2) field, for valid output of LFSR.
    
    Example: for 5-bit LFSR, fpoly=[5,2], [5,3], [5,4,3,2], etc
    for M-bit LFSR fpoly = [M,...]

    To get the list of feedback polynomials check method 'get_fpolyList'
    or check Refeferece:
    Ref: List of some primitive polynomial over GF(2)can be found at

    * http://www.partow.net/programming/polynomials/index.html
    * http://www.ams.org/journals/mcom/1962-16-079/S0025-5718-1962-0148256-1/S0025-5718-1962-0148256-1.pdf
    * http://poincare.matf.bg.ac.rs/~ezivkovm/publications/primpol1.pdf


initstate : binary np.array (row vector) or str ='ones' or 'random', optional (default = 'ones')):
    Initial state vector of LFSR. initstate can not be all zeros.

    default (initstate='ones')
      Initial state is intialized with ones and length of register is equal to
      degree of feedback polynomial
    if state='rand' or 'random'
       Initial state is intialized with random binary sequence of length equal to
       degree of feedback polynomial
    if passed as list or numpy array
       example initstate = [1,1,0,0,1]

   *Theoretically the length initial state vector should be equal to order of polynomial (M), however, it can easily be bigger than that
   which is why all the validation of state vector and fpoly allows bigger length of state vector, however small state vector will raise an error.*


counter_start_zero: bool (default = True), whether to start counter with 0 or 1:
    If True, initial outbit is set to -1, so is feedbackbit, until first .next() clock is excecuted.
    
    This initial output is not stacked in seq. The output sequence should be same, in anycase, for example if you need run 10 cycles, using runKCycle(10) methed.

verbose : boolean, optional (default=False):
    If True, state of LFSR will be printed at every cycle(iteration)
    

conf: str {'fibonacci', 'galois'}, default conf='fibonacci':
    : configuration mode of LFSR, either fabonacci or galoisi.
    : Example of 16-bit LFSR:
    
    Fibonacci: https://en.wikipedia.org/wiki/Linear-feedback_shift_register#/media/File:LFSR-F16.svg
    Galois: https://en.wikipedia.org/wiki/Linear-feedback_shift_register#/media/File:LFSR-G16.svg
    
seq_bit_index: int, index of shift register for output sequence:
    Default=-1, which means the last register.
    
     : seq_bit_index can varies from -M to M-1,for M-bit LFSR. For example 5-bit LFSR, seq_bit_index=-5,-4,-3,-2,-1, 0, 1, 2, 3, 4
     : seq_bit_index=-1, means output sequence is taken out from last Register, -2, second last,

Methods
-------


Clocking (running LFSR):
~~~~~~~~~

.. list-table:: **Clocking (running LFSR)**
   :widths: 30 50
   :header-rows: 1

   * - Method
     - Discription
   * - ``next()``
     - Executing/running one cycle
   * - ``runKCycle(k)``
     - Executing/running k cycles
   * - ``runFullPeriod()``
     - Executing/running a full period of cylces



Setters :
~~~~~~~~~

.. list-table:: **Setting parameters**
   :widths: 30 50
   :header-rows: 1

   * - Method
     - Discription
   * - ``reset()```
     - Reset to initial settings
   * - ``set_fpoly(fpoly)``
     - Change/set fpoly
   * - ``set_conf(conf)``
     - Change/set configuration
   * - ``set_state(state)``
     - Change/set state
   * - ``set_seq_bit_index(bit_index)``
     - Change/set seq_bit_index


Getters:
~~~~~~~~~

.. list-table:: **Fetching Attributes**
   :widths: 30 50
   :header-rows: 1

   * - Method
     - Discription
   * - ``getFullPeriod()``
     - Get sequence of a period
   * - ``get_fPoly()``
     - Get feedback polynomial
   * - ``get_initState()``
     - Get initial state
   * - ``get_currentState()`` 
     - Get current state
   * - ``getState()``
     - Get current state as string
   * - ``get_outputSeq()``
     - Get output sequence
   * - ``getSeq()``
     - Get output sequence as string
   * - ``get_period()``
     - Get period
   * - ``get_expectedPeriod()``
     - Get expected period
   * - ``get_count()``
     - Get counter


Testing LFSR Properties:
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: **Testing Properties of LFSR**
   :widths: 30 80
   :header-rows: 1

   * - Method
     - Discription
   * - ``test_properties()``
     - Test all the properties for a valid LFSR
   * - ``balance_property(p)``
     - Test Balance property for a given sequence p
   * - ``runlength_property(p)``
     - Test Runlength property for a given sequence p
   * - ``autocorr_property(p)``
     - Test Autocorrelation property for a given sequence p
   * - ``test_p(p)``
     - Test three properties for a given sequence p




Displaying/printing:
~~~~~~~~~~~~~~~~

.. list-table:: **Displaying/printing**
   :widths: 30 80
   :header-rows: 1

   * - Method
     - Discription
   * - ``info()``
     - Display all the attribuates of LFSR
   * - ``print(L [LFSR Object] )``
     - Display all the attribuates of LFSR (where ``L = LFSR()``)
   * - ``repr(L [LFSR Object] )``
     - Display all the input parameters of LFSR (where ``L = LFSR()``)
   * - ``info()``
     - Display all the attribuates of LFSR
   * - ``Viz()``
     - Display LFSR as a figure with a current state of LSFR with feedback polynomials and given configuration



Deprecated/replaced methods :
~~~~~~~~~~~~~~~~~~~~~~~~~~~

*These methods will be deprecated in future version 1.0.7*


.. list-table:: **Deprecated methods for future version**
   :widths: 30 80
   :header-rows: 1

   * - Method
     - Discription
   * - ``runFullCycle()``
     - Changed to ``runFullPeriod()``, full cycle is misnomer 
   * - ``set()``
     - Changed to ``set_fpoly`` and ``set_state`` 
   * - ``changeFpoly(newfpoly)``
     - Changed to ``set_fpoly``
   * - ``change_conf(conf)``
     - Changed to ``set_conf``



.. 
  :``next()``: Executing/running one cycle
  :``runKCycle(k)``: Executing/running k cycles
  :``runFullPeriod()``: Executing/running a full period of cylces
  :``reset()``: Reset to initial settings
  :``set_fpoly(fpoly)``: Change/set fpoly
  :``set_conf(conf)``:  Change/set configuration
  :``set_state(state)``:  Change/set state
  :``set_seq_bit_index(bit_index)``: Change/set seq_bit_index
  :``getFullPeriod()``: Get sequence of a period
  :``get_fPoly()``: Get feedback polynomial
  :``get_initState()``: Get initial state
  :``get_currentState()``: Get current state
  :``getState()``:  Get current state as string
  :``get_outputSeq()``: Get output sequence
  :``getSeq()``:  Get output sequence as string
  :``get_period()``: Get period
  :``get_expectedPeriod()``: Get expected period
  :``get_count()``: Get counter
  :``test_properties()``: Test all the properties for a valid LFSR
  :``balance_property(p)``: Test Balance property for a given sequence p
  :``runlength_property(p)``: Test Runlength property for a given sequence p
  :``autocorr_property(p)``: Test Autocorrelation property for a given sequence p
  :``test_p(p)``: Test three properties for a given sequence p
  :``info()``: Display all the attribuates of LFSR
  :``print(L [LFSR Object] )``: Display all the attribuates of LFSR (where ``L = LFSR()``)
  :``repr(L [LFSR Object] )``: Display all the input parameters of LFSR (where ``L = LFSR()``)
  :``info()``: Display all the attribuates of LFSR
  :``Viz()``: Display LFSR as a figure with a current state of LSFR with feedback polynomials and given configuration
  :``runFullCycle()``: Changed to ``runFullPeriod()``, full cycle is misnomer 
  :``set()``: : Changed to ``set_fpoly`` and ``set_state`` 
  :``changeFpoly(newfpoly)``: : Changed to ``set_fpoly``
  :``change_conf(conf)``:     : Changed to ``set_conf``


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
  If -1, no cycle has been excecuted, count =0,  when counter_start_zero is True
 
feedbackbit : binary bit
  If -1, no cycle has been excecuted, count =0,  when counter_start_zero is True

M : int
  Length of LFSR, M-bit LFSR

expectedPeriod : int (also saved as T)
  Expected period of sequence.
  If feedback polynomial is primitive and irreducible (as per reference)
  period will be 2^M -1
 
T : int (also saved as expectedPeriod)
  Expected period of sequence
  If feedback polynomial is primitive and irreducible (as per reference)
  period will be 2^M -1
 
feedpoly : str
  feedback polynomial

