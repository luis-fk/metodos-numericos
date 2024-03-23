# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:59:38 2021

@author: Elisa
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl

#condicoes iniciais
#t=np.sqrt(np.pi)
#xin=0
#yin=-2*(np.sqrt(np.pi))
#tfin=np.sqrt(4*np.pi)


#define a função (f1  e f2 da tarefa)
def F(t,y_i):
  f1 = -1.2*y_i[-1] + 7*np.exp(-0.3*t)
  #f2 = (y_i[1])/t -4*(y_i[0])*(t**2)
  return f1

#define a função de discretização phi
def Phi(F,t,y_i,dt):
    p1 = F(t,y_i) #função phi para método de euler
    #p2 = F(t+dt, y_i + dt*p1) #função phi para método de euler aprimorado 
    return p1

#define método de Euler
def Euler(t0, tfin, xin, yin, n, F):
    i=1
    tsol=[t0]
    xsol=[xin]
    ysol=[yin]
    yn=np.array([xin, yin])
    dt=(tfin - t0)/n

    while i<=n:
        yn=yn +dt*Phi(F,t0,yn,dt)[0]
        tk=t0+dt
        xsol.append(yn[0])
        ysol.append(yn[1])
        tsol.append(tk)
        t0=tk
        xin=yn[0]
        yin=yn[1]
        i=i+1
    return(tsol,xsol,ysol)

def Eaprimorado(t0, tfin, xin, yin, n, F):
    i=1
    tsol=[t0]
    xsol=[xin]
    ysol=[yin]
    yn=np.array([xin, yin])
    dt=(tfin - t0)/n

    while i<=n:
        yn=yn +(dt/2)*(Phi(F,t0,yn,dt)[0] + Phi(F,t0,yn,dt)[1])
        tk=t0+dt
        xsol.append(yn[0])
        ysol.append(yn[1])
        tsol.append(tk)
        t0=tk
        xin=yn[0]
        yin=yn[1]
        i=i+1
    return(tsol,xsol,ysol)  

def Eimplicito(t0, tfin, xin, yin, n, F):
    i=1
    tsol=[t0]
    xsol=[xin]
    ysol=[yin]
    yn=np.array([xin, yin])
    dt=(tfin - t0)/n
    
    while i<=n:
        tk=t0 + dt
        c=1/((1-(dt/tk)) + 4*((dt)**2)*((tk)**2)) 
        xk= ((1-(dt/tk))*xin +dt*yin)*c
        yk=((-4*(tk**2)*dt*xin) +yin)*c 
        xsol.append(xk)
        ysol.append(yk)
        tsol.append(tk)
        t0=tk
        xin=xk
        yin=yk
        i=i+1
    return(tsol,xsol,ysol)

def Erro(t0, tfin, xin, yin, m, F):
    i=m
    qtdm=[]
    taberrog=[]
    tabh=[]
    n=2**m
    tabq=[]
    tabp=[]
    #falta a ultima parte da tabela e(t,2h)/e(t,h)
    
    while i<=14:
        h=(tfin-t0)/(2**i)
        qtdm.append(i)
        tabh.append(h)
        listaxE=Euler(t0, tfin, xin, yin, n, F)[1]
        listayE=Euler(t0, tfin, xin, yin, n, F)[2]
        xaE=listaxE[-1]
        yaE=listayE[-1]
        xe=np.sin((tfin)**2)
        ye=2*(tfin)*np.cos((tfin)**2)
        errox=abs(xe-xaE)
        erroy=abs(ye-yaE)
        errog=max([errox,erroy])
        taberrog.append(errog)
        if i>2:
            q=abs((taberrog[-2])/(taberrog[-1]))
            tabq.append(q)
            p=math.log(q,2)
            tabp.append(p)
        i=i+1
        n=2**i
     
    return(qtdm,tabh,taberrog,tabq,tabp)

def ErroApr(t0, tfin, xin, yin, m, F):
    i=m
    qtdm=[]
    taberrog=[]
    tabh=[]
    n=2**m
    tabq=[]
    tabp=[]
    #falta a ultima parte da tabela e(t,2h)/e(t,h)
    
    while i<=14:
        h=(tfin-t0)/(2**i)
        qtdm.append(i)
        tabh.append(h)
        listaxE=Eaprimorado(t0, tfin, xin, yin, n, F)[1]
        listayE=Eaprimorado(t0, tfin, xin, yin, n, F)[2]
        xaE=listaxE[-1]
        yaE=listayE[-1]
        xe=np.sin((tfin)**2)
        ye=2*(tfin)*np.cos((tfin)**2)
        errox=abs(xe-xaE)
        erroy=abs(ye-yaE)
        errog=max([errox,erroy])
        taberrog.append(errog)
        if i>2:
            q=abs((taberrog[-2])/(taberrog[-1]))
            tabq.append(q)
            p=math.log(q,2)
            tabp.append(p)
        i=i+1
        n=2**i
     
    return(qtdm,tabh,taberrog,tabq,tabp)
    

def ErroImp(t0, tfin, xin, yin, m, F):
    i=m
    qtdm=[]
    taberrog=[]
    tabh=[]
    n=2**m
    tabq=[]
    tabp=[]
    #falta a ultima parte da tabela e(t,2h)/e(t,h)
    
    while i<=16:
        h=(tfin-t0)/(2**i)
        qtdm.append(i)
        tabh.append(h)
        listayE=Eimplicito(t0, tfin, xin, yin, n, F)
        yaE=listayE[-1]

        # y1 = np.sin((t)**2)
        # y2 = 2*(t)*np.cos((t)**2)


        ye=(70/9)*np.exp(-0.3*tfin) - (43/9)*np.exp(-1.2*tfin)
        
        erroy=abs(ye-yaE)
        errog=erroy
        taberrog.append(errog)
        if i>2:
            q=abs(taberrog[-2])/(taberrog[-1])
            tabq.append(q)
            p=math.log(q,2)
            tabp.append(p)
        i=i+1
        n=2**i
     
    return(qtdm,tabh,taberrog,tabq,tabp)

#ERRO DE DISCR SEM UTILIZAR A SOLUCAO EXATA
def ErroICaso2(t0, tfin, xin, yin, m, F):
    i=m
    qtdm=[]
    taberrog=[]
    tabh=[]
    n=2**m
    tabq=[]
    tabp=[]
    listax=[]
    listay=[]
    #falta a ultima parte da tabela e(t,2h)/e(t,h)
    
    while i<=14:
        h=(tfin-t0)/(2**i)
        qtdm.append(i)
        tabh.append(h)
        xE=Eimplicito(t0, tfin, xin, yin, n, F)[1]
        yE=Eimplicito(t0, tfin, xin, yin, n, F)[2]
        listax.append(xE[-1])
        listay.append(yE[-1])
        if i==3:
            errox=abs(-listax[-2] + listax[-1])
            erroy=abs(-listay[-2] + listay[-1])
            errog = max(errox,erroy)
            taberrog.append(errog)
        if i>3:
            errox=abs(-listax[-2] + listax[-1])
            erroy=abs(-listay[-2] + listay[-1])
            errog = max(errox,erroy)
            taberrog.append(errog)           
            q=abs((taberrog[-2])/(taberrog[-1]))
            tabq.append(q)
            p=math.log(q,2)
            tabp.append(p)
        i=i+1
        n=2**i
     
    return(qtdm,tabh,taberrog,tabq,tabp)

opcao = 0
print('Vamos testar o método de Euler implícito')
while opcao!=8:
    print('''       [1] Gráfico x vs t - diferentes n
          [2] Gráfico y vs t - diferentes n
          [3] Gráfico x vs t - solução exata e numérica
          [4] Gráfico y vs t - solução exata e numérica
          [5] Gráfico x,y vs t - solução exata e numérica
          [6] Tabela erro de discretização COM solução exata
          [7] Tabela erro de discretização SEM solução exata
          [8] Sair do teste''')
    opcao = int(input('Qual é a sua opção?'))
    if opcao==1:
        teste1_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 64, F)
        teste2_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 128, F)
        teste3_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 256, F)
        teste4_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 512, F)
        #Gráfico Método de Euler Implicito- x(t) diferentes n
        plt.plot(teste1_I[0],teste1_I[1],'k--', label='n=64')
        plt.plot(teste2_I[0],teste2_I[1], 'k:', label='n=128')
        plt.plot(teste3_I[0],teste3_I[1], 'k',label='n=256')
        plt.plot(teste4_I[0],teste4_I[1], 'k-.',label='n=512')
        plt.title("Método de Euler Implícito - Gráfico x(t)")
        plt.xlabel("(t)")
        plt.ylabel("x(t)")
        plt.legend()
        plt.show()
    elif opcao==2:
        teste1_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 64, F)
        teste2_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 128, F)
        teste3_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 256, F)
        teste4_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 512, F)
        #Gráfico Método de Euler Implicito- y(t) diferentes n
        plt.plot(teste1_I[0],teste1_I[2],'k--', label='n=64')
        plt.plot(teste2_I[0],teste2_I[2], 'k:', label='n=128')
        plt.plot(teste3_I[0],teste3_I[2], 'k',label='n=256')
        plt.plot(teste4_I[0],teste4_I[2], 'k-.',label='n=512')
        plt.title("Método de Euler Implícito - Gráfico y(t)")
        plt.xlabel("(t)")
        plt.ylabel("y(t)")
        plt.legend()
        plt.show()
    elif opcao==3:
        #solução exata
        t1=np.linspace(math.sqrt(math.pi),2*math.sqrt(math.pi), 500,  endpoint=True)
        xe=np.sin((t1)**2)
        ye=2*(t1)*np.cos((t1)**2)
        #Gráfico x(t) Euler Implícito
        teste4_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 512, F)
        plt.plot(teste4_I[0],teste4_I[1], 'k--', label='x(t) numérica')
        pl.plot(t1,xe,'k', label='x(t) exata')
        plt.xlabel("(t)")
        plt.ylabel("x(t)")
        plt.title("Método de Euler Implícito para o Problema de Cauchy")
        plt.legend()
        plt.show()
    elif opcao==4:
        #solução exata
        t1=np.linspace(math.sqrt(math.pi),2*math.sqrt(math.pi), 500,  endpoint=True)
        xe=np.sin((t1)**2)
        ye=2*(t1)*np.cos((t1)**2)
        #Gráfico y(t) Euler Implícito
        teste4_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 512, F)
        plt.plot(teste4_I[0],teste4_I[2], 'k--', label='y(t) numérica')
        pl.plot(t1,ye,'k', label='y(t) exata')
        plt.xlabel("(t)")
        plt.ylabel("y(t)")
        plt.ylim([-10,10])
        plt.title("Método de Euler Implícito para o Problema de Cauchy")
        plt.legend()
        plt.show()
    elif opcao==5:
        #solução exata
        t1=np.linspace(math.sqrt(math.pi),2*math.sqrt(math.pi), 500,  endpoint=True)
        xe=np.sin((t1)**2)
        ye=2*(t1)*np.cos((t1)**2)
        teste4_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 256, F)
        plt.plot(teste4_I[0],teste4_I[1], 'k-.', label='x(t) numérica',) + plt.plot(teste4_I[0],teste4_I[2], 'k:', label='y(t) numérica') + pl.plot(t1,xe,'k', label='x(t) exata') + pl.plot(t1,ye,'k', label='y(t) exata',linewidth=0.7) 
        plt.xlabel('t')
        plt.ylabel('x(t) e y(t)')
        plt.ylim([-8,8])
        plt.title('Aproximação numérica para o método de Euler implícito com n=256')
        plt.legend()
        plt.show()
    elif opcao==6:
        testeerroI=ErroImp(0, 1, 0, 3, 2, F)   
        print(testeerroI)
    elif opcao==7:
        testeCaso2I=ErroICaso2(0, 1, 0, 3, 2, F)
        print(testeCaso2I)
    elif opcao==8:
        print('Finalizando...')
    else:
        print('Opção inválida. Tente novamente:')
                      
print('Fim da tarefa')          
        
    
#testeerro=Erro(np.sqrt(np.pi), (np.sqrt(np.pi))+1, 0, -2*(np.sqrt(np.pi)), 2, F)   
#print(testeerro)  
     
#testeerroA=ErroApr(np.sqrt(np.pi), (np.sqrt(np.pi))+1, 0, -2*(np.sqrt(np.pi)), 2, F)   
#print(testeerroA)      

#testeerroI=ErroImp(np.sqrt(np.pi), (np.sqrt(np.pi))+1, 0, -2*(np.sqrt(np.pi)), 2, F)   
#print(testeerroI)  

#teste1_E= Euler(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 16, F)
#print(np.array(teste1_E))

#teste2_E = Euler(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 64, F)
#print(np.array(teste1_E))

#teste3_E = Euler(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 128, F)
#print(np.array(teste1_E))

#teste4_E = Euler(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 256, F)
#print(np.array(teste1_E))

#teste1_A = Eaprimorado(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 16, F)
#print(np.array(teste1_A)
#teste2_A = Eaprimorado(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 32, F)
#teste3_A = Eaprimorado(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 64, F)
#teste4_A = Eaprimorado(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 128, F)

#teste1_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 64, F)
#print(np.array(teste1_I))
#teste2_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 128, F)
#teste3_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 256, F)
#teste4_I = Eimplicito(np.sqrt(np.pi), 2*np.sqrt(np.pi), 0, -2*(np.sqrt(np.pi)), 512, F)

#solução exata
#t1=np.linspace(math.sqrt(math.pi),2*math.sqrt(math.pi), 500,  endpoint=True)
#xe=np.sin((t1)**2)
#ye=2*(t1)*np.cos((t1)**2)

#Gráfico x(t) Euler 
#plt.plot(teste4_E[0],teste4_E[1], 'k--', label='x(t) numérica')
#pl.plot(t1,xe,'k', label='x(t) exata')
#plt.xlabel("(t)")
#plt.ylabel("x(t)")
#plt.ylim([-10,10])
#plt.title("Método de Euler para o Problema de Cauchy")
#plt.legend()
#plt.show()

#Gráfico y(t) Euler
#plt.plot(teste4_E[0],teste4_E[2], 'k--', label='y(t) numérica')
#pl.plot(t1,ye,'k', label='y(t) exata')
#plt.xlabel("(t)")
#plt.ylabel("y(t)")
#plt.ylim([-20,20])
#plt.title("Método de Euler para o Problema de Cauchy")
#plt.legend()
#plt.show()



#plt.title("Método de Euler - Gráfico x(t) ")

#plt.plot(tsol,ysol,'k--')
#pl.plot(t1,ye,'k')
#plt.xlabel("(t)")
#plt.ylabel("y(t)")
#plt.title("Método de Euler - Gráfico y(t) ")

#Gráfico Método de Euler - x(t) diferentes n
#plt.plot(teste1_E[0],teste1_E[1],'k--', label='n=16')
#plt.plot(teste2_E[0],teste2_E[1], 'k:', label='n=64')
#plt.plot(teste3_E[0],teste3_E[1], 'k',label='n=128')
#plt.plot(teste4_E[0],teste4_E[1], 'k-.',label='n=256')
#plt.title("Método de Euler - Gráfico x(t)")
#plt.ylim([-3,3])
#plt.xlabel("(t)")
#plt.ylabel("x(t)")
#plt.legend()
#plt.show()

#Gráfico Método de Euler - y(t) diferentes n
#plt.plot(teste1_E[0],teste1_E[2],'k--', label='n=16')
#plt.plot(teste2_E[0],teste2_E[2], 'k:', label='n=64')
#plt.plot(teste3_E[0],teste3_E[2], 'k',label='n=128')
#plt.plot(teste4_E[0],teste4_E[2], 'k-.',label='n=256')
#plt.title("Método de Euler - Gráfico y(t)")
#plt.ylim([-3,3])
#plt.xlabel("(t)")
#plt.ylabel("y(t)")
#plt.legend()
#plt.show()

#Gráfico Método de Euler Aprimorado- x(t) diferentes n
#plt.plot(teste1_A[0],teste1_A[1],'k--', label='n=16')
#plt.plot(teste2_A[0],teste2_A[1], 'k:', label='n=32')
#plt.plot(teste3_A[0],teste3_A[1], 'k',label='n=64')
#plt.plot(teste4_A[0],teste4_A[1], 'k-.',label='n=128')
#plt.title("Método de Euler Aprimorado - Gráfico x(t)")
#plt.ylim([-3,3])
#plt.xlabel("(t)")
#plt.ylabel("x(t)")
#plt.legend()
#plt.show()

#Gráfico Método de Euler aprimorado - y(t) diferentes n
#plt.plot(teste1_A[0],teste1_A[2],'k--', label='n=16')
#plt.plot(teste2_A[0],teste2_A[2], 'k:', label='n=32')
#plt.plot(teste3_A[0],teste3_A[2], 'k',label='n=64')
#plt.plot(teste4_A[0],teste4_A[2], 'k-.',label='n=128')
#plt.title("Método de Euler Aprimorado - Gráfico y(t)")
#plt.ylim([-3,3])
#plt.xlabel("(t)")
#plt.ylabel("y(t)")
#plt.legend()
#plt.show()

#Gráfico x(t) Euler Aprimorado
#plt.plot(teste2_A[0],teste2_A[1], 'k--', label='x(t) numérica')
#pl.plot(t1,xe,'k', label='x(t) exata')
#plt.xlabel("(t)")
#plt.ylabel("x(t)")
#plt.ylim([-10,10])
#plt.title("Método de Euler Aprimorado para o Problema de Cauchy")
#plt.legend()
#plt.show()

#Gráfico y(t) Euler Aprimorado
#plt.plot(teste2_A[0],teste2_A[2], 'k--', label='y(t) numérica')
#pl.plot(t1,ye,'k', label='y(t) exata')
#plt.xlabel("(t)")
#plt.ylabel("y(t)")
#plt.ylim([-20,20])
#plt.title("Método de Euler Aprimorado para o Problema de Cauchy")
#plt.legend()
#plt.show()

#Gráfico Método de Euler Implicito- x(t) diferentes n
#plt.plot(teste1_I[0],teste1_I[1],'k--', label='n=64')
#plt.plot(teste2_I[0],teste2_I[1], 'k:', label='n=128')
#plt.plot(teste3_I[0],teste3_I[1], 'k',label='n=256')
#plt.plot(teste4_I[0],teste4_I[1], 'k-.',label='n=512')
#plt.title("Método de Euler Implícito - Gráfico x(t)")
#plt.ylim([-3,3])
#plt.xlabel("(t)")
#plt.ylabel("x(t)")
#plt.legend()
#plt.show()

#Gráfico Método de Euler Implicito- y(t) diferentes n
#plt.plot(teste1_I[0],teste1_I[2],'k--', label='n=64')
#plt.plot(teste2_I[0],teste2_I[2], 'k:', label='n=128')
#plt.plot(teste3_I[0],teste3_I[2], 'k',label='n=256')
#plt.plot(teste4_I[0],teste4_I[2], 'k-.',label='n=512')
#plt.title("Método de Euler Implícito - Gráfico y(t)")
#plt.ylim([-3,3])
#plt.xlabel("(t)")
#plt.ylabel("y(t)")
#plt.legend()
#plt.show()

#Gráfico x(t) Euler Implícito
#plt.plot(teste4_I[0],teste4_I[1], 'k--', label='x(t) numérica')
#pl.plot(t1,xe,'k', label='x(t) exata')
#plt.xlabel("(t)")
#plt.ylabel("x(t)")
#plt.ylim([-10,10])
#plt.title("Método de Euler Implícito para o Problema de Cauchy")
#plt.legend()
#plt.show()

#Gráfico y(t) Euler Implícito
#plt.plot(teste4_I[0],teste4_I[2], 'k--', label='y(t) numérica')
#pl.plot(t1,ye,'k', label='y(t) exata')
#plt.xlabel("(t)")
#plt.ylabel("y(t)")
#plt.ylim([-10,10])
#plt.title("Método de Euler Implícito para o Problema de Cauchy")
#plt.legend()
#plt.show()

