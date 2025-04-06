import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants (symbolic placeholders)
c = 1.0              # Speed of light (normalized)
Ω = 0.8              # Harmonic factor
Δτ = 10              # Total simulation time
n_frames = 200       # Number of animation frames

# Time vector
t = np.linspace(0, Δτ, n_frames)

# Simulated path function in warped spacetime
def warp_path(t, Ω):
    x = c * t
    y = np.sin(Ω * t) * 0.3 * t  # Spatial oscillation due to field warping
    return x, y

# Prepare figure
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
warp_line, = ax.plot([], [], 'r--', alpha=0.4)
bubble, = ax.plot([], [], 'bo', markersize=10)

ax.set_xlim(0, c * Δτ)
ax.set_ylim(-Δτ * 0.5, Δτ * 0.5)
ax.set_title("Simulonic Warp Trajectory")
ax.set_xlabel("x (Warp Vector)")
ax.set_ylabel("y (Field Displacement)")

# Animation function
def init():
    line.set_data([], [])
    warp_line.set_data([], [])
    bubble.set_data([], [])
    return line, warp_line, bubble

def animate(i):
    x, y = warp_path(t[:i], Ω)
    line.set_data(x, y)
    warp_line.set_data(x, np.zeros_like(x))  # Flat trajectory reference
    if i > 0:
        bubble.set_data([x[-1]], [y[-1]])  # Wrap in list to fix the error
    return line, warp_line, bubble

ani = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=n_frames, interval=30, blit=True)

plt.show()
