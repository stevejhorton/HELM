# pip install matplotlib imageio
import numpy as np, matplotlib.pyplot as plt, imageio, os

# --------------------------------------------------
# 1.  Parameters that match your PNG
# --------------------------------------------------
x      = np.array([0, 2, 6, 10, 12])
y_base = np.array([1.00, 0.75, 0.50, 0.25, 0.00, -0.25, -0.50, -0.75, -1.00])
labels = ["HELM Vacuum Energy Cancellation",
          "Raw Strain Energy", "LatticeBackPressure",
          "Cancellation Level", "DarkEnergy (sun)"]

# --------------------------------------------------
# 2.  Build 60 frames (5 s @ 12 fps)
# --------------------------------------------------
frames_folder = "_frames"
os.makedirs(frames_folder, exist_ok=True)

for i in range(60):
    t = i / 59                       # 0 → 1
    phase = 2*np.pi*t                # full sine cycle

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=120)
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("Lattice Position")
    ax.set_ylabel("Energy / Cancellation")

    # Static horizontal guidelines
    for yy in y_base:
        ax.axhline(yy, color="grey", lw=0.3, alpha=0.4)

    # Animated wiggle for each curve
    for k, label in enumerate(labels):
        offset = k*0.15                # stagger the curves
        y = 0.8*np.sin(phase + x*0.4 + offset) * np.exp(-x/12)
        color = plt.cm.plasma(k/4)
        ax.plot(x, y, color=color, label=label, lw=2.5)

    ax.legend(fontsize=7, loc="upper right")
    ax.set_title("Dark-Energy Vacuum Cancellation", fontsize=10)

    # Save frame
    fname = f"{frames_folder}/frame_{i:03d}.png"
    plt.savefig(fname, bbox_inches="tight")
    plt.close()

# --------------------------------------------------
# 3.  Assemble GIF
# --------------------------------------------------
images = [imageio.imread(f"{frames_folder}/frame_{i:03d}.png") for i in range(60)]
imageio.mimsave("dark_energy.gif", images, fps=12)

# Optional: delete temporary PNGs
import shutil
shutil.rmtree(frames_folder)
