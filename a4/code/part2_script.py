# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:19:00 2020

@author: tiffa
"""

from bnetbase import *
from carDiagnosis import *

# %% Q1
# initialize all the variables
A = Variable('A', ['a', '-a'])
B = Variable('B', ['b', '-b'])
C = Variable('C', ['c', '-c'])
D = Variable('D', ['d', '-d'])
E = Variable('E', ['e', '-e'])
F = Variable('F', ['f', '-f'])
G = Variable('G', ['g', '-g'])
H = Variable('H', ['h', '-h'])
I = Variable('I', ['i', '-i'])

# initialize the factors
FA = Factor('P(A)',     [A])
FB = Factor('P(B|A,H)', [B, A, H])
FC = Factor('P(C|B,G)', [C, B, G])
FD = Factor('P(D|C,F)', [D, C, F])
FE = Factor('P(E|C)',   [E, C])
FF = Factor('P(F)',     [F])
FG = Factor('P(G)',     [G])
FH = Factor('P(H)',     [H])
FI = Factor('P(I|B)',   [I, B])

# add values to the tables
FA.add_values([['a', 0.9], ['-a', 0.1]])
FB.add_values([['b',  'a',  'h',  1.0], \
               ['b',  'a',  '-h', 0.0], \
               ['b',  '-a', 'h',  0.5], \
               ['b',  '-a', '-h', 0.6], \
               ['-b', 'a',  'h',  0.0], \
               ['-b', 'a',  '-h', 1.0], \
               ['-b', '-a', 'h',  0.5], \
               ['-b', '-a', '-h', 0.4]])
FC.add_values([['c',  'b',  'g',  0.9], \
               ['c',  'b',  '-g', 0.9], \
               ['c',  '-b', 'g',  0.1], \
               ['c',  '-b', '-g', 1.0], \
               ['-c', 'b',  'g',  0.1], \
               ['-c', 'b',  '-g', 0.1], \
               ['-c', '-b', 'g',  0.9], \
               ['-c', '-b', '-g', 0.0]])
FD.add_values([['d',  'c',  'f',  0.0], \
               ['d',  'c',  '-f', 1.0], \
               ['d',  '-c', 'f',  0.7], \
               ['d',  '-c', '-f', 0.2], \
               ['-d', 'c',  'f',  1.0], \
               ['-d', 'c',  '-f', 0.0], \
               ['-d', '-c', 'f',  0.3], \
               ['-d', '-c', '-f', 0.8]])
FE.add_values([['e',  'c',  0.2], \
               ['e',  '-c', 0.4], \
               ['-e', 'c',  0.8], \
               ['-e', '-c', 0.6]])
FF.add_values([['f', 0.1], ['-f', 0.9]])
FG.add_values([['g', 1.0], ['-g', 0.0]])
FH.add_values([['h', 0.5], ['-h', 0.5]])
FI.add_values([['i',  'b',  0.3], \
               ['i',  '-b',  0.9], \
               ['-i', 'b', 0.7], \
               ['-i', '-b', 0.1]])

# initialize bayes net
Q1 = BN('Q1', [A,B,C,D,E,F,G,H,I], [FA,FB,FC,FD,FE,FF,FG,FH,FI])


if __name__ == '__main__':
    #(a)
    print("Question 1a")
    A.set_evidence('a')
    probs = VE(Q1, B, [A])
    print('P(b|a) = {} P(-b|a) = {}'.format(probs[0], probs[1]))

    #(b)
    print("Question 1b")
    A.set_evidence('a')
    probs = VE(Q1, C, [A])
    print('P(c|a) = {} P(-c|a) = {}'.format(probs[0], probs[1]))

    #(c)
    print("Question 1c")
    A.set_evidence('a')
    E.set_evidence('-e')
    probs = VE(Q1, C, [A,E])
    print('P(c|a,-e) = {} P(-c|a,-e) = {}'.format(probs[0], probs[1]))

    #(d)
    print("Question 1d")
    A.set_evidence('a')
    F.set_evidence('-f')
    probs = VE(Q1, C, [A,F])
    print('P(c|a,-f) = {} P(-c|a,-f) = {}'.format(probs[0], probs[1]))


#### Question 2 Written ####
# %%
test_q1 = False
test_q2 = False
test_q3 = False
test_q4 = True
if __name__ == '__main__':
    if test_q1:
        # Question 1
        # Car starts is independent of Air Filter given Air System.
        asys.set_evidence('okay')
        print("asys = " + asys.get_evidence())
        probs = VE(car, st, [asys])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
        
        asys.set_evidence('okay')
        af.set_evidence('clean')
        print("asys = " + asys.get_evidence())
        print("af = " + af.get_evidence())
        probs = VE(car, st, [asys, af])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        asys.set_evidence('okay')
        af.set_evidence('dirty')
        print("asys = " + asys.get_evidence())
        print("af = " + af.get_evidence())
        probs = VE(car, st, [asys, af])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
        
        asys.set_evidence('faulty')
        print("asys = " + asys.get_evidence())
        probs = VE(car, st, [asys])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        asys.set_evidence('faulty')
        af.set_evidence('clean')
        print("asys = " + asys.get_evidence())
        print("af = " + af.get_evidence())
        probs = VE(car, st, [asys, af])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        asys.set_evidence('faulty')
        af.set_evidence('dirty')
        print("asys = " + asys.get_evidence())
        print("af = " + af.get_evidence())
        probs = VE(car, st, [asys, af])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
    if test_q2:
        print("Testing Q2")

        # first show that spark plugs and voltage at plug are independent not given spark quality
        sp.set_evidence('too_wide')
        print("sp = " + sp.get_evidence())
        probs = VE(car, pv, [])
        print("original probability")
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
        print()
        probs = VE(car, pv, [sp])
        print("prob given evidence")
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
        print()
        
        
        pv.set_evidence('weak')
        print("pv = " + pv.get_evidence())
        probs = VE(car, sp, [])
        print("original probability")
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(sp.name, sp.domain()[i], 100*probs[i]))
        print()
        probs = VE(car, sp, [pv])
        print("prob given evidence")
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(sp.name, sp.domain()[i], 100*probs[i]))
        print()
        
        # second, show that they are dependent when given spark quality
        print("now with spark quality evidence given... dependent?")
        sq.set_evidence('very_bad')
        
        sp.set_evidence('too_wide')
        print("sp = " + sp.get_evidence())
        probs = VE(car, pv, [sq])
        print("original probability")
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
        print()
        probs = VE(car, pv, [sp,sq])
        print("prob given evidence")
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
        print()
        
        
        pv.set_evidence('weak')
        print("pv = " + pv.get_evidence())
        probs = VE(car, sp, [sq])
        print("original probability")
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(sp.name, sp.domain()[i], 100*probs[i]))
        print()
        probs = VE(car, sp, [pv,sq])
        print("prob given evidence")
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(sp.name, sp.domain()[i], 100*probs[i]))
        print()
        
    if test_q3:
        print("Testing Q3")
        # Question 3
        probs = VE(car, st, [])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        # asys = 'okay' increases the probability of 'Car Starts'
        asys.set_evidence('okay')
        print("asys = " + asys.get_evidence())
        probs = VE(car, st, [asys])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        # cc = 'true' increases the probability of 'Car Starts'
        asys.set_evidence('okay')
        cc.set_evidence('true')
        print("asys = " + asys.get_evidence())
        print("cc = " + cc.get_evidence())
        probs = VE(car, st, [asys, cc])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        # sq = 'good' increases the probability of 'Car Starts'
        asys.set_evidence('okay')
        cc.set_evidence('true')
        tm.set_evidence('good')
        print("asys = " + asys.get_evidence())
        print("cc = " + cc.get_evidence())   
        print("tm = " + tm.get_evidence())
        probs = VE(car, st, [asys, cc, tm])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
        
        # sq = 'good' increases the probability of 'Car Starts'
        asys.set_evidence('okay')
        cc.set_evidence('true')
        tm.set_evidence('good')
        fs.set_evidence('okay')
        print("asys = " + asys.get_evidence())        
        print("cc = " + cc.get_evidence())   
        print("tm = " + tm.get_evidence())
        print("fs = " + fs.get_evidence())
        probs = VE(car, st, [asys, cc, tm, fs])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        # sq = 'good' increases the probability of 'Car Starts'
        asys.set_evidence('okay')
        fs.set_evidence('okay')
        cc.set_evidence('true')
        sq.set_evidence('good')
        tm.set_evidence('good')
        print("asys = " + asys.get_evidence())
        print("fs = " + fs.get_evidence())
        print("cc = " + cc.get_evidence())
        print("sq = " + sq.get_evidence())    
        print("tm = " + tm.get_evidence())
        probs = VE(car, st, [asys, cc, tm, fs, sq])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
    if test_q4:
        print("Testing Q4")
        probs = VE(car, st, [])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        # asys = 'faulty' increases the probability of 'Car Starts'
        asys.set_evidence('faulty')
        print("asys = " + asys.get_evidence())
        probs = VE(car, st, [asys])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        # cc = 'false' increases the probability of 'Car Starts'
        asys.set_evidence('faulty')
        tm.set_evidence('bad')
        print("asys = " + asys.get_evidence())
        print("cc = " + tm.get_evidence())
        probs = VE(car, st, [asys, tm])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        # tm = 'bad' increases the probability of 'Car Starts'
        asys.set_evidence('faulty')
        fs.set_evidence('faulty')
        tm.set_evidence('bad')
        print("asys = " + asys.get_evidence())
        print("fs = " + fs.get_evidence())
        print("tm = " + tm.get_evidence())
        probs = VE(car, st, [asys, tm, fs])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        # fs = 'faulty' increases the probability of 'Car Starts'
        asys.set_evidence('faulty')
        cc.set_evidence('false')
        tm.set_evidence('bad')
        fs.set_evidence('faulty')
        print("asys = " + asys.get_evidence())
        print("cc = " + sq.get_evidence())
        print("tm = " + tm.get_evidence())
        print("fs = " + fs.get_evidence())
        probs = VE(car, st, [asys, tm, fs, cc])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
        # sq = 'very_bad' increases the probability of 'Car Starts'
        asys.set_evidence('faulty')
        cc.set_evidence('false')
        tm.set_evidence('bad')
        fs.set_evidence('faulty')
        sq.set_evidence('very_bad')
        print("asys = " + asys.get_evidence())
        print("cc = " + cc.get_evidence())
        print("tm = " + tm.get_evidence())
        print("fs = " + fs.get_evidence())
        print("sq = " + sq.get_evidence())
        probs = VE(car, st, [asys, tm, fs, cc, sq])
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
        print()
    
