import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

from constants import Teams

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

sombra = pd.read_csv('./player_data/sombra.csv')

print(sombra['stat_name'].unique())

interesting_stats = ['EMP Efficiency', "Enemies EMP'd", 'Enemies Hacked', 'Final Blows', 'Time Building Ultimate',
                     'Time Elapsed per Ultimate Earned', 'Time Holding Ultimate', 'Time Played',
                     'Ultimates Earned - Fractional', 'Ultimates Used', 'Solo Kills', 'Eliminations']

sombra = sombra[sombra['stat_name'].isin(interesting_stats)]
sombra_sums = sombra[['team_name', 'player_name', 'stat_name', 'stat_amount']].groupby(
    by=['team_name', 'player_name', 'stat_name']).sum().reset_index()

sombra_sums = sombra_sums.pivot(index=['team_name', 'player_name'], columns='stat_name', values='stat_amount').fillna(
    0.0).reset_index()


def per_10(stat):
    sombra_sums['{} per 10'.format(stat)] = 10 * sombra_sums[stat] / (sombra_sums['Time Played'] / 60)


per_10('Enemies Hacked')
per_10('Enemies EMP\'d')
per_10('Solo Kills')
per_10('Final Blows')
per_10('Eliminations')


sombra_sums['Ultimates Earned per 10'] = 10 * sombra_sums['Ultimates Earned - Fractional'] / (
        sombra_sums['Time Building Ultimate'] / 60)
sombra_sums['Time to Build EMP'] = sombra_sums['Time Building Ultimate'] / sombra_sums['Ultimates Earned - Fractional']
sombra_sums['Time Holding EMP'] = sombra_sums['Time Holding Ultimate'] / sombra_sums['Ultimates Earned - Fractional']

sombra_sums['EMP Efficiency'] = sombra_sums['Enemies EMP\'d'] / sombra_sums['Ultimates Used']


sombra_sums = sombra_sums[sombra_sums['Time Played'] > 600]

print(sombra_sums)

#

def plot_stats(frame, x_label, y_label, size_label, size_scale=1.0):
    fig = plt.figure(figsize=(10, 8))

    for ind in frame.index:
        row = frame.loc[ind, :]
        label = row['player_name']
        x = row[x_label]
        y = row[y_label]
        used = row[size_label]
        team = row['team_name']
        color = Teams.TeamColors[team]
        plt.scatter(x, y, label=label, s=used * size_scale, color=color)

    for ind in sombra_sums.index:
        row = frame.loc[ind, :]
        label = row['player_name']
        x = row[x_label]
        y = row[y_label]
        team = row['team_name']
        color = Teams.TeamColors[team]
        txt = plt.text(x * 1.005, y * 1.005, label, color=color, weight='bold', alpha=.75)
        txt.set_path_effects([path_effects.withStroke(linewidth=.5, foreground='k')])

    return fig


plot_stats(sombra_sums, 'Time to Build EMP', 'EMP Efficiency', 'Ultimates Used', 3)

plt.xlabel('Time to Build EMP (sec)')
plt.ylabel('EMP Efficiency')
plt.title('EMP Efficiency vs Time to Build EMP')
plt.text(82, 2.1, '*Dot size based on number of EMPs Used', weight='bold', size='x-small', wrap=True)
plt.savefig('./plots/sombra/emp_efficiency.png')

plot_stats(sombra_sums, 'Time Holding EMP', 'EMP Efficiency', 'Ultimates Used', 3)

plt.xlabel('Time Holding EMP (sec)')
plt.ylabel('EMP Efficiency')
plt.title('EMP Efficiency vs Time Holding EMP')
plt.text(82, 2.1, '*Dot size based on number of EMPs Used', weight='bold', size='x-small', wrap=True)
plt.savefig('./plots/sombra/emp_efficiency2.png')

plot_stats(sombra_sums, 'Enemies Hacked per 10', 'Solo Kills per 10', 'Time Played', 1 / 50)

plt.xlabel('Enemies Hacked per 10')
plt.ylabel('Solo Kills per 10')
plt.title('Assassin or Hacker')
plt.text(28, .9, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)
plt.savefig('./plots/sombra/hack_vs_assassin.png')

plot_stats(sombra_sums, 'Enemies Hacked per 10', 'Final Blows per 10', 'Time Played', 1 / 50)

plt.xlabel('Enemies Hacked per 10')
plt.ylabel('Final Blows per 10')
plt.title('Assassin or Hacker')
plt.text(29, 7.3, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)
plt.savefig('./plots/sombra/hack_vs_assassin2.png')

plot_stats(sombra_sums, 'Time to Build EMP', 'Time Holding EMP', 'Ultimates Used', 3)

plt.xlabel('Time to Build EMP (sec)')
plt.ylabel('Time Holding EMP (sec)')
plt.title('Time Holding EMP vs Time to Build EMP')
plt.text(82, 10, '*Dot size based on number of EMPs Used', weight='bold', size='x-small', wrap=True)
plt.savefig('./plots/sombra/emp_hold_build.png')