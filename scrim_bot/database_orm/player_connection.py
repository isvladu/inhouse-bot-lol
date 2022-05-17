from typing import Optional

from scrim_bot.core.player import Player
from scrim_bot.database_orm.connection import Connection


# TODO: Change implementation of updates to contain only required parameter.
#       Add a new update method that takes player as a parameter.
class PlayerConnection(Connection):
    """
    Represents the connection handling of operations with the Players table.
    """

    def __init__(self):
        super().__init__()
        self.table = super().getCollection("players")

    @staticmethod
    def decode_player(document):
        if document is None:
            return None
        else:
            return Player(document["_id"], document["name"], document["roles"], document["elo"],
                          document["summoner_name"])

    def getPlayer(self, unique_id: int) -> Optional[Player]:
        return self.decode_player(self.table.find_one({"_id": unique_id}))

    def insertPlayer(self, player: Player):
        self.table.insert_one(player.encode_player())

    def updatePlayer(self, player: Player):
        query = {"_id": player.id}
        values = {"$set": {"roles": player.getRoles(), "elo": player.elo, "summoner_name": player.summoner_name}}

        self.table.update_one(query, values)

    def updatePlayerRoles(self, _id: str, roles: list[str]):
        query = {"_id": _id}
        values = {"$set": {"roles": roles}}

        self.table.update_one(query, values)

    def updatePlayerElo(self, _id: str, elo: int):
        query = {"_id": _id}
        values = {"$set": {"elo": elo}}

        self.table.update_one(query, values)

    def updatePlayerSummonerName(self, _id: str, summoner_name: str):
        query = {"_id": _id}
        values = {"$set": {"summoner_name": summoner_name}}

        self.table.update_one(query, values)
