import numpy as np
import matplotlib.pyplot as plt
import crout

def spline(x, y, derivada, var):
    n = len(x)
    a = {k: v for k, v in enumerate(y)}
    h = {k: x[k+1] - x[k] for k in range(n - 1)}
      
    matrizA = [[2*h[0]] + [h[0]] + [0]*(n-2)]
    for i in range(1, n-1):
        linhas = [0]*n
        linhas[i-1] = h[i-1]
        linhas[i] = 2*(h[i-1] + h[i])
        linhas[i+1] = h[i]
        matrizA.append(linhas)
    matrizA.append([0]*(n-2) + [h[n-2]] + [2*h[n-2]])
    
    ##########################
    # mudar derivadas abaixo #
    ##########################
    matrizB = [(3/h[0])*(a[1]-a[0]) - 3*derivada[0][var]] 
    for k in range(1, n-1):
        linhas = 3*((a[k+1]-a[k])/h[k]) - 3*((a[k]-a[k-1])/h[k-1])
        matrizB.append(linhas)
    matrizB.append(3*derivada[1][var] - (3/h[n-2])*(a[n-1]-a[n-2]))

    
    c = dict(zip(range(n), crout.solucaoTridiagonal(matrizA, matrizB)))
    #c1 = dict(zip(range(n), np.linalg.solve(matrizA, matrizB)))
    
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
    data = np.loadtxt('inputs-outputs/dados.txt')
    derivadas = np.loadtxt('inputs-outputs/derivadas.txt')
    tempo = data[:, 0]
    eixo = ['x', 'y', 'z']
    variavel = ['Posição', 'Velocidade']
    corpo = 0
    i = 1
    while i < 18:
        corpo += 1
        for k in range(2):
            for j in range(3):
                coordenada = data[:, i]
                
                polinomios = spline(tempo, coordenada, derivadas, i-1)
                plt.scatter(tempo, coordenada, zorder=3, s=20, color='black')

                plt.xlabel(f'Tempo')
                plt.ylabel(f'{variavel[k]}')
                plt.title(f'Spline Vinculado Para a {variavel[k]} {eixo[j]} do Corpo {corpo}')
                for key, value in polinomios.items():
                    def polinomio(x):
                        return eval(value['eq'])
                    t = np.linspace(*value['domain'], 100)
                    plt.plot(t, polinomio(t), label=f"$S_{key}(x)$", color='black')

                # plt.legend()
                plt.savefig(f'imagens/splines/splineVinculado{i}.png')
                plt.clf()
                if i < 18:
                    i += 1
                else:
                    break

main()