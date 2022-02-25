import requests
import pandas as pd
from sportsipy.ncaab.boxscore import Boxscore
from sportsipy.ncaab.schedule import Schedule
import json
import firebase_admin

cred = credentials.RefreshToken('token.json')
app = firebase_admin.initialize_app(cred)


URL = "https://www.ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings"
html = requests.get(URL).content
df_list = pd.read_html(html)
df = df_list[-1]

df.to_json('temp.json', orient='records')

uconn_schedule = Schedule('CONNECTICUT')

for game in uconn_schedule:
	if(game.points_for > game.points_against):
		print('WIN vs ' + game.opponent_name+': ' + str(game.points_for) + ' - ' + str(game.points_against) + ' @ ' + game.location)
	else:
		print('LOSS vs ' + game.opponent_name + ': ' + str(game.points_against) + ' - ' + str(game.points_for) + ' @ ' + game.location)
