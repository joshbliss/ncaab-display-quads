from sportsipy.ncaab.teams import Teams
import firebase_admin
import json
from firebase_admin import credentials, db

teams = Teams()

cred = credentials.Certificate('token.json')
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://ncaam-quadrant-breakdown-default-rtdb.firebaseio.com'})
ref = db.reference("/Teams")
successfulTeams = {}
unsuccessfulTeams = []

#Collect all teams that have mismatched abbreviations across NCAA and Sportsipy API
"""
for team in teams:
    print(team.name)
    try:
        match = ref.order_by_child("School").equal_to(team.name).get()
        if match:
            successfulTeams[team.name] = team.abbreviation
        else:
            unsuccessfulTeams.append(team.name)
    except firebase_admin.exceptions.InvalidArgumentError:
        unsuccessfulTeams.append(team.name)

with open('TeamAbbreviations.json', 'w') as file:
    file.write(json.dumps(successfulTeams))

with open('teamNameMismatch.json', 'w') as file:
    file.write(json.dumps(unsuccessfulTeams))
"""

f = open('teamNameMismatch.json')
mismatches = json.load(f)

ff = open('TeamAbbreviations.json')
abbreviations = json.load(ff)

attemptToMatch = {}
index = 0

orderedNcaaTeams = ref.order_by_child("School").get()
print(orderedNcaaTeams)

#Mismatches are in alphabetical order, so they should align with teams not in abbreviations
for team in Teams():
    if team.name not in abbreviations:
        attemptToMatch[mismatches[index]] = team.abbreviation
        index+=1

with open('attemptedMatches.json', 'w') as file:
    file.write(json.dumps(attemptToMatch))
