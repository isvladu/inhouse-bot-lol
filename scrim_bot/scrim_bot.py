import logging

import discord
from discord.ext import commands

from config import TOKEN
from scrim_bot.utils.constants import PREFIX

intents = discord.Intents.default()
intents.members = True


class ScrimBot(commands.Bot):
    """
    Bot handling role-based matchmaking for LoL games
    """

    def __init__(self, **options):
        super().__init__(PREFIX, intents=intents, case_insensitive=True, **options)

        from scrim_bot.cogs.registration_cog import RegistrationCog

        self.add_cog(RegistrationCog(self))

        self.logger = logging.getLogger(__name__)

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user}")

    def run(self, *args, **kwargs):
        super().run(TOKEN, *args, **kwargs)
