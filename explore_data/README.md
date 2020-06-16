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