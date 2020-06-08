## Investigating Why Erster Isn't Playing

In this tutorial I will use the data from the stats lab page to investigate Erster's play time this season.

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### 0.1 Requirements
The code in this tutorial was written in python 3.7 and uses the following libraries:
Pandas

The environment.yml page for the entire project contains everything you need to run this script.

### 1. What is Erster's Hero Pool?

The first thing we are going to look into is what Erster's hero pool is. Based on his [Liquipedia Page](https://liquipedia.net/overwatch/Jeong_Joon) we that Erster is best at Genji, Doomfist, Pharah, Mei, and Tracer.
This matches anecdotal evidence that we have heard from various Atlanta Reign player's streams and from the league casters. Knowing this we can look into see what he has played in his time with the Atlanta Reign.


Below is Erster's hero pool for his entire OWL Career. The majority of this data is from GOATs and
before role lock so it throws a wrench in some of the numbers. We will likely never see Erster play Brig, D.Va, Zarya, Ana, or any other Tank or Support again in OWL.
![Hero Pool](screen_shots/hero_pool.png)

We also have his hero pool for the 2020 season. From here we can see that he has almost exclusively played Mei with a little bit of Tracer, Junkrat, Reaper and Sombra thrown in.
He has also played Doomfist and Soldier for what was likely an overtime contest, Widowmaker for what was likely an attempt at a pick out of spawn, Symmetra for a TP out of spawn, and Genji for less than a second.
![Hero Pool](screen_shots/hero_pool_2020.png)

