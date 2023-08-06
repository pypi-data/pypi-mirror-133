import random as rnd
import requests

seed = None

def fetch_evolution():
    global seed
    seed_candidate = str(requests.get('https://www.coindesk.com/pf/api/v3/content/fetch/prices?query=%7B%22iso%22%3A%22all%22%7D&d=117&_website=coindesk').json()['BTC']['change']['percent']).split('.')[1]
    if seed_candidate != seed:
        seed = seed_candidate
        rnd.seed(seed)
        return

def random():
    fetch_evolution()
    return rnd.random()