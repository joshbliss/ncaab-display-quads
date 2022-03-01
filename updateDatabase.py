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

df.to_json('temp.json', orient='records')

f = open('temp.json')
teams = json.load(f)

for team in teams:
    currentTeam = ref.order_by_child("School").equal_to(team['School']).get()
    for i in currentTeam:
        teamKey = i
    for key in team:
        ref.child(teamKey).child(key).set(team[key])
        print("set " + str(key) + " to " + str(team[key]) + " for " + teamKey)
