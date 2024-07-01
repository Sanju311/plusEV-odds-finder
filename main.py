from constants import sports, regions, books, markets 
from constants import getEventsAPI, getEventOddsAPI

import requests
import redis
import time



def main(): 
    findBets()


def findBets():
    
    #search through all sports  before waiting for a few hours for potential odds changes
    for sport in sports:
        
        try:

            events = requests.get(getEventsAPI(sport))
            events_JSON = events.json()

            for event in events_JSON:

                currEvent = {}
                currEvent['id'] = event['id']
                currEvent['leauge'] = event['sport_title']
                currEvent['teams'] = event['home_team'] + event['away_team']    
                currEvent['start_time'] = event['commence_time']       

                #search for favorable odds for the given event, one event  
                findOdds(currEvent)    

        except requests.exceptions.ConnectionError as e:
            print(e)

        except requests.exceptions.RequestException as e:
            print(e)

        except Exception as e:
            print(e)

    time.sleep(3600*3)


def findOdds(event):
    
    try:

        all_odds = requests.get(getEventOddsAPI(event['id']))
        all_odds = all_odds.json()

        redis_client = redis.Redis(host='localhost', port=6379, db=0)

        for sportsbook in all_odds["bookmakers"]:
            populateCache(sportsbook, redis_client)
            findValue(event, redis_client)


    except requests.exceptions.ConnectionError as e:
        print(e)

    except requests.exceptions.RequestException as e:
        print(e)

    except Exception as e:
        print(e)




def populateCache(sportsbook, redis_client):
    
    sportsbook_name = sportsbook['key']

    for market in sportsbook['markets']:
        for outcome in market['outcomes']:
            #sample key value: "fanduelh2hnetherlands","2.74"
            redis_client.set(sportsbook_name + market['key'] + outcome['name'], outcome['price'])


def findValue(event, redis_client):
    

    #logic to find value 
    sendMail()

    #clear cache 



#send mail notification to subscribers 
def sendMail():
    






if __name__ == "__main__":
    main()

