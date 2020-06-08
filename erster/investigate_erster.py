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


def minute_breakdown(frame):
    # Total Team Play Time
    total_min = frame['stat_amount'].sum()

    ptime = frame[['player', 'stat_amount']].groupby(by='player').sum().reset_index()
    ptime['play_percent'] = ptime['stat_amount'] / total_min

    print('Percentage of Atlanta Reign Play Time by Player')
    ptime.columns = ['player', 'time_played', 'play_percent']
    ptime = ptime.sort_values(by='play_percent', ascending=False)
    print(ptime)
    print('\n\n')

    total_matchs = len(frame['match_id'].unique())
    match_cnt = frame[['player', 'match_id']].drop_duplicates().groupby(by=['player']).count().reset_index()
    match_cnt.columns = ['player', 'match_count']
    match_cnt['play_percent'] = match_cnt['match_count'] / total_matchs
    match_cnt = match_cnt.sort_values(by='play_percent', ascending=False)

    print('Percentage of Atlanta Reign Matches')
    print(match_cnt)
    print('\n\n')

    total_maps = frame[['match_id', 'map_name']].drop_duplicates().shape[0]
    map_cnt = frame[['player', 'match_id', 'map_name']].drop_duplicates().groupby(
        by=['player']).count().reset_index()
    map_cnt = map_cnt[['player', 'map_name']]
    map_cnt.columns = ['player', 'map_count']
    map_cnt['play_percent'] = map_cnt['map_count'] / total_maps
    map_cnt = map_cnt.sort_values(by='play_percent', ascending=False)

    print('Percentage of Atlanta Reign Maps Played')
    print(map_cnt)
    print('\n\n')

# 2.1 What Percentage of Atlanta Reign's Minutes, Matches and Maps has Erster Played in?
print('2.1 What Percentage of Atlanta Reign\'s Minutes, Matches and Maps has Erster Played in?')

# Filter the dataframe so that we only have Time Played Rows for Atlanta Reign with specific heroes
atlanta_frame = player_frame[(player_frame['stat_name'] == 'Time Played') & (player_frame['team'] == 'Atlanta Reign') & (player_frame['hero'] != 'All Heroes') & (player_frame['season'] == '2020')]
minute_breakdown(atlanta_frame)

# 2.2 What Percentage of Atlanta Reign's Mei Minutes, Matches and Maps has Erster Played?
print('2.2 What Percentage of Atlanta Reign\'s Mei Minutes, Matches and Maps has Erster Played?')


# Filter the dataframe so that we only have Time Played Rows for Atlanta Reign with specific heroes
atlanta_mei_frame = player_frame[(player_frame['stat_name'] == 'Time Played') & (player_frame['team'] == 'Atlanta Reign') & (player_frame['hero'] == 'Mei') & (player_frame['hero'] != 'All Heroes') & (player_frame['season'] == '2020')]
minute_breakdown(atlanta_mei_frame)




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