function seq = LFSRv3(s,t,N)
%s=initial state of LFSR, you can choose any lenght of LFSR
%Instruction:========== 
% INPUT
% s : 1D binary vector -  state of LFSR i.e. s = [1,1,1,1,1]
% t : 1D int vector - feedback polynomial i.e t = [5,2] for x^5 + x^2 +1
%     values in t always should be in decending order
% N : int - length  of output sequence 
% OUTPUT
% seq : 1XN binary vector, output sequence

%Save LFSR.m in your current directory and type following
%on Command window for simulating 5 bit LFSR with tap [5 2]
%--EXAMPLE-------------------
%>>s=[1 1 0 0 1]  
%>>t=[5 2]
%>>seq =LFSRv3(s,t,50) 
%---------------------------
%seq = generated sequence 
%-----------------------------------------------------------
%If any doubt, confusion or feedback please contact me
% NIKESH BAJAJ 
% http://nikeshbajaj.in
% bajaj.nikkey@gmail.com
% Asst. Professor at Lovely Profesional University
% Masters from Aligarh Muslim University,India 
%--------------------------------------------------

n=length(s);
c(1,:)=s;
m=length(t);
seq(1) = s(n)
% N = 2^n-2
for k=1:N-1;
    b(1)=xor(s(t(1)), s(t(2)));
    if m>2;
        for i=1:m-2;
        b(i+1)=xor(s(t(i+2)), b(i));
        end
    end
    j=1:n-1;
    s(n+1-j)=s(n-j);
    s(1)=b(m-1);
    seq(k+1)=s(n);
end
