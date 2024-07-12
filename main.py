from constants import SPORTS, BOOKS, MARKETS, EV_THRESHOLD
from constants import getEventsAPI, getEventOddsAPI

import requests
import redis
import time
import json


first_run = True
counter = 0


def main(): 
    findBets()


def findBets():
    

    file_name_counter = 0
    #search through all sports  before waiting for a few hours for potential odds changes
    for sport in SPORTS:
        
        try:

            events = requests.get(getEventsAPI(sport))
            events_JSON = events.json()

            file_name =  "events.json"

            # with open(file_name, 'w') as file:
            #     json.dump(events_JSON, file, indent=4)


            counter = 0
            for event in events_JSON:
                counter+=1

                if counter < 3:
                    currEvent = {}
                    currEvent['id'] = event['id']
                    currEvent['leauge'] = event['sport_key']
                    currEvent['teams'] = [event['home_team'], event['away_team'] , "Draw"]    
                    currEvent['start_time'] = event['commence_time']       

                    #search for favorable odds for the given event, one event  
                    print(currEvent)
                    findOdds(currEvent)
                

        except requests.exceptions.ConnectionError as e:
            print(e)

        except requests.exceptions.RequestException as e:
            print(e)

        except Exception as e:
            print(e)

    #time.sleep(3600*3)


def findOdds(event):
    
    try:
        
        global counter 
        counter+=1

        # api = getEventOddsAPI(event['leauge'], event['id'])
        # all_odds = requests.get(api)
        # all_odds = all_odds.json()

        #create new file for each event's odds
        file_name = "event_" + str(counter) + "_odds.json"
        # with open(file_name, 'w') as file:
        #     json.dump(all_odds, file, indent=4)

            
        with open(file_name,'r') as file:
            all_odds = json.load(file)

        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        for sportsbook in all_odds[0]['bookmakers']:
            populateCache(sportsbook, redis_client)
        
        for market in all_odds[0]['bookmakers'][0]['markets']:
            findValue(market['key'], event, redis_client)
        
        redis_client.flushdb()

    except requests.exceptions.ConnectionError as e:
        print(e)

    except requests.exceptions.RequestException as e:
        print(e)

    except Exception as e:
        print(e)



def populateCache(sportsbook, redis_client):
    
    sportsbook_name = sportsbook['key']

    print("\nrediskey value pairs: ")
    for market in sportsbook['markets']:
        for outcome in market['outcomes']:
            #sample key value: "fanduelh2hnetherlands","2.74"
            print("key:" + sportsbook_name + market['key'] + outcome['name'] + " value: " + str(outcome['price']))
            redis_client.set(sportsbook_name + market['key'] + outcome['name'], str(outcome['price']))


def findValue(market, event, redis_client):
    
    if(market == "h2h"):
        
        #loop through every market and compare all possible odds 
        true_odds = getTrueOddsH2H(event, redis_client, market)

        for outcome in event['teams']:
            for book in BOOKS:
                
                curr_odds = redis_client.get(book + market + outcome)

                if (curr_odds != None):

                    EV = true_odds[outcome]/(1/curr_odds)
                    if(EV > 1):
                        sendMail(event, book, market , outcome, EV)
                        
                                     
    elif(market == "spreads"):
        print("spreads")
    elif(market == "totals"):
        print("spreads")


def getTrueOddsH2H(event, redis_client, market):

    #find real odds using pinnacles line and subtracting vig
    true_odds = {}
    implied_odds = 0
        
    for outcome in event['teams']:
        sharp_line_coded = redis_client.get("pinnacle" + market + outcome)

        if sharp_line_coded != None:
            sharp_line_decoded = float(sharp_line_coded.decode('utf-8'))
            implied_odds += 1/sharp_line_decoded
            true_odds[outcome] = 1/sharp_line_decoded
        else:
            return None

    juice = implied_odds - 1
        
    for key, value in true_odds.items():
        true_odds[key] = value*(1-juice)

    return true_odds


    



#send mail notification to subscribers 
#def sendMail(event, book, market, outcome, EV):







if __name__ == "__main__":
    main()

