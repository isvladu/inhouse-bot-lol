import requests
import random

from config import RIOT_TOKEN


class Summoner:
    """
    Class that validates when a summoner is added.
    """

    icon_id: int
    summoner_name: str
    timer: int

    account_endpoint: str = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    icon_url: str = "https://ddragon.leagueoflegends.com/cdn/12.9.1/img/profileicon/"

    def __init__(self, summoner_name: str):
        self.icon_id = random.randint(0, 5)
        self.summoner_name = summoner_name
        self.timer = 30

    def getSummonerIconURL(self):
        return self.icon_url + str(self.icon_id) + ".png"

    def getSummonerIcon(self):
        headers = {"X-Riot-Token": RIOT_TOKEN}
        url = self.account_endpoint + self.summoner_name

        r = requests.get(url=url, headers=headers)

        return r.json()["profileIconId"]

    def validateSummoner(self):
        return self.getSummonerIcon() == self.icon_id
