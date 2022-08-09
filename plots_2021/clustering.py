import pandas as pd
import datetime
from sklearn.cluster import KMeans

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

heroes = pd.read_csv('./player_data/hero_data_clean.csv')

def calc_match_date(dt):
    parsed = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return parsed.date().strftime("%Y/%m/%d")


def determine_stage(date):
    if date < '2021/05/15':
        return 'May Melee'
    elif '2021/05/15' < date < '2021/06/20':
        return 'June Joust'
    elif '2021/06/20' < date < '2021/07/25':
        return 'Summer Showdown'
    elif '2021/07/25' < date < '2021/08/25':
        return 'Countdown Cup'
    else:
        return 'Playoffs'


heroes['match_date'] = heroes['start_time'].apply(calc_match_date)
heroes['stage'] = heroes['match_date'].apply(determine_stage)

interesting_stats = ['Time Played']

heroes_care = heroes[heroes['stat_name'].isin(interesting_stats)]
hero_sums = heroes_care[['team_name', 'hero_name', 'esports_match_id', 'stage', 'map_name', 'stat_amount']].groupby(
    by=['team_name', 'hero_name', 'stage', 'map_name', 'esports_match_id']).sum().reset_index()


def calculate_play_percent(group):
    group['Percent Played'] = 6 * 100 * group['stat_amount'] / group['stat_amount'].sum()
    return group


hero_sums = hero_sums.groupby(by=['team_name', 'esports_match_id', 'map_name', 'stage']).apply(calculate_play_percent)

hero_sums = hero_sums.pivot(index=['team_name', 'esports_match_id', 'map_name', 'stage'], columns='hero_name', values='Percent Played').fillna(
    0.0).reset_index()
hero_sums['Label'] = hero_sums['team_name'] + '-' + hero_sums['stage'] + '-' + hero_sums['map_name'] + '-' + hero_sums['esports_match_id'].astype(str)
hero_pct_np = hero_sums.to_numpy()
X = hero_pct_np[:, 4:-1]
Y_label = hero_pct_np[:, -1]

clusters = 8
kmeans = KMeans(n_clusters=clusters, random_state=0)
kmeans.fit(X)
labels = kmeans.labels_
df = pd.DataFrame({'Team': Y_label, 'Classification': labels})
print(df)

def split_label(row):
    row['Team Name'] = row['Team'].split('-')[0]
    row['Map Name'] = row['Team'].split('-')[2]
    row['Match Id'] = int(row['Team'].split('-')[3])
    return row

df = df.apply(split_label, axis=1)
df = df[['Team Name', 'Match Id', 'Map Name', 'Classification']]



centers = pd.DataFrame(kmeans.cluster_centers_)
centers.columns = hero_sums.columns[4:-1]
centers = centers.round(2)
centers['Label'] = [i for i in range(0, clusters)]

comps = []

for ind in centers.index:
    row = centers.iloc[ind, :]
    comp = ','.join(row[row>50].index.tolist())
    comps.append({'Label': comp, "Cluster": row['Label']})

comps_df = pd.DataFrame(comps)
comps_df.to_csv('out/comps_list.csv', index=False)


heroes_with_cluster = heroes.merge(df, left_on=['team_name', 'esports_match_id', 'map_name'], right_on=['Team Name', 'Match Id', 'Map Name'])
heroes_with_cluster = heroes_with_cluster[['map_type', 'map_name', 'player_name', 'stat_name', 'hero_name', 'stat_amount', 'match_date', 'stage', 'Team Name', 'Match Id', 'Classification']]
heroes_with_cluster.columns = ['Map Type', 'Map Name', 'Player', 'Stat', 'Hero', 'Amount', 'Match Date', 'Stage', 'Team Name', 'Match Id', 'Classification']

heroes_with_cluster.to_csv('out/hero_data_bk.csv', index=False)

heroes_with_cluster[['Team Name', 'Player']].drop_duplicates().to_csv('out/teams_players.csv', index=False)
heroes_with_cluster[['Stat']].drop_duplicates().to_csv('out/stats.csv', index=False)
heroes_with_cluster[['Stage']].drop_duplicates().to_csv('out/stage.csv', index=False)
heroes_with_cluster[['Hero']].drop_duplicates().to_csv('out/heroes.csv', index=False)
heroes_with_cluster[['Map Type']].drop_duplicates().to_csv('out/map_types.csv', index=False)
heroes_with_cluster[['Map Name']].drop_duplicates().to_csv('out/map_names.csv', index=False)






