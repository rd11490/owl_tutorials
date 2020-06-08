import warnings
warnings.simplefilter(action='ignore')

import pandas as pd
import os
from pytz import timezone
import datetime


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

csvs = os.listdir('data')
frames = []

for file in csvs:
    frame = pd.read_csv('{}/{}'.format('data', file))
    frame=frame.rename(columns={'esports_match_id': 'match_id', 'tournament_title': 'stage', 'player_name': 'player',
                          'hero_name': 'hero', 'team_name': 'team', 'pelstart_time': 'start_time'})
    frames.append(frame)

player_frame = pd.concat(frames)

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

def calc_season(dt):
    parsed = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M")
    return parsed.date().strftime("%Y")

erster_frame = player_frame[(player_frame['stat_name'] == 'Time Played') & (player_frame['player'] == 'Erster') & (player_frame['hero'] != 'All Heroes')]


erster_frame['season'] = erster_frame['start_time'].apply(calc_season)
erster_frame['game_date'] = erster_frame['start_time'].apply(calc_match_date)
erster_frame['game_week'] = erster_frame['game_date'].apply(calc_match_week_and_year)


total_time = erster_frame['stat_amount'].sum()
play_time = erster_frame[['hero', 'stat_amount']].groupby(by='hero').sum().reset_index()
play_time['play_percent'] = play_time['stat_amount'] / total_time

play_time = play_time.sort_values(by='play_percent', ascending = False)
print('Erster Play Time By Hero')
print(play_time)
print('\n\n')

erster_2020_frame = erster_frame[(erster_frame['season'] == '2020')]

total_time_2020 = erster_2020_frame['stat_amount'].sum()
play_time_2020 = erster_2020_frame[['hero', 'stat_amount']].groupby(by='hero').sum().reset_index()
play_time_2020['play_percent'] = play_time_2020['stat_amount'] / total_time_2020

play_time_2020 = play_time_2020.sort_values(by='play_percent', ascending = False)

print('Erster Play Time By Hero in 2020')
print(play_time_2020)
