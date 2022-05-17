import logging

from datetime import datetime

from scrim_bot.core.player import Player

logger = logging.getLogger(__name__)


class Queue:
    """
    Class representing a queue.
    """

    queue_list: list[Player]
    start_time: datetime

    def __init__(self, queue_list: list[Player] = None):
        if queue_list is None:
            self.queue_list = []
        else:
            self.queue_list = queue_list

    # Returns current queue timer as a tuple of (minutes, seconds)
    def getQueueTimer(self, current_time: datetime):
        difference = (current_time - self.start_time).total_seconds()
        m, s = divmod(difference, 60)
        return m, s

    def addPlayerToQueue(self, player: Player):
        if player in self.queue_list:
            logger.error("Player already in queue!")
            return # this needs to raise an exception
        
        if self.queue_list:
            self.start_time = datetime.now()
        self.queue_list.append(player)
        logger.info(f"Added player {player.id} - {player.name} to queue")
        
        if len(self.queue_list) > 9:
            self.findMatch()

    def removePlayerFromQueue(self, player: Player):
        if player not in self.queue_list:
            logger.error("Player not in queue!")
            return # this needs to raise an exception
        self.queue_list.remove(player)
        
    def findMatch(self):
        pass
