## Calculating Strength of Schedule for the 2021 OWL Season
Over the course of the 2021 Regular Season a number of people in the community have brought up issues with the
unbalanced schedule. After reading a number of posts, tweets and thoughts on the subject, I wanted to explore it for myself. 

In this exploration we will using [Regularized Map Score Added](../rmsa) to determine the strength of schedule
for each team in the Overwatch League this season. The script used to generate these results can be found [here](calculate_strength_of_schedule.py)

### 0.1 TLDR Final Results

| team | adjusted sos rank | adjusted sos | raw sos rank | raw sos |
| ---- | ------------- | ------------ | -------- | ------- |
Florida Mayhem     |       1.0     |   383.85   |    3.0  | 390.83
Atlanta Reign      |      2.0    |    371.32   |    6.0 |  283.21
London Spitfire      |      3.0    |    348.99   |    2.0 |  421.22
Dallas Fuel      |      4.0    |    340.76   |    9.0 |  263.76
Houston Outlaws      |      5.0    |    334.50   |    5.0 |  303.68
Los Angeles Gladiators      |      6.0    |    325.50   |    7.0 |  269.67
San Francisco Shock      |      7.0    |    303.13   |   10.0 |  252.94
Vancouver Titans      |      8.0    |    225.71   |    4.0 |  333.25
Boston Uprising      |      9.0    |    219.65   |   11.0 |  227.79
Shanghai Dragons      |     10.0    |    215.79   |   19.0 |   75.37
Toronto Defiant      |     11.0    |    188.99   |   14.0 |  182.72
Philadelphia Fusion      |     12.0    |    172.84   |   15.0 |  166.79
Seoul Dynasty      |     13.0    |    158.61   |   16.0 |  150.54
Washington Justice      |     14.0    |    155.78   |   13.0 |  191.51
Guangzhou Charge      |     15.0    |    143.76   |   12.0 |  224.69
Paris Eternal      |     16.0    |    137.23   |   17.0 |  149.50
Hangzhou Spark      |     17.0    |    133.96   |    8.0 |  264.68
Chengdu Hunters      |     18.0    |     87.29   |   20.0 |   10.21
Los Angeles Valiant      |     19.0    |    -20.77   |    1.0 |  431.21
New York Excelsior      |     20.0    |    -30.33   |   18.0 |  107.07

### 0.2 Requirements
The code in this tutorial was written in python 3.7 and uses the following libraries:
Pandas
sklearn

The environment.yml page for the entire project contains everything you need to run this script.

### 1.0 Calculating Strength of Schedule
At the time of this writeup, all the regular season games except for the Countdown Cup tournament match have been played.
Using the method we developed in the [RMSA tutorial](../rmsa) we can calculate a team rating for each team in the league. 
This rating accounts for the strength of your opponent in each match you play, so it should be more accurate than just
using map differential and win-loss record.

| team |  rmsa |
| ---- | ----- |
Los Angeles Gladiators |  74.22
Shanghai Dragons |  70.73
Dallas Fuel |  67.32
San Francisco Shock |  63.35
Atlanta Reign  | 63.03
Chengdu Hunters  | 50.41
Seoul Dynasty |  47.54
Houston Outlaws |  47.36
Philadelphia Fusion |  32.21
Washington Justice  |  8.81
Paris Eternal  |  5.00
New York Excelsior |   1.98
Florida Mayhem |  -0.61
Boston Uprising  | -0.68
Guangzhou Charge  | -3.93
Hangzhou Spark  | -9.53
Toronto Defiant | -12.30
London Spitfire | -46.43
Vancouver Titans  |-64.69
Los Angeles Valiant |-100.00

We can then naively sum up the ratings of every team on each teams schedule to get that teams strength of schedule.
From this you can see that arguably 4 of the 6 worst teams in the league played the hardest schedules, while some of the
best teams in the league played the easiest schedules.

| team | raw rank | raw sos |
| ---  | -------- | ------  |
Los Angeles Valiant   |    1.0 |  431.21
London Spitfire   |    2.0 |  421.22
Florida Mayhem   |    3.0 |  390.83
Vancouver Titans   |    4.0 |  333.25
Houston Outlaws    |   5.0  | 303.68
Atlanta Reign    |   6.0 |  283.21
Los Angeles Gladiators    |   7.0 |  269.67
Hangzhou Spark   |    8.0 |  264.68
Dallas Fuel   |    9.0 |  263.76
San Francisco Shock    |  10.0  | 252.94
Boston Uprising    |  11.0  | 227.79
Guangzhou Charge  |    12.0 |  224.69
Washington Justice   |   13.0  | 191.51
Toronto Defiant    |  14.0 |  182.72
Philadelphia Fusion    |  15.0 |  166.79
Seoul Dynasty    |  16.0 |  150.54
Paris Eternal   |   17.0  | 149.50
New York Excelsior    |  18.0 |  107.07
Shanghai Dragons   |   19.0 |   75.37
Chengdu Hunters    |  20.0  |  10.21

In recent discussions about strength of schedule, many people have pointed out that with due to the small sample sizes,
each team's own rating will impact their strength of schedule just due to the fact that the other teams all played that team. 

For example every team in APAC played Los Angeles Valiant twice and two teams played then three times. Because LAV were the worst
team in the league, beating them will artificially inflate all of their opponents team rating and thus drive up their
strength of schedule higher than it should be. 

I believe this issue is overstated using team rating like the ones we are using
in this write up that attempt to account for opponent strength, and thus give less credit for beating bad teams, but we 
should still explore this idea.

### Calculating Adjusted Strength of Schedule
In order to calculate "adjusted strength of schedule" for a team we want to remove all matches that team played in from
our dataset then recalculate our team ratings. We can then sum up the ratings for our removed team's schedule to get a new
strength of schedule. We then repeat this process for every team in the league.


##### Example: Florida Mayhem
We first remove every Florida Mayhem match from our list of scored maps and rerun the team ratings calculation. Below we
can see the ratings for every team in the league if Florida Mayhem were removed from the schedule

| team |   RMSA  |  team dropped |
| ---- | ------  | -----------   |
Shanghai Dragons |  79.96 | Florida Mayhem
Los Angeles Gladiators |  73.80 | Florida Mayhem
Dallas Fuel |  69.74 | Florida Mayhem
Atlanta Reign |  67.14 | Florida Mayhem
San Francisco Shock |  60.23 | Florida Mayhem
Chengdu Hunters |  59.29 | Florida Mayhem
Seoul Dynasty |  54.28 | Florida Mayhem
Houston Outlaws |  41.93 | Florida Mayhem
Philadelphia Fusion |  36.69 | Florida Mayhem
Paris Eternal |   7.17 | Florida Mayhem
New York Excelsior |   5.59 | Florida Mayhem
Washington Justice |   4.16 | Florida Mayhem
Boston Uprising |   1.27 | Florida Mayhem
Guangzhou Charge |   0.28 | Florida Mayhem
Toronto Defiant |  -4.20 | Florida Mayhem
Hangzhou Spark |  -5.87 | Florida Mayhem
London Spitfire | -51.58 | Florida Mayhem
Vancouver Titans | -70.05 | Florida Mayhem
Los Angeles Valiant | -100.00 | Florida Mayhem

We can then add up the RMSA for each team on Florida's schedule to generate a new adjusted strength of schedule

| team | RMSA | 
| ---- | -----  |
Atlanta Reign | 67.14
Vancouver Titans | -70.05
San Francisco Shock | 60.23
Paris Eternal | 7.17
London Spitfire | -51.58
Houston Outlaws | 41.93
Dallas Fuel | 69.74
Washington Justice | 4.16
Toronto Defiant | -4.2
Boston Uprising | 1.27
Dallas Fuel | 69.74
Washington Justice | 4.16
Atlanta Reign | 67.14
Boston Uprising | 1.27
Houston Outlaws | 41.93
Los Angeles Gladiators | 73.8
--- | ---
Total | 383.85

### Final Results

| team | adjusted sos rank | adjusted sos | raw sos rank | raw sos |
| ---- | ------------- | ------------ | -------- | ------- |
Florida Mayhem     |       1.0     |   383.85   |    3.0  | 390.83
Atlanta Reign      |      2.0    |    371.32   |    6.0 |  283.21
London Spitfire      |      3.0    |    348.99   |    2.0 |  421.22
Dallas Fuel      |      4.0    |    340.76   |    9.0 |  263.76
Houston Outlaws      |      5.0    |    334.50   |    5.0 |  303.68
Los Angeles Gladiators      |      6.0    |    325.50   |    7.0 |  269.67
San Francisco Shock      |      7.0    |    303.13   |   10.0 |  252.94
Vancouver Titans      |      8.0    |    225.71   |    4.0 |  333.25
Boston Uprising      |      9.0    |    219.65   |   11.0 |  227.79
Shanghai Dragons      |     10.0    |    215.79   |   19.0 |   75.37
Toronto Defiant      |     11.0    |    188.99   |   14.0 |  182.72
Philadelphia Fusion      |     12.0    |    172.84   |   15.0 |  166.79
Seoul Dynasty      |     13.0    |    158.61   |   16.0 |  150.54
Washington Justice      |     14.0    |    155.78   |   13.0 |  191.51
Guangzhou Charge      |     15.0    |    143.76   |   12.0 |  224.69
Paris Eternal      |     16.0    |    137.23   |   17.0 |  149.50
Hangzhou Spark      |     17.0    |    133.96   |    8.0 |  264.68
Chengdu Hunters      |     18.0    |     87.29   |   20.0 |   10.21
Los Angeles Valiant      |     19.0    |    -20.77   |    1.0 |  431.21
New York Excelsior      |     20.0    |    -30.33   |   18.0 |  107.07

Overall the strength of schedule for each team only changes slightly when you remove that team from the ratings calculation. 
This is likely because the team ratings we are using is already attempting to account for the strength of your opponents
and gives credit for quality wins while discounting wins over bad teams. The one major exception is the Los Angeles Valiant. 
They drop from having the hardest schedule in the league to having the second easiest schedule in the league when you remove them from consideration.
By looking at every team's raw RMSA and comparing it to their RMSA with LAV removed, it can be seen that every team in APAC
had their RMSA decrease. This means that even while attempting to account for opponent strength, raw RMSA is likely still too high
on the Valiant and are expecting them to perform better than they actually are. When you remove 2 or 3 matches where each team performs better than expected
from the calculation, their RMSA goes down, and it drags down the Valiant's Strength of Schedule.


| team | RMSA | raw RMSA | team dropped |
| ---- | ------ | ---------- | ------------ |
Los Angeles Gladiators|72.62 | 74.22 |Los Angeles Valiant
Shanghai Dragons|61.91 | 70.73 |Los Angeles Valiant
Atlanta Reign|61.11 | 63.03|Los Angeles Valiant
Dallas Fuel|59.0 | 67.32 |Los Angeles Valiant
San Francisco Shock|56.46 | 63.35 |Los Angeles Valiant
Houston Outlaws|37.74|47.36|Los Angeles Valiant
Chengdu Hunters|30.74|50.41|Los Angeles Valiant
Seoul Dynasty|26.69|47.54|Los Angeles Valiant
Philadelphia Fusion|12.45|32.21|Los Angeles Valiant
Washington Justice|-10.72|8.81|Los Angeles Valiant
Paris Eternal|-12.39|5.00|Los Angeles Valiant
Boston Uprising|-14.25|-0.68|Los Angeles Valiant
Florida Mayhem|-17.31|-0.61|Los Angeles Valiant
Toronto Defiant|-34.88| -12.30 |Los Angeles Valiant
New York Excelsior|-39.99|1.98|Los Angeles Valiant
Guangzhou Charge|-43.47| -3.93 |Los Angeles Valiant
Hangzhou Spark|-54.09| -9.53 |Los Angeles Valiant
London Spitfire|-74.79 | -46.43|Los Angeles Valiant
Vancouver Titans|-96.01| -64.69|Los Angeles Valiant