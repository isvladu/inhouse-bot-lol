from typing import Optional

from scrim_bot.core.player import Player
from scrim_bot.database_orm.connection import Connection


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

    def updatePlayerRoles(self, player: Player):
        query = {"_id": player.id}
        values = {"$set": {"roles": player.getRoles()}}

        self.table.update_one(query, values)

    def updatePlayerElo(self, player: Player):
        query = {"_id": player.id}
        values = {"$set": {"elo": player.elo}}

        self.table.update_one(query, values)

    def updatePlayerSummonerName(self, player: Player):
        query = {"_id": player.id}
        values = {"$set": {"summoner_name": player.summoner_name}}

        self.table.update_one(query, values)
