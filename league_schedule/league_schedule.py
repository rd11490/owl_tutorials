import requests
import pandas as pd
import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Required headers for the API
headers = {
    'x-origin': 'overwatchleague.com',
    'referer': 'https://overwatchleague.com/',
}

# A function to call the league schedule endpoint and return the json response
def download_week(week):
    # Query params required for calling the endpoint. The endpoint is paged by league week.
    params = (
        ('stage', 'regular_season'),
        ('page', week),
        ('season', '2021'),
        ('locale', 'en-us'),
    )

    # Call the endpoint with the required headers and query params
    response = requests.get('https://wzavfvwgfk.execute-api.us-east-2.amazonaws.com/production/owl/paginator/schedule', headers=headers, params=params)
    return response.json()

# A function to convert the response json to a dataframe of league matches
def extract_matches(events, week):
    matches = []
    for e in events:
        # isEncore is a field that determines if the match is the original play (false) or if the match is being replayed in a different timezone (true)
        # Team Name = TBD is for tournament matches where the matches haven't been determined yet.
        if (not e['isEncore']) and (e['competitors'][0]['name'] != "TBD") and (e['competitors'][1]['name'] != "TBD"):
            # Convert each item in the league schedule into an object we can use to build our league schedule
            matches.append({
                'week': week,
                'startDate': datetime.datetime.fromtimestamp(e['startDate']/1000).strftime('%Y-%m-%d'),
                'startDateTime': e['startDate'],
                'team1Id': e['competitors'][0]['id'],
                'team1Name': e['competitors'][0]['name'],
                'team1ShortName': e['competitors'][0]['abbreviatedName'],
                'team2Id': e['competitors'][1]['id'],
                'team2Name': e['competitors'][1]['name'],
                'team2ShortName': e['competitors'][1]['abbreviatedName'],
            })
    return matches

# Call the league schedule api and extract the data for the specified week
def get_week_matches(week):
    week_resp = download_week(week)
    return extract_matches(week_resp['content']['tableData']['events'][0]['matches'], week)

weeks = []
for w in range(1, 20):
    weeks = weeks + get_week_matches(w)

frame = pd.DataFrame(weeks)

print(frame)
frame.to_csv('2021_league_schedule.csv')

