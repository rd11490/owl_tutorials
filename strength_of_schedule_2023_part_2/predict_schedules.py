import pandas as pd

from strength_of_schedule_2023_part_2.constants import Maps, Teams
from strength_of_schedule_2023_part_2.helpers import build_rmsa_map, predict_match

# Pandas options for better printing
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

###
# Set up RMSA for a generic "Average" team
###
generic_team = 'Generic Average Team'


def build_average_team(rmsa_frame, map_type):
    map_frame = rmsa_frame[rmsa_frame['map_type'] == map_type]
    return pd.DataFrame([{
        'team': generic_team,
        'rmsa attack': map_frame['rmsa attack'].mean(),
        'rmsa attack stdev': map_frame['rmsa attack stdev'].mean(),
        'rmsa defend':map_frame['rmsa defend'].mean(),
        'rmsa defend stdev': map_frame['rmsa defend stdev'].mean(),
        'rmsa': 0,
        'normalized rmsa': 0,
        'map_type': map_type
    }])


rmsa_frame = pd.read_csv('data/rmsa-2023.csv')

rmsa_frame = rmsa_frame[rmsa_frame['team'].isin(Teams.West23)]

average_control = build_average_team(rmsa_frame, Maps.Control)
average_hybrid = build_average_team(rmsa_frame, Maps.Hybrid)
average_escort = build_average_team(rmsa_frame, Maps.Escort)
average_push = build_average_team(rmsa_frame, Maps.Push)

rmsa_frame = pd.concat([rmsa_frame, average_control, average_hybrid, average_escort, average_push], ignore_index=True)

rmsa_map = build_rmsa_map(rmsa_frame)

####
# Read in created Schedules
####

rmsa_schedule = pd.read_csv('out/rmsa_schedule.csv')
map_score_schedule = pd.read_csv('out/map_score_schedule.csv')
match_score_schedule = pd.read_csv('out/match_score_schedule.csv')
table_schedule = pd.read_csv('out/table_schedule.csv')

first_half_schedule = pd.read_csv('data/2023_league_schedule_first_half.csv')

map_rotation = [Maps.Control, Maps.Hybrid, Maps.Escort, Maps.Push, Maps.Control]

teams_and_opponents = []


def handle_row(row):
    teams_and_opponents.append({
        'teamId': row['team1Id'],
        'teamName': row['team1Name'],
        'teamShortName': row['team1ShortName'],
        'opponentId': row['team2Id'],
        'opponentName': row['team2Name'],
        'opponentShortName': row['team2ShortName']
    })
    teams_and_opponents.append({
        'teamId': row['team2Id'],
        'teamName': row['team2Name'],
        'teamShortName': row['team2ShortName'],
        'opponentId': row['team1Id'],
        'opponentName': row['team1Name'],
        'opponentShortName': row['team1ShortName']
    })


first_half_schedule.apply(handle_row, axis=1)
first_half_schedule = pd.DataFrame(teams_and_opponents)


def predict_schedule(opponents, schedule_team, schedule_type):
    for first_half_opponent in opponents:
        result = predict_match(generic_team, first_half_opponent, map_rotation, rmsa_map, maps_to_win=3)
        result['schedule_type'] = schedule_type
        result['team_schedule'] = schedule_team
        team_schedule_results.append(result)


team_schedule_results = []
for i in range(0, 1000):
    for team in Teams.West23:
        first_half_opponents = first_half_schedule[first_half_schedule['teamName'] == team]['opponentName'].values

        rmsa_schedule_opponents = rmsa_schedule[rmsa_schedule['team'] == team][
            ['doubleOpponent1', 'doubleOpponent2', 'doubleOpponent3', 'doubleOpponent4']].values[0]

        map_score_schedule_opponents = map_score_schedule[map_score_schedule['team'] == team][
            ['doubleOpponent1', 'doubleOpponent2', 'doubleOpponent3', 'doubleOpponent4']].values[0]

        match_score_schedule_opponents = match_score_schedule[match_score_schedule['team'] == team][
            ['doubleOpponent1', 'doubleOpponent2', 'doubleOpponent3', 'doubleOpponent4']].values[0]

        table_placement_schedule_opponents = table_schedule[table_schedule['team'] == team][
            ['doubleOpponent1', 'doubleOpponent2', 'doubleOpponent3', 'doubleOpponent4']].values[0]


        predict_schedule(first_half_opponents, team, 'First Half Schedule')
        predict_schedule(rmsa_schedule_opponents, team, 'RMSA Schedule')
        predict_schedule(map_score_schedule_opponents, team, 'Map Score Schedule')
        predict_schedule(match_score_schedule_opponents, team, 'Match Score Schedule')
        predict_schedule(table_placement_schedule_opponents, team, 'Table Placement Schedule')

schedule_results_frame = pd.DataFrame(team_schedule_results)

schedule_results_frame.to_csv('out/schedule_test_results.csv')
