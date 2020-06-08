## Automate the Download and Extraction of StatsLab Data

In this tutorial I will show you how to download and extract data from the StatsLab page on the Overwatch League page.

If you see any issues or think there is a better way to do something,
don't hesitate to open a PR, submit an issue, or reach out to me directly

### 0.1 Requirements
This tutorial uses the latest version of Google Chrome for finding the endpoint information.
The code in this tutorial was written in python 3.7 and uses the following libraries:
Pandas
Requests

The environment.yml page for the entire project contains everything you need to run this script.


### 1. Where to download the data?

All data can be manually downloaded from https://overwatchleague.com/en-us/statslab .

![StatsLab Page](screen_shots/statslab_page.png)

There are four zip files here containing team stats per map played and player stats for each season.
These can easily be manually downloaded,
but I'm lazy and want to automate this so I only have to click a button
and have my data update on its own. To do this we will write a script to find the links to download the zip files on the page,
extract the zip files, and save the csv files contained within.

#### 1.1 Find the links to the zip files
The first think we want to do is go look at the source for the page.
You can view any page source in Chrome by right-clicking the page and selecting "View Source"
![View Source](screen_shots/view_source.png)

That will open a new tab with the source of the page:
![Source](screen_shots/source.png)

We can now search the source for the links to the zip files by searching the page for ".zip"
![Find Zip](screen_shots/find_zip.png)

Now that we have found the 4 zip files, we can look to find a pattern so that we can use regex to extract the links.

1. https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/bltc1b83b55692b42f4/5e4c1368de213a0dff736e29/phs_2018.zip
2. https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt034e0b484f2dae47/5e4c1369b6a7c40dd9c69e9f/phs_2019.zip
3. https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt7e0ffce2b617f0d2/5ecd3a75a84f2107d1775f56/phs_2020.zip
4. https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt67ebb7496ecd1ac4/5ecd3a5d80e1cd5cdc708bb6/match_map_stats.zip

Just from looking at the links, they seem to be some sort of fingerprinted assets so we can not expect the links to be consistent.
Because we can not expect the links to remain consistent, we need to extract them from the page every time we want to download. The simplest pattern to extract these links is to
pull everything between `https://assets` and `.zip`. The regex for this would be `r'(https://assets.*?.zip)'`


The script below will go to the statslab page, convert the source to a string, and extract all links that match out pattern into a list
```python
import requests
import re

# Make a request to get the html of the overwatch league stats lab page
resp_text = requests.get("https://overwatchleague.com/en-us/statslab").text

# Regex extract all zip file hrefs on the page
links = re.findall( r'(https://assets.*?.zip)', resp_text)

for l in links:
    print(l)
```
This will print out:
```
https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/bltc1b83b55692b42f4/5e4c1368de213a0dff736e29/phs_2018.zip
https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt034e0b484f2dae47/5e4c1369b6a7c40dd9c69e9f/phs_2019.zip
https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt7e0ffce2b617f0d2/5ecd3a75a84f2107d1775f56/phs_2020.zip
https://assets.blz-contentstack.com/v3/assets/blt321317473c90505c/blt67ebb7496ecd1ac4/5ecd3a5d80e1cd5cdc708bb6/match_map_stats.zip
```
which matches the links we found above.