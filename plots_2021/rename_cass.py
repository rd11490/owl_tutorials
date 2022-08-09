import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

heroes = pd.read_csv('./player_data/hero_data.csv')

heroes.loc[heroes['hero_name'] == 'McCree', 'hero_name'] = 'Cassidy'

heroes.to_csv('./player_data/hero_data_clean.csv', index=False)

