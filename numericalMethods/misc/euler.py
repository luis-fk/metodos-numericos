import matplotlib.pyplot as plt
import math
import numpy as np
import sys

def f(t,y):
    ''' Definicao da EDO'''
    f = -y/100
    return f

#-----------------------------------------------------------------------------

def euler(t,tf,n):
    '''Metodo de Euler'''
    y = [0]*(n+1)
    tempos = [0]*(n+1)
    y[0] = 200
    tempos[0] = t
    delta_t = (tf-t)/n
    for i in range(0,n):
        y[i+1] = y[i] + f(tempos[i], y[i])*delta_t
        tempos[i+1] = tempos[i] + delta_t

    erro = abs(solucao(tf) - y[n-1])
    
    return delta_t, erro, tempos, y

#-----------------------------------------------------------------------------

def solucao(t):
    '''Solucaoo da EDO calculada na questao 1 da tarefa 1'''
    s =200*math.exp(-t/100)
    return s

#############################################################################
#############################################################################

def main():
    ''' Programa principal que realiza o metodo de Euler k vezes onde a cada
    realizacao o intervalo utilizado no metodo e da forma 1/2^k'''
    k = 18 #Quantidade de iteracoes
    deltas = [0]*(k-2)
    erros = [0]*(k-2)
    nArr = [0]*(k-2)
    tempoFinal = 500
    
    for i in range(2,k):
         n = 2**i
         nArr[i-2] = n
         metodo = euler(0, tempoFinal, n)
         deltas[i-2], erros[i-2] = metodo[0:2]
         plt.plot(metodo[2], metodo[3], color='black')
         plt.xlabel('t')
         plt.ylabel('y(t)')
         plt.title('Convergência do Método de Runge-Kutta de 4° ordem')
         
    with open('numericalMethods/table.txt', 'w') as file:
        # Redirect the standard output to the file
        sys.stdout = file
        
        print(r"\hline\hline\h \\")
        print(r" n & Passo(Delta t) & $|e(t,h)|$ & $q=\frac{|e(t,2h)|}{|e(t,h)|}$ \\\\")
        print(r"\hline\hline \\")
        
        for i in range(len(deltas)):    
            if i >= 1:
                print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros[i]:.6f} & {erros[i-1]/erros[i]:.6f} \\")
            else:
                print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros[i]:.6f} \\")
        print(r"\hline\hline")
        
        # Reset the standard output to the console
        sys.stdout = sys.__stdout__
    
    plt.savefig('numericalMethods/convergencia.png')
    plt.show()
    
    X = np.linspace(0, tempoFinal, 1024)
    Y = np.linspace(0, tempoFinal, 1024)
    for i in range(len(X)):
        Y[i] = solucao(X[i])
    aprox = euler(0, tempoFinal, n)
    
    plt.plot(aprox[2],aprox[3], color='black', linestyle=(0,(1,1,3,1)),
             label = f'Aproximação numérica com n = {n}')
    plt.plot(X, Y, c = 'k', label = "Função verdadeira conhecida")
    plt.xlabel('t')
    plt.ylabel('y(t)')
    plt.title('Comparação entre o Método Numérico e a Solução Exata')
    plt.legend()
    plt.savefig('numericalMethods/comparacao.png')
    plt.show()

main()
    

