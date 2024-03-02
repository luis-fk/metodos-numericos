# -*- coding: utf-8 -*-
""" 
Spyder Editor Spyder 3.2.3 

# MAP5725 - Roma, 01-02/2020.

# General, Explicit One-Step Methods for 
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
    return k1     # end: classical RK-44

    
#    return 1/6*(k1 + 2*k2 + 2*k3 + k4)     # end: classical RK-44
############################################################################
############################################################################
def f(t, y):
    # input n-dim ode system right hand side: f=(f0,f1,...,fn-1)
    # ATTENTION: Python arrays and lists start at index "0" !!!!
    
    f0 =  y[1]
    f1 = -y[0]
    
    return np.array([f0,f1])
############################################################################
############################################################################
def oneStepMethod(t0,y0,T,n):
    t_n = [t0];           # time interval: t in [t0,T]
    y_n = [np.array(y0)]  # initial condition
                         
    h   = (T-t0)/n        # time step

    while t_n[-1] < T:
        y_n.append( y_n[-1] + h*phi(t_n[-1],y_n[-1],h,f) )
        t_n.append(t_n[-1] + h)
        h = min(h, T-t_n[-1])
    y_n = np.array(y_n)
    
    return (T-t0)/n,y_n[-1]
############################################################################
def ye(t):
    # exact solution 
    return math.cos(t)
############################################################################
############################################################################
def main():
    t0=0; y0=[1,0];  # initial condition
    T=10             # final time
    
    m=9;  h=[0]*m;   # number of cases to run. Initialize list of time steps
    yn=[y0]*m;       # initialize list of approximations at final time T
    
    for i in range(1,m+1): # run m times same code with h->0
        n=16*2**(i-1)      # number of time steps in i-th case
        
        h[i-1],yn[i-1]=oneStepMethod(t0,y0,T,n);
        
        # example of convergence analysis for one of the components        
        r =0
        if i>1:
            r = abs(ye(T)-yn[i-2][0])/abs(ye(T)-yn[i-1][0])
#            r = math.log(abs(ye(T)-yn[i-2][0])/abs(ye(T)-yn[i-1][0]))/math.log(h[i-2]/h[i-1])
        print("%5d & %9.3e & %9.3e & %9.3e \\\\" % (n,h[i-1],abs(ye(T)-yn[i-1][0]),r)); 
        
#    for i in range(1,m):
#        print(i)
#        print(math.log(abs(ye(T)-yn[i-1][0])/abs(ye(T)-yn[i][0]))/
#              math.log(h[i-1]/h[i]));       
#        
#    for i in range(1,m-1):
#        print(math.log(abs(yn[i-1][0]-yn[i][0])/abs(yn[i][0]-yn[i+1][0]))/
#              math.log(h[i]/h[i+1]));
main()

