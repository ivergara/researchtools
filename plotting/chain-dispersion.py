# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns
sns.set(style='ticks', palette='Set2')

plt.style.use(['seaborn-white', 'seaborn-paper'])
#matplotlib.rc("font", family="Times New Roman")

#params = {
#   'axes.labelsize': 8,
#   'text.fontsize': 8,
#   'legend.fontsize': 10,
#   'xtick.labelsize': 10,
#   'ytick.labelsize': 10,
#   'text.usetex': False,
#   'figure.figsize': [4.5, 4.5]
#   }
#matplotlib.rcParams.update(params)


fig, ax = plt.subplots()

# Generate data
x = np.arange(0,2,0.01)  # Wavevector
y1 = np.abs(np.sin(np.pi*x))*np.pi/2  # Lower boundary
y2 = np.abs(np.sin(np.pi*x/2))*np.pi  # Upper boundary

ax.set_xticks(np.arange(0,2,0.5), minor= True)
ax.set_xlabel(r"Wave vector (k/$\pi$)")
ax.set_ylabel("Energy / J")
ax.fill_between(x, y1, y2, alpha=0.8)
fig.text(0.37, 0.55, "Two-Spinon Continuum", fontsize=10)
fig.set_size_inches(4.5, 4.5)
fig.tight_layout()
ax.plot(x,y1, 'k', x,y2, 'k')
fig.savefig("chain-disp.pdf")