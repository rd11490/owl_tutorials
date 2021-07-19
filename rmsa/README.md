## An attempt at ranking the performance of a team in a season

In this "tutorial" we will attempt to generate a rating for each team that accounts who each team players and how dominant their win is. 
We will do this by coming up with a method for calculating a "map score" for each map played, then use regularized linear 
regression on a sparse team matrix in an attempt to give each team credit for the result of the map.

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### 0.1 Requirements
The code in this tutorial was written in python 3.7 and uses the following libraries:
Pandas
Requests
sklearn

The environment.yml page for the entire project contains everything you need to run this script.


### 1. Calculating Map Score

