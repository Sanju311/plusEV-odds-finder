from constants import SPORTS, BOOKS, EXPERIMENTAL_EV_CURVE
from constants import getEventsAPI, getEventOddsAPI
from email_config import sendMail

import requests
import redis
import time
import json

counter = 0

def main(): 

    findBets()


def findBets():
    
    file_name_counter = 0
    #search through all sports  before waiting for a few hours for potential odds changes
    for sport in SPORTS:
        
        try:

            # events = requests.get(getEventsAPI(sport))
            # events_JSON = events.json()

            file_name =  "events.json"

            # with open(file_name, 'w') as file:
            #     json.dump(events_JSON, file, indent=4)

            with open(file_name , 'r') as file:
                events_JSON = json.load(file)


            counter = 0
            for event in events_JSON:
                counter+=1

                if counter < 4:
                    currEvent = {}
                    currEvent['id'] = event['id']
                    currEvent['leauge'] = event['sport_key']
                    currEvent['outcomes'] = [event['home_team'], event['away_team']]
                    currEvent['start_time'] = event['commence_time'] 

                    if(event['sport_key'] == "soccer_usa_mls" or event['sport_key'] == "soccer_epl"):
                        currEvent['outcomes'].append("Draw")

                    #search for favorable odds for the given event, one event  
                    print(currEvent)
                    findOdds(currEvent)
                
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

        #write odds data to files
        file_name = "event_" + str(counter) + "_totals_odds.json"
        # with open(file_name, 'w') as file:
        #     json.dump(all_odds, file, indent=4)

        #read from odds data to files 
        with open(file_name,'r') as file:
            all_odds = json.load(file)

        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        averages = populateCache(all_odds[0]['bookmakers'], redis_client)
        findValue(event, redis_client, averages)
        
        redis_client.flushall()

    except Exception as e:
        print(e)



def populateCache(sportsbooks, redis_client):
    
    print("\nrediskey value pairs: ")

    averages = {}
    counter = 0

    try:
        for sportsbook in sportsbooks:
            
            sportsbook_name = sportsbook['key']
            counter+=1

            for outcome in sportsbook['markets'][0]['outcomes']:
                #sample key value: "fanduelnetherlands","2.74"
                print("key:" + sportsbook_name + outcome['name'] + " value: " + str(outcome['price']))
                redis_client.set(sportsbook_name + outcome['name'], str(outcome['price']))
                
                if outcome['name'] not in averages:
                    averages[outcome['name']] = 0.0
                
                averages[outcome['name']] += outcome['price']

        if counter != 0:
            for team, price in averages.items():
                    averages[team] = 1/(price/counter)

        averages['num_boooks'] = counter
        return averages

    except Exception as e:
        print(e)
    
    



def findValue(event, redis_client, averages):

    #loop through every market and compare all possible odds 
    true_odds = getTrueOddsH2H(event, redis_client)

    if true_odds == None:
        
        for outcome in event['outcomes']:
            for book in BOOKS:

                curr_odds = redis_client.get(book + outcome)
                
                if (curr_odds != None):
                    count = averages['num_books']
                    curr_odds_decoded = float(curr_odds.decode('utf-8'))
                    average_exclusive = ((averages[outcome] * count) - curr_odds_decoded)/(count-1)

                    EV = (average_exclusive)/(1/curr_odds_decoded)
                    if(EV >= EXPERIMENTAL_EV_CURVE[count-1]):
                        print("found a bet: " + book + outcome + str(curr_odds_decoded))
                        sendMail(event, book + outcome, curr_odds_decoded , EV -1, "based on experimental data")

    else:

        for outcome in event['outcomes']:
            for book in BOOKS:
                
                curr_odds = redis_client.get(book + outcome)


                if (curr_odds != None):
                    curr_odds_decoded = float(curr_odds.decode('utf-8'))

                    EV = true_odds[outcome]/(1/curr_odds_decoded)
                    if(EV > 1 and curr_odds_decoded < 5):
                        
                        print("found a bet: " + book + outcome + str(curr_odds_decoded))
                        sendMail(event, book + outcome, curr_odds_decoded , EV , "based on pinnacle data")                                           


def getTrueOddsH2H(event, redis_client):

    #find real odds using pinnacles line and subtracting vig
    true_odds = {}
    implied_odds = 0
        
    for outcome in event['outcomes']:
        sharp_line_coded = redis_client.get("pinnacle" + outcome)

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



if __name__ == "__main__":
    main()

