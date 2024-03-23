import matplotlib.pyplot as plt
import numpy as np
import sys
import math

def phi(t, y, z, dt):

    k0 = f1(z)
    l0 = f2(y, z)
    
    k1 = f1(z + dt/2*l0)
    l1 = f2(y + 1/2*dt*k0, z + 1/2*dt*l0)
    
    k2 = f1(z + dt/2*l1)
    l2 = f2(y + 1/2*dt*k1, z + 1/2*dt*l1)
    
    k3 = f1(z + dt*l2)
    l3 = f2(y + dt*k2, z + dt*l2)

    return ((1/6)*(k0 + 2*k1 + 2*k2 + k3), (1/6)*(l0 + 2*l1 + 2*l2 + l3))


def f1(z)->float:
    f1 =  z
    return (f1)


def f2(y, z)->float:
    f2 =  6*y-z
    return (f2)


def solucao(t):
    s1 = 2*np.exp(2*t) + np.exp(-3*t)
    return (s1)

def solucao2(t):
    s2 = 4*np.exp(2*t) -3*np.exp(-3*t)
    return (s2)

def rungeKutta(t, tf, n):
    t_n = [(t)]
    T = (tf)
    z = [(1)]  # initial condition
    y = [(3)]
        
    dt = ((T-t_n[-1])/n)
    while t_n[-1] < T:
        yk, zk = phi(t_n[-1], y[-1], z[-1], dt)
        y.append(y[-1] + dt*yk)
        z.append(z[-1] + dt*zk)
        t_n.append(t_n[-1] + dt)
    
    ySol = np.array(y)
    zSol = np.array(z)
    erro_ySol = abs(solucao(tf) - ySol[-1])
    erro_zSol = abs(solucao2(tf) - zSol[-1])
    print(ySol[-1], solucao(tf), zSol[-1], solucao2(tf))
    return (T-t)/n, erro_ySol, erro_zSol, t_n, ySol
    
        
def main():
    k = 10 #Quantidade de iteracoes
    deltas = [0]*(k-2)
    erros_y1 = [0]*(k-2)
    erros_y2 = [0]*(k-2)
    nArr = [0]*(k-2)
    tempoFinal = 1
    
    for i in range(2,k):
         n = 2**i
         nArr[i-2] = n
         metodo = rungeKutta(0, tempoFinal, n) # (T-t)/n, erro_y1, erro_y2, t_n, y1
         deltas[i-2], erros_y1[i-2], erros_y2[i-2] = metodo[0:3]
         plt.plot(metodo[3], metodo[4], color='black')
         plt.xlabel('t')
         plt.ylabel('y(t)')
         plt.title('Convergência do Método de Runge-Kutta de 4° ordem para a variável y1')
         
    # tabela de y1
    with open('inputs-outputs/table1.txt', 'w') as file:
        # Redirect the standard output to the file
        sys.stdout = file
        
        print(r"\hline\hline\ \\")
        print(r" n & Passo(Delta t) & $|e(t,h)|$ & $q=\frac{|e(t,2h)|}{|e(t,h)|}$ \\\\")
        print(r"\hline\hline \\")
        
        for i in range(len(deltas)):    
            if i >= 1:
                print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros_y1[i]:.6f} & {math.log((erros_y1[i-1]/erros_y1[i]),2):.6f} \\")
            else:
                print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros_y1[i]:.6f} \\")
        print(r"\hline\hline")
        
        # Reset the standard output to the console
        sys.stdout = sys.__stdout__
    
    # tabela de y2
    with open('inputs-outputs/table2.txt', 'w') as file:
        # Redirect the standard output to the file
        sys.stdout = file
        
        print(r"\hline\hline\ \\")
        print(r" n & Passo(Delta t) & $|e(t,h)|$ & $q=\frac{|e(t,2h)|}{|e(t,h)|}$ \\\\")
        print(r"\hline\hline \\")
        
        for i in range(len(deltas)):    
            if i >= 1:
                print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros_y2[i]:.6f} & {math.log((erros_y2[i-1]/erros_y2[i]),2):.6f} \\")
            else:
                print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros_y2[i]:.6f} \\")
        print(r"\hline\hline")
        
        # Reset the standard output to the console
        sys.stdout = sys.__stdout__
    
    plt.savefig('imagens/convergencia.png')
    # plt.show()
    
    X = np.linspace(0, tempoFinal, 1024)
    Y = np.linspace(0, tempoFinal, 1024)
    for i in range(len(X)):
        Y[i] = solucao(X[i])
    metodo = rungeKutta(0, tempoFinal, n)
    aprox = metodo[3], metodo[4] 
    
    plt.plot(aprox[0],aprox[1], color='black', linestyle=(0,(1,1,3,1)),
             label = f'Aproximação numérica com n = {n}')
    plt.plot(X, Y, c = 'k', label = "Função verdadeira conhecida")
    plt.xlabel('t')
    plt.ylabel('y(t)')
    plt.title('Comparação entre o Método Numérico e a Solução Exata')
    plt.legend()
    plt.savefig('imagens/comparacao.png')

main()