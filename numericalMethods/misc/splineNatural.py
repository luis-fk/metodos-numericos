import numpy as np
import matplotlib.pyplot as plt
import crout

def spline(x, y):
    n = len(x)
    a = {k: v for k, v in enumerate(y)}
    h = {k: x[k+1] - x[k] for k in range(n - 1)}
      
    matrizA = [[1] + [0]*(n-1)]
    for i in range(1, n-1):
        linhas = [0]*n
        linhas[i-1] = h[i-1]
        linhas[i] = 2*(h[i-1] + h[i])
        linhas[i+1] = h[i]
        matrizA.append(linhas)
    matrizA.append([0]*(n-1) + [1])
      
    matrizB = [0]
    for k in range(1, n-1):
        linhas = 3*((a[k+1]-a[k])/h[k]) - 3*((a[k]-a[k-1])/h[k-1])
        matrizB.append(linhas)
    matrizB.append(0)
    
    c = dict(zip(range(n), crout.solucaoTridiagonal(matrizA, matrizB)))
    
    b = {}
    d = {}
    for k in range(n-1):
        b[k] =  (1/h[k]) * (a[k+1]-a[k]) - (h[k]/3) * (2*c[k]+c[k+1])
        d[k] = (c[k+1] - c[k])/(3*h[k])
    
    polinomios = {}
    for k in range(n-1):
        equacoes = f'{a[k]}{b[k]:+}*(x{-x[k]:+}) \
                     {c[k]:+}*(x{-x[k]:+})**2 \
                     {d[k]:+}*(x{-x[k]:+})**3'
        polinomios[k] = {'eq': equacoes, 'domain': [x[k], x[k+1]]}
    
    return polinomios


def main():
    # Ler os dados do arquivo
    data = np.loadtxt('inputs-outputs/output.txt')
    
    # Separar os dados para cada corpo
    coordenadasY = data
    coordenadasX = np.arange(len(coordenadasY))
    # coordenadasY = data[:, 3:6]
    # coordenadasZ = data[:, 6:]
    
    polinomios = spline(coordenadasX ,coordenadasY)
    plt.scatter(coordenadasX, coordenadasY, zorder=3, s=20, color='black')
    plt.xlabel('Posição X')
    plt.ylabel('Tempo')
    for key, value in polinomios.items():
        def polinomio(x):
            return eval(value['eq'])
        t = np.linspace(*value['domain'], 100)
        plt.plot(t, polinomio(t), label=f"$S_{key}(x)$")

    # plt.legend()
    exp_function = lambda x: np.exp(x)
    t = np.linspace(0, len(coordenadasY)-1, 100)
    plt.plot(t, exp_function(t), label="Exponential Function")
    plt.savefig('imagens/spline.png')

main()


