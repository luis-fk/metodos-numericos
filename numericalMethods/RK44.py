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


def f(t, y):
    f0 =  -y*0.00001 # cos(x) - função
    return (f0)


def solucao(t):
    s =(10000)*(math.exp((-t)*0.00001))
    return (s)


def rungeKutta(t, tf, n):
    t_n = [(t)]
    T = (tf)        # time interval: t in [t0,T]
    y_n = [(10000)]  # initial condition
    
    dt = ((T-t_n[-1])/n)
    while t_n[-1] < T:
        y_n.append(y_n[-1] + dt*phi(t_n[-1],y_n[-1],dt,f))
        t_n.append(t_n[-1] + dt)
        
    y_n = np.array(y_n)
    erro = abs(solucao(tf) - y_n[-1])
    print(solucao(tf), y_n[-1])

    return (T-t)/n, erro, t_n, y_n
    
    
def main():
    k = 10 #Quantidade de iteracoes
    deltas = [0]*(k-2)
    erros = [0]*(k-2)
    nArr = [0]*(k-2)
    tempoFinal = 100000
    
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
    

