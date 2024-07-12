from constants import sports
from constants import getEventsAPI
import requests


api = getEventsAPI("soccer_usa_mls")

events = requests.get(api)
eventsJSON = events.json()

print(eventsJSON)
