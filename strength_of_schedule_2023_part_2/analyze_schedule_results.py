import pandas as pd

from strength_of_schedule_2023_part_2.constants import Teams

# Pandas options for better printing
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

schedule_results = pd.read_csv('out/schedule_test_results.csv')

generic_team = 'Generic Average Team'


def calculate_schedule_results(schedule_results, schedule_type, matches):
    generic_team_results = []
    for t in Teams.West23:
        team_schedule_result = schedule_results[schedule_results['team_schedule'] == t]
        first_half = team_schedule_result[team_schedule_result['schedule_type'] == schedule_type]
        iterations = 10000
        map_wins = round(first_half['team_one_map_wins'].sum() / iterations, 2)
        map_losses = round(first_half['team_two_map_wins'].sum() / iterations, 2)
        map_diff = round(map_wins - map_losses, 2)
        match_wins = round(first_half[first_half['winner'] == generic_team].shape[0] / iterations, 2)
        match_losses = round(matches - match_wins, 2)
        generic_team_results.append({
            'schedule': t,
            'wins': match_wins,
            'losses': match_losses,
            'map wins': map_wins,
            'map losses': map_losses,
            'map diff': map_diff
        })
    first_half_results_df = pd.DataFrame(generic_team_results)
    return first_half_results_df


first_half_results = calculate_schedule_results(schedule_results, 'First Half Schedule', 8)
rmsa_results = calculate_schedule_results(schedule_results, 'RMSA Schedule', 4)
map_score_results = calculate_schedule_results(schedule_results, 'Map Score Schedule', 4)
match_score_results = calculate_schedule_results(schedule_results, 'Match Score Schedule', 4)
table_placement_results = calculate_schedule_results(schedule_results, 'Table Placement Schedule', 4)

print('First Half Schedule Results')
print(first_half_results)
print(first_half_results.describe())

print('RMSA Schedule Results')
print(rmsa_results)
print(rmsa_results.describe())


print('Map Score Schedule Results')
print(map_score_results)
print(map_score_results.describe())

print('Match Score Schedule Results')
print(match_score_results)
print(match_score_results.describe())

print('Table Placement Schedule Results')
print(table_placement_results)
print(table_placement_results.describe())