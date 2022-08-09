import pandas as pd
import datetime
import random
from sklearn.ensemble import RandomForestClassifier

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

hero_sums = hero_sums.pivot(index=['team_name', 'esports_match_id', 'map_name', 'stage'], columns='hero_name',
                            values='Percent Played').fillna(
    0.0).reset_index()
hero_sums['Label'] = hero_sums['team_name'] + '-' + hero_sums['stage'] + '-' + hero_sums['map_name'] + '-' + hero_sums[
    'esports_match_id'].astype(str)
hero_pct_np = hero_sums.to_numpy()
X = hero_pct_np[:, 4:-1]
Y_label = hero_pct_np[:, -1]

inds = random.sample(list(hero_sums.index), 25)
for i in inds:
    print(i)
    print(hero_sums.loc[i, :])

# Classifications:
classifications = {
    0: 'Rush',
    1: 'Poke/Dive Hybrid',
    2: 'Double Bubble',
    3: 'Anti-Dive',
    4: 'Classic Dive',
    5: 'Double Shield',
    6: 'Talon Dive',

}
# # Manual entries
manual_class_inds = [59, 1338, 1540, 645, ]
ind_classifications = [1, 6, 1, 2, ]

# Preset entries:
presets = pd.DataFrame([
    {
        'label': 4,
        'Ana': 100,
        'D.Va': 100,
        'Brigitte': 100,
        'Winston': 100,
    },
    {
        'label': 2,
        'Ana': 100,
        'Zarya': 100,
        'Brigitte': 100,
        'Winston': 100,
    },
    {
        'label': 5,
        'Orisa': 100,
        'Sigma': 100,
        'Brigitte': 100,
        'Baptiste': 100,
    },
    {
        'label': 5,
        'Orisa': 100,
        'Sigma': 100,
        'Zenyatta': 100,
        'Baptiste': 100,
    },
    {
        'label': 6,
        'Winston': 100,
        'D.Va': 100,
        'Lúcio': 100,
        'Moira': 100,
    },
    {
        'label': 6,
        'Wrecking Ball': 100,
        'D.Va': 100,
        'Lúcio': 100,
        'Moira': 100,
    },
    {
        'label': 7,
        'Wrecking Ball': 100,
        'D.Va': 100,
        'Zenyatta': 100,
        'Brigitte': 100,
    },
    {
        'label': 1,
        'Wrecking Ball': 100,
        'Sigma': 100,
        'Zenyatta': 100,
        'Brigitte': 100,
    },
    {
        'label': 1,
        'Wrecking Ball': 100,
        'Sigma': 100,
        'Zenyatta': 100,
        'Mercy': 100,
    },
    {
        'label': 0,
        'Reinhardt': 100,
        'D.Va': 100,
        'Baptiste': 100,
        'Lúcio': 100,
    },
    {
        'label': 3,
        'Reinhardt': 100,
        'D.Va': 100,
        'Baptiste': 100,
        'Brigitte': 100,
    },
    {
        'label': 3,
        'Orisa': 100,
        'D.Va': 100,
        'Baptiste': 100,
        'Brigitte': 100,
    }
])

manual_classifications = hero_sums.iloc[manual_class_inds, 4:-1]
manual_classifications['label'] = ind_classifications
train = pd.concat([manual_classifications, presets]).fillna(0.0)

hero_pct_np = hero_sums.to_numpy()
X = hero_pct_np[:, 4:-1]
Y_label = hero_pct_np[:, -1]
