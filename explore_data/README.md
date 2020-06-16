## Investigating The Overwatch League Data

In this tutorial I will explore the different data provided by the Overwatch League.

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### 0.1 Requirements
The code in this tutorial was written in python 3.7 and uses the following libraries:
Pandas

The environment.yml page for the entire project contains everything you need to run this script.

### 1. Map Data

The first thing we are going to look at is the map data. Let's do a brief exploration of the data and find some very basic statistics on the different game modes.

The first thing we want to do is import pandas, disable warnings, and set the print options for pandas so that our data is more readable when printing to console.
```python
import warnings
warnings.simplefilter(action='ignore')

import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
```

Now we want to read in the data and see what we are working with

```python
# Read in our map stats data
map_data = pd.read_csv('data/match_map_stats.csv')

print(map_data.head(20))

# Print out our columns so we can see what we are looking at
print('Dataframe Columns')
for c in map_data.columns:
    print(c)

```

Running those lines of code we can see a sample of hte data provided. We will also print out the column names so that we have a reference for later
```
   round_start_time  round_end_time                       stage  match_id  game_number            match_winner              map_winner            map_loser          map_name  map_round  winning_team_final_map_score  losing_team_final_map_score control_round_name                attacker                defender           team_one_name           team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score
0    1/11/2018 0:12  1/11/2018 0:20  Overwatch League - Stage 1     10223            1     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock            Dorado          1                             3                            2                NaN     San Francisco Shock     Los Angeles Valiant     Los Angeles Valiant     San Francisco Shock                  75.615051                   0.000000              0.000000            240.000000                        NaN                        NaN                         2                         0
1    1/11/2018 0:22  1/11/2018 0:27  Overwatch League - Stage 1     10223            1     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock            Dorado          2                             3                            2                NaN     Los Angeles Valiant     San Francisco Shock     Los Angeles Valiant     San Francisco Shock                  75.649597                  75.615051            125.750572              0.000000                        NaN                        NaN                         3                         2
2    1/11/2018 0:34  1/11/2018 0:38  Overwatch League - Stage 1     10223            2     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock  Temple of Anubis          1                             4                            3                NaN     San Francisco Shock     Los Angeles Valiant     Los Angeles Valiant     San Francisco Shock                   0.000000                   0.000000            250.492004            240.000000                        NaN                        NaN                         2                         0
3    1/11/2018 0:40  1/11/2018 0:44  Overwatch League - Stage 1     10223            2     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock  Temple of Anubis          2                             4                            3                NaN     Los Angeles Valiant     San Francisco Shock     Los Angeles Valiant     San Francisco Shock                   0.000000                   0.000000            225.789032            250.492004                        NaN                        NaN                         2                         2
4    1/11/2018 0:46  1/11/2018 0:49  Overwatch League - Stage 1     10223            2     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock  Temple of Anubis          3                             4                            3                NaN     Los Angeles Valiant     San Francisco Shock     Los Angeles Valiant     San Francisco Shock                   0.000000                   0.000000             36.396057            250.492004                        NaN                        NaN                         4                         2
5    1/11/2018 0:51  1/11/2018 0:56  Overwatch League - Stage 1     10223            2     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock  Temple of Anubis          4                             4                            3                NaN     San Francisco Shock     Los Angeles Valiant     Los Angeles Valiant     San Francisco Shock                   0.000000                   0.000000              0.000000             36.396057                        NaN                        NaN                         3                         4
6    1/11/2018 1:11  1/11/2018 1:16  Overwatch League - Stage 1     10223            3     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock             Ilios          1                             2                            1         Lighthouse     Los Angeles Valiant     San Francisco Shock     Los Angeles Valiant     San Francisco Shock                   0.000000                   0.000000              0.000000              0.000000                       99.0                      100.0                         0                         1
7    1/11/2018 1:17  1/11/2018 1:20  Overwatch League - Stage 1     10223            3     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock             Ilios          2                             2                            1              Ruins     Los Angeles Valiant     San Francisco Shock     Los Angeles Valiant     San Francisco Shock                   0.000000                   0.000000              0.000000              0.000000                      100.0                        0.0                         1                         1
8    1/11/2018 1:20  1/11/2018 1:25  Overwatch League - Stage 1     10223            3     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock             Ilios          3                             2                            1               Well     Los Angeles Valiant     San Francisco Shock     Los Angeles Valiant     San Francisco Shock                   0.000000                   0.000000              0.000000              0.000000                      100.0                       65.0                         2                         1
9    1/11/2018 1:32  1/11/2018 1:39  Overwatch League - Stage 1     10223            4     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock           Numbani          1                             2                            1                NaN     San Francisco Shock     Los Angeles Valiant     Los Angeles Valiant     San Francisco Shock                  75.549507                   0.000000              0.000000              0.000000                        NaN                        NaN                         1                         0
10   1/11/2018 1:41  1/11/2018 1:45  Overwatch League - Stage 1     10223            4     Los Angeles Valiant     Los Angeles Valiant  San Francisco Shock           Numbani          3                             2                            1                NaN     Los Angeles Valiant     San Francisco Shock     Los Angeles Valiant     San Francisco Shock                  75.563667                  75.549507            165.840027              0.000000                        NaN                        NaN                         2                         1
11   1/11/2018 2:08  1/11/2018 2:13  Overwatch League - Stage 1     10224            1  Los Angeles Gladiators  Los Angeles Gladiators     Shanghai Dragons            Dorado          1                             1                            0                NaN        Shanghai Dragons  Los Angeles Gladiators  Los Angeles Gladiators        Shanghai Dragons                  70.161865                   0.000000              0.000000            240.000000                        NaN                        NaN                         0                         0
12   1/11/2018 2:15  1/11/2018 2:15  Overwatch League - Stage 1     10224            1  Los Angeles Gladiators  Los Angeles Gladiators     Shanghai Dragons            Dorado          2                             1                            0                NaN  Los Angeles Gladiators        Shanghai Dragons  Los Angeles Gladiators        Shanghai Dragons                  70.178932                  70.161865            186.312805              0.000000                        NaN                        NaN                         1                         0
13   1/11/2018 2:25  1/11/2018 2:34  Overwatch League - Stage 1     10224            2  Los Angeles Gladiators  Los Angeles Gladiators     Shanghai Dragons  Temple of Anubis          1                             2                            1                NaN        Shanghai Dragons  Los Angeles Gladiators  Los Angeles Gladiators        Shanghai Dragons                   0.000000                   0.000000              0.000000            240.000000                        NaN                        NaN                         1                         0
14   1/11/2018 2:36  1/11/2018 2:38  Overwatch League - Stage 1     10224            2  Los Angeles Gladiators  Los Angeles Gladiators     Shanghai Dragons  Temple of Anubis          2                             2                            1                NaN  Los Angeles Gladiators        Shanghai Dragons  Los Angeles Gladiators        Shanghai Dragons                   0.000000                   0.000000            356.864014              0.000000                        NaN                        NaN                         2                         1
15   1/11/2018 2:52  1/11/2018 2:58  Overwatch League - Stage 1     10224            3  Los Angeles Gladiators  Los Angeles Gladiators     Shanghai Dragons             Ilios          1                             2                            0               Well        Shanghai Dragons  Los Angeles Gladiators        Shanghai Dragons  Los Angeles Gladiators                   0.000000                   0.000000              0.000000              0.000000                       99.0                      100.0                         0                         1
16   1/11/2018 2:59  1/11/2018 3:03  Overwatch League - Stage 1     10224            3  Los Angeles Gladiators  Los Angeles Gladiators     Shanghai Dragons             Ilios          2                             2                            0              Ruins        Shanghai Dragons  Los Angeles Gladiators        Shanghai Dragons  Los Angeles Gladiators                   0.000000                   0.000000              0.000000              0.000000                       58.0                      100.0                         0                         2
17   1/11/2018 3:11  1/11/2018 3:15  Overwatch League - Stage 1     10224            4  Los Angeles Gladiators  Los Angeles Gladiators     Shanghai Dragons       Eichenwalde          1                             1                            0                NaN        Shanghai Dragons  Los Angeles Gladiators  Los Angeles Gladiators        Shanghai Dragons                   0.000000                   0.000000              0.000000              0.000000                        NaN                        NaN                         0                         0
18   1/11/2018 3:17  1/11/2018 3:19  Overwatch League - Stage 1     10224            4  Los Angeles Gladiators  Los Angeles Gladiators     Shanghai Dragons       Eichenwalde          3                             1                            0                NaN  Los Angeles Gladiators        Shanghai Dragons  Los Angeles Gladiators        Shanghai Dragons                   0.000000                   0.000000            107.624008              0.000000                        NaN                        NaN                         1                         0
19   1/11/2018 3:46  1/11/2018 3:53  Overwatch League - Stage 1     10225            1           Seoul Dynasty             Dallas Fuel        Seoul Dynasty        Junkertown          1                             3                            2                NaN             Dallas Fuel           Seoul Dynasty           Seoul Dynasty             Dallas Fuel                 102.004578                   0.000000             63.691517            240.000000                        NaN                        NaN                         3                         0
```


```
Dataframe Columns
round_start_time
round_end_time
stage
match_id
game_number
match_winner
map_winner
map_loser
map_name
map_round
winning_team_final_map_score
losing_team_final_map_score
control_round_name
attacker
defender
team_one_name
team_two_name
attacker_payload_distance
defender_payload_distance
attacker_time_banked
defender_time_banked
attacker_control_perecent
defender_control_perecent
attacker_round_end_score
defender_round_end_score
```

The next thing we want to do is look at all of the maps.
Because Control has separate maps per round, we want to make sure to include the control map name.
We do this by selecting just the map name and control round name columns, dropping duplicate rows, and iterating through the unique combinations.
```python
print('Maps')
# Grab all of the map names
for i, row in map_data[['map_name', 'control_round_name']].drop_duplicates().sort_values(by='map_name').iterrows():
    map = row['map_name']
    control = row['control_round_name']

    if pd.isna(control):
        print(map)
    else:
        print('{} - {}'.format(map, control))
```

```
Maps
Blizzard World
Busan - Sanctuary
Busan - Downtown
Busan - MEKA Base
Dorado
Eichenwalde
Hanamura
Havana
Hollywood
Horizon Lunar Colony
Ilios - Ruins
Ilios - Well
Ilios - Lighthouse
Junkertown
King's Row
Lijiang Tower - Control Center
Lijiang Tower - Night Market
Lijiang Tower - Garden
Nepal - Village
Nepal - Sanctum
Nepal - Shrine
Numbani
Oasis - City Center
Oasis - Gardens
Oasis - University
Paris
Rialto
Route 66
Temple of Anubis
Volskaya Industries
Watchpoint: Gibraltar
```

From the map names we can sort the maps into their game modes, and apply the game mode to each row in the dataframe.
```python
# Classify maps into game types
class MapType:
    Assault = 'Assault'
    Control = 'Control'
    Escort = 'Escort'
    Hybrid = 'Hybrid'

    map_types = {
        'Hanamura': Assault,
        'Horizon Lunar Colony': Assault,
        'Paris': Assault,
        'Temple of Anubis': Assault,
        'Volskaya Industries': Assault,

        'Busan': Control,
        'Ilios': Control,
        'Lijiang Tower': Control,
        'Nepal': Control,
        'Oasis': Control,

        'Dorado': Escort,
        'Havana': Escort,
        'Junkertown': Escort,
        'Rialto': Escort,
        'Route 66': Escort,
        'Watchpoint: Gibraltar': Escort,

        'Numbani': Hybrid,
        'Eichenwalde': Hybrid,
        "King's Row": Hybrid,
        'Hollywood': Hybrid,
        'Blizzard World': Hybrid,
    }


# Determine the map type for each map
def calc_map_type(map_name):
    return MapType.map_types[map_name]

map_data['map_type'] = map_data['map_name'].apply(calc_map_type)
print('\n\n')
print('Map Data with map type included')
print(map_data.head(20))
```

#### 1.1 Control Maps
Now that we can sort games by game mode, we can go look at stats for each game mode.
The first thing we will look into is the percentage of control rounds that end 100% to 99%

To do this we will select only the rows that represent control rounds. Then we will only take the columns relevant to control.
Finally we will generate and apply our condition for games that end 100% - 99%.
```python
control_map_data = map_data[map_data['map_type'] == MapType.Control]
print('\n\n')
print('Control Maps Only')
print(control_map_data.head(20))

# Remove columns that don't matter for control
control_map_data = control_map_data[['stage', 'match_id', 'game_number', 'map_name', 'control_round_name', 'map_type', 'map_round', 'map_winner', 'attacker', 'defender', 'attacker_control_perecent', 'defender_control_perecent']]
print('\n\n')
print('Control Maps Relevant Data Only')
print(control_map_data.head(20))

# What percentage of control maps go to 100% - 99%?

close_games = control_map_data[((control_map_data['attacker_control_perecent'] == 99.0) & (control_map_data['defender_control_perecent'] == 100.0)) | ((control_map_data['attacker_control_perecent'] == 100.0) & (control_map_data['defender_control_perecent'] == 99.0))]

num_close_game = close_games.shape[0]
num_games =  control_map_data.shape[0]
print('\n\n')
print('Percentage of Contorl Maps that End 100 to 99: {}/{} = {}'.format(num_close_game,num_games,num_close_game/num_games))
```

The result of this is that almost a quarter of control rounds end 100 to 99.
```
Percentage of Contorl Maps that End 100 to 99: 521/2143 = 0.243117125524965
```

#### 1.2 Escort Maps
For Escort Maps we are going to look at the average amount of time banked when a team completes an Escort Map.
We will select only Escort Maps and the relevant columns, Then we will select only rounds where the attacker completed the map, group by the map name and generate stats
for the attacker_time_banked column.

```python
# Escort Maps:
escort_map_data = map_data[map_data['map_type'] == MapType.Escort]
print('\n\n')
print('Escort Maps Only')
print(escort_map_data.head(20))

escort_map_data = escort_map_data[['stage', 'match_id', 'game_number', 'map_name', 'map_type', 'map_round', 'map_winner', 'attacker', 'defender', 'attacker_payload_distance', 'attacker_time_banked', 'attacker_round_end_score']]
print('\n\n')
print('Escort Maps Relevant Data Only')
print(escort_map_data.head(20))
print('\n\n')

# What is the average time banked per map?
escort_completion = escort_map_data[escort_map_data['attacker_round_end_score'] == 3]
print(escort_completion[['map_name', 'attacker_time_banked']].groupby('map_name').describe().reset_index())

```

```
                map_name attacker_time_banked
                                        count       mean        std  min       25%        50%         75%         max
0                 Dorado                112.0  72.044178  67.093867  0.0  0.000000  60.000000  121.753778  250.113129
1                 Havana                 41.0  65.389452  64.716069  0.0  9.102005  46.192017  107.382004  191.113037
2             Junkertown                130.0  82.840385  77.638999  0.0  0.000000  60.000000  149.697994  253.175995
3                 Rialto                 83.0  90.726058  85.317946  0.0  7.291515  60.000000  154.867996  311.573975
4               Route 66                104.0  60.519268  55.113313  0.0  0.000000  60.000000   89.243271  208.093368
5  Watchpoint: Gibraltar                160.0  86.728193  77.024638  0.0  0.000000  68.421696  145.398533  259.073975
```

#### 1.3 Hybrid Maps

For hybrid maps we are going to find the percentage of full holds on each map. To do this we will get select the map_name and at attacker_round_end_score,
group by the map_name, and count the number of games on each map. We will then select only rounds where the attacker was not able to capture the first point and repeat the process.
We will then merge the counts per map together and divide to calculate the percentage of games played on each hybrid map that result in a full hold.

```python
# Hybrid Maps:
hybrid_map_data = map_data[map_data['map_type'] == MapType.Hybrid]
print('\n\n')
print('Hybrid Maps Only')
print(hybrid_map_data.head(20))

hybrid_map_data = hybrid_map_data[['stage', 'match_id', 'game_number', 'map_name', 'map_type', 'map_round', 'map_winner', 'attacker', 'defender', 'attacker_payload_distance', 'attacker_time_banked', 'attacker_round_end_score']]
print('\n\n')
print('Hybrid Maps Relevant Data Only')
print(hybrid_map_data.head(20))
print('\n\n')

# Which Map are you most likely to get full held on?
map_counts = hybrid_map_data[['map_name','attacker_round_end_score']].groupby('map_name').count().reset_index()
map_counts.columns = ['map_name', 'times_played']
hybrid_held = hybrid_map_data[hybrid_map_data['attacker_round_end_score'] == 0]
full_held = hybrid_held[['map_name', 'attacker_time_banked']].groupby('map_name').count().reset_index()
full_held.columns = ['map_name', 'times_full_held']
full_held_pct = full_held.merge(map_counts, on='map_name')
full_held_pct['full_hold_percent'] = full_held_pct['times_full_held']/full_held_pct['times_played']
full_held_pct = full_held_pct.sort_values(by='full_hold_percent', ascending=False)
print('Chance to be full held on each Hybrid Map')
print(full_held_pct)
```

```
Chance to be full held on each Hybrid Map
         map_name  times_full_held  times_played  full_hold_percent
0  Blizzard World               37           309           0.119741
2       Hollywood               30           292           0.102740
4         Numbani               27           328           0.082317
1     Eichenwalde               20           286           0.069930
3      King's Row               29           469           0.061834
```

#### 1.4 Assault Maps

The final map data we will explore is the spread of rounds played on each Assault map. To do this we will select the match_id, map_name, and map_round,
select the maximum round number for each map, count the number of matches that ended on each round number and calculate the percentage of matches ended on each round number per map

```python
# 2 CP
assault_map_data = map_data[map_data['map_type'] == MapType.Assault]
print('\n\n')
print('Hybrid Maps Only')
print(assault_map_data.head(20))

assault_map_data = assault_map_data[['stage', 'match_id', 'game_number', 'map_name', 'map_type', 'map_round', 'map_winner', 'attacker', 'defender', 'attacker_time_banked', 'attacker_round_end_score']]
print('\n\n')
print('Assault Maps Relevant Data Only')
print(assault_map_data.head(20))
print('\n\n')

print("How many rounds do the average 2CP Map Go?")
def match_percent(group):
    sum = group['match_id'].sum()
    group['match_percent'] = group['match_id'] / sum
    return group

max_score_group = assault_map_data[['match_id', 'map_name', 'map_round']].groupby(by=['match_id', 'map_name']).max().reset_index().groupby(by=['map_name', 'map_round']).count().reset_index().groupby(by=['map_name'])
max_score = max_score_group.apply(match_percent)
max_score.columns = ['map_name', 'map_round', 'match_count', 'match_percent']
print(max_score)
```

```

How many rounds do the average 2CP Map Go?
                map_name  map_round  match_count  match_percent
0               Hanamura          2           99       0.642857
1               Hanamura          3           10       0.064935
2               Hanamura          4           41       0.266234
3               Hanamura          5            1       0.006494
4               Hanamura          6            2       0.012987
5               Hanamura          7            1       0.006494
6   Horizon Lunar Colony          2           72       0.562500
7   Horizon Lunar Colony          3            6       0.046875
8   Horizon Lunar Colony          4           38       0.296875
9   Horizon Lunar Colony          5            3       0.023438
10  Horizon Lunar Colony          6            9       0.070312
11                 Paris          2           30       0.461538
12                 Paris          3            5       0.076923
13                 Paris          4           22       0.338462
14                 Paris          5            4       0.061538
15                 Paris          6            4       0.061538
16      Temple of Anubis          2          108       0.624277
17      Temple of Anubis          3           14       0.080925
18      Temple of Anubis          4           43       0.248555
19      Temple of Anubis          5            1       0.005780
20      Temple of Anubis          6            7       0.040462
21   Volskaya Industries          2           78       0.461538
22   Volskaya Industries          3           10       0.059172
23   Volskaya Industries          4           62       0.366864
24   Volskaya Industries          5            4       0.023669
25   Volskaya Industries          6           15       0.088757
```

The complete script can be found [here](explore_map_data.py)