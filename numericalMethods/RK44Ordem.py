import numpy as np
import matplotlib.pyplot as plt
import sys
import math
# Define o tipo de dados para precisão dupla
dp = np.float64

# Ordem da ODE
m = 18
G = 6.6743e-11
m1 = 1.9885e30
m2 = 5.972e27
m3 = 5.972e27

def f(x, Yvec):
    """
    Função f que calcula o vetor f.
    """
    
    distancia12 = (((Yvec[0]-Yvec[6])**2  + (Yvec[1]-Yvec[7])**2  + (Yvec[2]-Yvec[8])**2))**(3/2)
    distancia13 = (((Yvec[0]-Yvec[12])**2 + (Yvec[1]-Yvec[13])**2 + (Yvec[2]-Yvec[14])**2))**(3/2)
    distancia23 = (((Yvec[6]-Yvec[12])**2 + (Yvec[7]-Yvec[13])**2 + (Yvec[8]-Yvec[14])**2))**(3/2)

    fvec = np.zeros(m, dtype=dp)
    
    fvec[0] = Yvec[3] # x1
    fvec[1] = Yvec[4] # y1
    fvec[2] = Yvec[5] # z1
    fvec[3] = -G*(m2*((Yvec[0]-Yvec[6])/distancia12) + m3*((Yvec[0]-Yvec[12])/distancia13)) # vx1
    fvec[4] = -G*(m2*((Yvec[1]-Yvec[7])/distancia12) + m3*((Yvec[1]-Yvec[13])/distancia13)) # vy2
    fvec[5] = -G*(m2*((Yvec[2]-Yvec[8])/distancia12) + m3*((Yvec[2]-Yvec[14])/distancia13)) # vz3
 
    fvec[6] = Yvec[9]  # x2
    fvec[7] = Yvec[10] # y2
    fvec[8] = Yvec[11] # z2
    fvec[9] =  -G*(m1*((Yvec[6]-Yvec[0])/distancia12) + m3*((Yvec[6]-Yvec[12])/distancia23)) # vx2
    fvec[10] = -G*(m1*((Yvec[7]-Yvec[1])/distancia12) + m3*((Yvec[7]-Yvec[13])/distancia23)) # vy2
    fvec[11] = -G*(m1*((Yvec[8]-Yvec[2])/distancia12) + m3*((Yvec[8]-Yvec[14])/distancia23)) # vz3
    
    fvec[12] = Yvec[15] # x3
    fvec[13] = Yvec[16] # y3
    fvec[14] = Yvec[17] # z3
    fvec[15] = -G*(m1*((Yvec[12]-Yvec[0])/distancia13) + m2*((Yvec[12]-Yvec[6])/distancia23)) # vx3
    fvec[16] = -G*(m1*((Yvec[13]-Yvec[1])/distancia13) + m2*((Yvec[13]-Yvec[7])/distancia23)) # vy3
    fvec[17] = -G*(m1*((Yvec[14]-Yvec[2])/distancia13) + m2*((Yvec[14]-Yvec[8])/distancia23)) # vz3

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


    y_k[0] = [           0, 0, 0, 0,  0, 5000, 
                1.47095e11, 0, 0, 0, 30290, 0, 
               -1.47095e11, 0, 0, 0, -30290, 0] 

    dt = (T - t0) / n

    i = 0
    while(t_n[-1] < T):
        y_k[i+1] = y_k[i] + dt * phi(t_n[i], y_k[i], dt)
        t_n.append(t_n[i] + dt)
        i+=1

    return dt, t_n, y_k

def main():
    k = 12  # Quantidade de iterações
    deltas = [0] * (k - 2)
    nArr = [0] * (k - 2)
    tempoFinal = 100000000
                 
    
    tempo = []
    imagens = [[] for range in range(m)]
    for i in range(2, k):
        yk = []
        n = 2**i
        nArr[i - 2] = n
        metodo = rungeKutta(0, tempoFinal, n)  # dt, t_n, y_k
        yk.append(metodo[2])
        tempo.append(metodo[1])
        deltas[i-2] = metodo[0]
        for j in range(m):
                auxiliar = []
                for l in range(n+1):
                    auxiliar.append(yk[0][l][j])
                imagens[j].append(auxiliar)

    posicao = [1,2,3,7,8,9,13,14,15]
    for j in range(m):
        for i in range(k-2):
            plt.plot(tempo[i], imagens[j][i], label = f'n = {nArr[i]}', color='black')  # Plotando apenas a primeira coluna de y_k
            plt.xlabel('Tempo (s)')
            if (j+1) in posicao:
                plt.ylabel('Posição (m)')
            else:
                plt.ylabel('Velocidade (m/s)')
                
            plt.title(f'Convergência do Método de Runge-Kutta de 4ª ordem')
            plt.savefig(f'imagens/convergencia/convergencia{j+1}.png')
        plt.clf()
    
    deltas = np.array(deltas)
    
    with open('inputs-outputs/tables.txt', 'w') as file:
        # Redirect the standard output to the file
        sys.stdout = file
        for j in range(m):
            print("tabela ", j+1)
            print("\n")
            print(r"\hline\hline\ \\")
            print(r"n & Passo (Delta t) & $\eta(t,h)$ & $log_{2}(\lvert \frac{\eta(t,2h)-\eta(t,h)}{\eta(t,h)-\eta(t,h/2))}\lvert$) & e(t, h/2) \\\\")
            print(r"\hline\hline \\")
            
            for i in range(k-3):    
                if i >= 2:
                    numerator = imagens[j][i+1][-1] - imagens[j][i][-1]
                    denominator = imagens[j][i][-1] - imagens[j][i-1][-1]
                    if denominator == 0 or numerator == 0:
                        print(fr"{nArr[i]} & {deltas[i]:.6f} & {imagens[j][i][-1]:.6f} \\")
                    else:
                        ordem = abs(math.log(abs(numerator/denominator), 2))
                        erroGlobal = abs(denominator / ((2**ordem) - 1))
                        print(fr"{nArr[i]} & {deltas[i]:.6f} & {imagens[j][i][-1]:.6f} & {ordem:.6f} & {erroGlobal:.6f} \\")
                else:
                    print(fr"{nArr[i]} & {deltas[i]:.6f} & {imagens[j][i][-1]} \\")
            print(r"\hline\hline")
            print("\n")
            # Reset the standard output to the console
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
