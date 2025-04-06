import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants (for the second animation)
c = 1.0              # Speed of light (normalized)
Ω2 = 0.8             # Harmonic factor for the second animation
Δτ = 30              # Total simulation time
n_frames = 600       # Number of animation frames

# Time vector
t = np.linspace(0, Δτ, n_frames)

# Define the first warp trajectory function (Simulonic Bubble)
def warp_path1(t, Ω=1.2):
    x = np.cos(Ω * t) * t
    y = np.sin(Ω * t) * t
    return x, y

# Define the second warp trajectory function (Warped Spacetime)
def warp_path2(t, Ω):
    x = c * t
    y = np.sin(Ω * t) * 0.3 * t  # Spatial oscillation due to field warping
    return x, y

# Prepare figure
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-25, 25)
ax.set_ylim(-25, 25)
ax.set_title("Simulonic Warp and Warped Spacetime Transformation")
ax.set_xlabel("x (Warp Vector)")
ax.set_ylabel("y (Field Displacement)")

# Plot objects
line1, = ax.plot([], [], lw=2, label='Warp Trajectory 1')
line2, = ax.plot([], [], lw=2, color='green', label='Warp Trajectory 2')
warp_line1, = ax.plot([], [], 'k--', lw=0.5, alpha=0.5)
warp_line2, = ax.plot([], [], 'r--', lw=0.5, alpha=0.5)
bubble1, = ax.plot([], [], 'ro', label='Bubble 1')
bubble2, = ax.plot([], [], 'bo', label='Bubble 2')

# Initialization function
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    warp_line1.set_data([], [])
    warp_line2.set_data([], [])
    bubble1.set_data([], [])
    bubble2.set_data([], [])
    return line1, line2, warp_line1, warp_line2, bubble1, bubble2

# Animation function for combined warp bubble transformation
def animate(i):
    # First trajectory (Simulonic Warp)
    if i > 0:
        x1, y1 = warp_path1(t[:i])
    else:
        x1, y1 = warp_path1(t[:1])  # At least one point for the first frame
    
    # Second trajectory (Warped Spacetime)
    x2, y2 = warp_path2(t[:i], Ω2)
    
    # Ensure we don't try to access an empty array
    if len(x1) > 0 and len(y1) > 0:
        bubble1.set_data([x1[-1]], [y1[-1]])  # Set the first bubble to the latest position
    if len(x2) > 0 and len(y2) > 0:
        bubble2.set_data([x2[-1]], [y2[-1]])  # Set the second bubble to the latest position

    # Adjust the bubble sizes as a function of time (simulate bubble expansion/contraction)
    bubble_size1 = np.sin(t[i] / 2) + 1  # Bubble 1 size oscillates between 1 and 2
    bubble_size2 = np.cos(t[i] / 2) + 1  # Bubble 2 size oscillates between 1 and 2
    
    # Update the bubble sizes (scaling the markers)
    bubble1.set_markersize(bubble_size1 * 6)  # Bubble 1 size
    bubble2.set_markersize(bubble_size2 * 6)  # Bubble 2 size
    
    # Update the trajectories and baseline references
    line1.set_data(x1, y1)
    line2.set_data(x2, y2)
    warp_line1.set_data(x1, np.zeros_like(x1))  # Flat baseline reference for trajectory 1
    warp_line2.set_data(x2, np.zeros_like(x2))  # Flat baseline reference for trajectory 2
    
    return line1, line2, warp_line1, warp_line2, bubble1, bubble2

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=n_frames, init_func=init,
                              interval=30, blit=True)

plt.legend()
plt.tight_layout()
plt.show()
