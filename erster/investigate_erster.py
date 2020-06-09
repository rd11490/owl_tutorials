import warnings
warnings.simplefilter(action='ignore')

import pandas as pd
import os
import datetime


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

csvs = os.listdir('data') # Get all files in the data directory
frames = []

for file in csvs:
    # Read the file in as a CSV
    frame = pd.read_csv('{}/{}'.format('data', file))
    # Update column names so that they are consistent across years
    frame=frame.rename(columns={'esports_match_id': 'match_id', 'tournament_title': 'stage', 'player_name': 'player',
                          'hero_name': 'hero', 'team_name': 'team', 'pelstart_time': 'start_time'})
    # Add the dataframe to a list
    frames.append(frame)

# Concat all of the dataframes together
player_frame = pd.concat(frames)

# Calculate the season from datetime
def calc_season(dt):
    parsed = datetime.datetime.strptime(dt, '%m/%d/%Y %H:%M')
    return parsed.date().strftime('%Y')

# Filter the frame for only Time Played rows
player_frame = player_frame[(player_frame['stat_name'] == 'Time Played') & (player_frame['hero'] != 'All Heroes')]

# Create a season column from the start_time column
player_frame['season'] = player_frame['start_time'].apply(calc_season)

# Filter the dataframe so that we only have Time Played Rows for Erster with specific heroes
erster_frame = player_frame[(player_frame['player'] == 'Erster')]


# 1. What is Erster's Hero Pool?
print('1. What is Erster\'s Hero Pool?')


# Calculate total time played
total_time = erster_frame['stat_amount'].sum()
# Calculate total time played per hero
play_time = erster_frame[['hero', 'stat_amount']].groupby(by='hero').sum().reset_index()
# Divide total time player per hero by total time played
play_time['play_percent'] = play_time['stat_amount'] / total_time
# Sort the results in descending order
play_time = play_time.sort_values(by='play_percent', ascending = False)
print('Erster Play Time By Hero')
print(play_time)


print('\n\n')

# Take only rows from the 2020 season
erster_2020_frame = erster_frame[(erster_frame['season'] == '2020')]
# Calculate total time played
total_time_2020 = erster_2020_frame['stat_amount'].sum()
# Calculate total time played per hero
play_time_2020 = erster_2020_frame[['hero', 'stat_amount']].groupby(by='hero').sum().reset_index()
# Divide total time player per hero by total time played
play_time_2020['play_percent'] = play_time_2020['stat_amount'] / total_time_2020
# Sort the results in descending order
play_time_2020 = play_time_2020.sort_values(by='play_percent', ascending = False)
print('Erster Play Time By Hero in 2020')
print(play_time_2020)

print('\n\n')
# 2. Has Erster Played the majority of the Reign's Minutes on Mei?
print('2. Has Erster Played the majority of the Reign\'s Minutes on Mei?')


def play_time_breakdown(frame):
    # Total Team Play Time
    total_min = frame['stat_amount'].sum()

    # Take only the player and the time played (stat_amount), group by the player and sum up the total play time.
    ptime = frame[['player', 'stat_amount']].groupby(by='player').sum().reset_index()

    # Take only the player and the time played (stat_amount), group by the player and sum up the total play time.
    ptime['play_percent'] = ptime['stat_amount'] / total_min

    # Rename the columns
    ptime.columns = ['player', 'time_played', 'play_percent']
    # Sort in Descending Order
    ptime = ptime.sort_values(by='play_percent', ascending=False)
    return ptime


def match_breakdown(frame):
    # Count the total number of matches played
    total_matchs = len(frame['match_id'].unique())
    # Take only the player and the match id, group by the player and count number of matches played.
    match_cnt = frame[['player', 'match_id']].drop_duplicates().groupby(by=['player']).count().reset_index()
    # Rename the columns
    match_cnt.columns = ['player', 'match_count']
    # Calculate the percentage of matches played
    match_cnt['play_percent'] = match_cnt['match_count'] / total_matchs
    # Sort in Descending Order
    match_cnt = match_cnt.sort_values(by='play_percent', ascending=False)
    return match_cnt


def map_breakdown(frame):
    # Count the total number of maps played
    total_maps = frame[['match_id', 'map_name']].drop_duplicates().shape[0]
    # Take only the player, the match id and the map name, group by player and count the number of maps each player played
    map_cnt = frame[['player', 'match_id', 'map_name']].drop_duplicates().groupby(
        by=['player']).count().reset_index()
    # Select only the player and the map count
    map_cnt = map_cnt[['player', 'map_name']]
    # Rename teh columns
    map_cnt.columns = ['player', 'map_count']
    # Calculate the percentage of maps played
    map_cnt['play_percent'] = map_cnt['map_count'] / total_maps
    # Sort in Descending Order
    map_cnt = map_cnt.sort_values(by='play_percent', ascending=False)
    return map_cnt




# 2.1 What Percentage of Atlanta Reign's Minutes, Matches and Maps has Erster Played in?
print('2.1 What Percentage of Atlanta Reign\'s Minutes, Matches and Maps has Erster Played in?')

# Filter the dataframe so that we only have Time Played Rows for Atlanta Reign with specific heroes
atlanta_frame = player_frame[(player_frame['stat_name'] == 'Time Played') & (player_frame['team'] == 'Atlanta Reign') & (player_frame['hero'] != 'All Heroes') & (player_frame['season'] == '2020')]

ptime = play_time_breakdown(atlanta_frame)
print('Percentage of Atlanta Reign Play Time by Player')
print(ptime)
print('\n\n')

match_cnt = match_breakdown(atlanta_frame)
print('Percentage of Atlanta Reign Matches')
print(match_cnt)
print('\n\n')

map_cnt = map_breakdown(atlanta_frame)
print('Percentage of Atlanta Reign Maps Played')
print(map_cnt)
print('\n\n')


# 2.2 What Percentage of Atlanta Reign's Mei Minutes, Matches and Maps has Erster Played?
print('2.2 What Percentage of Atlanta Reign\'s Mei Minutes, Matches and Maps has Erster Played?')


# Filter the dataframe so that we only have Time Played Rows for Atlanta Reign with Mei
atlanta_mei_frame = player_frame[(player_frame['stat_name'] == 'Time Played') & (player_frame['team'] == 'Atlanta Reign') & (player_frame['hero'] == 'Mei') & (player_frame['hero'] != 'All Heroes') & (player_frame['season'] == '2020')]
ptime = play_time_breakdown(atlanta_mei_frame)
print('Percentage of Atlanta Reign Play Time by Player On Mei')
print(ptime)
print('\n\n')

match_cnt = match_breakdown(atlanta_mei_frame)
print('Percentage of Atlanta Reign Matches Played On Mei')
print(match_cnt)
print('\n\n')

map_cnt = map_breakdown(atlanta_mei_frame)
print('Percentage of Atlanta Reign Maps Played On Mei')
print(map_cnt)
print('\n\n')

## Build a map of Game Date to Game Week:
game_date_map = {
    '2020/02/08':1,
    '2020/02/09':1,
    '2020/02/10':1,
    '2020/02/15':2,
    '2020/02/16':2,
    '2020/02/22':3,
    '2020/02/23':3,
    '2020/02/24':3,
    '2020/02/29':4,
    '2020/03/01':4,
    '2020/03/02':4,
    '2020/03/07':5,
    '2020/03/08':5,
    '2020/03/28':8,
    '2020/03/29':8,
    '2020/03/30':8,
    '2020/04/04':9,
    '2020/04/05':9,
    '2020/04/06':9,
    '2020/04/11':10,
    '2020/04/12':10,
    '2020/04/13':10,
    '2020/04/16':11,
    '2020/04/17':11,
    '2020/04/18':11,
    '2020/04/19':11,
    '2020/04/25':12,
    '2020/04/26':12,
    '2020/05/02':13,
    '2020/05/03':13,
    '2020/05/09':14,
    '2020/05/10':14,
    '2020/05/11':14,
    '2020/05/16':15,
    '2020/05/17':15,
    '2020/05/22':16,
    '2020/05/23':16,
    '2020/05/24':16,
    '2020/05/25':16
}

def match_date_to_league_week(dt):
    # Extract the date from the match start time and look up the match week
    parsed = datetime.datetime.strptime(dt, '%m/%d/%Y %H:%M')
    return game_date_map[parsed.date().strftime('%Y/%m/%d')]

# We only want matches from the 2020 season for this analysis
player_frame_2020 = player_frame[player_frame['season'] == '2020']

# Generate the match week
player_frame_2020['match_week'] = player_frame_2020['start_time'].apply(match_date_to_league_week)


def play_time_per_match(group):
    # Calculate play percentage in each group
    total_time = group['stat_amount'].sum()
    group['percent_played'] = group['stat_amount'] / total_time
    return group

# Determine weeks that OWL as a whole thought that Mei was meta
# Calculate play percentage of each hero in each week
week_pct = player_frame_2020.groupby(by='match_week').apply(play_time_per_match).reset_index()
# Group by match week and hero and sum out total play time and percentage so we have a breakdown per hero by week.
week_pct = week_pct[['hero', 'match_week', 'percent_played']].groupby(by=['match_week', 'hero']).sum().reset_index()

# Select only Mei
mei_week = week_pct[week_pct['hero'] == 'Mei']
# Multiply by 12 to get the Percent of time played per match week. We multiply by 12 because there are 12 players (6 players on 2 teams)
# in the game at any given time. If Mei had a percent_of_time_played of 2.0 it means that Mei was played at all times during the week
mei_week['percent_of_time_played'] = mei_week['percent_played'] * 12
# Weeks where Mei was played at least half the time by each team are weeks that we determine Mei to be meta
mei_week['meta'] = mei_week['percent_of_time_played'] >= 1
print('Mei Play Time per Week')
print(mei_week)

# Select only the weeks where Mei was meta
mei_week_meta_only = mei_week[mei_week['meta']]
mei_weeks_list = mei_week_meta_only['match_week']



# Determine weeks that Atlanta reign thought Mei was Meta
# Select only player rows for Atlanta Reign players
atlanta_player_frame_2020 = player_frame_2020[player_frame_2020['team'] == 'Atlanta Reign']
# Group by match week and calculate the play time for each player hero combination.
atlanta_week_pct = atlanta_player_frame_2020.groupby(by='match_week').apply(play_time_per_match).reset_index()
# Group by match week and hero and sum up total hero play time for each combination.
atlanta_week_pct = atlanta_week_pct[['hero', 'match_week', 'percent_played']].groupby(by=['match_week', 'hero']).sum().reset_index()
# Select only Mei Rows
atlanta_mei_week = atlanta_week_pct[atlanta_week_pct['hero'] == 'Mei']
# Multiply by 6 to get the percentage of time Mei was in the game for the Reign
atlanta_mei_week['percent_of_time_played'] = atlanta_mei_week['percent_played'] * 6
# Determine which weeks Atlanta played Mei for at least half the match
atlanta_mei_week['meta'] = atlanta_mei_week['percent_of_time_played'] >= 0.5
print('Atlanta Mei Play Time per Week')
print(atlanta_mei_week)
# Only select weeks where the Reign determined that Mei was meta
atlanta_mei_week_meta_only = atlanta_mei_week[atlanta_mei_week['meta']]
atlanta_mei_weeks_list = atlanta_mei_week_meta_only['match_week']

print('\n\n')
print('Weeks that OWL as a whole thought that Mei was meta')
print(list(mei_weeks_list))

print('Weeks that Atlanta reign Played')
print(list(atlanta_player_frame_2020['match_week'].unique()))

# Select weeks that Erster Played
erster_player_frame_2020 = player_frame_2020[player_frame_2020['player'] == 'Erster']
print('Weeks that Erster Played')
print(list(erster_player_frame_2020['match_week'].unique()))

print('Weeks that Atlanta thought that Mei was meta')
print(list(atlanta_mei_weeks_list))

print('\n\n')
# We see from the lists above that the only week Atlanta did not play Mei enough to meet our meta requirements when the
# league as a whole considered her meta was week 10 vs Philly. We can dig in and see what happened in week 10
print('Did Erster Play all of week 10?')
week_10_atl = atlanta_player_frame_2020[atlanta_player_frame_2020['match_week'] == 10]
week_10_play_time = play_time_breakdown(week_10_atl)
print('Play Time Breakdown for Atlanta Reign Week 10')
print(week_10_play_time)

print('\n\n')
week_10_map = map_breakdown(week_10_atl)
print('Map Breakdown for Atlanta Reign Week 10')
print(week_10_map)