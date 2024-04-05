import numpy as np

# Calcula a solução de um sistema de equações tri-diagonais
# usando o método de Crout
def solucaoTridiagonal(A, b):
    # Aplica o método de Crout para obter as matrizes L e U
    L, U = crout(A)
    # Aplica a substituição direta para obter a solução da primeira eq. 
    y = substituicaoDireta(L, b)
    # Aplica a substituição reversa para obter a solução da eq. original
    x = substituicaoReversa(U, y)
    # Retorna o vetor solução x
    return x


# Aplica o método de Crout para obter as matrizes L e U
def crout(A):

    n = len(A) # Tamanho do sistema

    # Cria as matrizes L e U
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    # Preenche a diagonal principal das matrizes L e U com 1
    for z in range(n):
        U[z][z] = 1             

        # Calcula a coluna z da matrizes L e U
        for j in range(z,n):
            LTemp = A[j][z]
        
            # Calcula o valor de L[j,z]
            for k in range(z):
                LTemp -= L[j][k]*U[k][z]
                
            L[j][z] = LTemp
            

        # Calcula a coluna z da matriz U
        for j in range(z+1, n):
            UTemp = A[z][j]
            
            # Calcula o valor de U[z,j]
            for k in range(z): 
                UTemp -= L[z][k]*U[k][j]
                
            U[z][j] = UTemp / L[z][z]

    return (L, U)


# Aplica a substituição direta para obter a solução da primeira eq.
def substituicaoDireta(L, b):
    y = np.full_like(b, 0) # Vetor solução da primeira eq.
    
    # Aplica a substituição direta para cada eq.
    for k in range(len(b)):
        y[k] = b[k]
        
        for i in range(k):
            y[k] = y[k] - (L[k][i]*y[i])
            
        y[k] = y[k] / L[k][k]
    
    return y


# Aplica a substituição reversa para obter a solução da eq. original
def substituicaoReversa(U, y):
    x = np.full_like(y, 0) # Vetor solução original
    
    # Aplica a substituição reversa para cada eq.
    for k in range(len(x), 0, -1):
        x[k-1] = (y[k-1] - np.dot(U[k-1, k:], x[k:])) / U[k-1][k-1] 
     
    return x
