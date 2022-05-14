from config import TOKEN
from scrim_bot.utils.constants import PREFIX
import logging

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True


class ScrimBot(commands.Bot):
    """
    Bot handling role-based matchmaking for LoL games
    """

    def __init__(self, **options):
        super().__init__(PREFIX, intents=intents, case_insensitive=True, **options)

        from scrim_bot.cogs.role_cog import RoleCog

        self.add_cog(RoleCog(self))

        self.logger = logging.getLogger(__name__)

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user}")

    def run(self, *args, **kwargs):
        super().run(TOKEN, *args, **kwargs)
