from datetime import datetime, timezone, timedelta


API_KEY = "63971622c64f6ae72dc229f7eb1fbf76"
THE_ODDS_API_BASE = "https://api.the-odds-api.com/v4/sports/"
EV_THRESHOLD = ""

SPORTS = [
    
    "soccer_usa_mls"
    #"soccer_uefa_european_championship"
    #"americanfootball_nfl",
    #"basketball_nba",
    #"soccer_usa_mls"
    ]

US_BOOKS = "betmgm,betrivers,betus,draftkings,fanduel,pointsbet"
UK_BOOKS = ",betway"
EU_BOOKS = ",pinnacle"
ALL_BOOKS = US_BOOKS+UK_BOOKS+EU_BOOKS

BOOKS = ["betmgm", "betrivers", "betus", "draftkings", "fanduel", "pointsbet", "betway", "pinnacle"]

MARKETS = [ "h2h"]
#MARKETS = [ "h2h","spreads","totals"]

MAIN_MARKETS = "h2h"

OUTCOMES = {
    
    'h2h': []

}
#potential for more: "team_totals","btts","alternate_spreads"


#returns the events API
def getEventsAPI(sport):
    time_now = datetime.now(timezone.utc)
    time_plus_week = (time_now + timedelta(days=7)).isoformat()
    time_plus_week = (time_plus_week[:-13] + "Z")
    return THE_ODDS_API_BASE+sport+"/events?apiKey="+API_KEY+"&commenceTimeTo="+time_plus_week

def getAnyEventOddsAPI(sport, eventID):
    return THE_ODDS_API_BASE+sport+"/odds/?apiKey="+API_KEY+"&regions="

def getEventOddsAPI(sport, eventID):
    return THE_ODDS_API_BASE+sport+"/odds/?apiKey="+API_KEY+"&eventIds="+eventID+"&regions=us&markets="+MAIN_MARKETS+"&bookmakers="+ALL_BOOKS

