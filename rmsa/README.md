## Regularized Map Score Added - An Attempt to Build a Predictive All in One Metric for OWL Teams

In this "tutorial" we will attempt to generate a rating for each team that accounts who each team players and how dominant their win is. 
We will do this by coming up with a method for calculating a "map score" for each map played, then use regularized linear 
regression on a sparse team matrix in an attempt to give each team credit/blame for the result of the map.

Each game mode in Overwatch as a unique set of objectives and mechanics. In order to account for that we need to develop a
separate scoring system for each game mode. We also need to account for any limitations and bias in the data provided to
us by Overwatch League. The input data we will use is in the [Match Map Stats File](./input/match_map_stats.csv). There
are other tutorials in this project for how to [Automate the Download of Statslab Data](../getting_data/README.md) and 
[Exploring the Statslab Data](../explore_data/README.md).

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### Index
 - 0.1 [Results](#01-tldr-results)
 - 0.2 [Requirements to run the code](#02-requirements)
 - 1.0 [Calculating Map Score](#1-calculating-map-score)
 - 1.1 [Calculating Map Score - Assault](#11-assault-map-score)
 - 1.2 [Calculating Map Score - Escort](#12-escort-map-score)
 - 1.3 [Calculating Map Score - Hybrid](#13-hybrid-map-score)
 - 1.4 [Calculating Map Score - Control](#14-control-map-score)
 - 2.0 [Calculating Map Score Added](#2-calculating-map-score-added)
 - 2.1 [Calculating Map Score Added - Control](#21-control)
 - 2.2 [Calculating Map Score Added - Assault](#22-assault)
 - 2.3 [Calculating Map Score Added - Escord](#23-escort)
 - 2.4 [Calculating Map Score Added - Hybrid](#24-hybrid)
 - 2.5 [Calculating Total Map Score Added](#25-total-map-score-added)
 - 3.0 [Predicting Map Winners](#30-predicting-map-winners)
 - 4.0 [Future Work](#40-future-work)

### 0.1 TLDR Results:
#### 0.1.1 Total Map Score Added
``` 
                      team  Total Rating  rank
0              Dallas Fuel         1.025   1.0
1         Shanghai Dragons         0.994   2.0
3   Los Angeles Gladiators         0.643   3.0
4            Atlanta Reign         0.561   4.0
5          Houston Outlaws         0.522   5.0
8          Chengdu Hunters         0.461   6.0
7      San Francisco Shock         0.377   7.0
2            Seoul Dynasty         0.320   8.0
10     Philadelphia Fusion         0.086   9.0
6       Washington Justice         0.030  10.0
13          Hangzhou Spark        -0.041  11.0
15           Paris Eternal        -0.115  12.0
9          Boston Uprising        -0.173  13.0
14          Florida Mayhem        -0.175  14.0
16      New York Excelsior        -0.245  15.0
12        Guangzhou Charge        -0.419  16.0
11         Toronto Defiant        -0.636  17.0
18         London Spitfire        -0.859  18.0
17        Vancouver Titans        -0.996  19.0
19     Los Angeles Valiant        -1.360  20.0
```

#### 0.1.2 Control
```
                      team  Control rmsa attack  Control rmsa defend  Control rmsa  Control intercept
3              Dallas Fuel                0.121                0.093         0.214              0.783
16        Shanghai Dragons                0.090                0.086         0.176              0.783
15           Seoul Dynasty                0.016                0.090         0.106              0.783
9   Los Angeles Gladiators                0.071                0.024         0.096              0.783
0            Atlanta Reign                0.033                0.044         0.078              0.783
7          Houston Outlaws                0.017                0.046         0.063              0.783
19      Washington Justice                0.039                0.020         0.060              0.783
14     San Francisco Shock                0.044                0.004         0.048              0.783
2          Chengdu Hunters                0.024                0.014         0.038              0.783
1          Boston Uprising               -0.019                0.005        -0.014              0.783
13     Philadelphia Fusion                0.000               -0.020        -0.020              0.783
17         Toronto Defiant               -0.012               -0.011        -0.023              0.783
5         Guangzhou Charge                0.009               -0.037        -0.029              0.783
6           Hangzhou Spark               -0.036               -0.004        -0.040              0.783
4           Florida Mayhem               -0.027               -0.037        -0.064              0.783
12           Paris Eternal               -0.048               -0.030        -0.078              0.783
11      New York Excelsior               -0.057               -0.050        -0.107              0.783
18        Vancouver Titans               -0.073               -0.062        -0.134              0.783
8          London Spitfire               -0.080               -0.079        -0.159              0.783
10     Los Angeles Valiant               -0.114               -0.098        -0.212              0.783
```
#### 0.1.3 Assault
```
                      team  Assault rmsa attack  Assault rmsa defend  Assault rmsa  Assault intercept
16        Shanghai Dragons                0.197                0.247         0.444              1.116
3              Dallas Fuel                0.270                0.127         0.397              1.116
7          Houston Outlaws                0.098                0.167         0.266              1.116
14     San Francisco Shock                0.161                0.085         0.246              1.116
9   Los Angeles Gladiators                0.137                0.069         0.206              1.116
12           Paris Eternal                0.115                0.059         0.174              1.116
2          Chengdu Hunters                0.114                0.035         0.149              1.116
0            Atlanta Reign                0.059                0.048         0.107              1.116
19      Washington Justice               -0.010                0.082         0.072              1.116
15           Seoul Dynasty               -0.020                0.073         0.053              1.116
13     Philadelphia Fusion                0.079               -0.078         0.002              1.116
6           Hangzhou Spark                0.035               -0.143        -0.107              1.116
11      New York Excelsior               -0.132                0.013        -0.119              1.116
5         Guangzhou Charge               -0.097               -0.057        -0.155              1.116
4           Florida Mayhem               -0.173               -0.049        -0.222              1.116
17         Toronto Defiant               -0.148               -0.103        -0.251              1.116
8          London Spitfire               -0.070               -0.190        -0.260              1.116
1          Boston Uprising               -0.127               -0.186        -0.312              1.116
18        Vancouver Titans               -0.180               -0.153        -0.334              1.116
10     Los Angeles Valiant               -0.308               -0.046        -0.354              1.116
```

#### 0.1.4 Escort
```
                      team  Escort rmsa attack  Escort rmsa defend  Escort rmsa  Escort intercept
13     Philadelphia Fusion               0.075               0.048        0.123             0.908
0            Atlanta Reign               0.032               0.058        0.090             0.908
11      New York Excelsior               0.022               0.060        0.082             0.908
2          Chengdu Hunters               0.030               0.045        0.075             0.908
9   Los Angeles Gladiators               0.054               0.021        0.075             0.908
14     San Francisco Shock               0.039               0.033        0.071             0.908
16        Shanghai Dragons               0.011               0.052        0.063             0.908
7          Houston Outlaws               0.048              -0.000        0.047             0.908
3              Dallas Fuel               0.048              -0.015        0.033             0.908
12           Paris Eternal               0.027               0.004        0.031             0.908
4           Florida Mayhem              -0.015               0.043        0.028             0.908
15           Seoul Dynasty              -0.018               0.005       -0.013             0.908
6           Hangzhou Spark              -0.018              -0.001       -0.019             0.908
1          Boston Uprising              -0.023              -0.011       -0.034             0.908
17         Toronto Defiant              -0.028              -0.038       -0.067             0.908
19      Washington Justice              -0.038              -0.034       -0.072             0.908
5         Guangzhou Charge              -0.037              -0.039       -0.076             0.908
8          London Spitfire              -0.039              -0.053       -0.091             0.908
18        Vancouver Titans              -0.081              -0.064       -0.146             0.908
10     Los Angeles Valiant              -0.087              -0.113       -0.200             0.908
```

#### 0.1.5 Hybrid
```
                      team  Hybrid rmsa attack  Hybrid rmsa defend  Hybrid rmsa  Hybrid intercept
0            Atlanta Reign               0.116               0.092        0.208             0.926
1          Boston Uprising               0.212              -0.011        0.201             0.926
9   Los Angeles Gladiators               0.075               0.097        0.171             0.926
3              Dallas Fuel               0.081               0.086        0.167             0.926
6           Hangzhou Spark               0.176              -0.011        0.166             0.926
2          Chengdu Hunters               0.025               0.136        0.161             0.926
4           Florida Mayhem               0.132               0.014        0.146             0.926
16        Shanghai Dragons               0.046               0.088        0.135             0.926
7          Houston Outlaws               0.062               0.021        0.082             0.926
15           Seoul Dynasty               0.030               0.038        0.068             0.926
11      New York Excelsior               0.031              -0.024        0.007             0.926
13     Philadelphia Fusion               0.015              -0.013        0.002             0.926
14     San Francisco Shock               0.063              -0.099       -0.035             0.926
19      Washington Justice              -0.114               0.025       -0.089             0.926
5         Guangzhou Charge              -0.042              -0.089       -0.131             0.926
12           Paris Eternal              -0.150              -0.014       -0.164             0.926
8          London Spitfire              -0.137              -0.053       -0.190             0.926
18        Vancouver Titans              -0.225              -0.024       -0.249             0.926
17         Toronto Defiant              -0.167              -0.106       -0.273             0.926
10     Los Angeles Valiant              -0.228              -0.155       -0.383             0.926
```


### 0.2 Requirements
The code in this tutorial was written in python 3.7 and uses the following libraries:
Pandas
Requests
sklearn

The environment.yml page for the entire project contains everything you need to run this script.

### 1. Calculating Map Score


#### 1.1 Assault Map Score
The basic idea behind our calculation for map score on Assault is   
`How many times could you complete the map in at the rate at which you initially completed the map`.    
For example if the attacking team captures Point A then fails to capture Point B they will be given a map score of 
1 point divided by 2 total points on the map, or more simply put, 0.5. However, if the team captured both points and only
used half of their total time bank, then they will receive a map score of 2 points / 2 total points on the map plus an
additional 2 points / 2 total points on the map because at the rate they capped the map, they could have
theoretically completed the map twice.

This is a dangerous assumption to make because Assault is a map type subject to attacker snowballs
and massive defender advantages. There is absolutely no guarantee that an attacking teams capture rate would stay constant,
and a more accurate model could be generated for this relationship using extra rounds pushes and time banks, but for this
tutorial we are going to keep things simple. 

Another design decision we are making is to ignore any extra rounds of the map. From the point of view of this system,
if both teams complete the map in overtime, they will each receive a map score of 1.0. If they were able to capture with
time remaining then that banked time will be multiplied by the teams capture rate and added to the score. We are ignoring
extra rounds for a handful of reasons such as removing the complications of overtime rules and simplifying the view of the game.
By making this simplification we are also attempting to reduce the game to it's simplest and most often occurring state. 
We do not need to account for any randomness introduced by overtime spawns, stall strategies, and we can look solely at the base game. 
Obviously there is data lost by doing this, and it could harm the performance of our model, but we can explore those in a future iteration of the model.

One of the limitations of the input data is that partial captures are not provided. From the point of view of the data 
overwatch league provides us, a team that captures 99.9% of a control point got the same amount of progress as a team
that never even touched the point. Unfortunately there is nothing we can do about this and accept any bias and error this
lack of data introduces.

##### 1.1.1 Assault Map Score Examples 
Below I will provide a handful of sample matches, a look at the input rows, and the resulting map score.
###### Shanghai Dragons V Hangzhou Spark On Hanamura 2021-07-10
```
 round_start_time       round_end_time     stage  match_id  game_number      match_winner        map_winner       map_loser  map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name          attacker          defender   team_one_name     team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
8  2021-07-10 13:01:45  2021-07-10 13:09:08  OWL 2021     37315            2  Shanghai Dragons  Shanghai Dragons  Hangzhou Spark  Hanamura          1                             2                            1                 NaN  Shanghai Dragons    Hangzhou Spark  Hangzhou Spark  Shanghai Dragons                        0.0                        0.0                   0.0                   0.0                        NaN                        NaN                         1                         0  Assault  2021/07/10   2021
9  2021-07-10 13:10:39  2021-07-10 13:18:35  OWL 2021     37315            2  Shanghai Dragons  Shanghai Dragons  Hangzhou Spark  Hanamura          2                             2                            1                 NaN    Hangzhou Spark  Shanghai Dragons  Hangzhou Spark  Shanghai Dragons                        0.0                        0.0                   0.0                   0.0                        NaN                        NaN                         1                         2  Assault  2021/07/10   2021
```
In this game ShangHai attacked first, partially captured point 2 but did not complete the map. Then on defense they 
allowed HangZhou to capture the first point and not gain enough capture progress on the second point to win the map.
This resulted in a ShangHai victory 2-1.

Using our map score calculations we generate the following results:
```
team 1:  Hangzhou Spark
team 1 time 480
team 1 time banked 0.0
team 1 time used 480.0
team 1 points 1
team 1 rate:  0.0020833333333333333
team 1 points added:  0.0
team 1 score 0.5

team 2:  Shanghai Dragons
team 2 time 480
team 2 time banked 0.0
team 2 time used 480.0
team 2 points 2
team 2 rate:  0.004166666666666667
team 2 points added:  0.0
team 2 score 1.0
```

###### Shanghai Dragons V New York Excelsior On Volskaya Industries 2021-07-11
```
      round_start_time       round_end_time     stage  match_id  game_number      match_winner        map_winner           map_loser             map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name            attacker            defender       team_one_name     team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
2  2021-07-11 09:31:36  2021-07-11 09:33:45  OWL 2021     37406            2  Shanghai Dragons  Shanghai Dragons  New York Excelsior  Volskaya Industries          1                             3                            2                 NaN    Shanghai Dragons  New York Excelsior  New York Excelsior  Shanghai Dragons                        0.0                        0.0            290.697998              0.000000                        NaN                        NaN                         2                         0  Assault  2021/07/11   2021
3  2021-07-11 09:35:16  2021-07-11 09:40:56  OWL 2021     37406            2  Shanghai Dragons  Shanghai Dragons  New York Excelsior  Volskaya Industries          2                             3                            2                 NaN  New York Excelsior    Shanghai Dragons  New York Excelsior  Shanghai Dragons                        0.0                        0.0             80.251022            290.697998                        NaN                        NaN                         2                         2  Assault  2021/07/11   2021
4  2021-07-11 09:42:22  2021-07-11 09:44:00  OWL 2021     37406            2  Shanghai Dragons  Shanghai Dragons  New York Excelsior  Volskaya Industries          3                             3                            2                 NaN  New York Excelsior    Shanghai Dragons  New York Excelsior  Shanghai Dragons                        0.0                        0.0              0.000000            290.697998                        NaN                        NaN                         2                         2  Assault  2021/07/11   2021
5  2021-07-11 09:45:27  2021-07-11 09:46:13  OWL 2021     37406            2  Shanghai Dragons  Shanghai Dragons  New York Excelsior  Volskaya Industries          4                             3                            2                 NaN    Shanghai Dragons  New York Excelsior  New York Excelsior  Shanghai Dragons                        0.0                        0.0            244.712006              0.000000                        NaN                        NaN                         3                         2  Assault  2021/07/11   2021
```
In this game ShangHai attacked first and completed the map with 290 seconds in the time bank. Then on defense they 
allowed New York to complete the map with 90 seconds in the time bank. In extra rounds, ShangHai prevented New York from
capping and then met the win condition on the first point with 244 seconds remaining.
Using our map score calculations and ignoring everything that happened in the extra rounds we generate the following results:
```
team 1:  New York Excelsior
team 1 time 480
team 1 time banked 80.25102233886719
team 1 time used 399.7489776611328
team 1 points 2
team 1 rate:  0.005003139749604062
team 1 points added:  0.40150707980995
team 1 score 1.200753539904975

team 2:  Shanghai Dragons
team 2 time 480
team 2 time banked 290.697998046875
team 2 time used 189.302001953125
team 2 points 2
team 2 rate:  0.010565128627087845
team 2 points added:  3.0712617410021656
team 2 score 2.535630870501083
```

###### Los Angeles Gladiators V Atlanta Reign On Temple of Anubis 2021-07-12
```
       round_start_time       round_end_time     stage  match_id  game_number   match_winner              map_winner      map_loser          map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name                attacker                defender           team_one_name  team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
0  2021-07-12 00:29:55  2021-07-12 00:34:19  OWL 2021     37411            2  Atlanta Reign  Los Angeles Gladiators  Atlanta Reign  Temple of Anubis          1                             1                            0                 NaN           Atlanta Reign  Los Angeles Gladiators  Los Angeles Gladiators  Atlanta Reign                        0.0                        0.0               0.00000                   0.0                        NaN                        NaN                         0                         0  Assault  2021/07/12   2021
1  2021-07-12 00:35:50  2021-07-12 00:37:00  OWL 2021     37411            2  Atlanta Reign  Los Angeles Gladiators  Atlanta Reign  Temple of Anubis          2                             1                            0                 NaN  Los Angeles Gladiators           Atlanta Reign  Los Angeles Gladiators  Atlanta Reign                        0.0                        0.0             170.45401                   0.0                        NaN                        NaN                         1                         0  Assault  2021/07/12   2021

```
In this game Atlanta attacked first and did not fully capture the first point. Then on defense they 
allowed Los Angeles to capture enough of the point to meet their win condition with 170 seconds of time banked.
Using our map score calculations we generate the following results:
```
team 1:  Los Angeles Gladiators
team 1 time 240
team 1 time banked 170.45401000976562
team 1 time used 69.54598999023438
team 1 points 1
team 1 rate:  0.014378974260635584
team 1 points added:  2.45095382255254
team 1 score 1.72547691127627

team 2:  Atlanta Reign
team 2 time 240
team 2 time banked 0.0
team 2 time used 240.0
team 2 points 0
team 2 rate:  0.0
team 2 points added:  0.0
team 2 score 0.0
```

###### Los Angeles Gladiators V Boston Uprising On Hanamura 2021-07-11
```
      round_start_time       round_end_time     stage  match_id  game_number            match_winner              map_winner        map_loser  map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name                attacker                defender    team_one_name           team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
6  2021-07-11 21:12:39  2021-07-11 21:14:55  OWL 2021     37413            2  Los Angeles Gladiators  Los Angeles Gladiators  Boston Uprising  Hanamura          1                             2                            0                 NaN  Los Angeles Gladiators         Boston Uprising  Boston Uprising  Los Angeles Gladiators                        0.0                        0.0            283.992035              0.000000                        NaN                        NaN                         2                         0  Assault  2021/07/11   2021
7  2021-07-11 21:16:27  2021-07-11 21:20:58  OWL 2021     37413            2  Los Angeles Gladiators  Los Angeles Gladiators  Boston Uprising  Hanamura          2                             2                            0                 NaN         Boston Uprising  Los Angeles Gladiators  Boston Uprising  Los Angeles Gladiators                        0.0                        0.0              0.000000            283.992035                        NaN                        NaN                         0                         2  Assault  2021/07/11   2021

```
In this game Los Angeles attacked first and completed the map with 284 seconds of time banked. Then on defense they 
did not allow Boston to capture the first point.
Using our map score calculations we generate the following results:
```
team 1:  Boston Uprising
team 1 time 240
team 1 time banked 0.0
team 1 time used 240.0
team 1 points 0
team 1 rate:  0.0
team 1 points added:  0.0
team 1 score 0.0

team 2:  Los Angeles Gladiators
team 2 time 480
team 2 time banked 283.9920349121094
team 2 time used 196.00796508789062
team 2 points 2
team 2 rate:  0.010203666973957887
team 2 points added:  2.8977601474997856
team 2 score 2.448880073749893
```

#### 1.2 Escort Map Score
The basic idea behind our calculation for map score on Escort is very similar to what it is on Assault,  
`How many times could you complete the map in at the rate at which you initially completed the map`.    
The main difference is that we are provided payload distances, so we can determine how much of the map a team completed in finer detail than we can with Assault.
Like with Assault we will not be considering any payload progress in extra rounds and if the attacking team completes the map with time banked,
the rate at which they pushed the payload will be multiplied by the time banked and added to the total distance traveled. 
This method introduces all the same biases and errors as stated above but will keep our methodology consistent between game modes.

##### 1.2.1 Escort Map Score Examples 
Below I will provide a handful of sample matches, a look at the input rows, and the resulting map score.

###### Houston Outlaws V San Francisco Shock On Junkertown 2021-07-03
```
      round_start_time       round_end_time     stage  match_id  game_number     match_winner       map_winner            map_loser    map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name             attacker             defender        team_one_name    team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
2  2021-07-03 22:45:04  2021-07-03 22:53:18  OWL 2021     37302            2  Houston Outlaws  Houston Outlaws  San Francisco Shock  Junkertown          1                             6                            5                 NaN      Houston Outlaws  San Francisco Shock  San Francisco Shock  Houston Outlaws                 101.902588                   0.000000              0.000000              0.000000                        NaN                        NaN                         3                         0   Escort  2021/07/03   2021
3  2021-07-03 22:54:49  2021-07-03 23:00:32  OWL 2021     37302            2  Houston Outlaws  Houston Outlaws  San Francisco Shock  Junkertown          2                             6                            5                 NaN  San Francisco Shock      Houston Outlaws  San Francisco Shock  Houston Outlaws                 101.902588                 101.902588            197.912994             60.000000                        NaN                        NaN                         3                         3   Escort  2021/07/03   2021
4  2021-07-03 23:01:58  2021-07-03 23:04:57  OWL 2021     37302            2  Houston Outlaws  Houston Outlaws  San Francisco Shock  Junkertown          3                             6                            5                 NaN      Houston Outlaws  San Francisco Shock  San Francisco Shock  Houston Outlaws                   6.191345                 101.902588              0.000000            197.912994                        NaN                        NaN                         5                         3   Escort  2021/07/03   2021
5  2021-07-03 23:06:23  2021-07-03 23:11:42  OWL 2021     37302            2  Houston Outlaws  Houston Outlaws  San Francisco Shock  Junkertown          4                             6                            5                 NaN  San Francisco Shock      Houston Outlaws  San Francisco Shock  Houston Outlaws                   1.246674                   6.191345              0.000000              0.000000                        NaN                        NaN                         5                         6   Escort  2021/07/03   2021
```
In this game Houston attacked first, and completed the map in overtime. Then on defense they 
allowed San Francisco to complete the map with 137 seconds banked. Due to overtime rules this was increased to 197 seconds
and Houston was provided with 60 additional seconds. In overtime Houston beat San Francisco, however due to our assumptions, San Fransisco
will end up with a higher map score. This is a place where more research is needed. In my initial exploration of the data,
teams with larger time banks win in extra rounds about 62% of the time, which means changing this assumption could be some
low-hanging fruit for improvement.

Using our map score calculations we generate the following results:
```
total map distance  366.6735000610351
team 1:  San Francisco Shock
team 1 time 480.0
team 1 time banked 197.9129943847656
team 1 points 3
team 1 total distance traveled 356.9410705566406
team 1 rate:  1.2653580755276155
team 1 distance added:  250.43080569661475
team 1 score 1.6564378831635078

team 2:  Houston Outlaws
team 2 time 480.0
team 2 time banked 60.0
team 2 points 3
team 2 total distance traveled 356.9410705566406
team 2 rate:  0.8498596918015253
team 2 distance added:  50.99158150809152
team 2 score 1.1125228629743606
```

###### Paris Eternal V Vancouver Titans On Junkertown 2021-07-03
```
      round_start_time       round_end_time     stage  match_id  game_number   match_winner     map_winner         map_loser    map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name          attacker          defender     team_one_name  team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
6  2021-07-03 19:25:19  2021-07-03 19:36:14  OWL 2021     37304            2  Paris Eternal  Paris Eternal  Vancouver Titans  Junkertown          1                             3                            0                 NaN     Paris Eternal  Vancouver Titans  Vancouver Titans  Paris Eternal                 101.871811                   0.000000             14.005005              0.000000                        NaN                        NaN                         3                         0   Escort  2021/07/03   2021
7  2021-07-03 19:37:45  2021-07-03 19:42:08  OWL 2021     37304            2  Paris Eternal  Paris Eternal  Vancouver Titans  Junkertown          2                             3                            0                 NaN  Vancouver Titans     Paris Eternal  Vancouver Titans  Paris Eternal                  66.126717                 101.871811              0.000000             14.005005                        NaN                        NaN                         0                         3   Escort  2021/07/03   2021
```
In this map Paris attacked first and completed the map with 14 seconds of time banked. They then went on to only allow Vancouver
to push the payload 66 meters and prevented the team from capturing the first point.

Using our map score calculations we generate the following results:
```
total map distance  366.6735000610351
team 1:  Vancouver Titans
team 1 time 240
team 1 time banked 0.0
team 1 points 0
team 1 total distance traveled 66.12671661376953
team 1 rate:  0.2755279858907064
team 1 distance added:  0.0
team 1 score 0.18034222981143258

team 2:  Paris Eternal
team 2 time 480.0
team 2 time banked 14.0050048828125
team 2 points 3
team 2 total distance traveled 356.91029357910156
team 2 rate:  0.7659101434970272
team 2 distance added:  10.72657529947149
team 2 score 1.0026273205382379
```

###### Los Angeles Gladiators V Atlanta Reign On Watchpoint: Gibraltar 2021-07-12
```
      round_start_time       round_end_time     stage  match_id  game_number   match_winner              map_winner      map_loser               map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name                attacker                defender           team_one_name  team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
0  2021-07-12 00:59:57  2021-07-12 01:04:22  OWL 2021     37411            4  Atlanta Reign  Los Angeles Gladiators  Atlanta Reign  Watchpoint: Gibraltar          1                             1                            0                 NaN           Atlanta Reign  Los Angeles Gladiators  Los Angeles Gladiators  Atlanta Reign                  86.077660                    0.00000              0.000000                   0.0                        NaN                        NaN                         0                         0   Escort  2021/07/12   2021
1  2021-07-12 01:05:53  2021-07-12 01:09:33  OWL 2021     37411            4  Atlanta Reign  Los Angeles Gladiators  Atlanta Reign  Watchpoint: Gibraltar          2                             1                            0                 NaN  Los Angeles Gladiators           Atlanta Reign  Los Angeles Gladiators  Atlanta Reign                  86.086342                   86.07766             20.034012                   0.0                        NaN                        NaN                         1                         0   Escort  2021/07/12   2021
```
In this map Atlanta attacked first and was only able to push the cart 86 meters without capturing the first point. They then went on to only allow Los Angeles
to push the payload 86  meters and meet their win condition with 20 seconds of time banked.

Using our map score calculations we generate the following results:
```
total map distance  366.6735000610351
team 1:  Los Angeles Gladiators
team 1 time 240
team 1 time banked 20.034011840820312
team 1 points 1
team 1 total distance traveled 213.60558319091797
team 1 rate:  0.9710845980258594
team 1 distance added:  19.4547203352883
team 1 score 0.6356071641048833

team 2:  Atlanta Reign
team 2 time 240
team 2 time banked 0.0
team 2 points 0
team 2 total distance traveled 86.0776596069336
team 2 rate:  0.35865691502888997
team 2 distance added:  0.0
team 2 score 0.23475287849437013
```


#### 1.3 Hybrid Map Score
Hybrid uses the almost exact same scoring system as described by [Escort Map Score](#12-escort-map-score). The only change
is that there is no partial progress recorded for the first capture point, and when a team captures the first capture point, they are
rewarded a distance equal to the distance between the first and second capture point. For example the distance between 
the first and second points on Blizzard World is 127 meters, so if a team captures point A on Blizzard World 
they are given credit for 127 meters of cart progress,

##### 1.1.1 Hybrid Map Score Examples 
Below I will provide a handful of sample matches, a look at the input rows, and the resulting map score.
###### San Francisco Shock V Toronto Defiant On Hollywood 2021-05-29
```
      round_start_time       round_end_time     stage  match_id  game_number         match_winner           map_winner        map_loser   map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name             attacker             defender    team_one_name        team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
6  2021-05-29 21:20:21  2021-05-29 21:26:28  OWL 2021     37269            4  San Francisco Shock  San Francisco Shock  Toronto Defiant  Hollywood          1                             3                            1                 NaN  San Francisco Shock      Toronto Defiant  Toronto Defiant  San Francisco Shock                  79.113937                   0.000000            112.649017              0.000000                        NaN                        NaN                         3                         0   Hybrid  2021/05/29   2021
7  2021-05-29 21:27:59  2021-05-29 21:34:37  OWL 2021     37269            4  San Francisco Shock  San Francisco Shock  Toronto Defiant  Hollywood          2                             3                            1                 NaN      Toronto Defiant  San Francisco Shock  Toronto Defiant  San Francisco Shock                  66.239693                  79.113937              0.000000            112.649017                        NaN                        NaN                         1                         3   Hybrid  2021/05/29   2021
```
In this game San Francisco attacked first and completed the map with 112 seconds banked. Then on defense allowed Toronto 
to capture the first point and push the payload 66 meters towards the second point.

Using our map score calculations we generate the following results:
```
total map distance  366.6735000610351
team 1:  Toronto Defiant
team 1 time 390.0
team 1 time banked 0.0
team 1 points 1
team 1 total distance traveled 193.7589340209961
team 1 rate:  0.49681777954101564
team 1 distance added:  0.0
team 1 score 0.5284236084384165

team 2:  San Francisco Shock
team 2 time 480.0
team 2 time banked 112.64901733398438
team 2 points 3
team 2 total distance traveled 334.1524200439453
team 2 rate:  0.909627129942229
team 2 distance added:  102.46860232832462
team 2 score 1.190762414790247
```
###### Atlanta Reign V Los Angeles Gladiators On King's Row 2021-07-12
```
      round_start_time       round_end_time     stage  match_id  game_number         match_winner           map_winner        map_loser   map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name             attacker             defender    team_one_name        team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
0  2021-07-12 00:44:37  2021-07-12 00:48:52  OWL 2021     37411            3  Atlanta Reign  Atlanta Reign  Los Angeles Gladiators  King's Row          1                             1                            0                 NaN  Los Angeles Gladiators           Atlanta Reign  Atlanta Reign  Los Angeles Gladiators                        0.0                        0.0              0.000000                   0.0                        NaN                        NaN                         0                         0   Hybrid  2021/07/12   2021
1  2021-07-12 00:50:23  2021-07-12 00:51:48  OWL 2021     37411            3  Atlanta Reign  Atlanta Reign  Los Angeles Gladiators  King's Row          2                             1                            0                 NaN           Atlanta Reign  Los Angeles Gladiators  Atlanta Reign  Los Angeles Gladiators                        0.0                        0.0            154.753006                   0.0                        NaN                        NaN                         1                         0   Hybrid  2021/07/12   2021
```
In this game Los Angeles attacked first and were not able to fully capture the first point. Atlanta then captured enough
of the control point to reach their win condition with 154 seconds banked.

Using our map score calculations we generate the following results:
```
total map distance  366.6735000610351
team 1:  Atlanta Reign
team 1 time 240
team 1 time banked 154.7530059814453
team 1 time used 85.24699401855469
team 1 points 1
team 1 total distance traveled 127.5192413330078
team 1 rate:  1.4958796236879885
team 1 distance added:  231.49186835210946
team 1 score 0.9791029611503357

team 2:  Los Angeles Gladiators
team 2 time 240
team 2 time banked 0.0
team 2 time used 240.0
team 2 points 0
team 2 total distance traveled 0.0
team 2 rate:  0.0
team 2 distance added:  0.0
team 2 score 0.0
```

###### Atlanta Reign V Los Angeles Gladiators On King's Row 2021-07-12
```
       round_start_time       round_end_time     stage  match_id  game_number            match_winner              map_winner        map_loser    map_name  map_round  winning_team_final_map_score  losing_team_final_map_score  control_round_name                attacker                defender    team_one_name           team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
2  2021-07-11 21:29:06  2021-07-11 21:33:49  OWL 2021     37413            3  Los Angeles Gladiators  Los Angeles Gladiators  Boston Uprising  King's Row          1                             4                            3                 NaN  Los Angeles Gladiators         Boston Uprising  Boston Uprising  Los Angeles Gladiators                   70.28952                    0.00000            197.097015              0.000000                        NaN                        NaN                         3                         0   Hybrid  2021/07/11   2021
3  2021-07-11 21:35:20  2021-07-11 21:41:48  OWL 2021     37413            3  Los Angeles Gladiators  Los Angeles Gladiators  Boston Uprising  King's Row          2                             4                            3                 NaN         Boston Uprising  Los Angeles Gladiators  Boston Uprising  Los Angeles Gladiators                   70.28952                   70.28952             92.700035            197.097015                        NaN                        NaN                         3                         3   Hybrid  2021/07/11   2021
4  2021-07-11 21:43:14  2021-07-11 21:45:16  OWL 2021     37413            3  Los Angeles Gladiators  Los Angeles Gladiators  Boston Uprising  King's Row          3                             4                            3                 NaN         Boston Uprising  Los Angeles Gladiators  Boston Uprising  Los Angeles Gladiators                    0.00000                   70.28952              0.000000            197.097015                        NaN                        NaN                         3                         3   Hybrid  2021/07/11   2021
5  2021-07-11 21:46:42  2021-07-11 21:47:55  OWL 2021     37413            3  Los Angeles Gladiators  Los Angeles Gladiators  Boston Uprising  King's Row          4                             4                            3                 NaN  Los Angeles Gladiators         Boston Uprising  Boston Uprising  Los Angeles Gladiators                    0.00000                    0.00000            123.880020              0.000000                        NaN                        NaN                         4                         3   Hybrid  2021/07/11   2021
```
In this game Los Angeles attacked first and completed the map with 197 seconds banked. Boston then went on to attack and complete the map with 92 seconds banked.
Boston then failed to capture the first point in extra rounds and Los Angeles met their win condition with 123 seconds banked.

Using our map score calculations we generate the following results:
```
total map distance  366.6735000610351
team 1:  Boston Uprising
team 1 time 480.0
team 1 time banked 92.70003509521484
team 1 points 3
team 1 total distance traveled 325.3280029296875
team 1 rate:  0.8399897557689348
team 1 distance added:  77.8670798394012
team 1 score 1.099602460232262

team 2:  Los Angeles Gladiators
team 2 time 480.0
team 2 time banked 197.09701538085935
team 2 points 3
team 2 total distance traveled 325.3280029296875
team 2 rate:  1.1499631344210162
team 2 distance added:  226.65430159240026
team 2 score 1.50537823003355
```

#### 1.4 Control Map Score
Control is a very different map type than the others in that teams play a first to two series across 3 separate stages.
The map score for each control map is simply calculated as the sum of  each team's score across all stages divided by
the total score required to win the map (200). The only downside to this method is that it can result in the possibility 
of the losing team having a significantly higher map score than the winner. 
If Team A wins stages 1 and 3 100-99 and loses stage 2 100-0 Team A would have a map score of 1.0 while Team B would
have a map score of 1.49. This edge case is consistent with our scoring in previous sections.

##### 1.4.1 Control Map Score Examples 
Below I will provide a handful of sample matches, a look at the input rows, and the resulting map score.
###### San Francisco Shock V Dallas Fuel On Ilios 2021-05-30
```
      round_start_time       round_end_time     stage  match_id  game_number         match_winner           map_winner    map_loser map_name  map_round  winning_team_final_map_score  losing_team_final_map_score control_round_name     attacker             defender team_one_name        team_two_name  attacker_payload_distance  defender_payload_distance  attacker_time_banked  defender_time_banked  attacker_control_perecent  defender_control_perecent  attacker_round_end_score  defender_round_end_score map_type  match_date season
0  2021-05-30 23:13:05  2021-05-30 23:16:55  OWL 2021     37265            5  San Francisco Shock  San Francisco Shock  Dallas Fuel    Ilios          1                             2                            1               Well  Dallas Fuel  San Francisco Shock   Dallas Fuel  San Francisco Shock                        0.0                        0.0                   0.0                   0.0                          0                        100                         0                         1  Control  2021/05/30   2021
1  2021-05-30 23:17:40  2021-05-30 23:23:26  OWL 2021     37265            5  San Francisco Shock  San Francisco Shock  Dallas Fuel    Ilios          2                             2                            1              Ruins  Dallas Fuel  San Francisco Shock   Dallas Fuel  San Francisco Shock                        0.0                        0.0                   0.0                   0.0                        100                         99                         1                         1  Control  2021/05/30   2021
2  2021-05-30 23:24:12  2021-05-30 23:29:31  OWL 2021     37265            5  San Francisco Shock  San Francisco Shock  Dallas Fuel    Ilios          3                             2                            1         Lighthouse  Dallas Fuel  San Francisco Shock   Dallas Fuel  San Francisco Shock                        0.0                        0.0                   0.0                   0.0                         99                        100                         1                         2  Control  2021/05/30   2021

```
In this map Shock won the first and third stages (Well and Lighthouse) and Dallas won the second stage (Ruins)
Using our map score calculations we generate the following results:
```
team 1:  Dallas Fuel
team 1 score 0.995

team 2:  San Francisco Shock
team 2 score 1.495
```

### 2. Calculating Map Score Added

Now that we have created a method for scoring each map type we want to be able to build a model to predict how two teams
playing against each other on that map type would perform. To do this we are going to attempt to use a method that is
commonly used in traditional team sports for assigning credit/blame to each player using only the players involved in
an event, and the outcome of the event. In our case instead of players we will be using teams. This is because Overwatch League
teams do not perform substitutions often enough to overcome multicolinearity. I plan to explore this subject in a later tutorial.  
  
The method we will be using to assign credit is regularized linear regression. We will build a sparse design matrix with 40 columns, 
an attacking and defending column for each team in Overwatch League. Each row will represent a single map played, the attacking team will
be represented by a 1, the defending team by a -1 and all other columns will be filled with 0s. Our target variable will be the map score
for that stage of the map. Below is an example of a row from our map score data and it's resulting row in our regression input.  
  
Map Score
```
   match_id  game_number map_name map_type      map_winner  match_date        team_one_name        team_two_name  team_one_score  team_two_score  season
0     37147            1    Busan  Control     Dallas Fuel  2021/05/02      Houston Outlaws          Dallas Fuel           0.495           1.000    2021
```
Input to regression
```
X = [ 0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.]
Y = [0.495]
```

Once we have built our design matrix and target array we can run our regression and attempt to generate an attack and defense coefficient for each team on each game mode.

There are some important things to note when reading the below results. Errors are not indicative of a prediction of which team will win the map but of
the predicted map score for the attacking team when playing against the defending team. In the next section we will perform an experiment to investigate 
how predictive Regularized Map Score Added is when attempting to predict the outcome of maps and matches.

Below are the results for the regression over the 2021 season up through the Summer Showdown Tournament.


#### 2.1 Control
Results:
```
                      team  Control rmsa attack  Control rmsa defend  Control rmsa  Control intercept
3              Dallas Fuel                0.121                0.093         0.214              0.783
16        Shanghai Dragons                0.090                0.086         0.176              0.783
15           Seoul Dynasty                0.016                0.090         0.106              0.783
9   Los Angeles Gladiators                0.071                0.024         0.096              0.783
0            Atlanta Reign                0.033                0.044         0.078              0.783
7          Houston Outlaws                0.017                0.046         0.063              0.783
19      Washington Justice                0.039                0.020         0.060              0.783
14     San Francisco Shock                0.044                0.004         0.048              0.783
2          Chengdu Hunters                0.024                0.014         0.038              0.783
1          Boston Uprising               -0.019                0.005        -0.014              0.783
13     Philadelphia Fusion                0.000               -0.020        -0.020              0.783
17         Toronto Defiant               -0.012               -0.011        -0.023              0.783
5         Guangzhou Charge                0.009               -0.037        -0.029              0.783
6           Hangzhou Spark               -0.036               -0.004        -0.040              0.783
4           Florida Mayhem               -0.027               -0.037        -0.064              0.783
12           Paris Eternal               -0.048               -0.030        -0.078              0.783
11      New York Excelsior               -0.057               -0.050        -0.107              0.783
18        Vancouver Titans               -0.073               -0.062        -0.134              0.783
8          London Spitfire               -0.080               -0.079        -0.159              0.783
10     Los Angeles Valiant               -0.114               -0.098        -0.212              0.783
```
Errors and CV Chosen Params
```
lambda:  0.05
intercept:  0.783

r^2:  0.105
MAE:  0.257
MSE:  0.103
```
#### 2.2 Assault
Results:
```
                      team  Assault rmsa attack  Assault rmsa defend  Assault rmsa  Assault intercept
16        Shanghai Dragons                0.197                0.247         0.444              1.116
3              Dallas Fuel                0.270                0.127         0.397              1.116
7          Houston Outlaws                0.098                0.167         0.266              1.116
14     San Francisco Shock                0.161                0.085         0.246              1.116
9   Los Angeles Gladiators                0.137                0.069         0.206              1.116
12           Paris Eternal                0.115                0.059         0.174              1.116
2          Chengdu Hunters                0.114                0.035         0.149              1.116
0            Atlanta Reign                0.059                0.048         0.107              1.116
19      Washington Justice               -0.010                0.082         0.072              1.116
15           Seoul Dynasty               -0.020                0.073         0.053              1.116
13     Philadelphia Fusion                0.079               -0.078         0.002              1.116
6           Hangzhou Spark                0.035               -0.143        -0.107              1.116
11      New York Excelsior               -0.132                0.013        -0.119              1.116
5         Guangzhou Charge               -0.097               -0.057        -0.155              1.116
4           Florida Mayhem               -0.173               -0.049        -0.222              1.116
17         Toronto Defiant               -0.148               -0.103        -0.251              1.116
8          London Spitfire               -0.070               -0.190        -0.260              1.116
1          Boston Uprising               -0.127               -0.186        -0.312              1.116
18        Vancouver Titans               -0.180               -0.153        -0.334              1.116
10     Los Angeles Valiant               -0.308               -0.046        -0.354              1.116
```
Errors and CV Chosen Params
```
lambda:  0.1
intercept:  1.116

r^2:  0.196
MAE:  0.524
RME:  0.441
```

#### 2.3 Escort
Results:
```
                      team  Escort rmsa attack  Escort rmsa defend  Escort rmsa  Escort intercept
13     Philadelphia Fusion               0.075               0.048        0.123             0.908
0            Atlanta Reign               0.032               0.058        0.090             0.908
11      New York Excelsior               0.022               0.060        0.082             0.908
2          Chengdu Hunters               0.030               0.045        0.075             0.908
9   Los Angeles Gladiators               0.054               0.021        0.075             0.908
14     San Francisco Shock               0.039               0.033        0.071             0.908
16        Shanghai Dragons               0.011               0.052        0.063             0.908
7          Houston Outlaws               0.048              -0.000        0.047             0.908
3              Dallas Fuel               0.048              -0.015        0.033             0.908
12           Paris Eternal               0.027               0.004        0.031             0.908
4           Florida Mayhem              -0.015               0.043        0.028             0.908
15           Seoul Dynasty              -0.018               0.005       -0.013             0.908
6           Hangzhou Spark              -0.018              -0.001       -0.019             0.908
1          Boston Uprising              -0.023              -0.011       -0.034             0.908
17         Toronto Defiant              -0.028              -0.038       -0.067             0.908
19      Washington Justice              -0.038              -0.034       -0.072             0.908
5         Guangzhou Charge              -0.037              -0.039       -0.076             0.908
8          London Spitfire              -0.039              -0.053       -0.091             0.908
18        Vancouver Titans              -0.081              -0.064       -0.146             0.908
10     Los Angeles Valiant              -0.087              -0.113       -0.200             0.908
```
Errors and CV Chosen Params
```
lambda:  0.2
intercept:  0.908

r^2:  0.112
MAE:  0.3
RME:  0.156
```

#### 2.4 Hybrid
Results:
```
                      team  Hybrid rmsa attack  Hybrid rmsa defend  Hybrid rmsa  Hybrid intercept
0            Atlanta Reign               0.116               0.092        0.208             0.926
1          Boston Uprising               0.212              -0.011        0.201             0.926
9   Los Angeles Gladiators               0.075               0.097        0.171             0.926
3              Dallas Fuel               0.081               0.086        0.167             0.926
6           Hangzhou Spark               0.176              -0.011        0.166             0.926
2          Chengdu Hunters               0.025               0.136        0.161             0.926
4           Florida Mayhem               0.132               0.014        0.146             0.926
16        Shanghai Dragons               0.046               0.088        0.135             0.926
7          Houston Outlaws               0.062               0.021        0.082             0.926
15           Seoul Dynasty               0.030               0.038        0.068             0.926
11      New York Excelsior               0.031              -0.024        0.007             0.926
13     Philadelphia Fusion               0.015              -0.013        0.002             0.926
14     San Francisco Shock               0.063              -0.099       -0.035             0.926
19      Washington Justice              -0.114               0.025       -0.089             0.926
5         Guangzhou Charge              -0.042              -0.089       -0.131             0.926
12           Paris Eternal              -0.150              -0.014       -0.164             0.926
8          London Spitfire              -0.137              -0.053       -0.190             0.926
18        Vancouver Titans              -0.225              -0.024       -0.249             0.926
17         Toronto Defiant              -0.167              -0.106       -0.273             0.926
10     Los Angeles Valiant              -0.228              -0.155       -0.383             0.926
```
Errors and CV Chosen Params
```
lambda:  0.075
intercept:  0.926

r^2:  0.185
MAE:  0.335
RME:  0.221
```

### 2.5 Total Map Score Added
The final thing we can do is attempt to create a power ranking by summing the RMSA for each game mode in a 5 map series. The results are shown below:
``` 
                      team  Total Rating  rank
0              Dallas Fuel         1.025   1.0
1         Shanghai Dragons         0.994   2.0
3   Los Angeles Gladiators         0.643   3.0
4            Atlanta Reign         0.561   4.0
5          Houston Outlaws         0.522   5.0
8          Chengdu Hunters         0.461   6.0
7      San Francisco Shock         0.377   7.0
2            Seoul Dynasty         0.320   8.0
10     Philadelphia Fusion         0.086   9.0
6       Washington Justice         0.030  10.0
13          Hangzhou Spark        -0.041  11.0
15           Paris Eternal        -0.115  12.0
9          Boston Uprising        -0.173  13.0
14          Florida Mayhem        -0.175  14.0
16      New York Excelsior        -0.245  15.0
12        Guangzhou Charge        -0.419  16.0
11         Toronto Defiant        -0.636  17.0
18         London Spitfire        -0.859  18.0
17        Vancouver Titans        -0.996  19.0
19     Los Angeles Valiant        -1.360  20.0
```

### 3.0 Predicting Map and Match Winners

In the previous section we showed the in sample map score prediction errors for each map played, but what we should really care about is how effective this
model is at predicting out of sample map winners. To do this we will split our data into a training set of all maps played in the May Melee and the June Joust and retrain our model.
We will then use our results to predict the winners of all maps in the Summer Showdown. The simple way to evaluate who will win is to take 
the attacker RMSA for team one, subtract the defender RMSA team two to get an estimate of the map score for team one. 
We then repeat the process for team two and compare to determine who will have a higher map score.
The code we used to do this exploration can be found [here](./team_rating_testing.py).

The results of this exploration is shown below:
```
Control Evaluation
Correctly Predicted: 102/140 (72.857%) Map results

Assault Evaluation
Correctly Predicted: 56/94 (59.574%) Map results

Hybrid Evaluation
Correctly Predicted: 56/92 (60.87%) Map results

Escort Evaluation
Correctly Predicted: 50/82 (60.976%) Map results
```

I also wrote code to test against match results for the Summer Showdown. I did this by determining the order of map type 
to be played in each match, and then simulated out the match, ending once a team got to 3 map wins using the same map win model as above.

Below are the results of that experiment:
```
The model correctly predicted 43 out of 52 matches (0.827%)
The model correctly predicted 23 out of 52 matches exactly (0.442%)

The model correctly predicted 34 out of 40 qualifier matches (0.85%)
The model correctly predicted 19 out of 40 qualifier matches exactly (0.475%)

The model would have scored 98.0 points if entered into the pickem challenge (This inclues double points matches but does not include knock out sunday or the tournament bracket)
```

### 4.0 Future Work
While working on this project I came across a couple of areas that I would like to explore further.
1. Is map score more predictive of future success than map win rate? Is it an actual predictive improvement?
2. The coefficients we generated for each team are point estimate with an underlying distribution behind them. This means that we can make a more complicated MCMC prediction model to attempt to determine map winners and match winners.
3. Build a match prediction engine. Given 2 teams and the order of game modes, predict who will win. Determine how well this system can predict final map score.
4. Extend this concept to players. I've done this in the past and found the lack of substitutions make it impossible to overcome multicolinearity, but it would still be interesting to explore