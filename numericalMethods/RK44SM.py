import numpy as np
import matplotlib.pyplot as plt
import sys
import math
# Define o tipo de dados para precisão dupla
dp = np.float64

# Ordem da ODE
m = 3

def f(x, Yvec):
    """
    Função f que calcula o vetor f.
    """
    fvec = np.zeros(m, dtype=dp)
    fvec[0] = Yvec[1]  # y1
    fvec[1] = Yvec[2]  # y2
    fvec[2] = -6*Yvec[2] -12*Yvec[1] - 8*Yvec[0]  # y3


    return fvec

def phi(x, Y_n, h):
    """
    Função iterate que calcula Y(t_n+1).
    """
    k1 = f(x, Y_n)
    k2 = f(x + h/2, Y_n + h*k1/2)
    k3 = f(x + h/2, Y_n + h*k2/2)
    k4 = f(x + h, Y_n + h*k3)

    Y_nplus1 = (k1 + 2*k2 + 2*k3 + k4) / 6
    return Y_nplus1

def rungeKutta(t0, tf, n):
    t_n = [t0]
    T = tf
    y_k = np.zeros((n+1, m))  # Matriz para armazenar y_k em cada passo
    
    y_k[0] = [1, 2, 0]  # Condições iniciais

    dt = (T - t0) / n

    i = 0
    while(t_n[-1] < T):
        y_k[i+1] = y_k[i] + dt * phi(t_n[i], y_k[i], dt)
        t_n.append(t_n[i] + dt)
        i+=1

    erros = calculaErro(y_k[-1], T)
    return dt, erros, t_n, y_k

def calculaErro(yk, tf):
    return abs(yk - solucao(tf))

def solucao(tf):
    solucao = []
    solucao.append(np.exp(-2*tf) + 4*tf*np.exp(-2*tf) + 6*(tf**2)*np.exp(-2*tf))
    solucao.append(2*np.exp(-2*tf) + 4*tf*np.exp(-2*tf) - 12*(tf**2)*np.exp(-2*tf))
    solucao.append(-32*tf*np.exp(-2*tf) + 24*(tf**2)*np.exp(-2*tf))
    return np.array(solucao)

def main():
    k = 12  # Quantidade de iterações
    deltas = [0] * (k - 2)
    nArr = [0] * (k - 2)
    tempoFinal = 10
    erros = []
    imagens_x = [[] for range in range(m)]
    imagens_y = [[] for range in range(m)]
    cores = [ 'r', 'g', 'b', 'c', 'm', 'y', 'k']
    for i in range(2, k):
        n = 2**i
        nArr[i - 2] = n
        metodo = rungeKutta(0, tempoFinal, n)  # dt, erros, t_n, y_k
        deltas[i-2] = metodo[0]
        erros.append(metodo[1])

        for j in range(m):
            imagens_x[j].append(metodo[2])
            imagens_y[j].append(metodo[3][:, j])


    for j in range(m):
        plt.plot(color=cores[j])
        for i in range(k-2):
            plt.plot(imagens_x[j][i], imagens_y[j][i], label = f'n = {nArr[i]}')  # Plotando apenas a primeira coluna de y_k
            plt.xlabel('Tempo')
            plt.ylabel(f'y$_{j}$(t)')
            plt.legend()
        plt.title(f'Convergência do Método de Runge-Kutta de 4ª ordem para a variável y$_{j+1}$')
        plt.savefig(f'imagens/convergencia{j+1}.png')
        plt.clf()

        X = np.linspace(0, tempoFinal, 2**k)
        
        Y = []
        for i in range(len(X)):
            Y.append(solucao(X[i])[j])
        
        plt.plot(X, Y, c = 'k', label = f"Função y$_{j+1}$ verdadeira conhecida")

        plt.plot(imagens_x[j][-1], imagens_y[j][-1], color='#7fe5fa', linestyle=(0,(1,2,3,2)),
                 label = f'Aproximação numérica com n={n}')  

        plt.xlabel('Tempo')
        plt.ylabel(f'y$_{j+1}$(t)')
        plt.title(f'Comparação entre o Método Numérico e a Solução Exata de y$_{j+1}$(t)')
        plt.legend()

        plt.savefig(f'imagens/comparacao{j+1}.png')
        plt.clf()
    
    deltas = np.array(deltas)
    erros = np.array(erros)


    with open('inputs-outputs/table1.txt', 'w') as file:
        # Redirect the standard output to the file
        sys.stdout = file
        for j in range(m):
            
            print("tabela ", j)
            print("\n")
            print(r"\hline\hline\ \\")
            print(r" n & Passo(Delta t) & $|e(t,h)|$ & $q=\frac{|e(t,2h)|}{|e(t,h)|}$ \\\\")
            print(r"\hline\hline \\")
            
            for i in range(k-2):    
                if i >= 1:
                    print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros[i][j]:.6f} & {math.log((erros[i-1][j]/erros[i][j]),2):.6f} \\")
                else:
                    print(fr"{nArr[i]} & {deltas[i]:.6f} & {erros[i][j]:.6f} \\")
            print(r"\hline\hline")
            print("\n")
            # Reset the standard output to the console
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
