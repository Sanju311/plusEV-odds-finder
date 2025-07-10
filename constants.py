from datetime import datetime, timezone, timedelta

# hidden = "63971622c64f6ae72dc229f7eb1fbf76"
THE_ODDS_API_BASE = "https://api.the-odds-api.com/v4/sports/"

SPORTS = [
    "baseball_mlb"
    # "soccer_usa_mls",
    # "americanfootball_nfl",
    # "americanfootball_ncaaf",
    # "basketball_nba",
    # "icehockey_nhl",
    # "basketball_ncaab",
    # "soccer_epl",
]

US_BOOKS = "betmgm,betrivers,betus,draftkings,fanduel,pointsbet"
UK_BOOKS = ",betway"
EU_BOOKS = ",pinnacle"
ALL_BOOKS = US_BOOKS+UK_BOOKS+EU_BOOKS

BOOKS = ["betmgm", "betrivers", "betus", "draftkings", "fanduel", "pointsbet", "betway", "pinnacle"]

MAIN_MARKETS = "h2h"


#sample size vs EV curve

EXPERIMENTAL_EV_CURVE = {
    1 : 1.14,
    2 : 1.125,
    3 : 1.10,
    4 : 1.0875, 
    5 : 1.083,
    6 : 1.08
}


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

