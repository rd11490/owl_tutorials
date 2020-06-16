import warnings
warnings.simplefilter(action='ignore')

import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Read in our map stats data
map_data = pd.read_csv('data/match_map_stats.csv')

print(map_data.head(20))
print('\n\n')


# Print out our columns so we can see what we are looking at
print('Dataframe Columns')
for c in map_data.columns:
    print(c)

print('\n\n')
print('Maps')
# Grab all of the map names
for i, row in map_data[['map_name', 'control_round_name']].drop_duplicates().sort_values(by='map_name').iterrows():
    map = row['map_name']
    control = row['control_round_name']

    if pd.isna(control):
        print(map)
    else:
        print('{} - {}'.format(map, control))


# Classify maps into game types
class MapType:
    Assault = 'Assault'
    Control = 'Control'
    Escort = 'Escort'
    Hybrid = 'Hybrid'

    map_types = {
        'Hanamura': Assault,
        'Horizon Lunar Colony': Assault,
        'Paris': Assault,
        'Temple of Anubis': Assault,
        'Volskaya Industries': Assault,

        'Busan': Control,
        'Ilios': Control,
        'Lijiang Tower': Control,
        'Nepal': Control,
        'Oasis': Control,

        'Dorado': Escort,
        'Havana': Escort,
        'Junkertown': Escort,
        'Rialto': Escort,
        'Route 66': Escort,
        'Watchpoint: Gibraltar': Escort,

        'Numbani': Hybrid,
        'Eichenwalde': Hybrid,
        "King's Row": Hybrid,
        'Hollywood': Hybrid,
        'Blizzard World': Hybrid,
    }

# Determine the map type for each map
def calc_map_type(map_name):
    return MapType.map_types[map_name]

map_data['map_type'] = map_data['map_name'].apply(calc_map_type)
print('\n\n')
print('Map Data with map type included')
print(map_data.head(20))
#
# # Control maps only
#
# control_map_data = map_data[map_data['map_type'] == MapType.Control]
# print('\n\n')
# print('Control Maps Only')
# print(control_map_data.head(20))
#
# # Remove columns that don't matter for control
# control_map_data = control_map_data[['stage', 'match_id', 'game_number', 'map_name', 'control_round_name', 'map_type', 'map_round', 'map_winner', 'attacker', 'defender', 'attacker_control_perecent', 'defender_control_perecent']]
# print('\n\n')
# print('Control Maps Relevant Data Only')
# print(control_map_data.head(20))
#
# # What percentage of control maps go to 100% - 99%?
#
# close_games = control_map_data[((control_map_data['attacker_control_perecent'] == 99.0) & (control_map_data['defender_control_perecent'] == 100.0)) | ((control_map_data['attacker_control_perecent'] == 100.0) & (control_map_data['defender_control_perecent'] == 99.0))]
#
# num_close_game = close_games.shape[0]
# num_games =  control_map_data.shape[0]
# print('\n\n')
# print('Percentage of Contorl Maps that End 100 to 99: {}/{} = {}'.format(num_close_game,num_games,num_close_game/num_games))
#
#
# # Escort Maps:
# escort_map_data = map_data[map_data['map_type'] == MapType.Escort]
# print('\n\n')
# print('Escort Maps Only')
# print(escort_map_data.head(20))
#
# escort_map_data = escort_map_data[['stage', 'match_id', 'game_number', 'map_name', 'map_type', 'map_round', 'map_winner', 'attacker', 'defender', 'attacker_payload_distance', 'attacker_time_banked', 'attacker_round_end_score']]
# print('\n\n')
# print('Escort Maps Relevant Data Only')
# print(escort_map_data.head(20))
# print('\n\n')
#
# # What is the average time banked per map?
# escort_completion = escort_map_data[escort_map_data['attacker_round_end_score'] == 3]
# print(escort_completion[['map_name', 'attacker_time_banked']].groupby('map_name').describe().reset_index())
#
# # Hybrid Maps:
# hybrid_map_data = map_data[map_data['map_type'] == MapType.Hybrid]
# print('\n\n')
# print('Hybrid Maps Only')
# print(hybrid_map_data.head(20))
#
# hybrid_map_data = hybrid_map_data[['stage', 'match_id', 'game_number', 'map_name', 'map_type', 'map_round', 'map_winner', 'attacker', 'defender', 'attacker_payload_distance', 'attacker_time_banked', 'attacker_round_end_score']]
# print('\n\n')
# print('Hybrid Maps Relevant Data Only')
# print(hybrid_map_data.head(20))
# print('\n\n')
#
# # Which Map are you most likely to get full held on?
# map_counts = hybrid_map_data[['map_name','attacker_round_end_score']].groupby('map_name').count().reset_index()
# map_counts.columns = ['map_name', 'times_played']
# hybrid_held = hybrid_map_data[hybrid_map_data['attacker_round_end_score'] == 0]
# full_held = hybrid_held[['map_name', 'attacker_time_banked']].groupby('map_name').count().reset_index()
# full_held.columns = ['map_name', 'times_full_held']
# full_held_pct = full_held.merge(map_counts, on='map_name')
# full_held_pct['full_hold_percent'] = full_held_pct['times_full_held']/full_held_pct['times_played']
# full_held_pct = full_held_pct.sort_values(by='full_hold_percent', ascending=False)
# print('Chance to be full held on each Hybrid Map')
# print(full_held_pct)
#
#
# # 2 CP
# assault_map_data = map_data[map_data['map_type'] == MapType.Assault]
# print('\n\n')
# print('Hybrid Maps Only')
# print(assault_map_data.head(20))
#
# assault_map_data = assault_map_data[['stage', 'match_id', 'game_number', 'map_name', 'map_type', 'map_round', 'map_winner', 'attacker', 'defender', 'attacker_time_banked', 'attacker_round_end_score']]
# print('\n\n')
# print('Assault Maps Relevant Data Only')
# print(assault_map_data.head(20))
# print('\n\n')
#
# print("How many rounds do the average 2CP Map Go?")
# def match_percent(group):
#     sum = group['match_id'].sum()
#     group['match_percent'] = group['match_id'] / sum
#     return group
#
# max_score_group = assault_map_data[['match_id', 'map_name', 'map_round']].groupby(by=['match_id', 'map_name']).max().reset_index().groupby(by=['map_name', 'map_round']).count().reset_index().groupby(by=['map_name'])
# max_score = max_score_group.apply(match_percent)
# max_score.columns = ['map_name', 'map_round', 'match_count', 'match_percent']
# print(max_score)