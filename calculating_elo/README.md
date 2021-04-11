## Calculate Team Elo across multiple seasons of Overwatch League

In this tutorial I will show you how to take the map result data from the StatsLab page on the Overwatch League page and use it to calculate the Elo rating for each team and game mode.

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### 0.1 Requirements
This tutorial uses the latest version of Google Chrome for finding the endpoint information.
The code in this tutorial was written in python 3.7 and uses the following libraries:  
Pandas  
Requests  

The environment.yml page for the entire project contains everything you need to run this script.


### 1. Exploring the data
The first thing we want to do is look at the map result data provided by the Overwatch League.
To do this we will use the pandas library to read in the CSV as a dataframe, and print the first 10 rows.
This is just to get an idea of the data we are working with.


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