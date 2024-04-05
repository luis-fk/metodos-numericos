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
    """Função f que calcula o vetor f."""
    
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

def rungeKutta(t0, dt, T):
    t_n = [t0]
    n = int(T/dt)
    y_k = np.zeros((n+1, m))  # Matriz para armazenar y_k em cada passo
    derivadas = np.zeros((n+1, m))
    y_k[0] = [           0, 0, 0, 0,      0, 5000, 
                1.47095e11, 0, 0, 0,  30290,    0, 
               -1.47095e11, 0, 0, 0, -30290,    0] 

    i = 0
    with open('inputs-outputs/derivadas.txt', 'w') as f:
        while(t_n[-1] < T):
            derivadas = phi(t_n[i], y_k[i], dt)
            
            if t_n[-1] == 0 or (t_n[-1] + dt) == T:
                for j in range(18):
                    f.write(str(derivadas[j]) + ' ')
                f.write('\n')
                
            y_k[i+1] = y_k[i] + dt * derivadas
            t_n.append(t_n[i] + dt)
            i+=1
            
    return dt, t_n, y_k

def main():
    tempoFinal = 1000000000
    dt = 10000
    
    metodo = rungeKutta(0, dt, tempoFinal)  # dt, t_n, y_k

    with open('inputs-outputs/dados.txt', 'w') as f:
        for i in range(0, len(metodo[1])):
            if i % 4 == 0:
                f.write(str(metodo[1][i]) + ' ' + str(metodo[2][i][0])  + ' ' + str(metodo[2][i][1])  + ' ' + str(metodo[2][i][2])  + ' ' +
                                                  str(metodo[2][i][3])  + ' ' + str(metodo[2][i][4])  + ' ' + str(metodo[2][i][5])  + ' ' +
                                                  str(metodo[2][i][6])  + ' ' + str(metodo[2][i][7])  + ' ' + str(metodo[2][i][8])  + ' ' +
                                                  str(metodo[2][i][9])  + ' ' + str(metodo[2][i][10]) + ' ' + str(metodo[2][i][11]) + ' ' +
                                                  str(metodo[2][i][12]) + ' ' + str(metodo[2][i][13]) + ' ' + str(metodo[2][i][14]) + ' ' +
                                                  str(metodo[2][i][15]) + ' ' + str(metodo[2][i][16]) + ' ' + str(metodo[2][i][16]) + '\n')
            

if __name__ == "__main__":
    main()
