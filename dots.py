import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Load data from the file
data = np.loadtxt('output.txt')

# Determine the number of steps
num_steps = len(data)

# Separate data for each body
data_a = data[:, :3]
data_b = data[:, 3:6]
data_c = data[:, 6:]

# Create paths for each body
walks = [data_a, data_b, data_c]

# Create the plot
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.axis('off')

# Create lines initially without data
lines = [ax.plot(walk[:, 0], walk[:, 1], walk[:, 2])[0] for walk in walks]

# Set axis properties
ax.set_xlim3d([data.min(), data.max()])
ax.set_ylim3d([data.min(), data.max()])
ax.set_zlim3d([data.min(), data.max()])

# Create scatter plots for current positions
sc_a = ax.scatter(data_a[:, 0], data_a[:, 1], data_a[:, 2], s=30, label='A')
sc_b = ax.scatter(data_b[:, 0], data_b[:, 1], data_b[:, 2], s=30, label='B')
sc_c = ax.scatter(data_c[:, 0], data_c[:, 1], data_c[:, 2], s=30, label='C')

def update_lines(num, walks, lines, scatter_objects, trail_length=100, current_position_size=30):
    for line, walk in zip(lines, walks):
        start_idx = max(0, num - trail_length)
        line.set_data(walk[start_idx:num, 0:2].T)
        line.set_3d_properties(walk[start_idx:num, 2])

    scatter_objects[0]._offsets3d = (data_a[num, 0], data_a[num, 1], data_a[num, 2])
    scatter_objects[1]._offsets3d = (data_b[num, 0], data_b[num, 1], data_b[num, 2])
    scatter_objects[2]._offsets3d = (data_c[num, 0], data_c[num, 1], data_c[num, 2])

    for scatter in scatter_objects:
        scatter._sizes = [current_position_size]  # Set the size of the current position

    ax.view_init(30, 0)
    fig.canvas.draw()
    return lines + scatter_objects

skip_interval = 10

# Create the animation
ani = animation.FuncAnimation(
    fig, 
    update_lines, 
    fargs=(walks, lines, [sc_a, sc_b, sc_c]), 
    frames=range(0, num_steps, skip_interval),
    interval=0.1, 
    blit=False,
    repeat=False)

plt.show()
