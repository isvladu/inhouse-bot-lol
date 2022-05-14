import discord
from discord.ext import commands
import logging

from scrim_bot.scrim_bot import ScrimBot

from scrim_bot.database_orm.player_connection import PlayerConnection
from scrim_bot.core.player import Player
from scrim_bot.core.role import RoleIsInvalid


class RoleCog(commands.Cog, name="Role"):
    """
    Manages role registration
    """

    def __init__(self, bot: ScrimBot):
        self.bot = bot
        self.connection = PlayerConnection()
        self.logger = logging.getLogger(__name__)

    @commands.command(aliases=["register_roles"])
    async def add_roles(self, ctx: commands.Context):
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
        role_list = ctx.message.content.split(' ')[1:]
        player = self.connection.getPlayer(ctx.author.id)

        if player is None:
            await ctx.send("You are not registered yet! Please register first before removing any roles!")
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
