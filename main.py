"""
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

def getTotalINTeams(year):
    url = "http://frc-events.firstinspires.org/{}/district/IN".format(year)
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')
    spans = soup.find_all(id='rankings')
    spans = list(map(lambda x: x.text.rstrip(), spans))
    return spans 

def callAPI(query):
    key = "Z37IOn5LR76k6oZX42Yj6qktALW6DNd1aoQMeUSGzf1EEq1Cf2yX9jJcjiiKGIDx" 
    url = "https://www.thebluealliance.com/api/v3/{}".format(query)
    headers = { 'X-TBA-Auth-Key' : key }
    response = requests.get(url, headers=headers)
    return response.json()

#pprint.pprint(getTotalINTeams(2020))

total_teams = 3898 # total number of active frc teams (2020)

sus_events = [] # suspended events
com_events = [] # completed events
all_events = [] # all events

active_teams = [] # all teams that have competed in at least one event
in_teams = [] # all indiana teams that have competed

# pull all events planned for 2020
events = callAPI('events/2020')
for event in events:
    # differntiate events that took place from suspended events
    if 'SUSPENDED' in event['name']:
        # remove ***SUSPENDED*** and extra space from event name
        name = event['name'][16:]
        sus_events.append(frc_event(event['key'], event['name'], event['week']))
    else:
        com_events.append(frc_event(event['key'], event['name'], event['week']))
        teams = callAPI('event/' + event['key'] + '/teams')
        for team in teams:
            obj = frc_team(team['key'], team['name'], team['state_prov'])
            if not obj in active_teams:
                active_teams.append(obj)
                if obj.state == "Indiana":
                    in_teams.append(obj)
    all_events += [(event['key'], event['name'])]

print("Total Events Scheduled: ", len(all_events))
print("Total Events Suspended: ", len(sus_events))
print("Percent Suspended: ", 100 * (len(sus_events) / len(all_events)))

print("Total Teams Participated: ", len(active_teams))
print("Total Percent Participated: ", 100 * (len(active_teams) / total_teams))
print("Total Indiana Teams Participated: ", len(in_teams))
