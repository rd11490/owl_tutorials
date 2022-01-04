import pandas as pd
import matplotlib.pyplot as plt

from constants import Teams

# Settings ot make data frame printing look better
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

# read in the season 4 player stats
season4 = pd.read_csv('./player_data/tracer.csv')

# Setting a minimum number of pulse bombs to filter out some low minute players
min_pulse_bombs_used = 50

# Filter for only tracer stats
tracer = season4[season4['hero_name'] == 'Tracer']

# Generate a list of player names and the team they play for
players_and_teams = tracer[['player_name', 'team_name']].groupby('player_name').head(1).reset_index()

# Filter for only the stats we care about
pulse_bomb_stats = ['Ultimates Used', 'Pulse Bomb Kills', 'Pulse Bombs Attached']
tracer = tracer[tracer['stat_name'].isin(pulse_bomb_stats)]


# Helper function to return 0 if a value is not present for one of the desired stats (i.e. the player got 0 pulse bomb kills)
def get_first_or_zero(value):
    if len(value) > 0:
        return value[0]
    else:
        return 0.0


# Helper function to pivot the data from tall to wide
def flatten_group(group):
    kills = group[group['stat_name'] == 'Pulse Bomb Kills']['stat_amount'].values
    attaches = group[group['stat_name'] == 'Pulse Bombs Attached']['stat_amount'].values
    used = group[group['stat_name'] == 'Ultimates Used']['stat_amount'].values

    return pd.Series({
        'Pulse Bomb Kills': get_first_or_zero(kills),
        'Pulse Bombs Attached': get_first_or_zero(attaches),
        'Ultimates Used': get_first_or_zero(used)
    })


# Sum up each stat for each player, then flatted the stats for each player
pb_stats = tracer[['player_name', 'stat_name', 'stat_amount']].groupby(
    by=['player_name', 'stat_name']).sum().reset_index().groupby(by=['player_name']).apply(flatten_group).reset_index()

# Calculate attach and kill rates
pb_stats['Attach Rate'] = pb_stats['Pulse Bombs Attached'] / pb_stats['Ultimates Used']
pb_stats['Kill Rate'] = pb_stats['Pulse Bomb Kills'] / pb_stats['Ultimates Used']
pb_stats['Kills Per Stick'] = pb_stats['Pulse Bomb Kills'] / pb_stats['Pulse Bombs Attached']


# join with list of players and teams to get each player's team for plotting
pb_stats = pb_stats.merge(players_and_teams, on='player_name')

pb_stats = pb_stats.sort_values(by='Ultimates Used', ascending=False)
print(pb_stats)
pb_stats = pb_stats[pb_stats['Ultimates Used'] > min_pulse_bombs_used]

# Plot each player for kills per stick
plt.figure(figsize=(10, 8))
plt.title('Pulse Bomb Kills Per Attach vs Attach Rate')
for ind in pb_stats.index:
    row = pb_stats.loc[ind, :]
    label = row['player_name']
    attach_rate = row['Attach Rate']
    kill_rate = row['Kills Per Stick']
    used = row['Ultimates Used']
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.scatter(attach_rate, kill_rate, label=label, s=used * 2, color=color)

# Label each player
for ind in pb_stats.index:
    row = pb_stats.loc[ind, :]
    label = row['player_name']
    attach_rate = row['Attach Rate']
    kill_rate = row['Kills Per Stick']
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.text(attach_rate + 0.005, kill_rate + 0.005, label, color=color, weight='bold')

plt.text(0.53, 0.51, '*Dot size based on \nnumber of pulse bombs used', weight='bold', size='x-small')
#
plt.xlim((0.3, 0.6))
plt.ylim((0.5, 1.5))

plt.xlabel('Pulse Bomb Attach Rate')
plt.ylabel('Pulse Bomb Kills Per Attach')

plt.savefig('./plots/tracer/pulse_bombs_kills_per_stick.png')

# Plot each player Again with kill Rate
plt.figure(figsize=(10, 8))
plt.title('Pulse Bomb Kill Rate vs Attach Rate')
for ind in pb_stats.index:
    row = pb_stats.loc[ind, :]
    label = row['player_name']
    attach_rate = row['Attach Rate']
    kill_rate = row['Kill Rate']
    used = row['Ultimates Used']
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.scatter(attach_rate, kill_rate, label=label, s=used * 2, color=color)

# Label each player
for ind in pb_stats.index:
    row = pb_stats.loc[ind, :]
    label = row['player_name']
    attach_rate = row['Attach Rate']
    kill_rate = row['Kill Rate']
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.text(attach_rate + 0.005, kill_rate + 0.005, label, color=color, weight='bold')

plt.text(0.53, 0.31, '*Dot size based on \nnumber of pulse bombs used', weight='bold', size='x-small')
#
plt.xlim((0.3, 0.6))
plt.ylim((0.3, 0.6))

plt.xlabel('Pulse Bomb Attach Rate')
plt.ylabel('Pulse Bomb Kill Rate')

plt.savefig('./plots/tracer/pulse_bombs_kill_rate.png')