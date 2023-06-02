from strength_of_schedule_2023_part_2.constants import Maps
import numpy as np

def build_rmsa_map(rmsa_frame):
    rmsa = {
        Maps.Control: {},
        Maps.Hybrid: {},
        Maps.Escort: {},
        Maps.Assault: {},
        Maps.Push: {}
    }
    for index in rmsa_frame.index:
        row = rmsa_frame.iloc[index]
        rmsa[row['map_type']][row['team']] = {'attack': row['rmsa attack'], 'attack stdev': row['rmsa attack stdev'],
                                              'defend': row['rmsa defend'], 'defend stdev': row['rmsa defend stdev']}
    return rmsa

def average_rmsa(rmsa, team, map_type, stat):
    stat_value = 0
    map_types = [m for m in [Maps.Control, Maps.Escort, Maps.Hybrid, Maps.Push] if m != map_type]
    for mt in map_types:
        stat_value += rmsa[mt][team][stat]
    return stat_value/3

def get_rmsa_from_map(rmsa, map_type, team):
    team_one_attack = rmsa[map_type][team]['attack']
    team_one_attack_stdev = rmsa[map_type][team]['attack stdev']
    team_one_defend = rmsa[map_type][team]['defend']
    team_one_defend_stdev = rmsa[map_type][team]['defend stdev']

    if (team_one_attack == 0) and (team_one_attack_stdev == 0) and (team_one_defend == 0) and (team_one_defend_stdev == 0):
        return average_rmsa(rmsa, team, map_type, 'attack'), average_rmsa(rmsa, team, map_type, 'attack stdev'), average_rmsa(rmsa, team, map_type, 'defend'), average_rmsa(rmsa, team, map_type, 'defend stdev')
    return team_one_attack, team_one_attack_stdev, team_one_defend, team_one_defend_stdev


def predict_match(team_one, team_two, map_order, rmsa, maps_to_win=3):
    # initialize each team to have 0 projected wins
    team_one_projected_wins = 0
    team_two_projected_wins = 0

    projected_winner = None
    loser = None

    # iterate over the game mode order, determine the expected winner of the game mode, increment wins, and continue
    # until one team reaches 3 wins
    for map_type in map_order:
        team_one_attack, team_one_attack_stdev, team_one_defend, team_one_defend_stdev = get_rmsa_from_map(rmsa, map_type, team_one)
        team_two_attack, team_two_attack_stdev, team_two_defend, team_two_defend_stdev = get_rmsa_from_map(rmsa, map_type, team_two)

        team_one_attack_estimate = np.random.normal(team_one_attack, team_one_attack_stdev)
        team_one_defend_estimate = np.random.normal(team_one_defend, team_one_defend_stdev)

        team_two_attack_estimate = np.random.normal(team_two_attack, team_two_attack_stdev)
        team_two_defend_estimate = np.random.normal(team_two_defend, team_two_defend_stdev)

        # estimate the map score for each team on the map
        team_one_attack_expected = team_one_attack_estimate - team_two_defend_estimate
        team_two_attack_expected = team_two_attack_estimate - team_one_defend_estimate

        # use estimated map score to determine the map winner
        if team_one_attack_expected > team_two_attack_expected:
            team_one_projected_wins += 1
        else:
            team_two_projected_wins += 1

        # break once a team reaches 3 map wins
        if team_one_projected_wins >= maps_to_win:
            projected_winner = team_one
            loser = team_two
            break

        if team_two_projected_wins >= maps_to_win:
            projected_winner = team_two
            loser = team_one
            break
    return {
        'team_one': team_one,
        'team_one_map_wins': team_one_projected_wins,
        'team_two': team_two,
        'team_two_map_wins': team_two_projected_wins,
        'winner': projected_winner,
        'loser': loser
    }
