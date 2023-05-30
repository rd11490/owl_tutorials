## Building a Balanced Schedule for the Second Half of 2023
The 2023 season of the Overwatch League returned to the dreaded 16-match format in the West, once again resulting in the 
possibility of unbalanced schedules. Luckily for fans, this season the league is going to try to balance schedules by 
using the first-half results to generate team ratings and then balance which teams will be played twice. 
I have concerns about how the league is going to go about doing this, using something naive like table placement 
or map differential, which are both impacted by the strength of schedule for the first half, so I wanted to take a stab at it myself. 
In this write-up, we are going to use the RMSA model results to generate team ratings and then use some basic optimization 
methods to build a schedule that is as balanced as possible.


In this exploration we will using [Regularized Map Score Added](../rmsa) to determine the strength of schedule
for each team in the Overwatch League this season. The script used to generate these results can be found [here](balance_schedule.py)

### 0.1 TLDR Final Results

| team                   | secondHalfOpponent1    | secondHalfOpponent2 | secondHalfOpponent3 | secondHalfOpponent4 | doubleOpponent1     | doubleOpponent2     | doubleOpponent3        | doubleOpponent4        | totalSOS |
|:-----------------------|:-----------------------|:--------------------|:--------------------|:--------------------|:--------------------|:--------------------|:-----------------------|:-----------------------|---------:|
| Atlanta Reign          | Florida Mayhem         | London Spitfire     | Toronto Defiant     | Washington Justice  | Vancouver Titans    | Los Angeles Valiant | Florida Mayhem         | Washington Justice     |      197 |
| Boston Uprising        | Los Angeles Gladiators | Florida Mayhem      | Los Angeles Valiant | Houston Outlaws     | Toronto Defiant     | London Spitfire     | New York Excelsior     | Houston Outlaws        |      200 |
| Florida Mayhem         | New York Excelsior     | Boston Uprising     | Atlanta Reign       | Washington Justice  | San Francisco Shock | Vegas Eternal       | Los Angeles Gladiators | Atlanta Reign          |      188 |
| Houston Outlaws        | New York Excelsior     | Boston Uprising     | Vegas Eternal       | Toronto Defiant     | London Spitfire     | New York Excelsior  | Los Angeles Gladiators | Boston Uprising        |      203 |
| London Spitfire        | San Francisco Shock    | New York Excelsior  | Los Angeles Valiant | Atlanta Reign       | Boston Uprising     | Houston Outlaws     | San Francisco Shock    | Los Angeles Valiant    |      195 |
| Los Angeles Gladiators | San Francisco Shock    | New York Excelsior  | Los Angeles Valiant | Boston Uprising     | Toronto Defiant     | Florida Mayhem      | Houston Outlaws        | Vegas Eternal          |      211 |
| Los Angeles Valiant    | Los Angeles Gladiators | Boston Uprising     | London Spitfire     | Vegas Eternal       | New York Excelsior  | Atlanta Reign       | Vancouver Titans       | London Spitfire        |      210 |
| New York Excelsior     | Los Angeles Gladiators | Florida Mayhem      | London Spitfire     | Houston Outlaws     | Los Angeles Valiant | Boston Uprising     | Houston Outlaws        | Vancouver Titans       |      201 |
| San Francisco Shock    | Los Angeles Gladiators | London Spitfire     | Vegas Eternal       | Vancouver Titans    | Florida Mayhem      | Washington Justice  | Vegas Eternal          | London Spitfire        |      200 |
| Toronto Defiant        | Atlanta Reign          | Washington Justice  | Houston Outlaws     | Vancouver Titans    | Boston Uprising     | Vegas Eternal       | Washington Justice     | Los Angeles Gladiators |      201 |
| Vancouver Titans       | San Francisco Shock    | Vegas Eternal       | Toronto Defiant     | Washington Justice  | Atlanta Reign       | Washington Justice  | Los Angeles Valiant    | New York Excelsior     |      201 |
| Vegas Eternal          | San Francisco Shock    | Los Angeles Valiant | Houston Outlaws     | Vancouver Titans    | Florida Mayhem      | Toronto Defiant     | San Francisco Shock    | Los Angeles Gladiators |      205 |
| Washington Justice     | Florida Mayhem         | Toronto Defiant     | Atlanta Reign       | Vancouver Titans    | Vancouver Titans    | Toronto Defiant     | San Francisco Shock    | Atlanta Reign          |      196 |


### 0.2 Requirements
The code in this tutorial was written in python 3.7 and uses the following libraries:
Pandas

The environment.yml page for the entire project contains everything you need to run this script.

### 1.0 Generating Balanced Schedules
In our schedule-making process, we need to make a few assumptions:
- Each team will play the four teams they did not face in the first half of the season.
- Each team will play a total of eight matches in the second half of the season.
- Two teams can play each other a maximum of two times in the season.
- Teams can play a team in the second half of the season twice.

With these constraints in mind, we can construct an initial schedule that may be unbalanced and then make adjustments to achieve balance.

We will begin with team ratings obtained from the RMSA model. These ratings are generated by simulating a complete 
round-robin of five games (Control, Hybrid, Escort, Push, Control) in the West region 10,000 times. 
The rating represents the percentage of matches each team wins during the simulation.

| rating | team |
|--------|------|
| 2      | VAL  |
| 7      | LVE  |
| 32     | TOR  |
| 35     | SFS  |
| 37     | VAN  |
| 38     | LDN  |
| 52     | GLA  |
| 52     | NYE  |
| 65     | WAS  |
| 66     | BOS  |
| 81     | FLA  |
| 88     | ATL  |
| 95     | HOU  |
 
Now that we have team ratings, we need to initialize the schedule. We will accomplish this using a brute force approach, 
primarily because I didn't invest the effort to implement a more efficient method, but also because it is effective. 
Here's how it works: we randomly select teams to play against each other while keeping track of the match count for each team.
We then verify the validity of each match by ensuring that neither team has been selected four times already and that the exact 
match hasn't been picked before. If a match is deemed invalid, it is disregarded, and a new match is randomly chosen. 
This process continues until all available matches have been exhausted. If we run out of valid matches before each team 
has played four times, the algorithm starts over from the beginning, repeating until a valid schedule is generated.

Below is a sample initial schedule created through this process.

| team                   | secondHalfOpponent1    | secondHalfOpponent2 | secondHalfOpponent3 | secondHalfOpponent4 | doubleOpponent1        | doubleOpponent2     | doubleOpponent3     | doubleOpponent4        | totalSOS |
|:-----------------------|:-----------------------|:--------------------|:--------------------|:--------------------|:-----------------------|:--------------------|:--------------------|:-----------------------|---------:|
| Atlanta Reign          | Florida Mayhem         | London Spitfire     | Toronto Defiant     | Washington Justice  | Los Angeles Gladiators | Vancouver Titans    | New York Excelsior  | Vegas Eternal          |      147 |
| Boston Uprising        | Los Angeles Gladiators | Florida Mayhem      | Los Angeles Valiant | Houston Outlaws     | Toronto Defiant        | New York Excelsior  | Washington Justice  | Vancouver Titans       |      183 |
| Florida Mayhem         | New York Excelsior     | Boston Uprising     | Atlanta Reign       | Washington Justice  | Vegas Eternal          | Toronto Defiant     | London Spitfire     | San Francisco Shock    |      113 |
| Houston Outlaws        | New York Excelsior     | Boston Uprising     | Vegas Eternal       | Toronto Defiant     | New York Excelsior     | Los Angeles Valiant | San Francisco Shock | London Spitfire        |      118 |
| London Spitfire        | San Francisco Shock    | New York Excelsior  | Los Angeles Valiant | Atlanta Reign       | Vancouver Titans       | Florida Mayhem      | New York Excelsior  | Houston Outlaws        |      256 |
| Los Angeles Gladiators | San Francisco Shock    | New York Excelsior  | Los Angeles Valiant | Boston Uprising     | Atlanta Reign          | Washington Justice  | Los Angeles Valiant | Vegas Eternal          |      168 |
| Los Angeles Valiant    | Los Angeles Gladiators | Boston Uprising     | London Spitfire     | Vegas Eternal       | Los Angeles Gladiators | Washington Justice  | San Francisco Shock | Houston Outlaws        |      252 |
| New York Excelsior     | Los Angeles Gladiators | Florida Mayhem      | London Spitfire     | Houston Outlaws     | Atlanta Reign          | Boston Uprising     | London Spitfire     | Houston Outlaws        |      284 |
| San Francisco Shock    | Los Angeles Gladiators | London Spitfire     | Vegas Eternal       | Vancouver Titans    | Florida Mayhem         | Vancouver Titans    | Los Angeles Valiant | Houston Outlaws        |      217 |
| Toronto Defiant        | Atlanta Reign          | Washington Justice  | Houston Outlaws     | Vancouver Titans    | Boston Uprising        | Washington Justice  | Florida Mayhem      | Vegas Eternal          |      228 |
| Vancouver Titans       | San Francisco Shock    | Vegas Eternal       | Toronto Defiant     | Washington Justice  | Atlanta Reign          | London Spitfire     | Boston Uprising     | San Francisco Shock    |      230 |
| Vegas Eternal          | San Francisco Shock    | Los Angeles Valiant | Houston Outlaws     | Vancouver Titans    | Florida Mayhem         | Toronto Defiant     | Atlanta Reign       | Los Angeles Gladiators |      257 |
| Washington Justice     | Florida Mayhem         | Toronto Defiant     | Atlanta Reign       | Vancouver Titans    | Los Angeles Gladiators | Toronto Defiant     | Boston Uprising     | Los Angeles Valiant    |      155 |

It becomes apparent that these schedules are highly imbalanced. Certain teams face exceedingly difficult schedules, 
such as Vegas, who has to compete against Atlanta, Florida, and the Gladiators. On the other hand, some teams enjoy 
considerably easier schedules, like Florida, who faces Vegas, Defiant, Shock, and London. To address this issue, 
we will apply some basic optimization techniques.

Here's our proposed approach: 
First, we randomly select two teams from the list. 
Next, we gather all eight opponents for these two teams and generate all possible combinations of two groups of four 
(resulting in a total of 70 combinations). We then filter out any combinations that contain a duplicate team within a group. 
For example, if we attempt to optimize the initial schedules for Reign and Shock, we would generate combinations such as:
```
Schedule 1 1: Los Angeles Gladiators, Vancouver Titans, New York Excelsior, Vegas Eternal
Schedule 2: Florida Mayhem, Vancouver Titans, Los Angeles Valiant, Houston Outlaws
```
We want to exclude combinations that have the Titans appearing twice in the same group. Additionally, we need to 
eliminate any sets that would result in Atlanta or Shock playing against themselves, as that is not possible.

Next, we calculate the strength of schedule (SoS) for each schedule in the set for every combination. 
We then determine the schedule set that exhibits the lowest difference in SoS when compared to the expected average. 

Below is an example calculation:
```
Los Angeles Gladiators, Vancouver Titans, New York Excelsior, Vegas Eternal, Florida Mayhem, Vancouver Titans, Los Angeles Valiant, Houston Outlaws

Schedule 1:
Los Angeles Gladiators: 56, Vancouver Titans: 42, New York Excelsior: 41, Vegas Eternal: 7
Sum: 147
Schedule 2:
Florida Mayhem: 83, Vancouver Titans: 42, Los Angeles Valiant: 2, Houston Outlaws: 90
Sum: 217
Diff: abs(147 - 200) + abs(217 - 200) = 70

Swap Result:

Schedule 1:
Vancouver Titans: 42, New York Excelsior: 41, Vegas Eternal: 7, Houston Outlaws: 90
Sum: 180
Schedule 2:
Vancouver Titans: 42, Los Angeles Valiant: 2, Florida Mayhem: 83, Los Angeles Gladiators: 56
Sum: 183
Diff: abs(180 - 200) + abs(183 - 200) = 37
```


Once this process is completed, we proceed to handle all schedule swaps for all teams. 
For example, if we swapped the schedules of Atlanta and Shock to accommodate the Outlaws and Gladiators, 
we need to update the schedules of the Outlaws and Gladiators accordingly to reflect their new opponents.

After ensuring the schedule swaps are properly updated, we can calculate the overall balance of the entire schedule. 
This is done by summing the differences between each team's strength of schedule (SoS) and the desired SoS. 
We then check if the difference falls below our desired cutoff of 15 points. If it does not, we repeat the process until 
either the difference falls below the cutoff or we reach 100,000 iterations.

The resulting schedule will resemble something like: 

| team                   | secondHalfOpponent1    | secondHalfOpponent2 | secondHalfOpponent3 | secondHalfOpponent4 | doubleOpponent1     | doubleOpponent2     | doubleOpponent3        | doubleOpponent4        | totalSOS |
|:-----------------------|:-----------------------|:--------------------|:--------------------|:--------------------|:--------------------|:--------------------|:-----------------------|:-----------------------|---------:|
| Atlanta Reign          | Florida Mayhem         | London Spitfire     | Toronto Defiant     | Washington Justice  | Vancouver Titans    | Los Angeles Valiant | Florida Mayhem         | Washington Justice     |      197 |
| Boston Uprising        | Los Angeles Gladiators | Florida Mayhem      | Los Angeles Valiant | Houston Outlaws     | Toronto Defiant     | London Spitfire     | New York Excelsior     | Houston Outlaws        |      200 |
| Florida Mayhem         | New York Excelsior     | Boston Uprising     | Atlanta Reign       | Washington Justice  | San Francisco Shock | Vegas Eternal       | Los Angeles Gladiators | Atlanta Reign          |      188 |
| Houston Outlaws        | New York Excelsior     | Boston Uprising     | Vegas Eternal       | Toronto Defiant     | London Spitfire     | New York Excelsior  | Los Angeles Gladiators | Boston Uprising        |      203 |
| London Spitfire        | San Francisco Shock    | New York Excelsior  | Los Angeles Valiant | Atlanta Reign       | Boston Uprising     | Houston Outlaws     | San Francisco Shock    | Los Angeles Valiant    |      195 |
| Los Angeles Gladiators | San Francisco Shock    | New York Excelsior  | Los Angeles Valiant | Boston Uprising     | Toronto Defiant     | Florida Mayhem      | Houston Outlaws        | Vegas Eternal          |      211 |
| Los Angeles Valiant    | Los Angeles Gladiators | Boston Uprising     | London Spitfire     | Vegas Eternal       | New York Excelsior  | Atlanta Reign       | Vancouver Titans       | London Spitfire        |      210 |
| New York Excelsior     | Los Angeles Gladiators | Florida Mayhem      | London Spitfire     | Houston Outlaws     | Los Angeles Valiant | Boston Uprising     | Houston Outlaws        | Vancouver Titans       |      201 |
| San Francisco Shock    | Los Angeles Gladiators | London Spitfire     | Vegas Eternal       | Vancouver Titans    | Florida Mayhem      | Washington Justice  | Vegas Eternal          | London Spitfire        |      200 |
| Toronto Defiant        | Atlanta Reign          | Washington Justice  | Houston Outlaws     | Vancouver Titans    | Boston Uprising     | Vegas Eternal       | Washington Justice     | Los Angeles Gladiators |      201 |
| Vancouver Titans       | San Francisco Shock    | Vegas Eternal       | Toronto Defiant     | Washington Justice  | Atlanta Reign       | Washington Justice  | Los Angeles Valiant    | New York Excelsior     |      201 |
| Vegas Eternal          | San Francisco Shock    | Los Angeles Valiant | Houston Outlaws     | Vancouver Titans    | Florida Mayhem      | Toronto Defiant     | San Francisco Shock    | Los Angeles Gladiators |      205 |
| Washington Justice     | Florida Mayhem         | Toronto Defiant     | Atlanta Reign       | Vancouver Titans    | Vancouver Titans    | Toronto Defiant     | San Francisco Shock    | Atlanta Reign          |      196 |

### 2.0 Why this Matters and How is it Different
The reality is that this process is likely very similar to what the league will do to generate balanced schedules 
(though I expect they will use some pre-packaged and optimized software). The big difference is that I am using RMSA instead
of map differential or table placement. This is because RMSA accounts for the strength of your opponents when generating ratings, 
while table placements and map differential is based opponent agnostic results. The perfect example of this is London and Toronto. 
London went 2-6, finished in 10th place, and has a map differential of -8. Toronto on the other hand has a record of 3-5 and a map 
differential of -3. Despite this, London just beat Toronto 3-1 and by RMSA is a noticably better team. The difference in their score is 
almost entirely due to London playing a much more difficult schedule in the first half of the season.

