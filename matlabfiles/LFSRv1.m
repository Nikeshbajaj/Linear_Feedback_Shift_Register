function[seq c]=LFSRv1(s,t)
%s=initial state of LFSR, you can choose any lenght of LFSR
%Instruction:========== 
%Save LFSR.m in your current directory and type following
%on Command window for simulating 5 bit LFSR with tap [5 2]
%--EXAMPLE-------------------
%>>s=[1 1 0 0 1] 
%>>t=[5 2]
%>>[seq c] =LFSRv1(s,t) 
%---------------------------
%seq = generated sequence
%c will be matrix containing the states of LFSR raw wise
% 
%-----------------------------------------------------------
%If any doubt, confusion or feedback please contact me
% NIKESH BAJAJ 
% http://nikeshbajaj.in
% bajaj.nikkey@gmail.com
% PhD Student, Queen Mary University of London & University of Genoa
% Asst. Professor at Lovely Profesional University
% Masters from Aligarh Muslim University,India
%--------------------------------------------------
n=length(s);
c(1,:)=s;
m=length(t);
for k=1:2^n-2;
b(1)=xor(s(t(1)), s(t(2)));
if m>2;
    for i=1:m-2;
    b(i+1)=xor(s(t(i+2)), b(i));
    end
end
j=1:n-1;
s(n+1-j)=s(n-j);
s(1)=b(m-1);
c(k+1,:)=s;
end
seq=c(:,n)';

Verification =1; % for avoiding verification make it 0

if Verification==1
%-------------------------------------------------------
%               VARIFICATION                            
%--------------------------------------------------------
disp('If you want to skip verification process go to line 38 and')
disp('and change Verification = 0')
disp(' ')
disp('VERIFICATION...........')
disp(' ')
%Verification
 m=length(seq);
code= seq;
%Balance Property
Ns=0; % number of 1s
Zs=0; % number of 0s
for k=1:m
    if seq(k)==1;
        Ns=Ns+1;
    else
        Zs=Zs+1;
    end
end
disp('1. BALANCE PROPERTY')
if Ns==Zs+1
    disp('The Code satisfies Balance Property ')
else
    disp('The Code does NOT satisfy Balance Property')
end
    fprintf('  number of 1s and 0s are %i %i  \n\n',Ns,Zs)
%Run Length Property
b=code;
r(1:20)=0;
i=1;
while b(1)==b(m);
    b=circshift(b, [1 1]);
end
if b(m)==0;
    b(m+1)=1;
else
    b(m+1)=0;
end
for k=1:m;
    if b(k)==b(k+1);
        i=i+1;
    else
        r(i)=r(i)+1;
            i=1;	
    end
end
i=0;
while r(20-i)==0;
    r(20-i)=[];
    i=i+1;
end
l=length(r);
p=0;
for k=1:l-2
    if r(k)==2*r(k+1)
        p=p+1;
    end
end
if r(l-1)==r(l);
    p=p+1;
end
disp('2. RUN LENGTH PROPERTY')
if p==l-1;
    disp('The code satisfies RUN LENGTH property')
else
    disp('The code does NOT satisfy RUN LENGTH property')
end
fprintf('  The run length is as follow\n')
disp(r)
%Autocorrelation
rx=code;
for k=1:2*m+1;
    ry=circshift(rx, [1 k-1]);
    a=0;
    d=0;
    for i=1:m;
        if rx(i)==ry(i);
            a=a+1;
        else
            d=d+1;
        end
    end
    rxx(k)=(a-d)/m;
end
%y=0;
%n=0:0.1:2*m+1;
figure(1)
plot(-m:m,rxx)
hold on
%plot(n,y,'-k', 'linewidth',2)
line([-m-1 m+1], [0 0], [1 1],'color', 'k')
title('Autocorrelation of sequence')
xlabel('Shift')
ylabel('Autocorreleation Function')
hold off
%axis([-m m min(rxx)-.02 1+.2])
p3=0;
if rxx(2:m)== -(1/m);
    p3=1;
end
disp('3. AUTOCORRELATION PROPERTY')
if p3==1;
    disp('The Code satisfies the Autocorrelation Property')
else
    disp('The Code does NOT satisfy the Autocorrelation Property')
end
    disp(' See the Figure 1')
end
