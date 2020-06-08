import warnings
warnings.simplefilter(action='ignore')

import pandas as pd
import os
from pytz import timezone
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
    parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M")
    return parsed.date().strftime("%Y")

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


# Filter the dataframe so that we only have Time Played Rows for Atlanta Reign with specific heroes
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
'2020/02/15':2,
'2020/02/16':2,
'2020/02/22':3,
'2020/02/23':3,
'2020/02/29':4,
'2020/03/01':4,
'2020/03/07':5,
'2020/03/08':5,
'2020/03/28':8,
'2020/03/29':8,
'2020/04/04':9,
'2020/04/05':9,
'2020/04/06':9,
'2020/04/11':10,
'2020/04/12':10,
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
'2020/05/16':15,
'2020/05/17':15,
'2020/05/22':16,
'2020/05/23':16,
'2020/05/24':16
}

def play_time_per_match(group):
    total_time = group['stat_amount'].sum()
    group['pct'] = group['stat_amount'] / total_time
    return group

week_pct = time_played.groupby(by='game_week').apply(play_time_per_match).reset_index()
week_pct = week_pct[['hero_name', 'game_week', 'pct']].groupby(by=['game_week', 'hero_name']).sum().reset_index()

mei_week = week_pct[week_pct['hero_name'] == 'Mei']
mei_week['meta'] = mei_week['pct'] >= 1/12
mei_week = mei_week[mei_week['meta']]
mei_week = mei_week[['game_week']]




def calc_match_date(dt):
    tz = timezone('US/Pacific')
    parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M").astimezone(tz)
    return parsed.date().strftime("%Y/%m/%d")

def calc_match_week_and_year(dt):
    parsed = datetime.datetime.strptime(dt, "%Y/%m/%d")
    year = parsed.isocalendar()[0]
    week = parsed.isocalendar()[1]
    if week < 10:
        week = '0' + str(week)
    return '{}-{}'.format(year, week)