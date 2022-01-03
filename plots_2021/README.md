# Overwatch League Stats - 2021
#### [Tracer](tracer/)
#### [Sombra](sombra/)


## Tracer
[Tracer Code](pulse_bomb_graph.py)
##### Pulse Bomb Kills Per Stick vs Attach Rate
![Pulse Bomb Status](plots/pulse_bombs_kills_per_stick.png)

From this plot the following trends can be assumed but not confirmed without watching replays to confirm

1. Players in the upper right quadrant are sticking low HP targets at a high rate
2. Players in the lower right quadrant are sticking tanks at a high rate
3. Players in the upper left quadrant are attempting to stick low HP targets but are not accurate
4. Players in the lower left quadrant are attempting to stick tanks but are not accurate

##### Pulse Bomb Kill Rate vs Attach Rate
![Pulse Bomb Status](plots/pulse_bombs_kill_rate.png)

This chart just gives us an idea of the efficiency of pulse bomb usage for each player.

## Sombra
[Sombra Code](sombra_graph.py)

On a recent episode of PlatChat, the hosts discussed Assassin's Sombra play, his time holding EMPs, and his high 
number of 0 player EMPs. After listening, I wanted to dig in and see how bad Assassin's Sombra really was. Thinking back
the season all I remember are his low lights, the missed solo EMP on lighthouse and the missed solo EMP on havana.
Now obviously only broad assumptions and trends can be found from this data. Overwatch is a complex game with lots of
confounding variables that result in a lot of context being needed when using stats. These stats can just server as a starting point
for further film study or to tell general trends in the data. The plots below are all limited to players with at least 
10 minutes of play time on Sombra in 2021

##### EMP Efficiency and Time to build EMP
![EMP Efficiency vs Time to build EMP](plots/emp_efficiency.png)
![EMP Efficiency vs Time Holding EMP](plots/emp_efficiency2.png)


The first thing I looked at was his EMP Efficiency (Players EMP'd per EMP) vs how quickly he builds EMP.
I expected him to have one of the lowest efficiencies of the entire league, but it turns out that he is about league average. 
Lip, often considered the best Somba in the league, averages less players hit by his EMPs than the king of MEMPs, 
even if the gap is very small, 2.55 players per EMP for Lip vs 2.66 for Assassin. One thing that does need to be accounted 
for is the play style. In general teams in the west played more rush comps and teams in the east played more dive,
so the theoretically Sombras playing in the west had more opportunity to get larger EMPs. It could be that if Assassin played against as
many dive comps as Lip, he could get a lower efficiency, but this type of claim would require film study to get more clarity on
and could never truly be answered.

##### Time Holding EMP vs Time to build EMP
![Time Holding EMP vs Time to build EMP](plots/emp_hold_build.png)

The next thing I wanted to look at was how long Assassin was holding onto his EMPs. After listing to PlatChat
discuss the subject, I assumed that Assassin would be one of the players holding EMP for the longest, but he was once
again league average. Once again there are always extenuating circumstances, but the general trends so far point to Assassin
more than likely being a better Sombra then the public thinks with some terrible low lights that have skewed the perception of him.


##### Assassin or Hacker?
![Eliminations per 10 vs Hacks per 10](plots/hack_vs_assassin3.png)
![Final Blows per 10 vs Hacks per 10](plots/hack_vs_assassin2.png)
![Solo Kills per 10 vs Hacks per 10](plots/hack_vs_assassin.png)

The last thing I wanted to look at was how the various Sombras in the league trying to secure kills vs how much time
they spend getting off hacks. Once again Assassin showed up as being about league average in Hacks per 10, and Eliminations, Final Blows and Solo Kills per 10.
One thing to note about this set of graphs is that hacking players and getting kills are not mutually exclusive, and the data alone can tell
us that a player is definitively sacrificing one stat for another without deeper film study.