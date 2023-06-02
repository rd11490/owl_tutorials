import random

import pandas as pd
import itertools
import copy

# Pandas options for better printing
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


# Build a dictionary to hold our second half schedule that we will be manipulating in this process
# Also build a counter for schedule initialization so that we build a valid initial schedule
def build_second_half_schedule_and_counter(teams):
    team_second_half = {}
    team_counter = {}
    for t in teams:
        team_second_half[t] = []
        team_counter[t] = 0
    return team_second_half, team_counter


# Take all teams that do not have 4 matches already and randomly select 2
# if the teams are not already in each's schedules and the teams are different, up the counter and return
# if not re-draw
def pick_match(team_counter, schedule):
    valid_match = False
    teams_to_pick = [k for k, v in team_counter.items() if v < 4]
    if len(teams_to_pick) < 2:
        return None
    while not valid_match:
        team1, team2 = random.sample(teams_to_pick, 2)
        if (team1 is not team2) and (team1 not in schedule[team2]) and (team2 not in schedule[team1]):
            team_counter[team1] = team_counter[team1] + 1
            team_counter[team2] = team_counter[team2] + 1
            return team1, team2


# Pick matches and build schedules until you have a complete schedule
def initialize_schedule(teams, team_rankings):
    team_second_half, team_counter = build_second_half_schedule_and_counter(teams)
    schedule_built = False
    while not schedule_built:
        match = pick_match(team_counter, team_second_half)
        if match is None:
            schedule_built = True
        else:
            team1, team2 = match
            team_second_half[team1].append((team2, team_rankings[team2]))
            team_second_half[team2].append((team1, team_rankings[team1]))

    return team_second_half, team_counter


# Function to check if the entire schedule is balanced using the max_sos_difference we determined above
def check_balanced(team_sos, max_sos_difference, target_avg):
    values = [v for k, v in team_sos.items()]
    diff = [abs(v - target_avg) for v in values]
    sum_diff = sum(diff)
    print(f'check_balanced: {sum_diff}, {values}')
    for v in values:
        if abs(target_avg - v) >= max_sos_difference:
            return False, sum_diff
    return True, sum_diff


# Randomly select 2 teams and their schedules
def find_randoms_schedules(team_sos):
    teams = list(team_sos.keys())
    team1 = None
    team2 = None
    while team1 == team2:
        team1 = random.choices(teams, k=1)[0]
        team2 = random.choices(teams, k=1)[0]
    return team1, team2


# Build all possible combinations of 2 sets for 4 opponents for optimizing 2 teams schedules
def generate_combinations(items):
    combinations = []
    for combo in itertools.combinations(items, 4):
        remaining_items = list(set(items) - set(combo))
        for remaining_combo in itertools.combinations(remaining_items, 4):
            combinations.append((list(combo), list(remaining_combo)))
    return combinations


# Remove any combinations of schedules that would result in two teams playing 3 times
def filter_swap_set_with_duplicates(swap_set):
    set1, set2 = swap_set
    return (len(set1) == len(set(set1))) and (len(set2) == len(set(set2)))


# Filter out any combinations that would result in a team playing against itself
def filter_swap_set_with_team_in(swap_team1, swap_team2, swap_set):
    set1, set2 = swap_set
    set1_has_team1 = all([t1[0] != swap_team1 for t1 in set1])
    set2_has_team2 = all([t2[0] != swap_team2 for t2 in set2])
    return set1_has_team1 and set2_has_team2


# Calculate the SoS difference from our target average for a combination
def calc_sos_diff_for_swap_set(swap_set, target_average):
    set1, set2 = swap_set
    score1 = abs(target_average - sum([t[1] for t in set1]))
    score2 = abs(target_average - sum([t[1] for t in set2]))

    return score1 + score2


# Given 2 teams and their schedules, generate all possible combinations of 2 sets of 4, select the schedule with the lowest
# difference in SoS that is also a valid schedule set
def smart_swap_teams(swap_team1, swap_team1_schedule, swap_team2, swap_team2_schedule, target_average):
    combinations = generate_combinations(swap_team1_schedule + swap_team2_schedule)
    combinations = [c for c in combinations if filter_swap_set_with_duplicates(c)]
    combinations = [c for c in combinations if filter_swap_set_with_team_in(swap_team1, swap_team2, c)]
    if len(combinations) == 0:
        return None, None
    min_swap_set = min(combinations, key=lambda x: calc_sos_diff_for_swap_set(x, target_average))
    return list(set(swap_team1_schedule) - set(min_swap_set[0])), list(set(swap_team2_schedule) - set(min_swap_set[1]))


# Attempt to optimize the schedules of 2 teams - if t is not possible to swap 2 schedules, select 2 new teams and try again
def get_random_schedules_to_swap_smart(team_sos, second_half, target_average):
    swap_set = False
    while not swap_set:
        swap_team1, swap_team2 = find_randoms_schedules(team_sos)
        swap_team1_schedule = second_half[swap_team1]
        swap_team2_schedule = second_half[swap_team2]
        to_swap_team_1, to_swap_team_2 = smart_swap_teams(swap_team1, swap_team1_schedule, swap_team2,
                                                          swap_team2_schedule, target_average)
        if (to_swap_team_1 is not None) and (to_swap_team_2 is not None):
            return swap_team1, to_swap_team_1, swap_team2, to_swap_team_2


def balance_schedule(schedule, rankings, max_sos_difference):
    # Take the average rating of all teams and multiply by 4 to get our target average
    average = rankings['rank'].mean()
    target_average = average * 4

    schedule = schedule.merge(rankings, left_on='opponentShortName', right_on='team')
    # build a dictionary for lookup of each team and their rating
    teams_and_ratings = schedule[['opponentName', 'rank']].drop_duplicates()
    team_rankings = {}
    for i in teams_and_ratings.index:
        row = teams_and_ratings.loc[i, :]
        team_rankings[row['opponentName']] = row['rank']

    teams = list(schedule['teamName'].unique())

    team_schedules = schedule[['teamName', 'opponentName', 'rank']]
    team_schedules = schedule.rename(columns={'rank': 'opponentRank'})

    all_teams = list(team_schedules['teamName'].unique())

    # Build the second half schedule for each team by find all teams they did not play in the first half
    second_half = []

    def get_second_half_schedule(group):
        team = group['teamName'].values[0]
        opponents = list(group['opponentName'])
        result = [oppo for oppo in all_teams if oppo not in opponents and oppo != team]
        second_half.append({
            'team': team,
            'secondHalfOpponent1': result[0],
            'secondHalfOpponent2': result[1],
            'secondHalfOpponent3': result[2],
            'secondHalfOpponent4': result[3]
        })

    team_schedules.groupby(by='teamName').apply(get_second_half_schedule)
    second_half_df = pd.DataFrame(second_half)

    # Initialize the schedule, check to see if it is valid, if not repeat until a valid schedule is found
    is_balanced = False
    team_second_half, team_counter = initialize_schedule(teams, team_rankings)
    while not is_balanced:
        team_second_half, team_counter = initialize_schedule(teams, team_rankings)
        is_balanced = True
        for k, v in team_second_half.items():
            if len(v) != 4 or len(set(v)) != 4:
                is_balanced = False

    # Print the initial schedule
    double_schedule = []
    for k, v in team_second_half.items():
        print(f'SOS {k}: {v}, {sum([i[1] for i in v])}')
        double_schedule.append({
            'team': k,
            'doubleOpponent1': v[0][0],
            'doubleOpponent2': v[1][0],
            'doubleOpponent3': v[2][0],
            'doubleOpponent4': v[3][0],
            'totalSOS': sum([i[1] for i in v])
        })
    double_schedule_df = pd.DataFrame(double_schedule)
    second_half_df_original = second_half_df.merge(double_schedule_df, on='team')
    print(second_half_df_original)

    # Build a lookup dictionary of each team's SoS
    team_sos = {}
    for k, v in team_second_half.items():
        team_sos[k] = sum([i[1] for i in v])

    # Optimize two team's schedules, then propagate those changes to the entire schedule, check the updated schedule balance
    # and repeat until all schedules are balanced within our initial conditions or until we've hit 100,000 iterations. If
    # 100,000 iterations are completed, then the most balanced schedule found will be returned
    iterations = 0
    cum_sum_schedule_diff = 9999
    best_schedule = None
    is_balanced = False
    while not is_balanced:
        print(f'Iteration: {iterations}')
        team1, remove_from_team1_lst, team2, remove_from_team2_lst = get_random_schedules_to_swap_smart(team_sos,
                                                                                                        team_second_half,
                                                                                                        target_average)

        team1_schedule = team_second_half[team1]
        team2_schedule = team_second_half[team2]

        for remove_from_team1 in remove_from_team1_lst:
            team1_schedule.remove(remove_from_team1)
            team2_schedule.append(remove_from_team1)

            team1_old_opponent_schedule = team_second_half[remove_from_team1[0]]
            team1_old_opponent_schedule.remove((team1, team_rankings[team1]))
            team1_old_opponent_schedule.append((team2, team_rankings[team2]))
            team_second_half[remove_from_team1[0]] = team1_old_opponent_schedule

        for remove_from_team2 in remove_from_team2_lst:
            team1_schedule.append(remove_from_team2)
            team2_schedule.remove(remove_from_team2)

            team2_old_opponent_schedule = team_second_half[remove_from_team2[0]]
            team2_old_opponent_schedule.remove((team2, team_rankings[team2]))
            team2_old_opponent_schedule.append((team1, team_rankings[team1]))
            team_second_half[remove_from_team2[0]] = team2_old_opponent_schedule

        team_second_half[team1] = team1_schedule
        team_second_half[team2] = team2_schedule

        # fix schedules of swapped teams:
        for k, v in team_second_half.items():
            team_sos[k] = sum([i[1] for i in v])

        is_balanced, sched_sos = check_balanced(team_sos, max_sos_difference, target_average)
        if is_balanced:
            best_schedule = copy.deepcopy(team_second_half)
            cum_sum_schedule_diff = sched_sos
        if cum_sum_schedule_diff > sched_sos:
            best_schedule = copy.deepcopy(team_second_half)
            cum_sum_schedule_diff = sched_sos
        iterations += 1
        if iterations > 100000:
            is_balanced = True

        # calculate each teams rating
        # if each team has rating +- 3 end
        # take top and bottom
        # swap 1 random team each (make sure not to have a team play themselves
    team_sos = {}
    for k, v in best_schedule.items():
        team_sos[k] = sum([i[1] for i in v])

    check_balanced(team_sos, max_sos_difference, target_average)
    double_schedule = []
    for k, v in best_schedule.items():
        print(f'SOS {k}: {v}, {sum([i[1] for i in v])}')
        double_schedule.append({
            'team': k,
            'doubleOpponent1': v[0][0],
            'doubleOpponent2': v[1][0],
            'doubleOpponent3': v[2][0],
            'doubleOpponent4': v[3][0],
            'totalSOS': sum([i[1] for i in v])
        })

    double_schedule_df = pd.DataFrame(double_schedule)

    second_half_df = second_half_df.merge(double_schedule_df, on='team')
    second_half_df['unbalanced'] = second_half_df['totalSOS'] - second_half_df['totalSOS'].mean()
    return second_half_df


#########
#
#  START THE CODE
#
#########

# Read in the 2023 first half schedule
frame = pd.read_csv(f'./data/2023_league_schedule_first_half.csv')
# Read in our rankings
rmsa_ratings = pd.read_csv('data/ratings.csv')
map_score_ratings = pd.read_csv('data/ratings_map_score.csv')
match_score_ratings = pd.read_csv('data/ratings_match_score.csv')
table_ratings = pd.read_csv('data/ratings_table.csv')

# Build schedules and merge with ratings to that we can get an idea of each team's strength of schedule
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


frame.apply(handle_row, axis=1)
team_schedules = pd.DataFrame(teams_and_opponents)

schedule = team_schedules.merge(rmsa_ratings, left_on='opponentShortName', right_on='team')
# build a dictionary for lookup of each team and their rating
teams_and_ratings = schedule[['opponentName', 'rank']].drop_duplicates()
rmsa_ratings_dict = {}
for i in teams_and_ratings.index:
    row = teams_and_ratings.loc[i, :]
    rmsa_ratings_dict[row['opponentName']] = row['rank']

rmsa_schedule = balance_schedule(team_schedules, rmsa_ratings, 15)

map_score_schedule = balance_schedule(team_schedules, map_score_ratings, 5)

match_score_schedule = balance_schedule(team_schedules, match_score_ratings, 2)

table_schedule = balance_schedule(team_schedules, table_ratings, 2)

rmsa_avg = rmsa_ratings['rank'].mean()
target_rms_average = rmsa_avg * 4


def add_rmsa_sos(schedule_frame, rmsa_ratings_dict):
    sos = []
    for i in schedule_frame.index:
        row = schedule_frame.iloc[i, :]
        oppos = [row['doubleOpponent1'], row['doubleOpponent2'], row['doubleOpponent3'], row['doubleOpponent4']]
        ratings = [rmsa_ratings_dict[o] for o in oppos]
        sos.append(sum(ratings))
    schedule_frame['rmsa_sos'] = sos
    schedule_frame['rmsa_unbalanced'] = schedule_frame['rmsa_sos'] - target_rms_average
    return schedule_frame


map_score_schedule = add_rmsa_sos(map_score_schedule, rmsa_ratings_dict)
match_score_schedule = add_rmsa_sos(match_score_schedule, rmsa_ratings_dict)
table_schedule = add_rmsa_sos(table_schedule, rmsa_ratings_dict)



rmsa_schedule.to_csv('out/rmsa_schedule.csv', index=False)
map_score_schedule.to_csv('out/map_score_schedule.csv', index=False)
match_score_schedule.to_csv('out/match_score_schedule.csv', index=False)
table_schedule.to_csv('out/table_schedule.csv', index=False)


print('Schedule Balanced on RMSA')
print(rmsa_schedule)
print('Schedule Balanced on Map Score')
print(map_score_schedule)
print('Schedule Balanced on Match Score')
print(match_score_schedule)
print('Schedule Balanced on Table Placement')
print(table_schedule)
