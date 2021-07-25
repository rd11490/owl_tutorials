import pandas as pd
import numpy as np
from sklearn.linear_model import RidgeCV
from sklearn import metrics

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

    attack_str = '{0} rmsa attack'.format(map_type)
    defend_str = '{0} rmsa defend'.format(map_type)

    rmts.columns = ['team', attack_str, defend_str]
    rmts[attack_str] = rmts[attack_str].astype(float)
    rmts[defend_str] = rmts[defend_str].astype(float)

    rmts['{} rmsa'.format(map_type)] = rmts[attack_str] + rmts[defend_str]
    rmts['{} intercept'.format(map_type)] = intercept

    print('r^2: ', model.score(stint_X_rows, stint_Y_rows))
    print('lambda: ', alpha_to_lambda(model.alpha_, stint_X_rows.shape[0]))
    print('intercept: ', intercept)

    pred = model.predict(stint_X_rows)
    print('MAE: ', metrics.mean_absolute_error(stint_Y_rows, pred))
    print('RME: ', metrics.mean_squared_error(stint_Y_rows, pred))

    # residuals = stint_Y_rows - pred
    # scalar = 1/(stint_X_rows.shape[0] - stint_X_rows.shape[1] - 1)
    # weights = np.ones(shape=(stint_X_rows.shape[0], 1))
    # idmat = np.eye(stint_X_rows.shape[1])
    # mult = np.matmul(np.transpose(stint_X_rows), weights)
    # important_part = np.linalg.inv(mult + idmat)
    # errors = np.matmul(np.transpose(residuals), residuals)
    # variance = errors * important_part * scalar
    # stdev_o = []
    # stdev_d = []
    # for i in range(0, 20):
    #     var_o = 1.96 * np.sqrt(variance[i][i])
    #     var_d = 1.96 * np.sqrt(variance[20 + i][20 +i])
    #
    #     stdev_o.append(var_o)
    #     stdev_d.append(var_d)
    #
    #
    # attack_str_var = attack_str + ' stdev'
    # defend_str_var = defend_str + ' stdev'
    #
    # rmts[attack_str_var] = stdev_o
    # rmts[defend_str_var] = stdev_d




    rmts = rmts.sort_values(by='{} rmsa'.format(map_type), ascending=False)
    print(rmts.head(1000))
    return rmts


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

merged = control_rmts.merge(escort_rmts, on='team').merge(hybrid_rmts, on='team').merge(assault_rmts, on='team')

merged['Total Rating'] = (merged['Control rmsa'] * 2) + merged['Escort rmsa'] + merged['Hybrid rmsa'] + merged[
    'Assault rmsa']
merged = merged.round(3)
print(merged)

ratings = merged[['team', 'Total Rating']]
ratings = ratings.sort_values(by='Total Rating', ascending=False)
ratings['rank'] = ratings['Total Rating'].rank(ascending=False)
print(ratings)

merged.to_csv('./results/rmsa.csv', index=False)
