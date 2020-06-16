## Investigating The Overwatch League Data

In this tutorial I will explore the different data provided by the Overwatch League.

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### 0.1 Requirements
The code in this tutorial was written in python 3.7 and uses the following libraries:
Pandas

The environment.yml page for the entire project contains everything you need to run this script.

### 1.0 Map Data

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
map_data = pd.read_csv('map_data/match_map_stats.csv')

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

### 2.0 Player Data

The StatsLab page also provides us with player stats data for each match. We can dig into this to find very interesting information about ability use, damage, healing, and more for each player in the league.
In this section we will find out all of the unique stats we have access to and then look into who owns the final blow record for each map and which player is the most accurate with their Sleep Dart when playing Ana

We are going to start the same way we did in the last section by importing the libraries we will be using and setting a few options to make our life easier.
```python
import warnings
warnings.simplefilter(action='ignore')

import pandas as pd
import os
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
```

There is way more data for players than there is for maps, so the data has been broken up into multiple files. In order to read them all into the same frame
we will load all of the CSVs in the player_data directory, read them in one at a time, rename various columns that are not consistent across files and concatenate them all together.
```python
csvs = os.listdir('player_data') # Get all files in the data directory
frames = []

for file in csvs:
    # Read the file in as a CSV
    frame = pd.read_csv('{}/{}'.format('player_data', file))
    # Update column names so that they are consistent across years
    frame=frame.rename(columns={'esports_match_id': 'match_id', 'tournament_title': 'stage', 'player_name': 'player',
                          'hero_name': 'hero', 'team_name': 'team', 'pelstart_time': 'start_time'})
    # Add the dataframe to a list
    frames.append(frame)


# Concat all of the dataframes together
player_frame = pd.concat(frames)
print(player_frame)
```

```
0        2/15/2019 0:11     21211           Overwatch League Stage 1  CONTROL                  Ilios    Bdosin   London Spitfire       All Damage Done  All Heroes  14845.193400
1        2/15/2019 0:11     21211           Overwatch League Stage 1  CONTROL                  Ilios    Bdosin   London Spitfire               Assists  All Heroes     13.000000
2        2/15/2019 0:11     21211           Overwatch League Stage 1  CONTROL                  Ilios    Bdosin   London Spitfire    Average Time Alive  All Heroes     87.623574
3        2/15/2019 0:11     21211           Overwatch League Stage 1  CONTROL                  Ilios    Bdosin   London Spitfire   Barrier Damage Done  All Heroes   5674.344475
4        2/15/2019 0:11     21211           Overwatch League Stage 1  CONTROL                  Ilios    Bdosin   London Spitfire  Damage - Quick Melee  All Heroes     78.000000
```

Now we can print all of the columns in the dataframe to see exactly what the dataframe looks like. We can also print out all of the unique stat_names so that we can see what sort of data we have access to.
```python
# Print all of the columns in the dataframe
print('Dataframe Columns')
for c in player_frame.columns:
    print(c)

print('\n\n')
# Print out all of the possible stats
for p in np.sort(player_frame['stat_name'].unique()):
    print(p)

```

```
Dataframe Columns
start_time
match_id
stage
map_type
map_name
player
team
stat_name
hero
stat_amount


Unique Stat Names:
Ability Damage Done
Accretion Kills
Accretion Stuns
Adaptive Shield Uses
Air Uptime
Air Uptime Percentage
All Damage Done
Amped Heal Activations
Amped Speed Activations
Amplification Matrix Assists
Amplification Matrix Casts
Amplification Matrix Efficiency
Armor - Rally
Armor - Repair Pack
Armor Packs Created
Armor Provided
Armor Uptime
Assists
Average Energy
Average Players per Teleporter
Average Time Alive
Barrage Efficiency
Barrage Kills
Barrier Damage Done
Biotic Field Healing Done
Biotic Fields Deployed
Biotic Grenade Kills
Biotic Launcher Healing Explosions
Biotic Launcher Healing Shots
Biotic Orb Damage Efficiency
Biotic Orb Healing Efficiency
Biotic Orb Maximum Damage
Biotic Orb Maximum Healing
Blaster Kills
Blizzard Efficiency
Blizzard Kills
Bob Gun Damage
Bob Kills
Charge Kills
Coach Gun Kills
Coalescence Healing
Coalescence Kills
Coalesence - Damage per Use
Coalesence - Healing per Use
Concussion Mine Kills
Critical Hit Accuracy
Critical Hit Kills
Critical Hits
Damage - Accretion
Damage - Barrage
Damage - Biotic Grenade
Damage - Biotic Orb
Damage - Blizzard
Damage - Bob
Damage - Bob Charge
Damage - Boosters
Damage - Call Mech
Damage - Chain Hook
Damage - Charge
Damage - Coach Gun
Damage - Coalescence
Damage - Concussion Mine
Damage - Deadeye
Damage - Death Blossom
Damage - Deflect
Damage - Discord Orb
Damage - Dragonblade
Damage - Dragonblade Total
Damage - Dragonstrike
Damage - Duplicate
Damage - Dynamite
Damage - EMP
Damage - Earthshatter
Damage - Fire Strike
Damage - Flashbang
Damage - Focusing Beam
Damage - Focusing Beam - Bonus Damage Only
Damage - Grappling Claw
Damage - Graviton Surge
Damage - Helix Rockets
Damage - Hyperspheres
Damage - Jump Pack
Damage - Meteor Strike
Damage - Micro Missiles
Damage - Minefield
Damage - Molten Core
Damage - Piledriver
Damage - Pistol
Damage - Primal Rage Leap
Damage - Primal Rage Melee
Damage - Primal Rage Total
Damage - Pulse Bomb
Damage - Quick Melee
Damage - RIP-Tire
Damage - Rising Uppercut
Damage - Rocket Punch
Damage - Scatter
Damage - Seismic Slam
Damage - Self Destruct
Damage - Sentry Turret
Damage - Shield Bash
Damage - Sonic
Damage - Steel Trap
Damage - Sticky Bombs
Damage - Storm Arrows
Damage - Swift Strike
Damage - Swift Strike Dragonblade
Damage - Tactical Visor
Damage - Total Mayhem
Damage - Turret Rockets
Damage - Venom Mine
Damage - Weapon
Damage - Weapon Charged
Damage - Weapon Hammer
Damage - Weapon Pistol
Damage - Weapon Primary
Damage - Weapon Recon
Damage - Weapon Scoped
Damage - Weapon Secondary
Damage - Weapon Sentry
Damage - Weapon Tank
Damage - Whole Hog
Damage Absorbed
Damage Amplified
Damage Blocked
Damage Done
Damage Prevented
Damage Reflected
Damage Taken
Damage Taken - Adaptive Shield
Damage Taken - Ball
Damage Taken - Tank
Deadeye Efficiency
Deadeye Kills
Death Blossom Efficiency
Death Blossom Kills
Death Blossoms
Deaths
Defensive Assists
Deflection Kills
Direct Hit Accuracy
Discord Orb Time
Dragonblade Efficiency
Dragonblade Kills
Dragonblades
Dragonstrike Efficiency
Dragonstrike Kills
Duplicate Kills
Dynamite Kills
EMP Efficiency
Earthshatter Efficiency
Earthshatter Kills
Earthshatter Stuns
Eliminations
Eliminations per Life
Enemies EMP'd
Enemies Frozen
Enemies Hacked
Enemies Hooked
Enemies Slept
Enemies Trapped
Energy Maximum
Environmental Deaths
Environmental Kills
Fan the Hammer Kills
Final Blows
Fire Strike Kills
Focusing Beam Accuracy
Focusing Beam Dealing Damage Seconds
Focusing Beam Kills
Focusing Beam Seconds
Frag Launcher Direct Hits
Freeze Spray Damage
Grappling Claw Impacts
Grappling Claw Kills
Grappling Claw Uses
Gravitic Flux Damage Done
Gravitic Flux Kills
Graviton Surge Efficiency
Graviton Surge Kills
Hammer Kills
Harmony Orb Time
Heal Song Time Elapsed
Healing - Biotic Grenade
Healing - Biotic Launcher
Healing - Biotic Orb
Healing - Coalescence
Healing - Harmony Orb
Healing - Healing Boost
Healing - Healing Boost Amped
Healing - Immortality Field
Healing - Inspire
Healing - Regenerative Burst
Healing - Repair Pack
Healing - Secondary Fire
Healing - Transcendence
Healing - Weapon
Healing - Weapon Scoped
Healing - Weapon Valkyrie
Healing Accuracy
Healing Amplified
Healing Done
Healing Received
Health Recovered
Helix Rocket Kills
Hero Damage Done
High Energy Kills
Hook Accuracy
Hooks Attempted
Hyperspheres Direct Hits
Icicle Damage
Immortality Field Deaths Prevented
Infra-Sight Efficiency
Infra-sight Uptime
Inspire Uptime
Inspire Uptime Percentage
Jump Pack Kills
Knockback Kills
Lifetime Energy Accumulation
Match Blinks Used
Mech Deaths
Mechs Called
Melee Final Blows
Melee Kills
Melee Percentage of Final Blows
Meteor Strike Efficiency
Meteor Strike Kills
Minefield Kills
Molten Core Efficiency
Molten Core Kills
Multikills
Nano Boost Assists
Nano Boost Efficiency
Nano Boosts Applied
Objective Kills
Objective Time
Offensive Assists
Overload Kills
Photon Projector Kills
Piledriver Kills
Piledriver Uses
Players Halted
Players Knocked Back
Players Resurrected
Players Saved
Players Teleported
Primal Rage Efficiency
Primal Rage Kills
Primal Rage Melee Accuracy
Primal Rage Melee Efficiency
Primal Rage Melee Hits
Primal Rage Melee Hits - Multiple
Primal Rage Melee Ticks
Primary Fire Accuracy
Primary Fire Average Level
Primary Fire Hits
Primary Fire Hits Hits - Level
Primary Fire Ticks
Projected Barrier Damage Blocked
Projected Barriers Applied
Pulse Bomb Attach Rate
Pulse Bomb Efficiency
Pulse Bomb Kills
Pulse Bombs Attached
Quick Melee Accuracy
Quick Melee Hits
Quick Melee Ticks
RIP-Tire Efficiency
RIP-Tire Kills
Rally Armor Efficiency
Recalls Used
Recon Assists
Recon Kills
Rocket Barrages
Rocket Direct Hits
Rocket Hammer Melee Accuracy
Rocket Hammer Melee Average Targets
Rocket Hammer Melee Hits
Rocket Hammer Melee Hits - Multiple
Rocket Hammer Melee Ticks
Roll Uptime
Roll Uptime Percentage
Roll Uses
Scatter Arrow Kills
Scoped Accuracy
Scoped Critical Hit Accuracy
Scoped Critical Hit Kills
Scoped Critical Hits
Scoped Hits
Scoped Shots
Secondary Direct Hits
Secondary Fire Accuracy
Secondary Fire Hits
Secondary Fire Ticks
Self Destruct Efficiency
Self Healing
Self Healing Percent of Damage Taken
Self-Destruct Kills
Self-Destructs
Sentry Kills
Sentry Turret Kills
Shielding - Adaptive Shield
Shields Created
Shots Fired
Shots Hit
Shots Missed
Sleep Dart Hits
Sleep Dart Shots
Sleep Dart Success Rate
Solo Kills
Sound Barrier Casts
Sound Barrier Efficiency
Sound Barriers Provided
Soundwave Kills
Speed Song Time Elapsed
Sticky Bombs Direct Hit Accuracy
Sticky Bombs Direct Hits
Sticky Bombs Kills
Sticky Bombs Useds
Storm Arrow Kills
Successful Freezes
Supercharger Assists
Supercharger Efficiency
Tactical Visor Efficiency
Tactical Visor Kills
Tactical Visors
Tank Efficiency
Tank Kills
Teleporter Pads Destroyed
Teleporter Uptime
Teleporters Placed
Tesla Cannon Accuracy
Tesla Cannon Efficiency
Tesla Cannon Hits
Tesla Cannon Hits - Multiple
Tesla Cannon Ticks
Time Alive
Time Building Ultimate
Time Discorded
Time Elapsed per Ultimate Earned
Time Hacked
Time Holding Ultimate
Time Played
Torbjörn Kills
Total Mayhem Kills
Total Time Frozen
Transcendence Efficiency
Transcendence Healing
Transcendence Percent of Healing
Turret Damage
Turret Kills
Turrets Destroyed
Ultimates Earned - Fractional
Ultimates Negated
Ultimates Used
Unscoped Accuracy
Unscoped Hits
Unscoped Shots
Valkyrie Healing Efficiency
Venom Mine Kills
Weapon Accuracy
Weapon Kills
Whole Hog Efficiency
Whole Hog Kills
of Rockets Fired
```


#### 2.1 Final Blow Records

In order to calculate who has the most final blows on each map we need to select only rows where the stat_name is Final Blows and we need the columns for match id, player, map_name, and stat_amount. We need to drop duplicates because final blows are repeated for each hero the player played reguardless of which hero they got the final blow on.
We will then group the data by map name and select the max player for each group.
```python
# Find out who has the most final blows in a single map for each map
final_blows = player_frame[player_frame['stat_name'] == 'Final Blows'][['match_id', 'map_name', 'player', 'stat_amount']].drop_duplicates()

def take_max(group):
    max_kills = group['stat_amount'].max()
    return group[group['stat_amount'] == max_kills]

max_final_blows = final_blows.groupby(by=['map_name']).apply(take_max).reset_index(drop=True).sort_values(by='stat_amount')[['map_name', 'player', 'stat_amount']]
max_final_blows.columns = ['map_name', 'player', 'final_blows']
print('Final Blow Leaders per Map')
print(max_final_blows)
```

```
Final Blow Leaders per Map
                 map_name       player  final_blows
18                  Paris        JinMu         21.0
22    Volskaya Industries    Architect         23.0
8                   Ilios         MekO         23.0
9                   Ilios  DreamKazper         23.0
23    Volskaya Industries       Profit         23.0
1                   Busan       Profit         24.0
17                  Oasis      STRIKER         26.0
14          Lijiang Tower        carpe         26.0
19                 Rialto    SeoMinSoo         27.0
15                  Nepal          eqo         27.0
4                Hanamura       Libero         28.0
0          Blizzard World    Architect         29.0
13             King's Row       Libero         29.0
12             King's Row         Fits         29.0
5                  Havana        carpe         29.0
11             King's Row        carpe         29.0
7    Horizon Lunar Colony        Fleta         30.0
24  Watchpoint: Gibraltar        GodsB         30.0
2                  Dorado        Decay         31.0
3             Eichenwalde        GodsB         32.0
21       Temple of Anubis   SAEBYEOLBE         32.0
6               Hollywood        Corey         34.0
16                Numbani   SAEBYEOLBE         35.0
20               Route 66     Birdring         37.0
10             Junkertown   sayaplayer         42.0
```

#### 2.1 Ana Sleep Dart Accuracy

To calculate career sleep dart accuracy we need to select only rows where the hero is Ana, and the stat name is either Sleep Dart Hits or Sleep Dart Shots, and we need to select the player, stat_name, and stat_amount columns.
Then we will group by player and sum up the sleep dart hits, and sleep dart attempts and calculate the accuracy per player. We want to filter to a minimum of 100 sleep dart shots just to filter out any low attempt players who don't play ana regularly, and sort by accuracy.



```python
# Find out which player is the most successful at getting sleeps on Ana
ana_sleep = player_frame[(player_frame['hero'] == 'Ana') & ((player_frame['stat_name'] == 'Sleep Dart Hits') | (player_frame['stat_name'] == 'Sleep Dart Shots'))][['player', 'stat_name','stat_amount']]

def calculate_sleep_efficency(group):
    sleeps_hit = group[group['stat_name'] == 'Sleep Dart Hits']['stat_amount'].sum()
    sleeps_shot = group[group['stat_name'] == 'Sleep Dart Shots']['stat_amount'].sum()

    return pd.Series({'sleep_darts_shot': sleeps_shot, 'sleep_darts_hit': sleeps_hit, 'sleep_accuracy': sleeps_hit/sleeps_shot})



ana_sleep = ana_sleep.groupby(by='player').apply(calculate_sleep_efficency)
ana_sleep = ana_sleep[ana_sleep['sleep_darts_shot'] >= 100]
sleep_stats = ana_sleep.sort_values(by='sleep_accuracy', ascending=False).head(10).reset_index()
print('Ana Sleep Dart Accuracy (min 100 attempts)')
print(sleep_stats)
```

```python
Ana Sleep Dart Accuracy (min 100 attempts)
      player  sleep_darts_shot  sleep_darts_hit  sleep_accuracy
0  ryujehong             798.0            306.0        0.383459
1        shu            1417.0            533.0        0.376147
2     Highly             383.0            139.0        0.362924
3  HarryHook             288.0            103.0        0.357639
4      uNKOE             445.0            159.0        0.357303
5    IZaYaKI             775.0            270.0        0.348387
6      Luffy            1332.0            461.0        0.346096
7      Rapel             372.0            128.0        0.344086
8     AimGod             872.0            300.0        0.344037
9   Twilight            1408.0            482.0        0.342330
```

The complete script can be found [here](explore_player_data.py)