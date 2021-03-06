import requests
import pandas as pd
from sportsipy.ncaab.boxscore import Boxscore
from sportsipy.ncaab.schedule import Schedule
import json
import firebase_admin
from firebase_admin import credentials, db
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/token.json'
cred = credentials.Certificate(path)
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://ncaam-quadrant-breakdown-default-rtdb.firebaseio.com'})

ref = db.reference("/Teams")

URL = "https://www.ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings"
html = requests.get(URL).content
df_list = pd.read_html(html)
df = df_list[-1]

df.to_json(os.path.dirname(os.path.abspath(__file__))+'/netRankings.json', orient='records')

f = open(os.path.dirname(os.path.abspath(__file__)) + '/netRankings.json')
teams = json.load(f)

ff = open(os.path.dirname(os.path.abspath(__file__)) + '/TeamAbbreviations.json')
abbreviations = json.load(ff)

for team in teams:
    currentTeam = ref.order_by_child("Abbreviation").equal_to(abbreviations[team['School']].lower()).get()
    for i in currentTeam:
        teamKey = i
    for key in team:
        ref.child(teamKey).child(key).set(team[key])
        print("set " + str(key) + " to " + str(team[key]) + " for " + teamKey)
