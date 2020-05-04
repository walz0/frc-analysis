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

key = "Z37IOn5LR76k6oZX42Yj6qktALW6DNd1aoQMeUSGzf1EEq1Cf2yX9jJcjiiKGIDx" 
url = "https://www.thebluealliance.com/api/v3/events/2020"
headers = { 'X-TBA-Auth-Key' : key }

response = requests.get(url, headers=headers)

sus_events = []
total_events = []

output = response.json()
for event in output:
    if 'SUSPENDED' in event['name']:
        # remove ***SUSPENDED*** and extra space from event name
        name = event['name'][16:]
        sus_events += [event['name']]
    total_events += [event['name']]

print("Total Events Scheduled: ", len(total_events))
print("Total Events Suspended: ", len(sus_events))
print("Percent Suspended: ", 100 * (len(sus_events) / len(total_events)))
