import pandas as pd
from rmsa.team_rating import extract_X_Y, calculate_rmts
from rmsa.utils.constants import Maps

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

map_scores = pd.read_csv('results/scored_maps.csv')

map_scores = map_scores[map_scores['season'] == 2021]

map_scores_swapped = map_scores.copy(deep=True)
map_scores_swapped['team_one_score'] = map_scores['team_two_score']
map_scores_swapped['team_two_score'] = map_scores['team_one_score']
map_scores_swapped['team_one_name'] = map_scores['team_two_name']
map_scores_swapped['team_two_name'] = map_scores['team_one_name']

map_scores = pd.concat([map_scores_swapped, map_scores])

map_scores = map_scores.dropna()

teams = list(set(list(map_scores['team_one_name'].values) + list(map_scores['team_two_name'].values)))
teams = [str(p) for p in teams]
teams = sorted(teams)


# Everything above this line is identical to map_scores.py
# Calculate who will win a map based on the RMSA
def determine_predicted_winner(row):
    net_one_attack = row['rmsa attack_one'] - row['rmsa defend_two']
    net_two_attack = row['rmsa attack_two'] - row['rmsa defend_one']
    if net_one_attack > net_two_attack:
        return row['team_one_name']
    else:
        return row['team_two_name']


# Evaluate each game type for prediction results
def evaluate(test_rows, rmsa):
    # Select the columns necessary for rmsa for each team
    rmsa_for_join = rmsa[['team', 'rmsa attack', 'rmsa defend']]
    # Select the necessary columns from scored map results
    test_rows_for_join = test_rows[['match_id', 'game_number', 'map_winner', 'team_one_name', 'team_two_name']]
    # Merge RMSA with our scored maps
    merged = test_rows_for_join.merge(rmsa_for_join, left_on='team_one_name', right_on='team').merge(rmsa_for_join,
                                                                                                     left_on='team_two_name',
                                                                                                     right_on='team',
                                                                                                     suffixes=(
                                                                                                         '_one',
                                                                                                         '_two'))
    # Drop Duplicates
    merged = merged.drop_duplicates()
    # Predict the winner of each map
    merged['predicted_winner'] = merged.apply(determine_predicted_winner, axis=1)
    # Determine if the prediction is correct
    merged['correct_prediction'] = merged['map_winner'] == merged['predicted_winner']

    total_maps = merged.shape[0]
    correct_preds = merged['correct_prediction'].sum()

    # Calculate the percentage of correct predictions
    print('Correctly Predicted: {}/{} ({}%) Map results'.format(correct_preds, total_maps,
                                                                round(100 * correct_preds / total_maps, 3)))


# Pull out the map scores for the Summer Showdown
map_scores_for_test = map_scores[map_scores['match_date'] > '2021/06/24']
# Pull out the map scores for all maps prior to the Summer Showdown
map_scores = map_scores[map_scores['match_date'] <= '2021/06/24']

#
# Calculate Control RMSA
control = map_scores[map_scores['map_type'] == Maps.Control]
control_X, control_Y = extract_X_Y(control)
control_rmts = calculate_rmts(control_X, control_Y, Maps.Control)

# Calculate Escort RMSA
escort = map_scores[map_scores['map_type'] == Maps.Escort]
escort_X, escort_Y = extract_X_Y(escort)
escort_rmts = calculate_rmts(escort_X, escort_Y, Maps.Escort)

# Calculate Hybrid RMSA
hybrid = map_scores[map_scores['map_type'] == Maps.Hybrid]
hybrid_X, hybrid_Y = extract_X_Y(hybrid)
hybrid_rmts = calculate_rmts(hybrid_X, hybrid_Y, Maps.Hybrid)

# Calculate Assault RMSA
assault = map_scores[map_scores['map_type'] == Maps.Assault]
assault_X, assault_Y = extract_X_Y(assault)
assault_rmts = calculate_rmts(assault_X, assault_Y, Maps.Assault)

# Calculate Correct prediction results for control
control_test = map_scores_for_test[map_scores_for_test['map_type'] == Maps.Control]
print('Control Evaluation')
evaluate(control_test, control_rmts)

# Calculate Correct prediction results for assault
assault_test = map_scores_for_test[map_scores_for_test['map_type'] == Maps.Assault]
print('Assault Evaluation')
evaluate(assault_test, assault_rmts)

# Calculate Correct prediction results for hybrid
hybrid_test = map_scores_for_test[map_scores_for_test['map_type'] == Maps.Hybrid]
print('Hybrid Evaluation')
evaluate(hybrid_test, hybrid_rmts)

# Calculate Correct prediction results for escort
escort_test = map_scores_for_test[map_scores_for_test['map_type'] == Maps.Escort]
print('Escort Evaluation')
evaluate(escort_test, escort_rmts)


##### Determine Match Winners

# Based on the first three maps of the series, determine the game type order (it rotates each week)
def determine_missing_maps(map_type_list):
    map_types = [Maps.Escort, Maps.Hybrid, Maps.Assault]
    map_5 = Maps.Control
    if len(map_type_list) >= 5:
        return map_type_list
    elif len(map_type_list) == 4:
        return map_type_list + [map_5]
    else:
        missing = list(set(map_types) - set(map_type_list))[0]
        return map_type_list + [missing, map_5]


# Determine the winner, predicted winner, and how many maps each team was predicted to win in each match
def evaluate_match(group):
    group_relevant = group[['game_number', 'map_type', 'map_winner', 'team_one_name', 'team_two_name']] \
        .drop_duplicates() \
        .sort_values(by="game_number").groupby(by='game_number').head(1).reset_index()

    team_one = group_relevant['team_one_name'].values[0]
    team_two = group_relevant['team_two_name'].values[0]

    # get the number of map wins each team actually got
    team_one_wins = group_relevant[group_relevant['map_winner'] == team_one].shape[0]
    team_two_wins = group_relevant[group_relevant['map_winner'] == team_two].shape[0]

    # determine the actual match winner
    if team_two_wins > team_one_wins:
        match_winner = team_two
    if team_one_wins > team_two_wins:
        match_winner = team_one

    # generate the map order
    map_order = list(group_relevant['map_type'].values)
    map_order = determine_missing_maps(map_order)

    # initialize each team to have 0 projected wins
    team_one_projected_wins = 0
    team_two_projected_wins = 0

    # iterate over the game mode order, determine the expected winner of the game mode, increment wins, and continue
    # until one team reaches 3 wins
    for map_type in map_order:
        team_one_attack = rmsa[map_type][team_one]['attack']
        team_one_defend = rmsa[map_type][team_one]['defend']
        team_two_attack = rmsa[map_type][team_two]['attack']
        team_two_defend = rmsa[map_type][team_two]['defend']

        # estimate the map score for each team on the map
        team_one_attack_expected = team_one_attack - team_two_defend
        team_two_attack_expected = team_two_attack - team_one_defend

        # use estimated map score to determine the map winner
        if team_one_attack_expected > team_two_attack_expected:
            team_one_projected_wins += 1
        else:
            team_two_projected_wins += 1

        # break once a team reaches 3 map wins
        if team_one_projected_wins >= 3:
            projected_winner = team_one
            break

        if team_two_projected_wins >= 3:
            projected_winner = team_two
            break

    # return an estimated match result
    return pd.Series({
        'team_one': team_one,
        'team_two': team_two,
        'match_winner': match_winner,
        'team_one_map_wins': team_one_wins,
        'team_two_map_wins': team_two_wins,
        'net_wins': team_one_wins - team_two_wins,
        'projected_winner': projected_winner,
        'team_one_projected_wins': team_one_projected_wins,
        'team_two_projected_wins': team_two_projected_wins,
        'projected_net_wins': team_one_projected_wins - team_two_projected_wins
    })


# Build a dictionary for RMSA
rmsa = {
    Maps.Control: {},
    Maps.Assault: {},
    Maps.Escort: {},
    Maps.Hybrid: {}
}

# Add control RMSA to the dictionary
for index in control_rmts.index:
    row = control_rmts.iloc[index]
    rmsa[Maps.Control][row['team']] = {'attack': row['rmsa attack'], 'defend': row['rmsa defend']}

# Add Assault RMSA to the dictionary
for index in assault_rmts.index:
    row = assault_rmts.iloc[index]
    rmsa[Maps.Assault][row['team']] = {'attack': row['rmsa attack'], 'defend': row['rmsa defend']}

# Add Escort RMSA to the dictionary
for index in escort_rmts.index:
    row = escort_rmts.iloc[index]
    rmsa[Maps.Escort][row['team']] = {'attack': row['rmsa attack'], 'defend': row['rmsa defend']}

# Add Hybrid RMSA to the dictionary
for index in hybrid_rmts.index:
    row = hybrid_rmts.iloc[index]
    rmsa[Maps.Hybrid][row['team']] = {'attack': row['rmsa attack'], 'defend': row['rmsa defend']}

# Apply our evaluation method to the season maps
evaluation = map_scores_for_test.groupby(by='match_id').apply(evaluate_match).reset_index()
# Add a boolean column to determine if the match winner was predicted correctly
evaluation['correct_match_prediction'] = evaluation['match_winner'] == evaluation['projected_winner']
correct = evaluation['correct_match_prediction'].sum()
print('The model correctly predicted {} out of {} matches ({}%)'.format(correct, evaluation.shape[0],
                                                                        round(correct / evaluation.shape[0], 3)))

# Add a boolean column to determine if the final score of the match was predicted correctly
evaluation['correct_exact_prediction'] = evaluation['net_wins'] == evaluation['projected_net_wins']
exect_correct = evaluation['correct_exact_prediction'].sum()
print('The model correctly predicted {} out of {} matches exactly ({}%)'.format(exect_correct, evaluation.shape[0],
                                                                                round(
                                                                                    exect_correct / evaluation.shape[0],
                                                                                    3)))

# Filter out the tournament matches and knockouts
qualifiers_only = evaluation[evaluation['match_id'] <= 37330]

# Build a dataframe of the double point matches
double_points = [
    {
        'match_id': 37307,
        'multiplier': 2
    },
    {
        'match_id': 37327,
        'multiplier': 2
    },
    {
        'match_id': 37299,
        'multiplier': 2
    },
    {
        'match_id': 37321,
        'multiplier': 2
    },
    {
        'match_id': 37294,
        'multiplier': 2
    },
    {
        'match_id': 37317,
        'multiplier': 2
    }
]
double_points = pd.DataFrame(double_points)

# Merge the double point matches into our evaluation dataframe
qualifiers_only = qualifiers_only.merge(double_points, on='match_id', how='outer')
# fill all non double point matches with 1.0
qualifiers_only = qualifiers_only.fillna(1.0)

correct = qualifiers_only['correct_match_prediction'].sum()
print('The model correctly predicted {} out of {} qualifier matches ({}%)'.format(correct, qualifiers_only.shape[0],
                                                                                  round(correct / qualifiers_only.shape[
                                                                                      0], 3)))

exect_correct = qualifiers_only['correct_exact_prediction'].sum()
print('The model correctly predicted {} out of {} qualifier matches exactly ({}%)'.format(exect_correct,
                                                                                          qualifiers_only.shape[0],
                                                                                          round(exect_correct /
                                                                                                qualifiers_only.shape[
                                                                                                    0], 3)))

# Calculate how many points the model would have gotten if entered into the pickem challenge
qualifiers_only['approximate_pickem_points'] = (2 * qualifiers_only['correct_match_prediction'] + qualifiers_only[
    'correct_exact_prediction']) * qualifiers_only['multiplier']

print('The model would have scored {} points if entered into the pickem challenge (qualifiers only)'.format(
    qualifiers_only['approximate_pickem_points'].sum()))
