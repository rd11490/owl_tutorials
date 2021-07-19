import pandas as pd
from rmsa.utils.constants import Maps, total_escort_map_distance, total_map_time, calc_map_type
from rmsa.utils.utils import calc_match_date, calc_season

# Some readability options for pandas print statements
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 1000)

# Read in our match_map_stats csv file
frame = pd.read_csv('./input/match_map_stats.csv')


# Determine the map type, match date, and season for every map played
frame['map_type'] = frame['map_name'].apply(calc_map_type)
frame['match_date'] = frame['round_end_time'].apply(calc_match_date)
frame['season'] = frame['round_end_time'].apply(calc_season)


# Split our dataframe into four different frames. Each frame will only contain maps for it's specific map type
escort_maps = frame[frame['map_type'] == Maps.Escort]
assault_maps = frame[frame['map_type'] == Maps.Assault]
control_maps = frame[frame['map_type'] == Maps.Control]
hybrid_maps = frame[frame['map_type'] == Maps.Hybrid]


###############################
# Calculate control map score #
###############################
# Controls maps are "easy" to score because each team is able to get a control percentage.
# Convert the percentage to a decimal and use it as the map score
control_maps['team_one_score'] = control_maps['attacker_control_perecent']/100
control_maps['team_two_score'] = control_maps['defender_control_perecent']/100


control_maps_score = control_maps[['match_id', 'game_number','map_name', 'map_type', 'map_winner', 'match_date',  'team_one_name', 'team_two_name', 'team_one_score', 'team_two_score', 'season']]

###############################
# Calculate Assault map score #
###############################


def calculate_assault_map_score(group):
    # Pull the highest round number played and take the row for that round
    highest = group['map_round'].max()
    row = group[group['map_round'] == highest]

    # Assign attackers as team 1 and defenders as team 2
    team_one = row['attacker'].values[0]
    team_two = row['defender'].values[0]

    # In assault, <team>_round_end_score is the number of points each team captured
    # It should be noted that if the first attacker is full held,
    # the second attacker only needs to get 33% to receive full credit for taking a point
    team_one_rounds = row['attacker_round_end_score'].values[0]
    team_two_rounds = row['defender_round_end_score'].values[0]

    # We all so want to pull out how much time each team banked if they capped before overtime
    team_one_time_banked = row['attacker_time_banked'].values[0]
    team_two_time_banked = row['defender_time_banked'].values[0]


    # We can use the number of rounds played to determine and how much time is banked to determine how much time was used
    # to capture the number of points the team captured.
    team_one_rounds_for_time = team_one_rounds
    team_two_rounds_for_time = team_two_rounds
    if row['map_winner'].values[0] == team_one and team_one_time_banked > 0.0:
        team_one_rounds_for_time -= 1
    elif row['map_winner'].values[0] == team_two and team_two_time_banked > 0.0:
        team_two_rounds_for_time -= 1

    team_one_total_time = total_map_time(Maps.Assault, team_one_rounds_for_time)
    team_two_total_time = total_map_time(Maps.Assault, team_two_rounds_for_time)

    # Once we have the number of points captured, the time banked, and time used, we can generate a map score
    team_one_score = 100 * team_one_rounds / (team_one_total_time - team_one_time_banked)
    team_two_score = 100 * team_two_rounds / (team_two_total_time - team_two_time_banked)

    # Save the map score in a dataframe
    return pd.Series({
        'map_name': row['map_name'].values[0],
        'map_type': row['map_type'].values[0],
        'map_winner': row['map_winner'].values[0],
        'match_date': row['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': team_one_score,
        'team_two_score': team_two_score,
        'season': row['season'].values[0]
    })

assault_scores = assault_maps.groupby(by=['match_id', 'game_number']).apply(calculate_assault_map_score).reset_index()

###############################
# Calculate Escort map score #
###############################


def calculate_escort_map_score(group):
    highest = group['map_round'].max()
    row = group[group['map_round'] == highest]

    map = row['map_name'].values[0]

    team_one = row['attacker'].values[0]
    team_two = row['defender'].values[0]
    team_one_rounds = row['attacker_round_end_score'].values[0]
    team_two_rounds = row['defender_round_end_score'].values[0]

    team_one_time_banked = row['attacker_time_banked'].values[0]
    team_two_time_banked = row['defender_time_banked'].values[0]

    team_one_distance = row['attacker_payload_distance'].values[0]
    team_two_distance = row['defender_payload_distance'].values[0]


    if row['map_winner'].values[0] == team_one and team_one_distance > 0.0:
        team_one_rounds -= 1
    elif row['map_winner'].values[0] == team_two and team_two_distance > 0.0:
        team_two_rounds -= 1

    team_one_total_distance = total_escort_map_distance(map, team_one_rounds) + team_one_distance
    team_two_total_distance = total_escort_map_distance(map, team_two_rounds) + team_two_distance

    team_one_total_time = total_map_time(Maps.Escort, team_one_rounds)
    team_two_total_time = total_map_time(Maps.Escort, team_two_rounds)



    team_one_score = team_one_total_distance / (team_one_total_time - team_one_time_banked)
    team_two_score = team_two_total_distance / (team_two_total_time - team_two_time_banked)

    # if team_one_score > team_two_score:
    #     team_one_score_percent = team_one_score / team_one_score
    #     team_two_score_percent = team_two_score / team_one_score
    # else:
    #     team_one_score_percent = team_one_score / team_two_score
    #     team_two_score_percent = team_two_score / team_two_score


    return pd.Series({
        'map_name': map,
        'map_type': row['map_type'].values[0],
        'map_winner': row['map_winner'].values[0],
        'match_date': row['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': team_one_score,
        'team_two_score': team_two_score,
        'season': row['season'].values[0]
    })

escort_maps_score = escort_maps.groupby(by=['match_id', 'game_number']).apply(calculate_escort_map_score).reset_index()


###############################
# Calculate Hybrid map score #
###############################


def calculate_hybrid_map_score(group):

    highest = group['map_round'].max()
    row = group[group['map_round'] == highest]

    map = row['map_name'].values[0]

    team_one = row['attacker'].values[0]
    team_two = row['defender'].values[0]
    team_one_rounds = row['attacker_round_end_score'].values[0]
    team_two_rounds = row['defender_round_end_score'].values[0]

    team_one_time_banked = row['attacker_time_banked'].values[0]
    team_two_time_banked = row['defender_time_banked'].values[0]

    team_one_distance = row['attacker_payload_distance'].values[0]
    team_two_distance = row['defender_payload_distance'].values[0]


    if row['map_winner'].values[0] == team_one and team_one_distance > 0.0:
        team_one_rounds -= 1
    elif row['map_winner'].values[0] == team_two and team_two_distance > 0.0:
        team_two_rounds -= 1

    team_one_total_distance = total_escort_map_distance(map, team_one_rounds) + team_one_distance
    team_two_total_distance = total_escort_map_distance(map, team_two_rounds) + team_two_distance

    team_one_total_time = total_map_time(Maps.Escort, team_one_rounds)
    team_two_total_time = total_map_time(Maps.Escort, team_two_rounds)



    team_one_score = team_one_total_distance / (team_one_total_time - team_one_time_banked)
    team_two_score = team_two_total_distance / (team_two_total_time - team_two_time_banked)

    # if team_one_score > team_two_score:
    #     team_one_score_percent = team_one_score / team_one_score
    #     team_two_score_percent = team_two_score / team_one_score
    # else:
    #     team_one_score_percent = team_one_score / team_two_score
    #     team_two_score_percent = team_two_score / team_two_score


    return pd.Series({
        'map_name': map,
        'map_type': row['map_type'].values[0],
        'map_winner': row['map_winner'].values[0],
        'match_date': row['match_date'].values[0],
        'team_one_name': team_one,
        'team_two_name': team_two,
        'team_one_score': team_one_score,
        'team_two_score': team_two_score,
        'season': row['season'].values[0]
    })

hybrid_maps_score = hybrid_maps.groupby(by=['match_id', 'game_number']).apply(calculate_hybrid_map_score).reset_index()

scored_maps = pd.concat([control_maps_score, hybrid_maps_score, escort_maps_score, assault_scores])

scored_maps.to_csv('results/scored_maps.csv', index=False)