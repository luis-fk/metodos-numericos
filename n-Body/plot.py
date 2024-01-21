import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Ler os dados do arquivo
data = np.loadtxt('output.txt')

# Determinar o número de passos
num_steps = len(data)

# Separar os dados para cada corpo
data_a = data[:, :3]
data_b = data[:, 3:6]
data_c = data[:, 6:]

# Criar as caminhadas para cada corpo
walks = [data_a, data_b, data_c]

# Criar o gráfico
fig = plt.figure(dpi=300)
ax = fig.add_subplot(projection="3d")
ax.axis('off')

# Criar linhas inicialmente sem dados
lines = [ax.plot(walk[:,0], walk[:,1], walk[:,2])[0] for walk in walks]

# Set the zoomed-in range
zoom_factor = 0.2  # Adjust the zoom factor as needed
ax.set_xlim3d([data.min() * zoom_factor, data.max() * zoom_factor])
ax.set_ylim3d([data.min() * zoom_factor, data.max() * zoom_factor])
ax.set_zlim3d([data.min() * zoom_factor, data.max() * zoom_factor])

sc_a = ax.scatter(data_a[:, 0], data_a[:, 1], data_a[:, 2], label='A')
sc_b = ax.scatter(data_b[:, 0], data_b[:, 1], data_b[:, 2], label='B')
sc_c = ax.scatter(data_c[:, 0], data_c[:, 1], data_c[:, 2], label='C')

trail_length = 50000
current_position_size_a = 10
current_position_size_b = 10
current_position_size_c = 10

ax.view_init(90, -90)

def update_lines(num, walks, lines):
    for line, walk in zip(lines, walks):
        start_idx = max(0, num - trail_length)
        line.set_data(walk[start_idx:num, 0:2].T)
        line.set_3d_properties(walk[start_idx:num, 2])
        
    sc_a._offsets3d = (data_a[num-5:num, 0], data_a[num-5:num, 1], data_a[num-5:num, 2])
    sc_a._sizes = [current_position_size_a]
    
    sc_b._offsets3d = (data_b[num-5:num, 0], data_b[num-5:num, 1], data_b[num-5:num, 2])
    sc_b._sizes = [current_position_size_b]
    
    sc_c._offsets3d = (data_c[num-5:num, 0], data_c[num-5:num, 1], data_c[num-5:num, 2])
    sc_c._sizes = [current_position_size_c]
    
    line_color = lines[0].get_color()
    sc_a._facecolors = [line_color]
    sc_a._edgecolors = [line_color]
    
    line_color = lines[1].get_color()
    sc_b._facecolors = [line_color]
    sc_b._edgecolors = [line_color]
    
    line_color = lines[2].get_color()
    sc_c._facecolors = [line_color]
    sc_c._edgecolors = [line_color]
    
    fig.canvas.draw()
    return lines

skip_interval = 4000

# Criar a animação
ani = animation.FuncAnimation(
    fig, 
    update_lines, 
    fargs=(walks, lines), 
    frames=range(0, num_steps*2, skip_interval),
    interval=0.001, 
    blit=False)

#plt.show()
ani.save('animation.gif', writer='pillow', fps=120)