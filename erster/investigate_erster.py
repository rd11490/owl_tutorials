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

# Filter the dataframe so that we only have Time Played Rows for Erster with specific heroes
erster_frame = player_frame[(player_frame['stat_name'] == 'Time Played') & (player_frame['player'] == 'Erster') & (player_frame['hero'] != 'All Heroes')]


# Calculate the season from datetime
def calc_season(dt):
    parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M")
    return parsed.date().strftime("%Y")

# Create a season column from the start_time column
erster_frame['season'] = erster_frame['start_time'].apply(calc_season)


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