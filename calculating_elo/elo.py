import pandas as pd
import datetime
from calculating_elo.maps import Maps


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# determine the game mode from map
def calc_game_mode(map_name):
    return Maps.game_mode[map_name]


# determine the season of the match
def calc_season(dt):
    parsed = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return parsed.date().strftime("%Y")

# Read in the csv
frame = pd.read_csv('map_data/match_map_stats.csv')


# Remove all star matches
frame = frame[frame['stage'].str.contains('All-Stars') == False]

# add the game mode, date, and season to the frame
frame['game_mode'] = frame['map_name'].apply(calc_game_mode)
frame['season'] = frame['round_end_time'].apply(calc_season)

# separate the frame into the different game modes
escort_maps = frame[frame['game_mode'] == Maps.Escort].copy()
assault_maps = frame[frame['game_mode'] == Maps.Assault].copy()
control_maps = frame[frame['game_mode'] == Maps.Control].copy()
hybrid_maps = frame[frame['game_mode'] == Maps.Hybrid].copy()

# select the columns we care about
escort_maps = escort_maps[['map_winner','team_one_name', 'team_two_name', 'season']].drop_duplicates()

assault_maps = assault_maps[['map_winner','team_one_name', 'team_two_name', 'season']].drop_duplicates()

hybrid_maps = hybrid_maps[['map_winner','team_one_name', 'team_two_name', 'season']].drop_duplicates()

control_maps = control_maps[['map_winner','team_one_name', 'team_two_name', 'season']].drop_duplicates()



# Update elo function
# Elo is updated in the form of RA' = RA + K(Sa - Ea)
# where:
#   RA' is the new elo
#   RA is thte current elo
#   K is the update factor, or the maximum you can move after a win/loss
#   Sa is the actual score of the map (1 for a win, .5 for a draw, 0 for a loss)
#   Ea is the expected score of the maP
#
# Ea is calculated in the form of q1/(q1 + q2)
# where:
#   qn is calculated as 10 ^ (Rn/400)

m = 500
initial_elo = 2500
k = 50
decay = .5

def update_elo(elo, winner, team1, team2):
    elo1 = elo[team1][-1]
    elo2 = elo[team2][-1]

    q1 = 10 ** (elo1 / m)
    q2 = 10 ** (elo2 / m)
    e1 = q1 / (q1 + q2)
    e2 = q2 / (q1 + q2)

    if winner == 'draw':
        s1 = 0.5
        s2 = 0.5
    elif winner == team1:
        s1 = 1.0
        s2 = 0.0
    else:
        s1 = 0.0
        s2 = 1.0

    elo[team1].append(elo1 + k * (s1-e1))
    elo[team2].append(elo2 + k * (s2-e2))
    return elo


# Take the difference between the current elo and 2500, reduce it by 50%, and adjust elo by that value.
# The idea is that between each season we want to regress each teams elo back towards neutral.
def decay_elo(teams_elo):
    new_elo = {}
    for team, elo in teams_elo.items():
        diff = teams_elo[team][-1] - initial_elo
        regress = diff * decay
        elo.append(elo[-1] - regress)
        new_elo[team] = elo
    return new_elo


def calculate_elo(match_frame):
    # Initialize the elo dictionary, set each team to 2500
    elo = {}
    for team in frame['team_one_name'].unique():
        elo[team] = [initial_elo]

    # storing the current season will allow us to determine when the season changes
    curr_season = match_frame.loc[match_frame.index[0], :]['season']
    # iterate over every row in the index
    for i in match_frame.index:
        # If the season changes we want to decay every team's elo back towards 2500 and reset the current season
        if match_frame.loc[i, :]['season'] != curr_season:
            elo = decay_elo(elo)
            curr_season = match_frame.loc[i, :]['season']

        # update each team's elo with the result of the map
        elo = update_elo(elo, match_frame.loc[i, :]['map_winner'], match_frame.loc[i, :]['team_one_name'],
                   match_frame.loc[i, :]['team_two_name'])
    return elo

# build a dataframe of the final Elo for each team and print
def print_standings(elo):
    print(pd.DataFrame([{'Team': k, 'Elo': round(v[-1], 2)} for k, v in elo.items()]).sort_values(by='Elo', ascending=False))


escort_elo_history = calculate_elo(escort_maps)
print('ESCORT MAP ELO')
print_standings(escort_elo_history)
print('\n')


control_elo_history = calculate_elo(control_maps)
print('CONTROL MAP ELO')
print_standings(control_elo_history)
print('\n')


assault_elo_history = calculate_elo(assault_maps)
print('ASSAULT MAP ELO')
print_standings(assault_elo_history)
print('\n')


hybrid_elo_history = calculate_elo(hybrid_maps)
print('HYBRID MAP ELO')
print_standings(hybrid_elo_history)
print('\n')


