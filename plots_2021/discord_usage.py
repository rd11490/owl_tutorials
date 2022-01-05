import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as path_effects

from constants import Teams

# Settings ot make data frame printing look better
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

# read in the season 4 player stats
season4 = pd.read_csv('./player_data/hero_data.csv')
#
# print(season4['stat_name'].unique())
# print(season4.columns)
# print(season4['hero_name'].unique())

hero_type = {
    'Echo': 'DPS',
    'Mei': 'DPS',
    'Reaper': 'DPS',
    'Sombra': 'DPS',
    'Symmetra': 'DPS',
    'Reinhardt': 'Tank',
    'Winston': 'Tank',
    'Wrecking Ball': 'Tank',
    'Ana': 'Support',
    'Baptiste': 'Support',
    'Moira': 'Support',
    'D.Va': 'Tank',
    'Brigitte': 'Support',
    'Lúcio': 'Support',
    'Doomfist': 'DPS',
    'Tracer': 'DPS',
    'Zenyatta': 'Support',
    'Ashe': 'DPS',
    'McCree': 'DPS',
    'Sigma': 'Tank',
    'Hanzo': 'DPS',
    'Zarya': 'Tank',
    'Pharah': 'DPS',
    'Widowmaker': 'DPS',
    'Orisa': 'Tank',
    'Genji': 'DPS',
    'Soldier: 76': 'DPS',
    'Junkrat': 'DPS',
    'Roadhog': 'Tank',
    'Bastion': 'DPS',
    'Mercy': 'Support',
    'Torbjörn': 'DPS'
}

hero_type_frame = pd.DataFrame(hero_type.items())
hero_type_frame.columns = ['hero_name', 'Role']

interesting_stats = ['Time Discorded', 'Time Hacked', 'Time Played', 'Time Alive']

season4 = season4[season4['stat_name'].isin(interesting_stats)]
season4_sums = season4[['team_name', 'esports_match_id', 'hero_name', 'stat_name', 'stat_amount']].groupby(
    by=['team_name', 'esports_match_id', 'hero_name', 'stat_name']).sum().reset_index()

season4_sums = season4_sums.pivot(index=['team_name', 'esports_match_id', 'hero_name'], columns='stat_name',
                                  values='stat_amount').fillna(
    0.0).reset_index()

teams = season4[['esports_match_id', 'team_name']].drop_duplicates()
teams = teams.merge(teams, on='esports_match_id', suffixes=('', '_opponent'))
teams = teams[teams['team_name'] != teams['team_name_opponent']]

season4_sums = season4_sums.merge(teams, on=['esports_match_id', 'team_name'])


discord_dist = season4_sums[['team_name_opponent', 'hero_name', 'Time Discorded']].groupby(
    by=['team_name_opponent', 'hero_name']).sum().reset_index()

discord_dist = discord_dist.merge(hero_type_frame, on='hero_name')
discord_dist['Squishy'] = (discord_dist['Role'] == 'Support') | (discord_dist['Role'] == 'DPS')


def additional_aggs(group, name):
    group[name] = 100 * group['Time Discorded'] / group['Time Discorded'].sum()
    return group


discord_dist_hero = discord_dist.groupby(by=['team_name_opponent']).apply(additional_aggs,
                                                                          name='Percent Discorded').reset_index()

discord_dist_squishy = discord_dist[['team_name_opponent', 'Squishy', 'Time Discorded']].groupby(
    by=['team_name_opponent', 'Squishy']).sum().reset_index()
discord_dist_squishy = discord_dist_squishy.groupby(by=['team_name_opponent']).apply(additional_aggs,
                                                                                     name='Squishy Percent Discorded').reset_index()

discord_dist_squishy['Squishy'] = np.where(discord_dist_squishy['Squishy'], 'Squishy', 'Tank')

discord_dist_role = discord_dist[['team_name_opponent', 'Role', 'Time Discorded']].groupby(
    by=['team_name_opponent', 'Role']).sum().reset_index()
discord_dist_role = discord_dist_role.groupby(by=['team_name_opponent']).apply(additional_aggs,
                                                                               name='Role Percent Discorded').reset_index()

# Plot Discord Targets Per Role By Team
width = 0.5
plt.figure(figsize=(10, 8))
plt.title('Discord Targets')
tanks = discord_dist_role[discord_dist_role['Role'] == 'Tank']
dps = discord_dist_role[discord_dist_role['Role'] == 'DPS']
support = discord_dist_role[discord_dist_role['Role'] == 'Support']

labels = tanks['team_name_opponent'].to_numpy()

tank_percent = tanks['Role Percent Discorded'].to_numpy()
dps_percent = dps['Role Percent Discorded'].to_numpy()
support_percent = support['Role Percent Discorded'].to_numpy()

dps_bottom = tank_percent + support_percent

plt.bar(labels, tank_percent, width=width, label='Tanks')
plt.bar(labels, support_percent, width=width, label='Supports', bottom=tank_percent)
plt.bar(labels, dps_percent, width=width, label='DPS', bottom=dps_bottom)
plt.xticks(rotation=45, ha="right")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.01), ncol=3)
plt.ylabel('Percent of Time Discord is on each Role')
plt.tight_layout()
plt.savefig('./plots/team/role_discord_usage.png')

# Plot each player for kills per stick
plt.figure(figsize=(10, 8))
plt.title('Discord Targets')


# Helper function to return 0 if a value is not present for one of the desired stats (i.e. the player got 0 pulse bomb kills)
def get_first_or_zero(value):
    if len(value) > 0:
        return value[0]
    else:
        return 0.0


def flatten_squishy_data(group):
    squishy_discord = group[group['Squishy'] == 'Squishy']['Squishy Percent Discorded'].values
    tank_discord = group[group['Squishy'] == 'Tank']['Squishy Percent Discorded'].values
    total_discord_time = group['Time Discorded'].sum()

    return pd.Series({
        'Squishy Percent Discorded': get_first_or_zero(squishy_discord),
        'Tank Percent Discorded': get_first_or_zero(tank_discord),
        'Total Time Discorded': total_discord_time
    })


squishy_flat = discord_dist_squishy[
    ['team_name_opponent', 'Squishy', 'Time Discorded', 'Squishy Percent Discorded']].groupby(
    by='team_name_opponent') \
    .apply(flatten_squishy_data) \
    .reset_index()

for ind in squishy_flat.index:
    row = squishy_flat.loc[ind, :]
    label = row['team_name_opponent']
    squishy_discord = row['Squishy Percent Discorded']
    tank_discord = row['Tank Percent Discorded']
    used = row['Total Time Discorded']
    team = row['team_name_opponent']
    color = Teams.TeamColors[team]
    plt.scatter(squishy_discord, tank_discord, label=label, s=used / 10, color=color)

# Label each player
for ind in squishy_flat.index:
    row = squishy_flat.loc[ind, :]
    label = row['team_name_opponent']
    squishy_discord = row['Squishy Percent Discorded']
    tank_discord = row['Tank Percent Discorded']
    used = row['Total Time Discorded']
    team = row['team_name_opponent']
    color = Teams.TeamColors[team]
    plt.text(squishy_discord + 0.4, tank_discord + 0.4, label, color=color, weight='bold')

plt.ylabel('Percent of Time Discord is on Tanks')
plt.xlabel('Percent of Time Discord is on Non-Tanks')
plt.text(52, 36, '*Dot size based on total time the team applied Discord Orb', weight='bold', size='x-small')
plt.xlim(35, 65)
plt.ylim(35, 65)



plt.tight_layout()
plt.savefig('./plots/team/squshiy_discord_usage.png')

# Plot Discord Targets Per Hero By Team
teams = ['Los Angeles Gladiators','Philadelphia Fusion', 'Chengdu Hunters', 'Shanghai Dragons']
fig = plt.figure(figsize=(10, 8))
plt.title('Discord Targets for Teams that played Zen the most')
for ind, team in enumerate(teams):
    width = 0.2
    team_discord = discord_dist_hero[discord_dist_hero['team_name_opponent'] == team]
    labels = team_discord['hero_name'].to_numpy()
    x = np.arange(len(labels))  # the label locations

    hero_percent = team_discord['Percent Discorded'].to_numpy()
    color = Teams.TeamColors[team]
    adj = 0
    if ind == 0:
        adj = -2 * width
    if ind == 1:
        adj = -width
    elif ind == 2:
        adj = 0
    elif ind == 3:
        adj = width
    plt.bar(x + adj, hero_percent, width=width, label=team, color=color)

plt.xticks(rotation=45, ha="right", labels=labels, ticks=x)
plt.tight_layout()
plt.legend()
plt.savefig('./plots/team/top_discord_usage.png')
plt.close(fig)

tanks = [item for item in hero_type if hero_type[item] == 'Tank']

season4_player_sums = season4[
    ['team_name', 'esports_match_id', 'hero_name', 'player_name', 'stat_name', 'stat_amount']].groupby(
    by=['team_name', 'esports_match_id', 'hero_name', 'stat_name', 'player_name']).sum().reset_index()



season4_player_sums = season4_player_sums.pivot(index=['team_name', 'esports_match_id', 'hero_name', 'player_name'],
                                columns='stat_name',
                                values='stat_amount').fillna(0.0).reset_index()

def calculate_total_stat_times(group):
    group['Total Discord Time'] = group['Time Discorded'].sum()
    group['Total Hacked Time'] = group['Time Hacked'].sum()
    return group



season4_player_sums = season4_player_sums.groupby(by=['team_name', 'esports_match_id']).apply(calculate_total_stat_times).reset_index()


tanks_frame = season4_player_sums[season4_player_sums['hero_name'].isin(tanks)]


tanks_disc_frame = tanks_frame[(tanks_frame['Time Discorded'] > 0)]
tanks_hack_frame = tanks_frame[(tanks_frame['Time Hacked'] > 0)]

total_disc_time = tanks_disc_frame[['team_name', 'Total Discord Time']].drop_duplicates().groupby(by='team_name').sum().reset_index()
total_hacked_time = tanks_disc_frame[['team_name', 'Total Hacked Time']].drop_duplicates().groupby(by='team_name').sum().reset_index()


tanks_disc_frame = tanks_disc_frame[['team_name', 'player_name', 'Time Discorded', 'Time Alive']].groupby(
    by=['player_name', 'team_name']).sum().reset_index()

tanks_disc_frame = tanks_disc_frame.merge(total_disc_time, on='team_name')

tanks_hack_frame = tanks_hack_frame[['team_name', 'player_name', 'Time Hacked', 'Time Alive']].groupby(
    by=['player_name', 'team_name']).sum().reset_index()

tanks_hack_frame = tanks_hack_frame.merge(total_hacked_time, on='team_name')

tanks_frame = tanks_disc_frame.merge(tanks_hack_frame, on=['team_name', 'player_name'],
                                     suffixes=(' vs Zen', ' vs Sombra'))

tanks_no_fun = tanks_frame[
    ['team_name', 'player_name', 'Time Discorded', 'Time Hacked', 'Time Alive vs Zen', 'Time Alive vs Sombra', 'Total Discord Time', 'Total Hacked Time']].groupby(
    by=['player_name', 'team_name']).sum().reset_index()

tanks_no_fun['Percent of Time Alive Discorded'] = 100 * tanks_no_fun['Time Discorded'] / tanks_no_fun['Time Alive vs Zen']
tanks_no_fun['Percent of Time Alive Hacked'] = 100 * tanks_no_fun['Time Hacked'] / tanks_no_fun['Time Alive vs Sombra']

tanks_no_fun['Percent of Teams Discords'] = 100 * tanks_no_fun['Time Discorded'] / tanks_no_fun['Total Discord Time']
tanks_no_fun['Percent of Teams Hacked'] = 100 * tanks_no_fun['Time Hacked'] / tanks_no_fun['Total Hacked Time']

tanks_no_fun['Time Alive'] = tanks_no_fun['Time Alive vs Sombra'] + tanks_no_fun['Time Alive vs Zen']

tanks_no_fun = tanks_no_fun[tanks_no_fun['Time Alive'] > 12000]

fig = plt.figure(figsize=(10, 8))
plt.title('Tanks Are Not Fun')

for ind in tanks_no_fun.index:
    row = tanks_no_fun.loc[ind, :]
    label = row['player_name']
    x = row['Percent of Time Alive Hacked']
    y = row['Percent of Time Alive Discorded']
    scale = row['Time Alive']
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.scatter(x, y, label=label, s=scale / 100, color=color)

# Label each player
for ind in tanks_no_fun.index:
    row = tanks_no_fun.loc[ind, :]
    label = row['player_name']
    x = row['Percent of Time Alive Hacked']
    y = row['Percent of Time Alive Discorded']
    scale = row['Time Alive']
    team = row['team_name']
    color = Teams.TeamColors[team]
    txt = plt.text(x * 1.02, y * 1.02, label, color=color, weight='bold', alpha=.75)
    txt.set_path_effects([path_effects.withStroke(linewidth=1, foreground='k')])

plt.ylabel('Percent of Time Discorded')
plt.xlabel('Percent of Time Hacked')
plt.text(3, 2.2, '*Dot size based on Time Alive in Games\nin which the opponent played either Zen or Sombra',
         weight='bold', size='x-small')

plt.tight_layout()
plt.savefig('./plots/team/tanks_no_fun.png')

fig = plt.figure(figsize=(10, 8))
plt.title('Tanks Are Not Fun')

for ind in tanks_no_fun.index:
    row = tanks_no_fun.loc[ind, :]
    label = row['player_name']
    x = row['Percent of Teams Hacked']
    y = row['Percent of Teams Discords']
    scale = row['Time Alive']
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.scatter(x, y, label=label, s=scale / 200, color=color)

# Label each player
for ind in tanks_no_fun.index:
    row = tanks_no_fun.loc[ind, :]
    label = row['player_name']
    x = row['Percent of Teams Hacked']
    y = row['Percent of Teams Discords']
    scale = row['Time Alive']
    team = row['team_name']
    color = Teams.TeamColors[team]
    txt = plt.text(x * 1.02, y * 1.02, label, color=color, weight='bold', alpha=.75)
    txt.set_path_effects([path_effects.withStroke(linewidth=1, foreground='k')])

plt.ylabel('Percent of Discords Received')
plt.xlabel('Percent of Hacks Received')
plt.text(50, 2.2, '*Dot size based on Time Alive in Games\nin which the opponent played either Zen or Sombra',
         weight='bold', size='x-small')

plt.tight_layout()
plt.savefig('./plots/team/tanks_no_fun2.png')



fig = plt.figure(figsize=(10, 8))
plt.title('Tanks Are Not Fun')

tanks_no_fun = tanks_no_fun[(tanks_no_fun['Percent of Teams Hacked'] >= 25) & (tanks_no_fun['Percent of Teams Hacked'] <= 50)&(tanks_no_fun['Percent of Teams Discords'] >= 20) & (tanks_no_fun['Percent of Teams Discords'] <= 30)]

for ind in tanks_no_fun.index:
    row = tanks_no_fun.loc[ind, :]
    label = row['player_name']
    x = row['Percent of Teams Hacked']
    y = row['Percent of Teams Discords']
    scale = row['Time Alive']
    team = row['team_name']
    color = Teams.TeamColors[team]
    plt.scatter(x, y, label=label, s=scale / 200, color=color)

# Label each player
for ind in tanks_no_fun.index:
    row = tanks_no_fun.loc[ind, :]
    label = row['player_name']
    x = row['Percent of Teams Hacked']
    y = row['Percent of Teams Discords']
    scale = row['Time Alive']
    team = row['team_name']
    color = Teams.TeamColors[team]
    txt = plt.text(x * 1.005, y * 1.005, label, color=color, weight='bold', alpha=.75)
    txt.set_path_effects([path_effects.withStroke(linewidth=1, foreground='k')])

plt.ylabel('Percent of Discords Received')
plt.xlabel('Percent of Hacks Received')
plt.text(35, 22.5, '*Dot size based on Time Alive in Games\nin which the opponent played either Zen or Sombra',
         weight='bold', size='x-small')
plt.tight_layout()
plt.savefig('./plots/team/tanks_no_fun2_zoom.png')


