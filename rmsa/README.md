## An attempt at ranking the performance of a team in a season

In this "tutorial" we will attempt to generate a rating for each team that accounts who each team players and how dominant their win is. 
We will do this by coming up with a method for calculating a "map score" for each map played, then use regularized linear 
regression on a sparse team matrix in an attempt to give each team credit/blame for the result of the map.

Each game mode in Overwatch as a unique set of objects and mechanics. In order to account for that we need to develop a
separate scoring system for each game mode. We also need to account for any limitations and bias in the data provided to
us by Overwatch League. The input data we will use is in the [Match Map Stats File](./input/match_map_stats.csv). There
are other tutorials in this project for how to [Automate the Download of Statslab Data](../getting_data/README.md) and 
[Exploring the Statslab Data](../explore_data/README.md).

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### 0.1 Requirements
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
rewarded a distance equal to the distance between the first and second capture point. For exmaple the distance between 
the first and second points on Blizzard World is 127 meters, so if a team captures point A on Blizzard World 
they are given credit for 127 meters of cart progress,



