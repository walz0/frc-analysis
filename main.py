"""
    TODO:
        - Sort team data into groups based on state_prov (participated and not)
            - Use a dictionary
        - Determine which teams have played the most events (more than 1)
        - A list of all states / territories as links that display a chart of
          percent participated. Optional button to view all teams participated / not.


Total Events Scheduled:  193
Total Events Suspended:  131
Percent Suspended:  67.88
Total Teams Registered 2020: 3912
Total Teams Participated:  2183
Total Teams Not Participated: 1729
Total Percent Participated:  55.802
Total Indiana Teams Participated:  35

DATA TO COLLECT:
    list of all events in 2020
    list of all teams in 2020 (participated and not)

FRC Data error:
    frc135, frc3494, frc829

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
import json
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


def tbaAPI(query):
    key = "Z37IOn5LR76k6oZX42Yj6qktALW6DNd1aoQMeUSGzf1EEq1Cf2yX9jJcjiiKGIDx" 
    url = "https://www.thebluealliance.com/api/v3/{}".format(query)
    headers = { 'X-TBA-Auth-Key' : key }
    response = requests.get(url, headers=headers)
    return response.json()


# get data from FIRST official leaderboard, incorrect data
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


# get all teams registered from a given state in a given year
def getStateTeams(state_prov, year):
    output = []
    # pull all events completed for given year as frc_event objects
    events = getAllEvents(year)
    for event in events:
        # differentiate events that took place from suspended events
        teams = tbaAPI('event/' + event.key + '/teams')
        for team in teams:
            team_obj = frc_team(team['key'], team['name'], team['state_prov'])
            if not team_obj in output:
                if team_obj.state == state_prov:
                    output.append(team_obj)
    return output


# get all teams from a given state in a given year who have competed
def getCompetedStateTeams(state_prov, year):
    output = []
    # pull all events completed for given year as frc_event objects
    events = getCompletedEvents(year)
    for event in events:
        # differentiate events that took place from suspended events
        teams = tbaAPI('event/' + event.key + '/teams')
        for team in teams:
            team_obj = frc_team(team['key'], team['name'], team['state_prov'])
            if not team_obj in output:
                if team_obj.state == state_prov:
                    output.append(team_obj)
    return output 

"""
:: Gets all teams from all events in given year
        
ERROR: repeated team_obj, maybe duplicate events?
        look into threads / parallel calls / async calls
"""
def getAllTeams(year):
    output = []
    # pull all events completed for given year as frc_event objects
    events = getAllEvents(year)
    for event in events:
        # differentiate events that took place from suspended events
        teams = tbaAPI('event/' + event.key + '/teams')
        for team in teams:
            team_obj = frc_team(team['key'], team['name'], team['state_prov'])
            if not team_obj.key in [o.key for o in output]:
                output.append(team_obj)
    return output 


# get all events scheduled for a given year
def getAllEvents(year): 
    events = tbaAPI('events/' + str(year))
    output = [frc_event(event['key'], event['name'], event['week']) for event in events]
    return output


def eventCount(year):
    return len(getAllEvents(year))


# get all completed events for a given year
def getCompletedEvents(year):
    sus_events = [] # suspended events
    com_events = [] # completed events

    # pull all events planned for 2020
    events = tbaAPI('events/' + str(year))
    for event in events:
        # differentiate events that took place from suspended events
        if 'SUSPENDED' in event['name']:
            # remove ***SUSPENDED*** and extra space from event name
            name = event['name'][16:]
            sus_events.append(frc_event(event['key'], event['name'], event['week']))
        else:
            com_events.append(frc_event(event['key'], event['name'], event['week']))
    return com_events


def getSuspendedEvents(year):
    sus_events = [] # suspended events
    com_events = [] # completed events

    # pull all events planned for 2020
    events = tbaAPI('events/2020')
    for event in events:
        # differentiate events that took place from suspended events
        if 'SUSPENDED' in event['name']:
            # remove ***SUSPENDED*** and extra space from event name
            name = event['name'][16:]
            sus_events.append(frc_event(event['key'], event['name'], event['week']))
        else:
            com_events.append(frc_event(event['key'], event['name'], event['week']))
    return sus_events
   

total_teams = 3898 # total number of active frc teams (2020)

teams_dict = {}

teams = getAllTeams(2020)
for team in teams:
    if team.state in teams_dict:
        teams_dict[team.state] += [team.key]
    else:
        teams_dict[team.state] = [team.key]

pprint.pprint(teams_dict)
with open('teams_by_state.json', 'w') as json_file:
    json.dump(teams_dict, json_file)

# print(len(getStateTeams('Hawaii', 2020)))

# pprint.pprint(getAllTeams(2020))
#print(getStateTeams('Indiana', 2020))

#print("Total Events Scheduled: ", len(all_events))
#print("Total Events Suspended: ", len(sus_events))
#print("Percent Suspended: ", round(100 * (len(sus_events) / len(all_events)), 2))
#
#print("Total Teams Participated: ", len(active_teams))
#print("Total Percent Participated: ", round(100 * (len(active_teams) / total_teams), 2))
#print("Total Indiana Teams Participated: ", len(in_teams))