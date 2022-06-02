import logging

from datetime import datetime

from scrim_bot.core.player import Player
from scrim_bot.interfaces.observer import Subject, Observer

logger = logging.getLogger(__name__)


class AlreadyInQueue(Exception):
    """
    Exception raised when a player is already in queue.
    """


class NotInQueue(Exception):
    """
    Exception raised when a player is not in queue.
    """


class Queue(Subject):
    """
    Class representing a queue.
    """

    queue_list: list[Player]
    players_in_queue: int
    timer: int = 0  # Representation in seconds of the queue timer
    _observers: list[Observer] = []

    def __init__(self, queue_list: list[Player] = None):
        if queue_list is None:
            self.queue_list = []
            self.players_in_queue = 0
        else:
            self.queue_list = queue_list
            self.players_in_queue = len(queue_list)

    def attach(self, observer: Observer) -> None:
        logger.info(f"Queue: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        logger.info(f"Queue: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def addPlayerToQueue(self, player: Player):
        if player in self.queue_list:
            logger.error("Player already in queue!")
            raise AlreadyInQueue(player)

        if not self.queue_list:
            self.start_time = datetime.now()
        self.queue_list.append(player)
        self.players_in_queue += 1
        self.notify()
        logger.info(f"Added player {player.id} - {player.name} to queue")

    def removePlayerFromQueue(self, player: Player):
        if player not in self.queue_list:
            logger.error("Player not in queue!")
            raise NotInQueue(player)
        self.queue_list.remove(player)
        self.players_in_queue -= 1
        self.notify()

    def findMatch(self): # TODO: implement this
        pass
