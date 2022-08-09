## An exploration team compositions based soley on hero selection in Season 4
In this exploration we will be looking at the various team compositions used in Season 4 
of Overwatch League. Specifically we will be applying a K-Means clustering algorithm to
the different compositions used to see what types of hero combinations result in base compositions.

### 0.1 Requirements
The code in this tutorial was written in python 3.7 and uses the following libraries:  
python 3.7  
The environment.yml page for the entire project contains everything you need to run this script.  

### The Exploration
For this exploration we will cluster team compositions based solely on the play time of each hero for each team on each map.
Unfortunately due to data constraints this is as granular as we can go, the stats-lab data only provides play time per 
hero, team, player, and map. We do not have access to the exact 6 heroes being played together at any given time. 
For each team, map, match combination, we will build a 1x30 array where each entry is the percentage of time a particular hero
was fielded during a map. We will then feed all of these into a k-means clustering algorithm with N (3-10) clusters, pull out the center of each cluster,
and determine the heroes that define that composition based on if the center of the cluster suggests a greater than 50% play time for that hero.

### The Results 

#### 3 Clusters
```
With 3 clusters the main comps are:
                                         Label  Cluster
0  Brigitte,D.Va,Tracer,Wrecking Ball,Zenyatta      0.0
1                          Baptiste,D.Va,Lúcio      1.0
2                    Ana,Brigitte,D.Va,Winston      2.0
```

When limiting to only 3 clusters, we see that the 3 main comps are:
##### Shanghai Poke/Dive hybrid
This was a standard composition in APAC that even saw some playtime in NA. We saw some variations of this that included
Sigma instead of D.Va, and the 6th DPS while mainly being Sombra, was occasionally swapped out for Ashe or Echo.

##### A comp centered on Lucio, Bap and D.Va
This is the basis of the Rush comps that NA played for the majority of the year, however you will notice a lack of Reinhardt and
Mei, and any other DPS. This is because the cluster also contains Orisa/D.Va anti-dive and Orisa/Sigma poke

#### A traditional dive with variable DPS
This is the basis of traditional dive, however the cluster also includes Zombie comp, the Ana-Mercy-Pharah comp from Countdown Cup,
and other variations of Dive.


#### 4 Clusters
```
With 4 clusters the main comps are:
                                         Label  Cluster
0         D.Va,Echo,Lúcio,Moira,Reaper,Winston      0.0
1                    Ana,Brigitte,D.Va,Winston      1.0
2  Brigitte,D.Va,Tracer,Wrecking Ball,Zenyatta      2.0
3                          Baptiste,D.Va,Lúcio      3.0
```

When limiting to only 4 clusters, we see that the 4 main comps are the three from above plus Zombie Comp:
#### Zombie Comp/Neo-GOATs/6-Man
This was a rigid comp for a rigid meta. We saw very slight variations involving soldier and ball, but this was almost 
always played in a mirror with the exact 6 heroes listed.


#### 5 Clusters
```
With 5 clusters the main comps are:
                                         Label  Cluster
0         D.Va,Echo,Lúcio,Moira,Reaper,Winston      0.0
1  Brigitte,D.Va,Tracer,Wrecking Ball,Zenyatta      1.0
2                 Baptiste,Brigitte,D.Va,Orisa      2.0
3            Baptiste,D.Va,Lúcio,Mei,Reinhardt      3.0
4             Ana,Brigitte,D.Va,Tracer,Winston      4.0
```
When limiting to 5 clusters, we see that the 3 of the main comps above, but now the Reinhardt brawl comp has been separated from the Orisa anti-dive comp:
#### Reinhardt Brawl
This composition was a staple of NA for the entire season. The 5 heroes shown were almost always played in this comp with
the second DPS being moved around between Symmetra, Cassidy and Tracer. 
#### Orisa Anti-Dive
The other half of the cluster that was split is made up of the Orisa anti-dive composition. The DPS were flexible in this comp,
but were mainly Ashe with either Echo or Tracer. We did see many variations though that included Torb, Sombra, and Cassidy. 
Double Shield with Sigma instead of D.Va is still contained in this cluster.

#### 6 Clusters
```
With 6 clusters the main comps are:
                                         Label  Cluster
0                               Ana,D.Va,Mercy      0.0
1  Brigitte,D.Va,Tracer,Wrecking Ball,Zenyatta      1.0
2            Baptiste,D.Va,Lúcio,Mei,Reinhardt      2.0
3         D.Va,Echo,Lúcio,Moira,Reaper,Winston      3.0
4                 Baptiste,Brigitte,D.Va,Orisa      4.0
5             Ana,Brigitte,D.Va,Tracer,Winston      5.0
```
When we get to 6 clusters, we have all the clusters from above, but we have now split the Dive/Poke hybrid that involved Mercy 
with either a Pharah and a Ball or an Echo with a Winston. 

#### 7 Clusters
```
With 7 clusters the main comps are:
                                         Label  Cluster
0            Baptiste,D.Va,Lúcio,Mei,Reinhardt      0.0
1                 Baptiste,Brigitte,D.Va,Orisa      1.0
2                    Baptiste,Echo,Orisa,Sigma      2.0
3  Brigitte,D.Va,Tracer,Wrecking Ball,Zenyatta      3.0
4         D.Va,Echo,Lúcio,Moira,Reaper,Winston      4.0
5             Ana,Brigitte,D.Va,Tracer,Winston      5.0
6                               Ana,D.Va,Mercy      6.0
```
We have now split Double Shield from Orisa anti-dive

#### 8 Clusters
```                                     Label  Cluster
0            Baptiste,D.Va,Lúcio,Mei,Reinhardt      0.0
1          Ana,D.Va,Mercy,Pharah,Wrecking Ball      1.0
2                  Ana,D.Va,Echo,Mercy,Winston      2.0
3         D.Va,Echo,Lúcio,Moira,Reaper,Winston      3.0
4                  Ana,Brigitte,Tracer,Winston      4.0
5                 Baptiste,Brigitte,D.Va,Orisa      5.0
6  Brigitte,D.Va,Tracer,Wrecking Ball,Zenyatta      6.0
7                    Baptiste,Echo,Orisa,Sigma      7.0
```
The two poke/dive hybrid comps with flyers are now split out from each other
#### 9 Clusters
```
With 9 clusters the main comps are:
                                               Label  Cluster
0                        Ana,D.Va,Echo,Mercy,Winston      0.0
1                       Baptiste,Brigitte,D.Va,Orisa      1.0
2                  Baptiste,D.Va,Lúcio,Mei,Reinhardt      2.0
3                Ana,D.Va,Mercy,Pharah,Wrecking Ball      3.0
4  Brigitte,D.Va,Sombra,Tracer,Wrecking Ball,Zeny...      4.0
5                   Ana,Brigitte,D.Va,Tracer,Winston      5.0
6               D.Va,Echo,Lúcio,Moira,Reaper,Winston      6.0
7        Ashe,Brigitte,Tracer,Wrecking Ball,Zenyatta      7.0
8                          Baptiste,Echo,Orisa,Sigma      8.0
```
Our clusters are no longer really splitting along meaningful lines, The Shanghai dive/poke hybrid has now split between the Ashe variation and the Sombra variation.
#### 10 Clusters
```
With 10 clusters the main comps are:
                                               Label  Cluster
0                        Ana,D.Va,Echo,Mercy,Winston      0.0
1                       Baptiste,Brigitte,D.Va,Orisa      1.0
2                  Baptiste,D.Va,Lúcio,Mei,Reinhardt      2.0
3                Ana,D.Va,Mercy,Pharah,Wrecking Ball      3.0
4                   Ana,Brigitte,D.Va,Tracer,Winston      4.0
5                  Ana,Brigitte,Tracer,Winston,Zarya      5.0
6               D.Va,Echo,Lúcio,Moira,Reaper,Winston      6.0
7  Ashe,Brigitte,Sigma,Tracer,Wrecking Ball,Zenyatta      7.0
8                          Baptiste,Echo,Orisa,Sigma      8.0
9  Brigitte,D.Va,Sombra,Tracer,Wrecking Ball,Zeny...      9.0
```


## Further Study
There is much more to compositions than just what heroes are played, many of the comps this clustering practice found are
of similar or the same arch-types, but cluster differently due to the heroes alone. The next logical step is to limit or even eliminate 
clustering on hero play time and instead swap to the attributes themselves of the comps, such as win conditions, sustain, time between team fights, etc.
As mentioned in the first section, we are unfortunately lacking in any and all data on this subject, and would therefore 
require a significant amount of work in order to investigate further.