import pandas as pd
from strength_of_schedule.constants import Teams
from strength_of_schedule.rmsa import calculate_rmsa

# Pandas options for better printing
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

# Read in our scored maps generated in the map_score script
map_scores_df = pd.read_csv('data/scored_maps.csv')

# Limit our results to 2021 maps
map_scores_df = map_scores_df[map_scores_df['season'] == 2021]

# Duplicate and mirror our map scores so that we can get a row for each team on attack and defense on each map
map_scores_swapped_df = map_scores_df.copy(deep=True)
map_scores_swapped_df['team_one_score'] = map_scores_df['team_two_score']
map_scores_swapped_df['team_two_score'] = map_scores_df['team_one_score']
map_scores_swapped_df['team_one_name'] = map_scores_df['team_two_name']
map_scores_swapped_df['team_two_name'] = map_scores_df['team_one_name']
map_scores_df = pd.concat([map_scores_swapped_df, map_scores_df])
map_scores_df = map_scores_df.dropna()

# Generate a list of teams
teams = list(set(list(map_scores_df['team_one_name'].values) + list(map_scores_df['team_two_name'].values)))
teams = [str(p) for p in teams]
teams = sorted(teams)

# Array of RMSA dataframes
total_rmsa_team_dropped = []

# Calculate RMSA with the entire schedule
raw_rmsa = calculate_rmsa(map_scores_df, teams)
print(raw_rmsa)

# iterate over each team
for team in Teams.East + Teams.West:
    # Remove all maps involving the current team.
    map_scores = map_scores_df[(map_scores_df['team_one_name'] != team) & (map_scores_df['team_two_name'] != team)]
    # Calculate Total RMSA for a league in which the current team does not exist
    total_rmsa = calculate_rmsa(map_scores, teams)
    total_rmsa['team dropped'] = team
    total_rmsa_team_dropped.append(total_rmsa)

# Convert them all into a single frame
rmsa_frame = pd.concat(total_rmsa_team_dropped)

playoff_dates = [
    # May Melee Knockouts and Tournament
    '2021-05-02',
    '2021-05-06',
    '2021-05-07',
    '2021-05-08',
    '2021-05-09',

    # June Joust Knockouts and Tournament
    '2021-06-06',
    '2021-06-10',
    '2021-06-11',
    '2021-06-12',
    '2021-06-13',

    # Summer Showdown Knockouts and Tournament
    '2021-07-11',
    '2021-07-12',
    '2021-07-15',
    '2021-07-16',
    '2021-07-17',
    '2021-07-18',

    # Countdown Cup Knockouts
    '2021-08-16',
    '2021-08-15'
]

# Read in the league schedule
schedule_frame = pd.read_csv('data/2021_league_schedule.csv')
# Filter out any playoff/knockout/tournament matches. We only want to calculate Strength of Schedule based on Regular Season Matches
schedule_frame = schedule_frame[schedule_frame['startDate'].isin(playoff_dates) == False]

# Create a dictionary where the teams are the key and the value is an empty array
schedule = {}
for t in Teams.East + Teams.West:
    schedule[t] = []

# Append each match to the dictionary
for i in schedule_frame.index:
    row = schedule_frame.loc[i, :]
    schedule[row['team1Name']].append(row['team2Name'])
    schedule[row['team2Name']].append(row['team1Name'])

sos = []
# Iterate over the teams again
for t in Teams.East + Teams.West:
    # Get the RMSA for each team when the current team was removed from the calculation
    rmsa_team_dropped = rmsa_frame[rmsa_frame['team dropped'] == t]
    schedule_arr = schedule[t]
    score = 0
    raw_score = 0
    # Iterate over the schedule and add the total rmsa for each team on the schedule
    for oppo in schedule_arr:
        score += rmsa_team_dropped[rmsa_team_dropped['team'] == oppo]['rmsa'].values[0]
        raw_score += raw_rmsa[raw_rmsa['team'] == oppo]['rmsa'].values[0]

    sos.append({'team': t, 'adjusted sos': score, 'raw sos': raw_score})

# Create a dataframe from the results, sort, rank and print
sos_df = pd.DataFrame(sos)
sos_df = sos_df.sort_values(by='adjusted sos', ascending=False)
sos_df['adjusted rank'] = sos_df['adjusted sos'].rank(ascending=False)
sos_df['raw rank'] = sos_df['raw sos'].rank(ascending=False)
sos_df = sos_df[['team', 'adjusted rank', 'adjusted sos', 'raw rank', 'raw sos']]
sos_df.to_csv('results/sos.csv', index=False)
rmsa_frame.to_csv('results/rmsa_sos.csv', index=False)
print(sos_df)
