import requests
import pandas as pd
from sportsipy.ncaab.boxscore import Boxscore
from sportsipy.ncaab.schedule import Schedule
import json
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

cred = credentials.Certificate('token.json')
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://ncaam-quadrant-breakdown-default-rtdb.firebaseio.com'})

ref = db.reference("/Teams")

f = open('netRankings.json')
teams = json.load(f)

ff = open('TeamAbbreviations.json')
abbreviations = json.load(ff)

#Initial script used to push abbreviations into database
#for i in teams:
#    i['Abbreviation'] = abbreviations[i['School']].lower()
#    ref.push(i)

URL = "https://www.ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings"
html = requests.get(URL).content
df_list = pd.read_html(html)
df = df_list[-1]

df.to_json('netRankings.json', orient='records')

uconn_schedule = Schedule('CONNECTICUT')


for game in uconn_schedule:
    if(game.datetime < datetime.now()):

        opponent = dict(ref.order_by_child("Abbreviation").equal_to(game.opponent_abbr).get())
    
        #only one should ever occur
        for i in opponent:
            rank = opponent[i]['Rank']

        location = game.location
        if location == 'Home':
            if rank <= 30: quad = "Q1"
            elif rank <= 75: quad = "Q2"
            elif rank <= 160: quad = "Q3"
            else: quad = "Q4"
        elif location == 'Away':
            if rank <= 75: quad = "Q1"
            elif rank <= 135: quad = "Q2"
            elif rank <= 240: quad = "Q3"
            else: quad = "Q4"
        else: #Neutral
            if rank <= 50: quad = "Q1"
            elif rank <= 100: quad = "Q2"
            elif rank <= 200: quad = "Q3"
            else: quad = "Q4"

        print("UConn " + quad + " " + location + " " +  str(game.result) + " vs " + game.opponent_name + ": " + str(game.points_for) + "-" + str(game.points_against))

