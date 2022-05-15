import asyncio
import logging

import discord
from discord.ext import commands

from scrim_bot.core.player import Player
from scrim_bot.core.role import RoleIsInvalid
from scrim_bot.database_orm.player_connection import PlayerConnection
from scrim_bot.scrim_bot import ScrimBot
from scrim_bot.utils.constants import MEMBER_ROLE_ID, REG_CHANNEL_ID, ROLE_REG_CHANNEL_ID, SUMM_REG_CHANNEL_ID
from scrim_bot.utils.summoner_validator import Summoner


class RegistrationCog(commands.Cog, name="Role"):
    """
    Manages role registration
    """

    def __init__(self, bot: ScrimBot):
        self.bot = bot
        self.connection = PlayerConnection()
        self.logger = logging.getLogger(__name__)

    @commands.command()
    async def register(self, ctx: commands.Context):
        if ctx.channel.id != REG_CHANNEL_ID:
            await ctx.send("Please use this command in it's respective channel: #registration!")
            return

        member_role = ctx.guild.get_role(MEMBER_ROLE_ID)
        if member_role in ctx.author.roles:
            await ctx.send("You are already registered!")
        else:
            await ctx.author.add_roles(member_role)
            await ctx.author.send(f"Hello @{ctx.author.name}!")

    @commands.command()
    async def add_roles(self, ctx: commands.Context):
        if ctx.channel.id != ROLE_REG_CHANNEL_ID:
            await ctx.send("Please use this command in it's respective channel: #role_registration!")
            return

        role_list = ctx.message.content.split(' ')[1:]
        player = self.connection.getPlayer(ctx.author.id)

        if player is None:
            new_player = Player(_id=ctx.author.id, name=ctx.author.name, roles=role_list)
            self.connection.insertPlayer(new_player)
            embed = discord.Embed(title=f"Registered __{new_player.name}__ to the database with roles",
                                  description=', '.join(new_player.getRoles()))
            await ctx.send(embed=embed)
        else:
            try:
                player.addRoles(role_list)
            except RoleIsInvalid as e:
                await ctx.send(f"Role {e.role} is invalid! Please try again!")
                return
            self.connection.updatePlayerRoles(player)
            embed = discord.Embed(title=f"Updated __{player.name}'s__ roles to",
                                  description=', '.join(player.getRoles()))
            await ctx.send(embed=embed)

    @commands.command()
    async def remove_roles(self, ctx: commands.Context):
        if ctx.channel.id != ROLE_REG_CHANNEL_ID:
            await ctx.send("Please use this command in it's respective channel: #role_registration!")
            return

        role_list = ctx.message.content.split(' ')[1:]
        player = self.connection.getPlayer(ctx.author.id)

        if player is None:
            await ctx.send("You don't have any roles registered!")
        else:
            try:
                player.removeRoles(role_list)
            except RoleIsInvalid as e:
                await ctx.send(f"Role {e.role} is invalid! Please try again!")
                return
            self.connection.updatePlayerRoles(player)
            embed = discord.Embed(title=f"Updated __{player.name}'s__ roles to",
                                  description=', '.join(player.getRoles()))
            await ctx.send(embed=embed)

    @commands.command()
    async def add_summoner(self, ctx: commands.Context):
        if ctx.channel.id != SUMM_REG_CHANNEL_ID:
            await ctx.send("Please use this command in it's respective channel: #summoner_registration!")
            return

        summoner_name = ctx.message.content.split(' ')[1]
        player = self.connection.getPlayer(ctx.author.id)
        summ_validator = Summoner(summoner_name)

        embed = discord.Embed(title=ctx.author.name,
                              description="Please change your profile icon in the League Client to the following to "
                                          "validate your account.")
        embed.set_image(url=summ_validator.getSummonerIconURL())
        await ctx.author.send(embed=embed)

        while not summ_validator.validateSummoner():
            if summ_validator.timer > 0:
                summ_validator.timer -= 2
                await asyncio.sleep(2)
            else:
                await ctx.send("Failed to validate your account in time. Please try again!")
                return

        if player is None:
            new_player = Player(_id=ctx.author.id, name=ctx.author.name, summoner_name=summoner_name)
            self.connection.insertPlayer(new_player)
            embed = discord.Embed(title=f"Registered __{new_player.name}__ to the database with summoner name",
                                  description=new_player.summoner_name)
            await ctx.send(embed=embed)
        else:
            player.summoner_name = summoner_name
            self.connection.updatePlayerSummonerName(player)
            embed = discord.Embed(title=f"Updated __{player.name}'s__ summoner name to",
                                  description=player.summoner_name)
            await ctx.send(embed=embed)

    @commands.command()
    async def remove_summoner(self, ctx: commands.Context):
        if ctx.channel.id != SUMM_REG_CHANNEL_ID:
            await ctx.send("Please use this command in it's respective channel: #summoner_registration!")
            return

        summoner_name = ctx.message.content.split(' ')[1]
        player = self.connection.getPlayer(ctx.author.id)

        if player is None:
            await ctx.send("That summoner name is not linked to you!")
        else:
            player.summoner_name = None
            self.connection.updatePlayerSummonerName(player)
            embed = discord.Embed(title=f"Removed __{player.name}'s__ summoner name",
                                  description=player.summoner_name)
            await ctx.send(embed=embed)

# TODO: Remove remove_summoner as it's use is not necessary.
#       Implement elo on summoner_name registration first time only to set the starting elo for each player.
#       Doesn't update when you change summoner name.
