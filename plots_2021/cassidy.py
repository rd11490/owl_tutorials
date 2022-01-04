import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

from constants import Teams

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

cass = pd.read_csv('./player_data/cassidy.csv')

# print(cass['stat_name'].unique())

interesting_stats = [
    'Shots Fired',
    'Shots Hit',
    'Shots Missed',
    'Critical Hits',
    'Ultimates Earned - Fractional',
    'Ultimates Used',
    'Fan the Hammer Kills',
    'Critical Hit Kills',
    'Solo Kills',
    'Time Holding Ultimate',
    'Time Building Ultimate',
    'Time Played',
    'Deadeye Kills',
    'Final Blows',
    'Eliminations',
    'All Damage Done',
    'Barrier Damage Done',
    'Hero Damage Done',
    'Deaths'
]

cass = cass[cass['stat_name'].isin(interesting_stats)]
cass_sums = cass[['team_name', 'player_name', 'stat_name', 'stat_amount']].groupby(
    by=['team_name', 'player_name', 'stat_name']).sum().reset_index()

cass_sums = cass_sums.pivot(index=['team_name', 'player_name'], columns='stat_name', values='stat_amount').fillna(
    0.0).reset_index()


def per_10(stat):
    cass_sums['{} per 10'.format(stat)] = 10 * cass_sums[stat] / (cass_sums['Time Played'] / 60)


cass_sums['Critical Hit Accuracy'] = cass_sums['Critical Hits'] / cass_sums['Shots Hit']

cass_sums['Time to Build Deadeye'] = cass_sums['Time Building Ultimate'] / cass_sums['Ultimates Earned - Fractional']
cass_sums['Time Holding Deadeye'] = cass_sums['Time Holding Ultimate'] / cass_sums['Ultimates Earned - Fractional']
cass_sums['Deadeye Efficiency'] = cass_sums['Deadeye Kills'] / cass_sums['Ultimates Used']

per_10('Deaths')
per_10('Eliminations')
per_10('Final Blows')
per_10('Solo Kills')
per_10('Hero Damage Done')
per_10('All Damage Done')
per_10('Fan the Hammer Kills')



cass_sums = cass_sums[cass_sums['Time Played'] > 1200]

print(cass_sums)



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
        txt = plt.text(x * 1.005, y * 1.005, label, color=color, weight='bold', alpha=.75)
        txt.set_path_effects([path_effects.withStroke(linewidth=.5, foreground='k')])

    return fig
#
#
plot_stats(cass_sums, 'Hero Damage Done per 10', 'Eliminations per 10', 'Time Played', 1/50)

plt.xlabel('Hero Damage per 10')
plt.ylabel('Eliminations per 10')
plt.title('Cassidy:\nEliminations vs Hero Damage Done')
plt.text(9500, 8.1, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)

plt.savefig('./plots/cassidy/hero_damage_vs_elims.png')

plot_stats(cass_sums, 'All Damage Done per 10', 'Eliminations per 10', 'Time Played', 1/50)

plt.xlabel('All Damage per 10')
plt.ylabel('Eliminations per 10')
plt.title('Cassidy:\nEliminations vs All Damage Done')
plt.text(14700, 8.1, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)

plt.savefig('./plots/cassidy/all_damage_vs_elims.png')

plot_stats(cass_sums, 'Hero Damage Done per 10', 'Final Blows per 10', 'Time Played', 1/50)

plt.xlabel('Hero Damage per 10')
plt.ylabel('Final Blows per 10')
plt.title('Cassidy:\nFinal Blows vs Hero Damage Done')
plt.text(9500, 4.3, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)

plt.savefig('./plots/cassidy/hero_damage_vs_final_blows.png')

plot_stats(cass_sums, 'Hero Damage Done per 10', 'Solo Kills per 10', 'Time Played', 1/50)

plt.xlabel('Hero Damage per 10')
plt.ylabel('Solo Kills per 10')
plt.title('Cassidy:\nSolo Kills vs Hero Damage Done')
plt.text(7000, 0.01, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)
plt.ylim(0,2)
plt.savefig('./plots/cassidy/hero_damage_vs_solo_kills.png')

plot_stats(cass_sums, 'Fan the Hammer Kills per 10', 'Final Blows per 10', 'Time Played', 1/50)

plt.xlabel('Fan the Hammer Kills per 10')
plt.ylabel('Final Blows per 10')
plt.title('Cassidy:\nFinal Blows vs Fan the Hammer Kills')
plt.text(4, 4.4, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)

plt.savefig('./plots/cassidy/fb_fan_kills.png')

plot_stats(cass_sums, 'Final Blows per 10', 'Critical Hit Accuracy', 'Time Played', 1/50)

plt.xlabel('Final Blows per 10')
plt.ylabel('Critical Hit Accuracy')
plt.title('Cassidy:\nCritical Hit Accuracy vs Final Blows per 10')
plt.text(5, 0.142, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)

plt.savefig('./plots/cassidy/crit_vs_fb.png')

plot_stats(cass_sums, 'Deaths per 10', 'Eliminations per 10', 'Time Played', 1/50)

plt.xlabel('Deaths per 10')
plt.ylabel('Eliminations per 10')
plt.title('Cassidy:\nEliminations vs Deaths')
plt.text(5, 8.3, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)

plt.savefig('./plots/cassidy/elims_vs_deaths.png')

plot_stats(cass_sums, 'Time Holding Deadeye','Time to Build Deadeye',  'Ultimates Used', 3)

plt.ylabel('Time to Build Deadeye (sec)')
plt.xlabel('Time Holding Deadeye (sec)')
plt.title('Time to Build Deadeye vs Time Holding Deadeye')
plt.text(97, 12, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)
plt.savefig('./plots/cassidy/deadeye_hold_build.png')

plot_stats(cass_sums, 'Time Holding Deadeye', 'Deadeye Efficiency', 'Ultimates Used', 3)

plt.xlabel('Time Holding Deadeye (sec)')
plt.ylabel('Deadeye Efficiency')
plt.title('Deadeye Efficiency vs Time Holding Deadeye')
plt.text(47, 0.09, '*Dot size based on Time Played', weight='bold', size='x-small', wrap=True)
plt.savefig('./plots/cassidy/deadeye_eff_hold.png')