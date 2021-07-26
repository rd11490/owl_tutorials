import pandas as pd
import numpy as np
from sklearn.linear_model import RidgeCV

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


def map_teams(row_in, teams):
    t1 = row_in[0]
    t2 = row_in[1]

    row_out = np.zeros([len(teams) * 2])

    row_out[teams.index(t1)] = 1
    row_out[teams.index(t2) + len(teams)] = -1
    return row_out


def extract_X_Y(frame):
    stints_x_base = frame[['team_one_name', 'team_two_name']].values

    stint_X_rows = np.apply_along_axis(map_teams, 1, stints_x_base, teams)

    stint_Y_rows = frame[['team_one_score']].values
    return stint_X_rows, stint_Y_rows


# Convert lambda value to alpha needed for ridge CV
def lambda_to_alpha(lambda_value, samples):
    return (lambda_value * samples) / 2.0


# Convert RidgeCV alpha back into a lambda value
def alpha_to_lambda(alpha_value, samples):
    return (alpha_value * 2.0) / samples


def calculate_rmts(stint_X_rows, stint_Y_rows, map_type):
    lambdas = [.01, 0.025, .05, 0.075, .1, .125, .15, .175, .2, .225, .25]

    alphas = [lambda_to_alpha(l, stint_X_rows.shape[0]) for l in lambdas]

    clf = RidgeCV(alphas=alphas, cv=5, fit_intercept=True, normalize=False)

    model = clf.fit(stint_X_rows, stint_Y_rows)

    team_arr = np.transpose(np.array(teams).reshape(1, len(teams)))
    coef_array_attack = np.transpose(model.coef_[:, 0:len(teams)])
    coef_array_def = np.transpose(model.coef_[:, len(teams):])

    team_coef_arr = np.concatenate([team_arr, coef_array_attack, coef_array_def], axis=1)

    # build a dataframe from our matrix
    rmts = pd.DataFrame(team_coef_arr)
    intercept = model.intercept_[0]

    attack_str = 'rmsa attack'
    defend_str = 'rmsa defend'

    rmts.columns = ['team', attack_str, defend_str]
    rmts[attack_str] = rmts[attack_str].astype(float)
    rmts[defend_str] = rmts[defend_str].astype(float)

    rmts['{} rmsa'.format(map_type)] = rmts[attack_str] + rmts[defend_str]
    rmts['{} intercept'.format(map_type)] = intercept

    return rmts

def determine_predicted_winner(row):
    net_one_attack = row['rmsa attack_one'] - row['rmsa defend_two']
    net_two_attack = row['rmsa attack_two'] - row['rmsa defend_one']
    if net_one_attack > net_two_attack:
        return row['team_one_name']
    else:
        return row['team_two_name']


def evaluate(test_rows, rmsa):
    rmsa_for_join = rmsa[['team', 'rmsa attack', 'rmsa defend']]
    test_rows_for_join = test_rows[['match_id', 'game_number', 'map_winner', 'team_one_name', 'team_two_name']]
    merged = test_rows_for_join.merge(rmsa_for_join, left_on='team_one_name', right_on='team').merge(rmsa_for_join, left_on='team_two_name', right_on='team', suffixes=('_one', '_two'))
    merged = merged.drop_duplicates()
    merged['predicted_winner'] = merged.apply(determine_predicted_winner, axis=1)
    merged['correct_prediction'] = merged['map_winner'] == merged['predicted_winner']

    total_maps = merged.shape[0]
    correct_preds = merged['correct_prediction'].sum()

    print('Correctly Predicted: {}/{} ({}%) Map results'.format(correct_preds, total_maps, round(100*correct_preds/total_maps,3)))


map_scores_for_test = map_scores[map_scores['match_date'] > '2021/06/24']
map_scores = map_scores[map_scores['match_date'] <= '2021/06/24']

control = map_scores[map_scores['map_type'] == Maps.Control]
control_X, control_Y = extract_X_Y(control)
control_rmts = calculate_rmts(control_X, control_Y, Maps.Control)

escort = map_scores[map_scores['map_type'] == Maps.Escort]
escort_X, escort_Y = extract_X_Y(escort)
escort_rmts = calculate_rmts(escort_X, escort_Y, Maps.Escort)

hybrid = map_scores[map_scores['map_type'] == Maps.Hybrid]
hybrid_X, hybrid_Y = extract_X_Y(hybrid)
hybrid_rmts = calculate_rmts(hybrid_X, hybrid_Y, Maps.Hybrid)

assault = map_scores[map_scores['map_type'] == Maps.Assault]
assault_X, assault_Y = extract_X_Y(assault)
assault_rmts = calculate_rmts(assault_X, assault_Y, Maps.Assault)


control_test = map_scores_for_test[map_scores_for_test['map_type'] == Maps.Control]
print('Control Evaluation')
evaluate(control_test, control_rmts)


assault_test = map_scores_for_test[map_scores_for_test['map_type'] == Maps.Assault]
print('Assault Evaluation')
evaluate(assault_test, assault_rmts)

hybrid_test = map_scores_for_test[map_scores_for_test['map_type'] == Maps.Hybrid]
print('Hybrid Evaluation')
evaluate(hybrid_test, hybrid_rmts)

escort_test = map_scores_for_test[map_scores_for_test['map_type'] == Maps.Escort]
print('Escort Evaluation')
evaluate(escort_test, escort_rmts)



