import asyncio
from datetime import datetime
import logging

import discord
from discord.ext import commands, tasks

from scrim_bot.core.player import Player
from scrim_bot.core.queue import AlreadyInQueue, NotInQueue, Queue
from scrim_bot.database_orm.player_connection import PlayerConnection
from scrim_bot.interfaces.observer import Observer, Subject
from scrim_bot.scrim_bot import ScrimBot
from scrim_bot.utils.constants import PREFIX, QUEUE_CHANNEL_ID, SUMM_REG_CHANNEL_ID


class FinalMeta(type(Observer), type(commands.Cog)):
    pass


class QueueCog(Observer, commands.Cog, metaclass=FinalMeta):
    """
    Manages queue and games.
    """

    def __init__(self, bot: ScrimBot):
        self.bot = bot
        self.connection = PlayerConnection()
        self.logger = logging.getLogger(__name__)

        self.queueIsStarted = False
        self.matchIsStarted = False

        self.queue = Queue()
        self.queue.attach(self)

        self.queue_message: discord.Message = None

    def update(self, subject: Subject) -> None:
        if subject.players_in_queue > 9:
            self.findValidMatch.start()
            self.showQueue.stop()
            self.queueIsStarted = False
            self.logger.info("Queue is filled with players")
        if subject.players_in_queue > 0 and not self.queueIsStarted:
            self.showQueue.start()
            self.queueIsStarted = True
        if subject.players_in_queue == 0 and self.queueIsStarted:
            self.queueIsStarted = False
            self.showQueue.stop()
            asyncio.run(self.queue_message.delete())

    def getChannel(self):
        return self.bot.get_channel(SUMM_REG_CHANNEL_ID)

    @tasks.loop(seconds=1)
    async def showQueue(self):
        self.queue.timer += 1
        m, s = divmod(self.queue.timer, 60)
        self.logger.info("Showing current queue...")
        description = ""
        guild = self.bot.guilds[0]
        for player in self.queue.queue_list:
            mention = guild.get_member(player.id).mention
            description += f"{mention}\n"
        embed = discord.Embed(
            title=f"Queue - {m}min, {s}s", description=description)
        if self.queue_message is None:
            self.queue_message = await self.getChannel().send(embed=embed)
        else:
            await self.queue_message.edit(embed=embed)

    @tasks.loop(seconds=5)
    async def findValidMatch(self):
        self.logger.info("Finding match...")
        self.queue.findMatch()

    @commands.command()
    async def queue(self, ctx: commands.Context):
        # if ctx.channel.id != QUEUE_CHANNEL_ID:
        #     await ctx.send("Please use this command in it's respective channel: #queue.")
        #     return
        player = self.connection.getPlayer(ctx.author.id)
        try:
            self.queue.addPlayerToQueue(player)
        except AlreadyInQueue as e:
            await ctx.send(f"{ctx.author.name} you are already in queue!")

    @commands.command()
    async def leave(self, ctx: commands.Context):
        player = self.connection.getPlayer(ctx.author.id)
        try:
            self.queue.removePlayerFromQueue(player)
        except NotInQueue as e:
            await ctx.send(f"{ctx.author.name} you are not in queue!")

    @commands.command()
    async def getQueue(self, ctx: commands.Context):
        await ctx.send(f"Time elapsed: {self.queue.getQueueTimer(datetime.now())[0]}min, {self.queue.getQueueTimer(datetime.now())[1]}s.")
        await ctx.send([f"{player.id} - {player.name}" for player in self.queue.queue_list])
