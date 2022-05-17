import asyncio
import logging

import discord
from discord.ext import commands

from scrim_bot.core.player import Player
from scrim_bot.core.queue import Queue
from scrim_bot.database_orm.player_connection import PlayerConnection
from scrim_bot.scrim_bot import ScrimBot
from scrim_bot.utils.constants import QUEUE_CHANNEL_ID


class QueueCog(commands.Cog, name="Queue"):
    """
    Manages queue and games.
    """

    def __init__(self, bot: ScrimBot):
        self.bot = bot
        self.queue = Queue()
        self.connection = PlayerConnection()
        self.logger = logging.getLogger(__name__)

    @commands.command()
    async def queue(self, ctx: commands.Context):
        if ctx.channel.id != QUEUE_CHANNEL_ID:
            await ctx.send("Please use this command in it's respective channel: #queue.")
            return

        # When you add a player to the queue it should be enveloped in a try/catch block
        pass
