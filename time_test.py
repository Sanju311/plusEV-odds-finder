import json

file_name = "sample_event_odds.json"

with open(file_name,'r') as file:
    all_odds = json.load(file)