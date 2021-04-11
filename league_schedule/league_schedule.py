import requests
import pandas as pd
import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

headers = {
    'x-origin': 'overwatchleague.com',
    'referer': 'https://overwatchleague.com/',
}

def download_week(week):
    params = (
        ('stage', 'regular_season'),
        ('page', week),
        ('season', '2021'),
        ('locale', 'en-us'),
    )

    response = requests.get('https://wzavfvwgfk.execute-api.us-east-2.amazonaws.com/production/owl/paginator/schedule', headers=headers, params=params)
    return response.json()

def extract_matches(events, week):
    matches = []
    for e in events:
        if (not e['isEncore']) and (e['competitors'][0]['name'] != "TBD") and (e['competitors'][1]['name'] != "TBD"):
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

def get_week_matches(week):
    week_resp = download_week(week)
    return extract_matches(week_resp['content']['tableData']['events'][0]['matches'], week)

weeks = []
for w in range(1, 20):
    weeks = weeks + get_week_matches(w)

frame = pd.DataFrame(weeks)

print(frame)
frame.to_csv('2021_league_schedule.csv')

