# -*- coding: utf-8 -*-
""" 
Spyder Editor Spyder 3.2.3 

# MAP5725 - Roma, 2023-01-03.

# general explicit one-Step methods and convergence tests implementation.

# (manufactured) problem with kwnown exact solution (mass-spring system) 
              d^2/dt^2 x(t) = - x(t)
              x(0)=1; d/dt x(0)=0
                         
"""
import math
import numpy as np
#############################################################################
def phi(t,y,dt,f):
    # define discretization function 
    
    k1 = f(t, y)
#    k2 = f(t+dt/2, y + dt/2*k1)
#    k3 = f(t+dt/2, y + dt/2*k2)
#    k4 = f(t+dt, y + dt*k3)
    return k1     # euler 
#    return 1/6*(k1 + 2*k2 + 2*k3 + k4)   # classical runge-kutta RK-44
############################################################################
############################################################################
def f(t, y):
    # input n-dim right hand side: f=(f0,f1,...,fn-1)
    # ATTENTION: Python arrays and lists start at index "0" !!!!
    
    f0 =  y[1]
    f1 = -y[0]
    
    return np.array([f0,f1])
############################################################################
############################################################################
def oneStepMethod(t0,y0,T,n):
    # compute approximate solution to the initial value problem
    t_n = [t0];           # time interval: t in [t0,T]
    y_n = [np.array(y0)]  # initial condition
                         
    h   = (T-t0)/n        # integration time step

    while t_n[-1] < T:
        # advance solution in time
        y_n.append( y_n[-1] + h*phi(t_n[-1],y_n[-1],h,f) ) 
        t_n.append(t_n[-1] + h)     # update clock
        h = min(h, T-t_n[-1])       # select new time step
    y_n = np.array(y_n)
    
    return (T-t0)/n,y_n[-1]
############################################################################
def ye(t):
    # exact solution 
    return math.cos(t)
############################################################################
############################################################################
def main():
    # input math model data
    t0=0; y0=[1,0];  # initial condition
    T=10             # final time
    
    # input numerical method data
    m=9;  h=[0]*m;   # number of cases to run. Initialize list of time steps
    yn=[y0]*m;       # initialize list of approximations
    
    print("ORDER BEHAVIOR CONVERGENCE TABLE");

    # case loop
    for i in range(1,m+1): # run m times same code with h progressively small
        n=16*2**(i-1);     # number of time steps in i-th case
        
        h[i-1],yn[i-1]=oneStepMethod(t0,y0,T,n);
        
        # verification via manufactured solution stragegy
        # convergence table to verify the method correct implementation 
        e=p=q=r=0;
        if i>1:
            q = abs((ye(T)-yn[i-2][0])/(ye(T)-yn[i-1][0]));
            r = h[i-2]/h[i-1];
            
            p = math.log(q)/math.log(r);
            
            e = abs(ye(T)-yn[i-1][0])
        print("%5d & %9.3e & %9.3e & %9.3e \\\\" % (n,h[i-1],e,p));
        
    print(" "); 
    
    # verification of the order without using/knowing the exact solution
    # convergence table to determine the behavior of the method for our problem    
    
    with open("behavior_convergence.txt", 'w', encoding='utf-8') as file2:
        file2.write("ORDER BEHAVIOR CONVERGENCE TABLE\n");

        e=p=q=r=0;
        for i in range(1,m+1):
            n=16*2**(i-1); 
            if i>2:
                q = abs((yn[i-3][0]-yn[i-2][0])/(yn[i-2][0]-yn[i-1][0]));
                r = h[i-2]/h[i-1];
            
                p = math.log(q)/math.log(r);
            
                e = abs((yn[i-2][0]-yn[i-1][0]));
                #print("%5d & %9.3e & %9.3e & %9.3e \\\\" % (n,h[i-1],e,p)); 
                file2.write("{:5d} & {:9.3e} & {:9.3e} & {:9.3e}\\\\\n".format(n,h[i-1],e,p))       
main()

