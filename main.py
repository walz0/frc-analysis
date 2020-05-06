"""
    TODO:
        -scraper for district data
            -compare team counts on tba and scraper
                -determine what teams are the discrepancy


Total Events Scheduled:  193
Total Events Suspended:  131
Percent Suspended:  67.88
Total Teams Participated:  2183
Total Percent Participated:  56.0
Total Indiana Teams Participated:  35

=-------------------------------------------------------------------=
        
    start on 'initiation line'
        can be loaded with 3 'power cell' balls
        auto for first 15 seconds
        teleop for 2:15 min
        score on opposite side of start
    
    ball ports
        low - 1
        outer - 2
        inner - 3

    'control panel' - color wheel
        rotate num - 10
        rotate to pos - 20 and 1 rp
            
    'rendezvous point' - climb
        two bots - 25 each (50)
        if level - 15
        if third bot is within climb zone - 5
        
    if total points at end game >= 65 gain 1 rp
"""

import requests
from bs4 import BeautifulSoup
import pprint

class frc_event():
    teams = []
    def __init__(self, key, name, week):
        self.key = key 
        self.name = name 
        self.week = week 

    def __str__(self):
        return self.key + ": ({})".format(self.name)
    
    def __repr__(self):
        return self.__str__()

class frc_team():
    def __init__(self, key, name, state):
        self.key = key 
        self.name = name 
        self.state = state

    def __str__(self):
        return self.key + ": ({})".format(self.name)
    
    def __repr__(self):
        return self.__str__()

def getIndianaTeams(year):
    # pull from district ranking leaderboard
    url = "http://frc-events.firstinspires.org/{}/district/IN".format(year)
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.table.find_all('tr')[1:]
    teams = []
    for row in rows:
        td = row.find_all('td')
        td = [x.text.strip() for x in td]
        raw_name = td[2]
        played = not (td[3] == td[4])
        if played:
            teams.append(frc_team('frc' + raw_name[:4].rstrip(), "", "Indiana"))
    teamCount = len(rows) - 1 # exclude the column label row
    return teams

def tbaAPI(query):
    key = "Z37IOn5LR76k6oZX42Yj6qktALW6DNd1aoQMeUSGzf1EEq1Cf2yX9jJcjiiKGIDx" 
    url = "https://www.thebluealliance.com/api/v3/{}".format(query)
    headers = { 'X-TBA-Auth-Key' : key }
    response = requests.get(url, headers=headers)
    return response.json()

total_teams = 3898 # total number of active frc teams (2020)

sus_events = [] # suspended events
com_events = [] # completed events
all_events = [] # all events

active_teams = [] # all teams that have competed in at least one event
in_teams = []
first_in_teams = getIndianaTeams(2020) # all indiana teams that have competed
#pprint.pprint(first_in_teams)

# pull all events planned for 2020
events = tbaAPI('events/2020')
for event in events:
    # differntiate events that took place from suspended events
    if 'SUSPENDED' in event['name']:
        # remove ***SUSPENDED*** and extra space from event name
        name = event['name'][16:]
        sus_events.append(frc_event(event['key'], event['name'], event['week']))
    else:
        com_events.append(frc_event(event['key'], event['name'], event['week']))
        teams = tbaAPI('event/' + event['key'] + '/teams')
        for team in teams:
            obj = frc_team(team['key'], team['name'], team['state_prov'])
            if not obj in active_teams:
                active_teams.append(obj)
                if obj.state == "Indiana":
                    in_teams.append(obj)
    all_events += [(event['key'], event['name'])]

print(len(in_teams))
print(len(first_in_teams))

outliers = []
in_teams_keys = [team.key for team in in_teams]
first_in_teams_keys = [team.key for team in first_in_teams]
pprint.pprint(in_teams_keys)
pprint.pprint(first_in_teams_keys)

for key in in_teams_keys:
    if not key in first_in_teams_keys:
        outliers += [key]

print(outliers)

#print("Total Events Scheduled: ", len(all_events))
#print("Total Events Suspended: ", len(sus_events))
#print("Percent Suspended: ", round(100 * (len(sus_events) / len(all_events)), 2))
#
#print("Total Teams Participated: ", len(active_teams))
#print("Total Percent Participated: ", round(100 * (len(active_teams) / total_teams), 2))
#print("Total Indiana Teams Participated: ", len(in_teams))
