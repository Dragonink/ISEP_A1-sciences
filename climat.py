import sys
from lib.perlin import PerlinNoiseFactory
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.animation import FuncAnimation

###* INPUT
SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 50
ITER = int(sys.argv[2]) if len(sys.argv) > 2 else 10
DT = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
print("SIMULATION DE TAILLE {0}x{0} SUR {1} FRAMES A VITESSE {2}".format(SIZE, ITER, DT))

###* DATA
##* Gas
pnf = PerlinNoiseFactory(2, octaves=4, unbias=True)
gas = np.array([[pnf(i/SIZE, j/SIZE) for j in range(SIZE)] for i in range(SIZE)])
C_MIN, C_MAX = 280, 630
min_gas, max_gas = np.min(gas), np.max(gas)
gas = np.vectorize(lambda x: (x - min_gas) / (max_gas - min_gas) * (C_MAX - C_MIN) + C_MIN)(gas)
##* Temperature
T_INI = 287.93
temp = np.full((1, SIZE, SIZE), T_INI)

###* COMPUTING
SENSI_CLIMAT = 0.1846
MYHRE = 5.35
comp_gas = np.vectorize(lambda c: c * SENSI_CLIMAT * MYHRE * DT)(np.log(np.vectorize(lambda C: C / C_MIN)(gas)))
for i in range(1, ITER + 1):
    temp = np.vstack((temp, [np.add(temp[-1], comp_gas)]))
T_MIN, T_MAX = np.min(temp), np.max(temp)

###* FIGURES
def frame(t:int):
    global temp, T_MIN, T_MAX
    if t >= len(temp):
        for i in range(len(temp), t + 1):
            temp = np.vstack((temp, [np.add(temp[-1], comp_gas)]))
        T_MIN, T_MAX = np.min(temp), np.max(temp)
    fig = plt.figure(num="Simulation [{0}] (x{1})".format(t, DT))
    #* Gas
    ax_gas = fig.add_subplot(121)
    ax_gas.set_axis_off()
    fig_gas = ax_gas.matshow(gas, cmap="GnBu", aspect="equal")
    cb_gas = fig.colorbar(ScalarMappable(norm=Normalize(vmin=C_MIN, vmax=C_MAX), cmap="GnBu"), ax=ax_gas, cmap="GnBu", orientation="horizontal")
    ax_gas.set_title("Concentration en gaz [ppm]", weight="bold")
    #* Temperature
    ax_temp = fig.add_subplot(122)
    ax_temp.set_axis_off()
    fig_temp = ax_temp.matshow(temp[t], cmap="jet", aspect="equal")
    cb_temp = fig.colorbar(ScalarMappable(norm=Normalize(vmin=T_MIN, vmax=T_MAX), cmap="jet"), ax=ax_temp, cmap="jet", orientation="horizontal")
    ax_temp.set_title("Température [K]", weight="bold")
    plt.show()
def animate(fps:int=5):
    fig = plt.figure(num="Simulation (x{0})".format(DT))
    #* Gas
    ax_gas = fig.add_subplot(121)
    ax_gas.set_axis_off()
    fig_gas = ax_gas.matshow(gas, cmap="GnBu", aspect="equal")
    cb_gas = fig.colorbar(ScalarMappable(norm=Normalize(vmin=C_MIN, vmax=C_MAX), cmap="GnBu"), ax=ax_gas, cmap="GnBu", orientation="horizontal")
    ax_gas.set_title("Concentration en gaz [ppm]", weight="bold")
    #* Temperature
    ax_temp = fig.add_subplot(122)
    ax_temp.set_axis_off()
    fig_temp = ax_temp.matshow(temp[0], cmap="jet", aspect="equal")
    cb_temp = fig.colorbar(ScalarMappable(norm=Normalize(vmin=T_MIN, vmax=T_MAX), cmap="jet"), ax=ax_temp, cmap="jet", orientation="horizontal")
    ax_temp.set_title("Température [K]", weight="bold")
    def anim(t:int):
        fig_temp = ax_temp.matshow(temp[t], cmap="jet", aspect="equal")
        fig_temp.set_clim(T_MIN, T_MAX)
        return [fig_temp]
    FuncAnimation(fig, anim, frames=len(temp), interval=(1000/fps), blit=True)
    plt.show()
def stats():
    fig = plt.figure(num="Statistiques sur la simulation (x{0})".format(DT))
    #* Gas
    ax_gas = fig.add_subplot(221)
    ax_gas.set_axis_off()
    fig_gas = ax_gas.matshow(gas, cmap="GnBu", aspect="equal")
    cb_gas = fig.colorbar(ScalarMappable(norm=Normalize(vmin=C_MIN, vmax=C_MAX), cmap="GnBu"), ax=ax_gas, cmap="GnBu")
    ax_gas.set_title("Concentration en gaz [ppm]", weight="bold")
    #* Temperature difference
    ax_gas = fig.add_subplot(222)
    ax_gas.set_axis_off()
    fig_gas = ax_gas.matshow(comp_gas, cmap="Reds", aspect="equal")
    cb_gas = fig.colorbar(ScalarMappable(norm=Normalize(vmin=np.min(comp_gas), vmax=np.max(comp_gas)), cmap="Reds"), ax=ax_gas, cmap="Reds")
    ax_gas.set_title("Différence de température [K]", weight="bold")
    #* Temperature mean
    mean_temp = [np.mean(temp[t]) for t in range(len(temp))]
    ax_temp = fig.add_subplot(212)
    fig_temp = ax_temp.plot(range(len(temp)), mean_temp, "o-r")
    ax_temp.grid(which="both")
    ax_temp.set_xlabel("Frame", weight="bold")
    ax_temp.set_ylabel("Température [K]", weight="bold")
    ax_temp.set_title("Température moyenne", weight="bold")
    plt.show()
