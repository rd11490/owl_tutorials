import warnings
warnings.simplefilter(action='ignore')

import pandas as pd
import os
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

csvs = os.listdir('player_data') # Get all files in the data directory
frames = []

for file in csvs:
    # Read the file in as a CSV
    frame = pd.read_csv('{}/{}'.format('player_data', file))
    # Update column names so that they are consistent across years
    frame=frame.rename(columns={'esports_match_id': 'match_id', 'tournament_title': 'stage', 'player_name': 'player',
                          'hero_name': 'hero', 'team_name': 'team', 'pelstart_time': 'start_time'})
    # Add the dataframe to a list
    frames.append(frame)


# Concat all of the dataframes together
player_frame = pd.concat(frames)

print(player_frame)
print('\n\n')

# Print all of the columns in the dataframe
print('Dataframe Columns:')
for c in player_frame.columns:
    print(c)

print('\n\n')

# Print out all of the possible stats
print('Unique Stat Names:')
for p in np.sort(player_frame['stat_name'].unique()):
    print(p)




print('\n\n')

# Find out who has the most final blows in a single map for each map
final_blows = player_frame[player_frame['stat_name'] == 'Final Blows'][['match_id', 'map_name', 'player', 'stat_amount']].drop_duplicates()

def take_max(group):
    max_kills = group['stat_amount'].max()
    return group[group['stat_amount'] == max_kills]

max_final_blows = final_blows.groupby(by=['map_name']).apply(take_max).reset_index(drop=True).sort_values(by='stat_amount')[['map_name', 'player', 'stat_amount']]
max_final_blows.columns = ['map_name', 'player', 'final_blows']
print('Final Blow Leaders per Map')
print(max_final_blows)
print('\n\n')


# Find out which player is the most successful at getting sleeps on Ana
ana_sleep = player_frame[(player_frame['hero'] == 'Ana') & ((player_frame['stat_name'] == 'Sleep Dart Hits') | (player_frame['stat_name'] == 'Sleep Dart Shots'))][['player', 'stat_name','stat_amount']]

def calculate_sleep_efficency(group):
    sleeps_hit = group[group['stat_name'] == 'Sleep Dart Hits']['stat_amount'].sum()
    sleeps_shot = group[group['stat_name'] == 'Sleep Dart Shots']['stat_amount'].sum()

    return pd.Series({'sleep_darts_shot': sleeps_shot, 'sleep_darts_hit': sleeps_hit, 'sleep_accuracy': sleeps_hit/sleeps_shot})



ana_sleep = ana_sleep.groupby(by='player').apply(calculate_sleep_efficency)
ana_sleep = ana_sleep[ana_sleep['sleep_darts_shot'] >= 100]
sleep_stats = ana_sleep.sort_values(by='sleep_accuracy', ascending=False).head(10).reset_index()
print('Ana Sleep Dart Accuracy (min 100 attempts)')
print(sleep_stats)