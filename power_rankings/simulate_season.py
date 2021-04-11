import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Manually setup Elo array
elos = [
    { 'team': 'ATL', 'elo': 1500 },
    { 'team': 'BOS', 'elo': 1500 },
    { 'team': 'CDH', 'elo': 1500 },
    { 'team': 'DAL', 'elo': 1500 },
    { 'team': 'FLA', 'elo': 1500 },
    { 'team': 'GLA', 'elo': 1500 },
    { 'team': 'GZC', 'elo': 1500 },
    { 'team': 'HOU', 'elo': 1500 },
    { 'team': 'HZS', 'elo': 1500 },
    { 'team': 'LDN', 'elo': 1500 },
    { 'team': 'NYE', 'elo': 1500 },
    { 'team': 'PAR', 'elo': 1500 },
    { 'team': 'PHI', 'elo': 1500 },
    { 'team': 'SEO', 'elo': 1500 },
    { 'team': 'SFS', 'elo': 1500 },
    { 'team': 'SHD', 'elo': 1500 },
    { 'team': 'TOR', 'elo': 1500 },
    { 'team': 'VAL', 'elo': 1500 },
    { 'team': 'VAN', 'elo': 1500 },
    { 'team': 'WAS', 'elo': 1500 }
]

# Turn elo array into a dataframe
elo_frame = pd.DataFrame(elos)


# Caculate probabilty of a team winning based on the two team's elo values
def calulate_match_odds(elo1, elo2):
    r1 = 10 ** (elo1 / 400)
    r2 = 10 ** (elo2 / 400)
    e1 = r1 / (r1 + r2)

    return e1



# Read the season schedule
season = pd.read_csv('./data/2021_league_schedule.csv')


# Merge the season with the elo frame so that we have a column for team1's elo and team2's elo
season = season.merge(elo_frame, left_on='team1ShortName', right_on='team').rename(columns={'elo':'team1Elo'}).drop(columns=['team']).merge(elo_frame, left_on='team2ShortName', right_on='team').rename(columns={'elo':'team2Elo'}).drop(columns=['team'])

# Calculate the probability that team 1 will win based on elo
season['team1WinProbability'] = calulate_match_odds(season['team1Elo'], season['team2Elo'])


# Reduce the columns to just the two team names and the probability that team 1 will win
season_for_sim = season[['team1Name', 'team2Name', 'team1WinProbability']]


# Function to simulate a season
def simulate_season(frame_for_sim):
    # rng roll for each match. The winner of each match is determined by the roll value and the probabilty that team 1 will win
    frame_for_sim['rng'] = np.random.random(size=len(frame_for_sim))
    frame_for_sim['team1Win'] = (frame_for_sim['rng'] <= frame_for_sim['team1WinProbability']).astype('int')
    frame_for_sim['team2Win'] = (frame_for_sim['rng'] > frame_for_sim['team1WinProbability']).astype('int')

    # The wins for each team are then aggregated and returned
    aggs1 = frame_for_sim[['team1Name', 'team1Win']].groupby('team1Name').sum().reset_index()
    aggs1.columns = ['Team', 'Wins']
    aggs2 = frame_for_sim[['team2Name', 'team2Win']].groupby('team2Name').sum().reset_index()
    aggs2.columns = ['Team', 'Wins']
    aggs = pd.concat([aggs1, aggs2]).groupby('Team').sum().reset_index()
    return aggs


def simulate_seasons(frame_for_sim, n):

    sims = []

    for sim in range(0, n):
        aggs = simulate_season(frame_for_sim.copy())
        aggs['sim'] = sim
        sims.append(aggs)
        print(aggs)

    sims_frame = pd.concat(sims)
    season_stats = sims_frame[['Team', 'Wins']].groupby('Team').describe().reset_index()
    season_stats = season_stats.sort_values(by=[('Wins','mean')], ascending=False)
    print(season_stats)


simulate_seasons(season_for_sim,10)



