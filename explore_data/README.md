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
```
import warnings
warnings.simplefilter(action='ignore')

import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
```

Now we want to read in the data and see what we are working with

```
# Read in our map stats data
map_data = pd.read_csv('data/match_map_stats.csv')

print(map_data.head(20))
```

Running those lines of code we can see a sample of hte data provided.
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
# Print out our columns so we can see what we are looking at
print('Dataframe Columns')
for c in map_data.columns:
    print(c)

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