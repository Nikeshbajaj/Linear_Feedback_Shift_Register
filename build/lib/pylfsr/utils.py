'''
Utilities for LFSR
---------------------------
Author @ Nikesh Bajaj
Date: 03 Jan 2023
Version : 1.0.7
Github :  https://github.com/Nikeshbajaj/Linear_Feedback_Shift_Register
Contact: n.bajaj@qmul.ac.uk
'''
from __future__ import absolute_import, division, print_function
name = "PyLFSR | utils"
import sys
import numpy as np
import functools, inspect, warnings

if sys.version_info[:2] < (3, 3):
    old_print = print
    def print(*args, **kwargs):
        flush = kwargs.pop('flush', False)
        old_print(*args, **kwargs)
        if flush:
            file = kwargs.get('file', sys.stdout)
            # Why might file=None? IDK, but it works for print(i, file=None)
            file.flush() if file is not None else sys.stdout.flush()


string_types = (type(b''), type(u''))

def deprecated(reason):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    if isinstance(reason, string_types):

        # The @deprecated is used with a 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated("please, use another function")
        #    def old_function(x, y):
        #      pass

        def decorator(func1):

            if inspect.isclass(func1):
                fmt1 = "class {name} will be deprecated in future version, {reason}."
            else:
                fmt1 = "function {name} will be deprecated in future version, {reason}."

            @functools.wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func1(*args, **kwargs)

            return new_func1

        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):

        # The @deprecated is used without any 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated
        #    def old_function(x, y):
        #      pass

        func2 = reason

        if inspect.isclass(func2):
            fmt2 = "class {name} will be deprecated in future version."
        else:
            fmt2 = "function {name} will be deprecated in future version."

        @functools.wraps(func2)
        def new_func2(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt2.format(name=func2.__name__),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func2(*args, **kwargs)

        return new_func2

    else:
        raise TypeError(repr(type(reason)))

A=['\\','-','/','|']

def progbar(i,N,title='',style=2,L=100,selfTerminate=True,delta=None):

    pf = int(100*(i+1)/float(N))
    st = ' '*(3-len(str(pf))) + str(pf) +'%|'

    if L==50:
        pb = '#'*int(pf//2)+' '*(L-int(pf//2))+'|'
    else:
        L = 100
        pb = '#'*pf+' '*(L-pf)+'|'
    if style==1:
        print(st+A[i%len(A)]+'|'+pb+title,end='\r', flush=True)
    elif style==2:
        print(st+pb+str(N)+'\\'+str(i+1)+'|'+title,end='\r', flush=True)
    if pf>=100 and selfTerminate:
        print('\nDone..')

def print_list(L,n=3,sep='\t\t'):
    L = [str(l) for l in L]
    mlen = np.max([len(ll) for ll in L])
    for k in range(0,len(L)-n,n):
        print(sep.join([L[ki] +' '*(mlen-len(L[ki])) for ki in range(k,k+n)]))
    if k+n<len(L):
        print(sep.join([L[ki] +' '*(mlen-len(L[ki])) for ki in range(k,len(L))]))

def pretty_print(List,n=3,sep='|\t',show_index=True,trimLength=None):
    List = [str(l) for l in List]
    for l in List: assert type(l)==str
    L = List.copy()
    if show_index: L = [str(i)+' '+ L[i] for i in range(len(L))]

    if trimLength is not None:
        L = [ll[:trimLength] for ll in L]
    else:
        mlen = np.max([len(ll) for ll in L])
        L = [ll+' '*(mlen-len(ll)) for ll in L]

    for k in range(0,len(L)-n,n):
        print(sep.join([L[ki] for ki in range(k,k+n)]))
    if k+n<len(L):
        print(sep.join([L[ki] for ki in range(k+n,len(L))]))

def _loadFpolyList():
    import os
    fname = 'primitive_polynomials_GF2_dict.txt'
    fname = os.path.join(os.path.dirname(__file__), fname)
    try:
        f = open(fname, "rb")
        lines = f.readlines()
        f.close()
        fpolyList = eval(lines[0].decode())
    except:
        raise Exception("File named:'{}' Not Found!!! \n try again, after downloading file from github save it in lfsr directory".format(fname))

    return fpolyList

def get_fpolyList(m=None):
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
    fpolyList = _loadFpolyList()
    if m is None:
        return fpolyList
    elif type(m)== int and m > 1 and m < 32:
        return fpolyList[m]
    else:
        print('Wrong input m. m should be int 1 < m < 32 or None. For greater than 32 order, please check following refrences')
        #Ref: List of some primitive polynomial over GF(2)can be found at
        print(" - http://www.partow.net/programming/polynomials/index.html")
        print(" - http://www.ams.org/journals/mcom/1962-16-079/S0025-5718-1962-0148256-1/S0025-5718-1962-0148256-1.pdf")
        print(" - http://poincare.matf.bg.ac.rs/~ezivkovm/publications/primpol1.pdf")

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

def lempel_ziv_patterns(seq):
    r"""Lempel-Ziv patterns.
    It is defined as a set of different patterns exists in a given sequence.

    As an example:
    s = '1001111011000010'
    patterns ==> 1, 0, 01, 11, 10, 110, 00, 010
    """

    if isinstance(seq, (list,np.ndarray)):
        seq = ''.join(seq.copy().astype(str))

    patterns = set()
    n = len(seq)

    i,k = 0, 1
    while i + k<=len(seq):
        pattern = seq[i: i + k]
        if pattern in patterns:
            k += 1
        else:
            patterns.add(pattern)
            i += k
            k = 1
    return patterns

def lempel_ziv_complexity(seq):
    r"""Lempel-Ziv Complexity.
    It is defined as the number of different patterns exists in a given stream.

    As an example:
    s = '1001111011000010'
    patterns ==> 1, 0, 01, 11, 10, 110, 00, 010
    #patterns = 8
    """
    return len(lempel_ziv_patterns(seq))

if __name__ == '__main__':
	import doctest
	doctest.testmod()
