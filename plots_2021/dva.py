import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

from constants import Teams

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

hero = pd.read_csv('./player_data/hero_data.csv')
dva = hero[hero['hero_name'] == 'D.Va']

interesting_stats = [
    'Ultimates Negated',
    'Damage Blocked',
    'Time Played'
]

dva = dva[dva['stat_name'].isin(interesting_stats)]
dva_sums = dva[['team_name', 'player_name', 'stat_name', 'stat_amount']].groupby(
    by=['team_name', 'player_name', 'stat_name']).sum().reset_index()
dva_sums = dva_sums.pivot(index=['team_name', 'player_name'], columns='stat_name', values='stat_amount').fillna(
    0.0).reset_index()

def per_10(frame, stat):
    frame['{} per 10'.format(stat)] = 10 * frame[stat] / (frame['Time Played'] / 60)
    return frame

dva_sums = per_10(dva_sums, 'Ultimates Negated')
dva_sums = per_10(dva_sums, 'Damage Blocked')

dva_sums = dva_sums[dva_sums['Time Played'] > 3600]

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

    for ind in frame.index:
        row = frame.loc[ind, :]
        label = row['player_name']
        x = row[x_label]
        y = row[y_label]
        team = row['team_name']
        color = Teams.TeamColors[team]
        txt = plt.text(x * 1.008, y * 1.008, label, color=color, weight='bold', alpha=.75)
        txt.set_path_effects([path_effects.withStroke(linewidth=1, foreground='k')])

    return fig

plot_stats(dva_sums, 'Damage Blocked per 10', 'Ultimates Negated per 10', 'Time Played', 1/100)

plt.xlabel('Damage Blocked per 10')
plt.ylabel('Ultimates Negated per 10')
plt.title('D.Va:\nUsing DM to Eat Ultimates vs Eat Damage')
plt.text(12000, 0.01, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)
plt.ylim(0, 0.5)
plt.show()