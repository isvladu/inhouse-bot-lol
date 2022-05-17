import logging
import random
import string
from scrim_bot.core.player import Player

from scrim_bot.core.role import Role

logger = logging.getLogger(__name__)


class Match:
    """
    Represents a match taking place.
    """

    game_id: int
    game_password: str
    blue_team: dict(Role, Player)
    red_team: dict(Role, Player)
    outcome: bool  # 0 if blue is the winner, 1 if red is the winner

    def __init__(self, game_id: int, blue_team: dict(Role, Player), red_team: dict(Role, Player)):
        self.blue_team = blue_team
        self.red_team = red_team
        self.game_password = random.choices(
            string.ascii_letters + string.digits, k=8)

    def getGameId(self) -> str:
        return f"inhouse{str(self.game_id)}"

    def getGamePassword(self) -> str:
        return self.game_password

    # Returns a tuple whose first element is the winner and the second element is the loser
    def getTeamResults(self):
        if self.outcome == 0:
            return self.blue_team, self.red_team
        else:
            return self.red_team, self.blue_team
