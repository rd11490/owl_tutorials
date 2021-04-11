import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Read the csv
frame = pd.read_csv('map_data/match_map_stats.csv')


# print out the first 10 rows just to see what type of data we are looking at
print(frame.head(10))


# Look at all of the unique stages
print('\nStages')
for stage in frame['stage'].unique():
    print(stage)

# Look at all of the unique maps
print('\nMaps')
for map in frame['map_name'].unique():
    print(map)

# Look at all of the unique teams
print('\nTeams')
for team in frame['team_one_name'].unique():
    print(team)