
import numpy as np

# Ler os dados do arquivo
data = np.loadtxt('output.txt')

# Separar os dados para cada corpo
coordenadasX = data[:, :3]
# coordenadasY = data[:, 3:6]
# coordenadasZ = data[:, 6:]

for i in range(0, 6):
    print(coordenadasX[i, 0], coordenadasX[i+1, 0], coordenadasX[i+2, 0])
    erro = np.log2(np.abs((coordenadasX[i+2, 0]-coordenadasX[i+1, 0])/(coordenadasX[i+1, 0]-coordenadasX[i, 0])))
    print(erro)