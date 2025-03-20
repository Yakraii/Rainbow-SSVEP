import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def sine_wave_modulation(frames=30):
    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    img, = ax.plot(x, np.sin(x))

    def update(frame):
        img.set_ydata(np.sin(x + 2 * np.pi * frame / frames))
        return img,

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=100)
    plt.title("Sine-Wave Modulation")
    plt.show()


def square_wave_flicker(frames=30):
    fig, ax = plt.subplots()
    rect = plt.Rectangle((0.2, 0.2), 0.6, 0.6, color='black')
    ax.add_patch(rect)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    def update(frame):
        rect.set_color('black' if frame % 2 == 0 else 'white')
        return rect,

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=100)
    plt.title("Square-Wave Flicker")
    plt.show()


def checkerboard_reversal(size=8, frames=30):
    board = np.indices((size, size)).sum(axis=0) % 2
    fig, ax = plt.subplots()
    img = ax.imshow(board, cmap='gray')

    def update(frame):
        img.set_array(1 - board if frame % 2 == 0 else board)
        return img,

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=100)
    plt.title("Checkerboard Reversal")
    plt.show()


def concentric_ring_motion(frames=30, num_rings=6):
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    def update(frame):
        ax.clear()
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        max_radius = 1.0
        phase = (frame / frames) * 2 * np.pi  # Phase for smooth expansion and contraction

        for i in range(num_rings):
            # Calculate the radius for each ring based on the phase
            radius = max_radius * (0.5 + 0.5 * np.sin(phase + i * np.pi / num_rings))
            circle = plt.Circle((0, 0), radius, color='black' if i % 2 == 0 else 'gray', fill=True)
            ax.add_patch(circle)

        return ax,

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=100, blit=True)
    plt.title("Concentric Ring Expansion-Contraction")
    plt.show()



def sine_grating(frames=30):
    x = np.linspace(-np.pi, np.pi, 100)
    y = np.linspace(-np.pi, np.pi, 100)
    X, Y = np.meshgrid(x, y)
    fig, ax = plt.subplots()
    img = ax.imshow(np.sin(X), cmap='gray', vmin=-1, vmax=1)

    def update(frame):
        img.set_array(np.sin(X + 2 * np.pi * frame / frames))
        return img,

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=100)
    plt.title("Sine Grating")
    plt.show()


# Call the functions to generate the visual stimuli
square_wave_flicker()
checkerboard_reversal()
concentric_ring_motion()
sine_grating()