# LFSR -Linear Feedback Shift Register
Genrate randon binary sequence using LFSR for any given feedback taps (polynomial), 
This will also check Three fundamental Property of LFSR 
* (1) Balance Property 
* (2) Runlength Property 
* (3) Autocorrelation Property


<p align="center">
  <img src="https://github.com/Nikeshbajaj/Linear_Feedback_Shift_Register/blob/master/LFSR1.jpg" width="500"/>
</p>


## MATLAB CODE for LFRS
### This MATLAB Code work for any length of LFSR with given taps (feedback polynomial) -Universal, There are three files LFSRnik1.m an LFSRnik2.m, LFSRnik3.m
### LFSRnik1
This function will return all the states of LFSR and will check Three fundamental Property of LFSR 
(1) Balance Property (2) Runlength Property (3) Autocorrelation Property

### LFSRnik2
This function will return only generated sequence will all the states of LFSR, no verification of properties are done
here. Use this function to avoid verification each time you execute the program.

### LFSRnik3 (faster)
<p>seq = LFSRnik3(s,t,N)</p>
this function generates N bit sequence only. This is faster then other two functions, as this does not gives each state of LFSR

## Tips
* If you want to use this function in middle of any program, use LFSRnik2 or LFSRnik1 with verification =0. 
* If you want to make it fast for long length of LFSR,use LFSRnik3.m 

______________________________________
If any doubt, confusion or feedback please contact me
### Nikesh Bajaj
### http://nikeshbajaj.in
<p> n.bajaj@qmul.ac.uk </p>
<p> bajaj[dot]nikkey [AT]gmail[dot]com </p>
### PhD Student, Queen Mary University of London & University of Genoa </p>
