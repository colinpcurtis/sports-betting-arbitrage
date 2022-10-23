import requests
import json
from functools import reduce
import os
from datetime import date

DATE = date.today().strftime("%m-%d-%y")

API_KEY = os.getenv("THE_ODDS_API_KEY")
MAKE_REQUEST = False

BOOKMAKERS = ["draftkings", "barstool", "betmgm"] 
SPORTS = ["americanfootball_ncaaf", "basketball_nba", "americanfootball_cfl", "baseball_mlb", "icehockey_nhl", "americanfootball_nfl"]

def load_data():
    if MAKE_REQUEST:
        host = "https://api.the-odds-api.com"

        sport = "upcoming"
        bookmakers = ",".join(BOOKMAKERS)

        path = f"/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=us&markets=h2h&bookmakers={bookmakers}"

        response = requests.get(host + path)
        data = response.json()
        with open(f'data-{DATE}.json', 'w+') as f:
            f.write(json.dumps(data, indent=4))
    else:
        with open(f'data-{DATE}.json', 'r') as f:
            data = json.loads(f.read())
    return data

def filterer(sporting_event):
    return sporting_event["sport_key"] in SPORTS

def reducer(accum, sporting_event):
    bookmakers = sporting_event["bookmakers"]
    arbs = []
    # for each bookmaker, return pairs with arb opportunities
    for bookmaker1 in bookmakers:
        for bookmaker2 in bookmakers:
            if bookmaker1 is not bookmaker2 and bookmaker1["key"] in BOOKMAKERS and bookmaker2["key"] in BOOKMAKERS:
                outcome11, outcome12 = bookmaker1["markets"][0]["outcomes"][0]["price"], bookmaker1["markets"][0]["outcomes"][1]["price"]
                outcome21, outcome22 = bookmaker2["markets"][0]["outcomes"][0]["price"], bookmaker2["markets"][0]["outcomes"][1]["price"]
                if (1 / outcome11) + (1 / outcome22) < 1:
                    if outcome11 < outcome22:
                        bet1 = 100
                        bet2 = bet1 * outcome11 / outcome22
                        bet = bet1 + bet2
                        percent_return = 100 * ((bet1 * outcome11) - bet) / bet
                    else:
                        bet1 = 100
                        bet2 = bet1 * outcome22 / outcome11
                        bet = bet1 + bet2
                        percent_return = 100 * ((bet2 * outcome11) - bet) / bet

                    arbs.append({
                        "sport": sporting_event["sport_key"],
                        "commence_time": sporting_event["commence_time"],
                        "bookmaker1": bookmaker1["key"],
                        "bookmaker2": bookmaker2["key"],
                        "outcome1": outcome11,
                        "outcome2": outcome22,
                        "bet1": bet1,
                        "bet2": bet2,
                        "team1": bookmaker1["markets"][0]["outcomes"][0]["name"],
                        "team2": bookmaker1["markets"][0]["outcomes"][1]["name"],
                        "percent_return": percent_return
                    })

                if (1 / outcome12) + (1 / outcome21) < 1:
                    if outcome12 < outcome21:
                        bet1 = 100
                        bet2 = bet1 * outcome12 / outcome21
                        bet = bet1 + bet2
                        percent_return = 100 * ((bet1 * outcome12) - bet) / bet
                    else:
                        bet1 = 100
                        bet2 = bet1 * outcome21 / outcome12
                        bet = bet1 + bet2
                        percent_return = 100 * ((bet2 * outcome12) - bet) / bet

                    arbs.append({
                        "sport": sporting_event["sport_key"],
                        "commence_time": sporting_event["commence_time"],
                        "bookmaker1": bookmaker1["key"],
                        "bookmaker2": bookmaker2["key"],
                        "outcome1": outcome12,
                        "outcome2": outcome21,
                        "bet1": bet1,
                        "bet2": bet2,
                        "team1": bookmaker1["markets"][0]["outcomes"][0]["name"],
                        "team2": bookmaker1["markets"][0]["outcomes"][1]["name"],
                        "percent_return": percent_return
                    })
    if arbs != []:
        accum.append(arbs)
        return accum
    else:
        return accum

def flatten(l):
    return [item for sublist in l for item in sublist]

if __name__ == "__main__":
    data = load_data()
    data = filter(filterer, data)

    arbs = reduce(reducer, data, [])

    arbs = flatten(arbs)

    arbs = sorted(arbs, key=lambda x: x["percent_return"])

    with open(f'arbs-{DATE}.json', 'w+') as f:
        f.write(json.dumps(arbs, indent=4))
