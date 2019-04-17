
MATLAB CODE
===========

Folder : https://github.com/Nikeshbajaj/Linear_Feedback_Shift_Register/tree/master/matlabfiles


Description
---------
Generate randon binary sequence using LFSR for any given feedback taps (polynomial), 
This will also check three fundamental properties of LFSR:
  1. Balance Property 
  2. Runlength Property 
  3. Autocorrelation Property

This MATLAB Code work for any length of LFSR with given taps (feedback polynomial) -Universal, There are three files LFSRv1.m an LFSRv2.m, LFSRv3.m

**LFSRv1**
---------
This function will return all the states of LFSR and will check Three fundamental Property of LFSR 
(1) Balance Property (2) Runlength Property (3) Autocorrelation Property

Example:
::
  
  s=[1 1 0 0 1] 
  t=[5 2]
  [seq c] =LFSRv1(s,t)


**LFSRv2**
---------
This function will return only generated sequence will all the states of LFSR, no verification of properties are done
here. Use this function to avoid verification each time you execute the program.

Example:

::
  
  s=[1 1 0 0 1] 
  t=[5 2]
  [seq c] =LFSRv2(s,t)

**LFSRv3 (faster)**
---------
<p>seq = LFSRv3(s,t,N)</p>
this function generates N bit sequence only. This is faster then other two functions, as this does not gives each state of LFSR

Exmple:

::
  
  s=[1 1 0 0 1]  
  t=[5 2]
  seq =LFSRv3(s,t,50)

**Tips**

* If you want to use this function in middle of any program, use LFSRv2 or LFSRv1 with verification =0. 
* If you want to make it fast for long length of LFSR,use LFSRv3.m 
