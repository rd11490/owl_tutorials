## Calculate Team Elo across multiple seasons of Overwatch League

In this tutorial I will show you how to take the map result data from the StatsLab page on the Overwatch League page and use it to calculate the Elo rating for each team and game mode.

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### 0.1 Requirements
This tutorial uses the latest version of Google Chrome for finding the endpoint information.
The code in this tutorial was written in python 3.7 and uses the following libraries:
Pandas

The environment.yml page for the entire project contains everything you need to run this script.


### 1. Exploring the data
The first thing we want to do is look at the map result data provided by the Overwatch League.
To do this we will use the pandas library to read in the CSV as a dataframe, and print the first 10 rows.
This is just to get an idea of the data we are working with. The full code for this section can be found [here](map_data_exploration.py)


```python
import pandas as pd

# Settings to make printed dataframes more human readable
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Read the csv
frame = pd.read_csv('map_data/match_map_stats.csv')

# print out the first 10 rows just to see what type of data we are looking at
print(frame.head(10))
```

This results in the following being printed to console:
```
      round_start_time       round_end_time                       stage  match_id  game_number         match_winner           map_winner            map_loser          map_name  map_round  winning_team_final_map_score  losing_team_final_map_score control_round_name             attacker             defender        team_one_name        team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score
0  2018-01-11 00:12:07  2018-01-11 00:20:07  Overwatch League - Stage 1     10223            1  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock            Dorado          1                             3                            2                NaN  San Francisco Shock  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock                  75.615051                   0.000000              0.000000            240.000000                        NaN                        NaN                         2                         0
1  2018-01-11 00:22:05  2018-01-11 00:27:59  Overwatch League - Stage 1     10223            1  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock            Dorado          2                             3                            2                NaN  Los Angeles Valiant  San Francisco Shock  Los Angeles Valiant  San Francisco Shock                  75.649597                  75.615051            125.750572              0.000000                        NaN                        NaN                         3                         2
2  2018-01-11 00:34:39  2018-01-11 00:38:29  Overwatch League - Stage 1     10223            2  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock  Temple of Anubis          1                             4                            3                NaN  San Francisco Shock  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock                   0.000000                   0.000000            250.492004            240.000000                        NaN                        NaN                         2                         0
3  2018-01-11 00:40:27  2018-01-11 00:44:41  Overwatch League - Stage 1     10223            2  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock  Temple of Anubis          2                             4                            3                NaN  Los Angeles Valiant  San Francisco Shock  Los Angeles Valiant  San Francisco Shock                   0.000000                   0.000000            225.789032            250.492004                        NaN                        NaN                         2                         2
4  2018-01-11 00:46:09  2018-01-11 00:49:48  Overwatch League - Stage 1     10223            2  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock  Temple of Anubis          3                             4                            3                NaN  Los Angeles Valiant  San Francisco Shock  Los Angeles Valiant  San Francisco Shock                   0.000000                   0.000000             36.396057            250.492004                        NaN                        NaN                         4                         2
5  2018-01-11 00:51:16  2018-01-11 00:56:55  Overwatch League - Stage 1     10223            2  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock  Temple of Anubis          4                             4                            3                NaN  San Francisco Shock  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock                   0.000000                   0.000000              0.000000             36.396057                        NaN                        NaN                         3                         4
6  2018-01-11 01:11:32  2018-01-11 01:16:33  Overwatch League - Stage 1     10223            3  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock             Ilios          1                             2                            1         Lighthouse  Los Angeles Valiant  San Francisco Shock  Los Angeles Valiant  San Francisco Shock                   0.000000                   0.000000              0.000000              0.000000                       99.0                      100.0                         0                         1
7  2018-01-11 01:17:19  2018-01-11 01:20:09  Overwatch League - Stage 1     10223            3  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock             Ilios          2                             2                            1              Ruins  Los Angeles Valiant  San Francisco Shock  Los Angeles Valiant  San Francisco Shock                   0.000000                   0.000000              0.000000              0.000000                      100.0                        0.0                         1                         1
8  2018-01-11 01:20:55  2018-01-11 01:25:08  Overwatch League - Stage 1     10223            3  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock             Ilios          3                             2                            1               Well  Los Angeles Valiant  San Francisco Shock  Los Angeles Valiant  San Francisco Shock                   0.000000                   0.000000              0.000000              0.000000                      100.0                       65.0                         2                         1
9  2018-01-11 01:32:26  2018-01-11 01:39:37  Overwatch League - Stage 1     10223            4  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock           Numbani          1                             2                            1                NaN  San Francisco Shock  Los Angeles Valiant  Los Angeles Valiant  San Francisco Shock                  75.549507                   0.000000              0.000000              0.000000                        NaN                        NaN                         1                         0

```

Right away some columns stand out as useful for calculating Elo. `round_start_time`
can be used to calculate the match date, and more importantly the league season in which the match took place,
`map_name` can be used to determine the game mode, and `map_winner, team_one_name, and team_two_name`
can all be used to determine who played in the map and who won.

We will also want to look at unique values of some of the important columns to make sure we have a full understanding of what data we are working with.
```python
# Look at all of the unique stages
print('\nStages')
for stage in frame['stage'].unique():
    print(stage)


Stages
Overwatch League - Stage 1
Overwatch League - Stage 1 - Title Matches
Overwatch League - Stage 2
Overwatch League - Stage 2 Title Matches
Overwatch League - Stage 3
Overwatch League - Stage 3 Title Matches
Overwatch League - Stage 4
Overwatch League - Stage 4 Title Matches
Overwatch League Inaugural Season Championship
Overwatch League Stage 1
Overwatch League Stage 1 Title Matches
Overwatch League Stage 2
Overwatch League Stage 2 Title Matches
Overwatch League Stage 3
Overwatch League Stage 3 Title Matches
Overwatch League Stage 4
Overwatch League 2019 Post-Season
OWL 2020 Regular Season
OWL APAC All-Stars
OWL North America All-Stars
```
Everything here looks normal, but we do have 2 stages for all star games that we want to filter out when we go to calculate elo.

```python
# Look at all of the unique maps
print('\nMaps')
for map in frame['map_name'].unique():
    print(map)

Maps
Dorado
Temple of Anubis
Ilios
Numbani
Eichenwalde
Junkertown
Oasis
Horizon Lunar Colony
Lijiang Tower
Volskaya Industries
Nepal
King's Row
Route 66
Hollywood
Hanamura
Watchpoint: Gibraltar
Blizzard World
Rialto
Busan
Paris
Havana

```
Nothing interesting in the list of maps, We will use this later for building a dictionary to relate map names to game modes.

```python
# Look at all of the unique teams
print('\nTeams')
for team in frame['map_winner'].unique():
    print(team)

Teams
Los Angeles Valiant
Los Angeles Gladiators
Dallas Fuel
Seoul Dynasty
draw
Florida Mayhem
London Spitfire
Philadelphia Fusion
Houston Outlaws
New York Excelsior
Boston Uprising
San Francisco Shock
Shanghai Dragons
Hangzhou Spark
Toronto Defiant
Atlanta Reign
Guangzhou Charge
Chengdu Hunters
Paris Eternal
Washington Justice
Vancouver Titans
Brick Movers
Team Universe
Triple A
Team Jake
Team Custa
Team Reinhardt
Team D.va
```
There are two interesting piece of information we gain by looking at the `map_winner` column. The first is that we have a bunch of all star teams we need to filter out.
The second, and more important piece if information is that when the map results in a draw, the string `draw` is put in the `map_winner` column.
This is important as we will have to account for it later.

