from constants import endpoints
from constants import sports
from constants import regions
from constants import getEvents

import requests
import json



# response = requests.get(endpoints['getEvents'])


# if response.status_code == 200:
#     data = response.json()
#     file_path = "api_response.json"
#     with open(file_path,'w') as json_file:
#         json.dump(data,json_file, indent=4)
# else:
#     print("error getting api data")



eventAPI = getEvents('d30e31303173a5724c8a8c118c4887e4')
print(eventAPI)
response2 = requests.get(eventAPI)
data = response2.json()

file_path = "nether_austria_pinnacle.json"
with open(file_path,'w') as json_file:
    json.dump(data,json_file, indent=4)

# for event in data:
#     eventID = event['id']
#     eventTime = event['commence_time']
#     eventName = event['home_team'] + event['away_team']

    

