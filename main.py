from constants import endpoints
from constants import sports
from constants import regions
from constants import getEventsAPI

import requests
import json
import redis



def main(): 
    while True:
        findBets()


def findBets():
    
    for sport in sports:
        
        try:

            events = requests.get(getEventsAPI(sport))
            eventsJSON = events.json()

            for event in eventsJSON:

                currEvent = []
                currEvent['id'] = event['id']
                currEvent['title'] = event['sport_title']
                currEvent['teams'] = event['home_team'] + event['away_team']           

                findOdds(currEvent)    

        except requests.exceptions.ConnectionError as e:
            print("Connection error:" + e)

        except requests.exceptions.RequestException as e:
            print("Request library error:" + e)   

        except Exception as e:
            print("General error:" + e)


        time.sleep(10)



def findOdds(event):
    print(event)


if __name__ == "__main__":
    main()






# r = redis.Redis(host="localhost", port=6379)
# r.set("france","germafsfsfnu")

# print(r.get("france"))


# for event in data:
#     eventID = event['id']
#     eventTime = event['commence_time']
#     eventName = event['home_team'] + event['away_team']

    
# response = requests.get(endpoints['getEvents'])

# if response.status_code == 200:
#     data = response.json()
#     file_path = "api_response.json"
#     with open(file_path,'w') as json_file:
#         json.dump(data,json_file, indent=4)
# else:
#     print("error getting api data")


# eventAPI = getEvents('d30e31303173a5724c8a8c118c4887e4')
# print(eventAPI)
# response2 = requests.get(eventAPI)
# data = response2.json()

# file_path = "nether_austria_pinnacle.json"
# with open(file_path,'w') as json_file:
#     json.dump(data,json_file, indent=4)