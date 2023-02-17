import matplotlib.pyplot as plt
import numpy as np

width = 0.5

fig = plt.figure(figsize=(12, 6))

labels = ('OW1', 'New Players', 'OW2', 'OW2 Settled')
y_pos = np.arange(3)

plt.subplot(2, 1, 2)
# Bronze
plt.barh(labels[0], 5, color='brown', label='Bronze (0-5%)', height=width)  # OW2
# Silver
plt.barh(labels[0], 15, color='silver', label='Silver (5-20%)', left=5, height=width)  # OW1
# Gold
plt.barh(labels[0], 30, color='gold', label='Gold (20-50%)', left=20, height=width)  # OW1
# Plat
plt.barh(labels[0], 30, color='teal', label='Plat (50-80%)', left=50, height=width)  # OW1
# Diamond
plt.barh(labels[0], 12, color='purple', label='Diamond (80-92%)', left=80, height=width)  # OW1
# Masters
plt.barh(labels[0], 5.5, color='red', label='Masters (92-97.5%)', left=92, height=width)  # OW1
# GM
plt.barh(labels[0], 2.5, color='green', label='GM (97.5-100%)', left=97.5, height=width)  # OW1

# New Players
plt.barh(labels[1], 30, color='brown', label='Bronze', height=width, left=0)  # New Players
plt.barh(labels[1], 40, color='silver', label='Silver', height=width, left=30)  # New Players
plt.barh(labels[1], 30, color='gold', label='Gold', height=width, left=70)  # New Players

# OW2
# Bronze
plt.barh(labels[2], 35, color='brown', label='Bronze', height=width)
# Silver
plt.barh(labels[2], 55, color='silver', label='Silver', left=35, height=width)
# Gold
plt.barh(labels[2], 60, color='gold', label='Gold', left=90, height=width)
# Plat
plt.barh(labels[2], 30, color='teal', label='Plat', left=150, height=width)
# Diamond
plt.barh(labels[2], 12, color='purple', label='Diamond', left=180, height=width)
# Masters
plt.barh(labels[2], 5.5, color='red', label='Masters', left=192, height=width)
# GM
plt.barh(labels[2], 2.5, color='green', label='GM', left=197.5, height=width)

plt.xlabel('Players')
plt.title('Players Per Rank Based On Underlying Skill At Start of OW2')
# plt.savefig('bar_plot_new_players.png')

# fig = plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)

# OW2
# Bronze
plt.barh(labels[2], 35, color='brown', label='Bronze', height=width)
# Silver
plt.barh(labels[2], 55, color='silver', label='Silver', left=35, height=width)
# Gold
plt.barh(labels[2], 60, color='gold', label='Gold', left=90, height=width)
# Plat
plt.barh(labels[2], 30, color='teal', label='Plat', left=150, height=width)
# Diamond
plt.barh(labels[2], 12, color='purple', label='Diamond', left=180, height=width)
# Masters
plt.barh(labels[2], 5.5, color='red', label='Masters', left=192, height=width)
# GM
plt.barh(labels[2], 2.5, color='green', label='GM', left=197.5, height=width)

# OW2 Settled
# Bronze
plt.barh(labels[3], 10, color='brown', height=width)  # OW2
# Silver
plt.barh(labels[3], 30, color='silver', left=10, height=width)  # OW1
# Gold
plt.barh(labels[3], 60, color='gold', left=40, height=width)  # OW1
# Plat
plt.barh(labels[3], 60, color='teal', left=100, height=width)  # OW1
# Diamond
plt.barh(labels[3], 24, color='purple', left=160, height=width)  # OW1
# Masters
plt.barh(labels[3], 11, color='red', left=184, height=width)  # OW1
# GM
plt.barh(labels[3], 5, color='green', left=195, height=width)  # OW1

plt.vlines(10, -1, 2, colors='k', label='Silver (5-20%)')
plt.vlines(40, -1, 2, colors='k', label='Gold (20-50%)')
plt.vlines(100, -1, 2, colors='k', label='Plat (50-80%)')
plt.vlines(160, -1, 2, colors='k', label='Diamond (80-92%)')
plt.vlines(184, -1, 2, colors='k', label='Masters (92-97.5%)')
plt.vlines(195, -1, 2, colors='k', label='GM (97.5-100%)')

plt.text(25, -1, 'Silver (5-20%)', color='k', wrap=True, horizontalalignment='center')
plt.text(70, -1, 'Gold (20-50%)', color='k', wrap=True, horizontalalignment='center')
plt.text(130, -1, 'Plat (50-80%)', color='k', wrap=True, horizontalalignment='center')
plt.text(172, -1, 'Diamond\n(80-92%)', color='k', wrap=True, horizontalalignment='center')
plt.text(189.5, -1, 'Masters\n(92-97.5%)', color='k', wrap=True, horizontalalignment='center')
plt.text(205, -1, 'GM\n(97.5+%)', color='k', wrap=True, horizontalalignment='center')

plt.ylim((-.5, 1.5))
fig.tight_layout(pad=3)

plt.title('Players Per Rank - Settled')
plt.savefig('ranked_players.png')
