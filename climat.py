import sys
import random
from lib.perlin import PerlinNoiseFactory
import numpy as np
from matplotlib import pyplot as plt

###* INPUT
size = int(sys.argv[1]) if len(sys.argv) > 1 else 50

###* DATA
## Gaz
pnf = PerlinNoiseFactory(2, octaves=4, unbias=True)
gaz = np.array([[pnf(i/size, j/size) for j in range(size)] for i in range(size)])
min_gaz, max_gaz = np.min(gaz), np.max(gaz)
gaz = np.vectorize(lambda x: (x - min_gaz) / (max_gaz - min_gaz))(gaz)
## Temperature
temp = np.zeros((1, size, size))

###* FIGURE
## Gaz
fig_gaz = plt.matshow(gaz, fignum="Gaz", cmap="GnBu", aspect="equal")
cb_gaz = plt.colorbar(fig_gaz, cmap="GnBu")
## Display
plt.axis("off")
plt.show()
