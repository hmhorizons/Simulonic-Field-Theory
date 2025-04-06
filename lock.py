import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the warp trajectory function
def warp_path(t, Ω=1.2):
    x = np.cos(Ω * t) * t
    y = np.sin(Ω * t) * t
    return x, y

# Time array
t = np.linspace(0.1, 20, 400)  # Ensure t does not start at 0 for gradient calculations

# Initialize plot
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-25, 25)
ax.set_ylim(-25, 25)
ax.set_title("Simulonic Warp Bubble Transformation")
ax.set_xlabel("X-axis (Causal Space)")
ax.set_ylabel("Y-axis (Temporal Displacement)")

# Plot objects
line, = ax.plot([], [], lw=2, label='Warp Trajectory')
warp_line, = ax.plot([], [], 'k--', lw=0.5, alpha=0.5)
bubble, = ax.plot([], [], 'ro', label='Warp Bubble')

# Initialization function
def init():
    line.set_data([], [])
    warp_line.set_data([], [])
    bubble.set_data([], [])
    return line, warp_line, bubble

# Animation function for warp bubble transformation
def animate(i):
    # Ensure we get at least the first point for x and y
    if i > 0:
        x, y = warp_path(t[:i])
    else:
        x, y = warp_path(t[:1])  # At least one point for the first frame
    
    # Update the position of the bubble
    bubble.set_data([x[-1]], [y[-1]])  # Set the bubble to the latest position
    
    # Adjust the bubble size as a function of time (simulate bubble expansion/contraction)
    bubble_size = np.sin(t[i] / 2) + 1  # Bubble size oscillates between 1 and 2
    
    # Update the bubble size (scaling the markers)
    bubble.set_markersize(bubble_size * 6)  # Increase bubble size dynamically
    
    # Update the trajectory and baseline reference
    line.set_data(x, y)
    warp_line.set_data(x, np.zeros_like(x))  # Flat baseline reference
    
    return line, warp_line, bubble

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=len(t), init_func=init,
                              interval=30, blit=True)

plt.legend()
plt.tight_layout()
plt.show()
