API_KEY = "63971622c64f6ae72dc229f7eb1fbf76"
THE_ODDS_API_BASE = "https://api.the-odds-api.com"
EV_THRESHOLD = ""


sports = {
    "hockey" : "icehockey_nhl",
    "euro" : "soccer_uefa_european_championship" 
}

regions = {
    "us1" : "us",
    "us2" : "us2",
    "uk" : "uk"
}

markets = {
    "moneyline": "h2h",
    "spread": "spreads",


}

endpoints = {
    "getSports": THE_ODDS_API_BASE+"/v4/sports/?apiKey="+API_KEY,
    "getEvents": THE_ODDS_API_BASE+ "/v4/sports/"+sports["euro"]+"/events/?apiKey="+API_KEY,
    "getEventOdds" : THE_ODDS_API_BASE+ "/v4/sports/"+sports["euro"]+"/events/++/odds/?apiKey="+API_KEY+"&regions="+regions["us1"]+ "&markets="+markets["spread"]
}

def getEvents(eventID):
    #return THE_ODDS_API_BASE+"/v4/sports/"+sports["euro"]+"/events/"+eventID+"/odds?apiKey="+API_KEY+"&regions="+regions["us2"]
    return THE_ODDS_API_BASE+"/v4/sports/"+sports["euro"]+"/events/"+eventID+"/odds?apiKey="+API_KEY+"&bookmakers=pinnacle"
