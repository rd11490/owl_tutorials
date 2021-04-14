## Calculate Team Elo across multiple seasons of Overwatch League

In this tutorial I will show you how to take the map result data from the StatsLab page on the Overwatch League page and use it to calculate the Elo rating for each team and game mode.

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### 0.1 Requirements
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
can all be used to determine who played in the map and who won. From this we also see that there is a row for each phase of each map.
Meaning there can be multipe rows per map. We will need to account for that when calculating Elo.

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


#### Building a map to look up Game Mode from Map Name

We can create a Maps class with constants for each map name, each game mode,
and a dictionary mapping the map name to the game mode.
This will come in handy when splitting maps between game modes later on.

```python
class Maps:
    Assault = 'Assault'
    Control = 'Control'
    Escort = 'Escort'
    Hybrid = 'Hybrid'

    Hanamura = 'Hanamura'
    HorizonLunarColony = 'Horizon Lunar Colony'
    Paris = 'Paris'
    TempleOfAnubis = 'Temple of Anubis'
    VolskayaIndustries = 'Volskaya Industries'
    Busan = 'Busan'
    Ilios = 'Ilios'
    LijiangTower = 'Lijiang Tower'
    Nepal = 'Nepal'
    Oasis = 'Oasis'
    Dorado = 'Dorado'
    Havana = 'Havana'
    Junkertown = 'Junkertown'
    Rialto = 'Rialto'
    Route66 = 'Route 66'
    Gibraltar = 'Watchpoint: Gibraltar'
    Numbani = 'Numbani'
    Eichenwalde = 'Eichenwalde'
    KingsRow = 'King\'s Row'
    Hollywood = 'Hollywood'
    BlizzardWorld = 'Blizzard World'

    game_mode = {
        Hanamura: Assault,
        HorizonLunarColony: Assault,
        Paris: Assault,
        TempleOfAnubis: Assault,
        VolskayaIndustries: Assault,

        Busan: Control,
        Ilios: Control,
        LijiangTower: Control,
        Nepal: Control,
        Oasis: Control,

        Dorado: Escort,
        Havana: Escort,
        Junkertown: Escort,
        Rialto: Escort,
        Route66: Escort,
        Gibraltar: Escort,

        Numbani: Hybrid,
        Eichenwalde: Hybrid,
        KingsRow: Hybrid,
        Hollywood: Hybrid,
        BlizzardWorld: Hybrid,
    }

```


### 2. Calculating Elo
Now that we have explored our data we can go about actually calculating each team's Elo for each game mode.
We will also want to provide a form of "decay" to each team's Elo between seasons.
If we were trying to build a robust model, we would likely base this decay factor off of something like team continuity,
regressing teams that changed dramatically back towards the initial value while allowing teams that remained mostly unchanged to remain where the finished the previous season.
In this tutorial we will naively decay every team back towards the initial value by 50%.

#### Basics behind the calculation

Each team playing has a rating Ra and Rb.
The expected score for each team can be calculated using the equation:
```
Ea = Qa / (Qa + Qb)
Where:
    Qa = 10 ^ (Ra/M)
    Qb = 10 ^ (Rb/M)


- Ea: Probability that Team A will win the map
- Rn: Elo of the team
- M: This is constant used to determine how many points of Elo represent a magnitude of 10 difference in win percentage.
```
Using the values generated for Ea and Eb we can then update the elo of each team after the map has been played useing the weight update rule:
```
Ra' = Ra + K(Sa - Ea)

- Ra': New Elo after updating
- Ra: Elo the team had before playing the match
- K: K-factor - The maximum value a teams rating can update after a match
- Sa: The result of the map (1 for a win, .5 for a draw, 0 for a loss)
- Ea: Probability that Team A will win the match (calculated above)
```

#### The Code:
Using the information we learned about our map results file and how to calculate Elo, we can now write a basic script to do this for us.
We will start the same way we always do by importing pandas, datetime and the Maps class we wrote above. We will also set a couple of basic pandas settings to make
printing dataframes more user friendly.
```python
import pandas as pd
import datetime
from calculating_elo.maps import Maps


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

```

We can start off by writing a couple of helper functions to determine the
game mode and the season in which the map took place. The `calc_game_mode`
function takes in a map name and looks up the game mode from the maps dictionary.
The `calc_season` function converts the datetime timestamp provided
with each row and extracts the year from the data. Because the league
season runs during the year and does not cross between multiple years, it is safe for us to just use the season year as the season of the match.

```python
# determine the game mode from map
def calc_game_mode(map_name):
    return Maps.game_modes[map_name]


# determine the season of the match
def calc_season(dt):
    parsed = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return parsed.date().strftime("%Y")
```


We then want to read in our map statistics csv into a dataframe and filter out the all-star games
```python
# Read in the csv
frame = pd.read_csv('map_data/match_map_stats.csv')


# Remove all-star matches
frame = frame[frame['stage'].str.contains('All-Stars') == False]
```

After that we want to add columns for season and game mode using the functions we created above.
```python
# add the game mode, date, and season to the frame
frame['game_mode'] = frame['map_name'].apply(calc_game_mode)
frame['season'] = frame['round_end_time'].apply(calc_season)
```
Now that we have our dataframe containing only OWL matches between actual OWL teams, we want to separate them out by game mode and select only the columns we care about.
We also need to limit ourselves to 1 row per map.

```python
# separate the frame into the different game modes
escort_maps = frame[frame['game_mode'] == Maps.Escort].copy()
assault_maps = frame[frame['game_mode'] == Maps.Assault].copy()
control_maps = frame[frame['game_mode'] == Maps.Control].copy()
hybrid_maps = frame[frame['game_mode'] == Maps.Hybrid].copy()

# select the columns we care about
escort_maps = escort_maps[['map_winner','team_one_name', 'team_two_name', 'season']].drop_duplicates()
assault_maps = assault_maps[['map_winner','team_one_name', 'team_two_name', 'season']].drop_duplicates()
hybrid_maps = hybrid_maps[['map_winner','team_one_name', 'team_two_name', 'season']].drop_duplicates()
control_maps = control_maps[['map_winner','team_one_name', 'team_two_name', 'season']].drop_duplicates()
```

In order to calculate elo, we need to set a couple of our constants.
We will set the initial elo to 2500, the maximum elo a team can earn in a match to 50, the decay between seasons to 50%, and the m value to 500.


```python
m = 500
initial_elo = 2500
k = 50
decay = .5
```


We need to write a function to calculate elo that we can apply to each of our four game mode dataframes.
The function will take in a dataframe with the columns `['map_winner','team_one_name', 'team_two_name', 'season']`,
initialize a dictionary where the key is the team name and the value is the `initial_elo` which is 2500 in this example.
We will then take the first season and store it so that we can check if the season changes. We then iterate over the index of the dataframe and
check to see if the season has changed. If the season changes we decay every team's elo. After that we update the elo for the two teams who played the map represented by the current row.
```python
def calculate_elo(match_frame):
    # Initialize the elo dictionary, set each team to 1500
    elo = {}
    for team in frame['team_one_name'].unique():
        elo[team] = [initial_elo]

    # storing the current season will allow us to determine when the season changes
    curr_season = match_frame.loc[match_frame.index[0], :]['season']
    # iterate over every row in the index
    for i in match_frame.index:
        # If the season changes we want to decay every team's elo back towards 1500 and reset the current season
        if match_frame.loc[i, :]['season'] != curr_season:
            elo = decay_elo(elo)
            curr_season = match_frame.loc[i, :]['season']

        # update each team's elo with the result of the map
        elo = update_elo(elo, match_frame.loc[i, :]['map_winner'], match_frame.loc[i, :]['team_one_name'],
                   match_frame.loc[i, :]['team_two_name'])
    return elo
```

You'll notice two functions in the above code that we have not written yet; the decay_elo function and the update_elo function. The update elo function is simple and straight forward.
We look up the elo from the elo dictionary for the two teams playing in the match. We then calculate the expected score, use the update rule to calculate the new elo, and append it back to our elo dictionary.


```python
def update_elo(elo, winner, team1, team2):
    elo1 = elo[team1][-1]
    elo2 = elo[team2][-1]



    q1 = 10 ** (elo1 / m)
    q2 = 10 ** (elo2 / m)
    e1 = q1 / (q1 + q2)
    e2 = q2 / (q1 + q2)

    if winner == 'draw':
        s1 = 0.5
        s2 = 0.5
    elif winner == team1:
        s1 = 1.0
        s2 = 0.0
    else:
        s1 = 0.0
        s2 = 1.0

    elo[team1].append(elo1 + k * (s1-e1))
    elo[team2].append(elo2 + k * (s2-e2))
    return elo
```

The decay_elo function is also simple and straight forward. We just itterate over the elo dictionary,
determine the difference between our initial elo and the team's current elo and subtract half of it from the current elo.

```python
# Take the difference between the current elo and 2500, reduce it by 50%, and adjust elo by that value.
# The idea is that between each season we want to regress each teams elo back towards neutral.
def decay_elo(teams_elo):
    new_elo = {}
    for team, elo in teams_elo.items():
        diff = teams_elo[team][-1] - initial_elo
        regress = diff * decay
        elo.append(elo[-1] - regress)
        new_elo[team] = elo
    return new_elo
```

Finally we want to write a helper function to conver the elo dictionary to a data frame and sort by elo in descending order.
```pyhton
# build a dataframe of the final Elo for each team and print
def print_standings(elo):
    print(pd.DataFrame([{'Team': k, 'Elo': round(v[-1], 2)} for k, v in elo.items()]).sort_values(by='Elo', ascending=False))

```

After having written all of the functions needed to calculate elo, we can now apply them to determine each team's elo by game mode.

```python
escort_elo_history = calculate_elo(escort_maps)
print('ESCORT MAP ELO')
print_standings(escort_elo_history)
print('\n')


control_elo_history = calculate_elo(control_maps)
print('CONTROL MAP ELO')
print_standings(control_elo_history)
print('\n')


assault_elo_history = calculate_elo(assault_maps)
print('ASSAULT MAP ELO')
print_standings(assault_elo_history)
print('\n')


hybrid_elo_history = calculate_elo(hybrid_maps)
print('HYBRID MAP ELO')
print_standings(hybrid_elo_history)
print('\n')

```

Running this will result in:
```
ESCORT MAP ELO
                      Team      Elo
8      Philadelphia Fusion  2611.75
11     San Francisco Shock  2605.72
17           Paris Eternal  2573.14
5           Florida Mayhem  2570.85
15         Chengdu Hunters  2570.81
9       New York Excelsior  2561.36
12          Hangzhou Spark  2555.63
2         Shanghai Dragons  2547.31
3            Seoul Dynasty  2533.72
14           Atlanta Reign  2529.59
6          London Spitfire  2489.61
0      Los Angeles Valiant  2475.37
18      Washington Justice  2472.75
7          Houston Outlaws  2471.62
1   Los Angeles Gladiators  2470.82
13         Toronto Defiant  2451.73
16        Guangzhou Charge  2441.09
4              Dallas Fuel  2399.71
19        Vancouver Titans  2390.38
10         Boston Uprising  2277.02


CONTROL MAP ELO
                      Team      Elo
11     San Francisco Shock  2673.14
8      Philadelphia Fusion  2615.54
1   Los Angeles Gladiators  2601.43
3            Seoul Dynasty  2599.53
16        Guangzhou Charge  2593.13
2         Shanghai Dragons  2590.48
12          Hangzhou Spark  2552.36
0      Los Angeles Valiant  2549.10
9       New York Excelsior  2523.65
5           Florida Mayhem  2505.39
17           Paris Eternal  2476.20
14           Atlanta Reign  2465.78
15         Chengdu Hunters  2460.64
13         Toronto Defiant  2434.89
4              Dallas Fuel  2429.64
18      Washington Justice  2423.69
7          Houston Outlaws  2411.15
6          London Spitfire  2405.83
19        Vancouver Titans  2398.07
10         Boston Uprising  2290.36


ASSAULT MAP ELO
                      Team      Elo
11     San Francisco Shock  2664.10
2         Shanghai Dragons  2652.30
16        Guangzhou Charge  2599.63
8      Philadelphia Fusion  2580.07
18      Washington Justice  2573.38
9       New York Excelsior  2552.81
17           Paris Eternal  2552.38
3            Seoul Dynasty  2550.51
15         Chengdu Hunters  2522.19
5           Florida Mayhem  2508.44
1   Los Angeles Gladiators  2481.62
14           Atlanta Reign  2480.08
0      Los Angeles Valiant  2477.49
6          London Spitfire  2453.91
12          Hangzhou Spark  2427.49
7          Houston Outlaws  2422.26
13         Toronto Defiant  2396.78
10         Boston Uprising  2385.03
4              Dallas Fuel  2375.87
19        Vancouver Titans  2343.65


HYBRID MAP ELO
                      Team      Elo
3            Seoul Dynasty  2638.82
11     San Francisco Shock  2636.49
8      Philadelphia Fusion  2623.39
16        Guangzhou Charge  2587.56
2         Shanghai Dragons  2569.22
15         Chengdu Hunters  2564.12
14           Atlanta Reign  2551.04
17           Paris Eternal  2547.96
9       New York Excelsior  2532.83
5           Florida Mayhem  2527.92
12          Hangzhou Spark  2524.52
1   Los Angeles Gladiators  2498.21
18      Washington Justice  2461.10
13         Toronto Defiant  2454.30
19        Vancouver Titans  2432.36
6          London Spitfire  2414.44
4              Dallas Fuel  2413.05
0      Los Angeles Valiant  2388.51
7          Houston Outlaws  2377.16
10         Boston Uprising  2257.00
```

The entirety of the code for calculating elo can be found [here](./elo.py)