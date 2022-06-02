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
from scrim_bot.utils.constants import PREFIX, QUEUE_CHANNEL_ID


class FinalMeta(type(Observer), type(commands.Cog)):
    pass

# TODO: This whole shit will need to be refactored at one point.
# TODO: Investigate about queue_channel needing to initialized at start or not.


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

        self.queueObject = Queue()
        self.queueObject.attach(self)

        self.queue_message: discord.Message = None
        self.queue_channel = bot.get_channel(QUEUE_CHANNEL_ID)

    def update(self, subject: Subject) -> None:
        if subject.players_in_queue > 9:
            self.logger.info("Finding match...")
            self.queueObject.findMatch()  # TODO: implement this
            self.showQueue.stop()
            self.queueIsStarted = False
            self.logger.info("Queue is filled with players")
            return
        if subject.players_in_queue > 0 and not self.queueIsStarted:
            self.showQueue.start()
            self.queueIsStarted = True
            return
        if subject.players_in_queue == 0 and self.queueIsStarted:
            self.queueIsStarted = False
            self.queueObject.timer = 0
            self.showQueue.stop()
            return

    def getChannel(self):
        return self.bot.get_channel(QUEUE_CHANNEL_ID)

    @tasks.loop(seconds=1)
    async def showQueue(self):
        self.queueObject.timer += 1
        m, s = divmod(self.queueObject.timer, 60)
        self.logger.info("Showing current queue...")
        description = ""
        guild = self.bot.guilds[0]
        for player in self.queueObject.queue_list:
            mention = guild.get_member(player.id).mention
            description += f"{mention}\n"
        embed = discord.Embed(
            title=f"Queue - {m}min, {s}s elapsed", description=description)
        if self.queue_message is None:
            self.queue_message = await self.getChannel().send(embed=embed)
        else:
            await self.queue_message.edit(embed=embed)

    @showQueue.after_loop
    async def after_showQueue(self):
        self.logger.info("Entered after loop")
        await self.queue_message.delete()
        self.queue_message = None

    @commands.command(aliases=["q"])
    async def queue(self, ctx: commands.Context):
        if ctx.channel.id != QUEUE_CHANNEL_ID:
            await ctx.send("Please use this command in it's respective channel: #queue.")
            return
        player = self.connection.getPlayer(ctx.author.id)
        try:
            self.queueObject.addPlayerToQueue(player)
            await asyncio.sleep(3)
            await ctx.message.delete()
        except AlreadyInQueue as e:
            await ctx.send(f"{ctx.author.name} you are already in queue!", delete_after=3)

    @commands.command(aliases=["l"])
    async def leave(self, ctx: commands.Context):
        player = self.connection.getPlayer(ctx.author.id)
        try:
            self.queueObject.removePlayerFromQueue(player)
            await asyncio.sleep(3)
            await ctx.message.delete()
        except NotInQueue as e:
            await ctx.send(f"{ctx.author.name} you are not in queue!", delete_after=3)
