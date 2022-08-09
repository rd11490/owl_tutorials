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

for clusters in range(3, 11):
    kmeans = KMeans(n_clusters=clusters, random_state=0)
    kmeans.fit(X)
    labels = kmeans.labels_

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

    print(f'With {clusters} clusters the main comps are:')
    print(comps_df)

    print('\n')




