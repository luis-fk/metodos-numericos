import matplotlib.pyplot as plt
import math
import numpy as np
import sys

def phi(t,y,dt,f):

    k1 = f(t, y)
    k2 = f(t+dt/2, y + dt/2*k1)
    k3 = f(t+dt/2, y + dt/2*k2)
    k4 = f(t+dt, y + dt*k3)
    
    return (1/6)*(k1 + 2*k2 + 2*k3 + k4)   

def phi2(t,y1, y2, y3, dt,f):

    k1 = f(t, y1, y2, y3)
    k2 = f(t+dt/2, y1 + (dt/2)*k1, y2 + (dt/2)*k1, y3 + (dt/2)*k1)
    k3 = f(t+dt/2, y1 + (dt/2)*k2, y2 + (dt/2)*k2, y3 + (dt/2)*k2)
    k4 = f(t+dt, y1 + dt*k3, y2 + dt*k3, y3 + dt*k3)
    
    return (1/6)*(k1 + 2*k2 + 2*k3 + k4)   


def f1(t, y):
    f1 =  y
    return (f1)


def f2(t, y):
    f2 =  y
    return (f2)


def f3(t, y1, y2, y3):
    f3 =  -6*y3 - 12*y2 - 8*y1
    return (f3)


def solucao(t):
    s = np.exp(-2*t) + (4*np.exp(-2*t)*t) + (6*np.exp(-2*t)*(t**2))
    return (s)


def rungeKutta(t, tf, n):
    t_n = [(t)]
    T = (tf)        # time interval: t in [t0,T]
    y1 = [(1)]  # initial condition
    y2 = [(2)]
    y3 = [(0)]
    
    dt = ((T-t_n[-1])/n)
    while t_n[-1] < T:
        y3.append(y3[-1] + dt*phi2(t_n[-1], y1[-1], y2[-1], y3[-1], dt, f3))
        y2.append(y2[-1] + dt*phi(t_n[-1], y3[-2], dt, f2))
        y1.append(y1[-1] + dt*phi(t_n[-1], y2[-2], dt, f1))
        t_n.append(t_n[-1] + dt)
    
    y = np.array(y1)
    erro = abs(solucao(tf) - y[-1])
    print(solucao(tf), y[-1])

    return (T-t)/n, erro, t_n, y
    
    
def main():
    k = 16 #Quantidade de iteracoes
    deltas = [0]*(k-2)
    erros = [0]*(k-2)
    nArr = [0]*(k-2)
    tempoFinal = 1
    
    for i in range(2,k):
         n = 2**i
         nArr[i-2] = n
         metodo = rungeKutta(0, tempoFinal, n)
         deltas[i-2], erros[i-2] = metodo[0:2]
         plt.plot(metodo[2], metodo[3], color='black')
         plt.xlabel('t')
         plt.ylabel('y(t)')
         plt.title('Convergência do Método de Runge-Kutta de 4° ordem')
         
    with open('inputs-outputs/table.txt', 'w') as file:
        # Redirect the standard output to the file
        sys.stdout = file
        
        print(r"\hline\hline\ \\")
        print(r" n & Passo(Delta t) & $|e(t,h)|$ & $q=\frac{|e(t,2h)|}{|e(t,h)|}$ \\\\")
        print(r"\hline\hline \\")
        
        for i in range(len(deltas)):    
            if i >= 1:
                print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros[i]:.6f} & {(erros[i-1]/erros[i]):.6f} \\")
            else:
                print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros[i]:.6f} \\")
        print(r"\hline\hline")
        
        # Reset the standard output to the console
        sys.stdout = sys.__stdout__
    
    plt.savefig('imagens/convergencia.png')
    # plt.show()
    
    X = np.linspace(0, tempoFinal, 1024)
    Y = np.linspace(0, tempoFinal, 1024)
    for i in range(len(X)):
        Y[i] = solucao(X[i])
    aprox = rungeKutta(0, tempoFinal, n)
    
    plt.plot(aprox[2],aprox[3], color='black', linestyle=(0,(1,1,3,1)),
             label = f'Aproximação numérica com n = {n}')
    plt.plot(X, Y, c = 'k', label = "Função verdadeira conhecida")
    plt.xlabel('t')
    plt.ylabel('y(t)')
    plt.title('Comparação entre o Método Numérico e a Solução Exata')
    plt.legend()
    plt.savefig('imagens/comparacao.png')
    # plt.show()

main()
    

