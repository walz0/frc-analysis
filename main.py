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
import pprint

class frc_event():
    def __init__(self, key, name, week):
        self.key = key 
        self.name = name 
        self.week = week 

    def __str__(self):
        return self.key + ": ({})".format(self.name)
    
    def __repr__(self):
        return self.__str__()


key = "Z37IOn5LR76k6oZX42Yj6qktALW6DNd1aoQMeUSGzf1EEq1Cf2yX9jJcjiiKGIDx" 
url = "https://www.thebluealliance.com/api/v3/events/2020"
headers = { 'X-TBA-Auth-Key' : key }

response = requests.get(url, headers=headers)

sus_events = [] # suspended events
com_events = [] # completed events
all_events = [] # all events

output = response.json()
for event in output:
    if 'SUSPENDED' in event['name']:
        # remove ***SUSPENDED*** and extra space from event name
        name = event['name'][16:]
        sus_events += [frc_event(event['key'], event['name'], event['week'])]
    else:
        com_events += [frc_event(event['key'], event['name'], event['week'])]
    all_events += [(event['key'], event['name'])]

print("Total Events Scheduled: ", len(all_events))
print("Total Events Suspended: ", len(sus_events))
print("Percent Suspended: ", 100 * (len(sus_events) / len(all_events)))

pprint.pprint(com_events)
