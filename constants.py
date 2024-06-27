from datetime import datetime, timezone, timedelta


API_KEY = "63971622c64f6ae72dc229f7eb1fbf76"
THE_ODDS_API_BASE = "https://api.the-odds-api.com/v4/sports/"
EV_THRESHOLD = ""

sports = {
    "soccer_uefa_european_championship", 
    "americanfootball_nfl",
    "basketball_nba",
    "soccer_usa_mls"
}

us_books = "betmgm,betrivers,betus,draftkings,fanduel,pointsbet"
uk_books = "betway"
eu_books = "pinnacle"
all_books = us_books+uk_books+eu_books

regions = "us"

markets = {
    "moneyline": "h2h",
    "spread": "spreads",
    "total": "totals",
    "team_toal": "team_totals",
    "bothToScore": "btts",
    "alt_spread": "alternate_spreads"
}

main_markets = "h2h,spreads,totals"

endpoints = {
    "getSports": THE_ODDS_API_BASE+"/v4/sports/?apiKey="+API_KEY,
    "getEvents": THE_ODDS_API_BASE+ "/v4/sports/"+sports["euro"]+"/events/?apiKey="+API_KEY,
    "getEventOdds" : THE_ODDS_API_BASE+ "/v4/sports/"+sports["euro"]+"/events/++/odds/?apiKey="+API_KEY+"&regions="+regions["us1"]+ "&markets="+markets["spread"]
}

#returns the events API
def getEventsAPI(sport):
    return THE_ODDS_API_BASE+sport+"/events?apiKey="+API_KEY

def getAnyEventOddsAPI(sport, eventID):
    return THE_ODDS_API_BASE+sport+"/odds/?apiKey="+API_KEY+"&regions="

def getEventOddsAPI(sport, eventID):
    time_now = datetime.now(timezone.utc)
    time_plus_week = (time_now + timedelta(days=7)).isoformat()
    time_plus_week = time_plus_week[:-6] + "Z"

    return THE_ODDS_API_BASE+sport+"/odds/?apiKey="+API_KEY+"&eventIds="+eventID+"&regions="+regions+"&markets="+main_markets+"&commenceTimeTo="+time_plus_week+"&bookmakers="+all_books