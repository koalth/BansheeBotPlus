import discord
from discord.utils import get
from discord.ext import commands

from core import Cog, Context, ServerModel


class Server(Cog):
    """Commands related to server settings"""

    async def show(self, ctx: Context):
        """Show the settings for this server."""
        pass

    async def set_manager_role(self, ctx: Context, role: discord.Role):
        """Set the manager role"""
        pass

    async def set_raider_role(self, ctx: Context, role: discord.Role):
        """Set the raider role"""
        pass

    guild = discord.SlashCommandGroup(
        "guild",
        "Commands related to the World of Warcraft guild.",
        guild_only=True,
        default_member_permissions=discord.Permissions(manage_guild=True)
    )

    @guild.command(name="set")
    @discord.option("name", description="The name of the guild in World of Warcraft")
    @discord.option("realm", description="The realm of the guild in World of Warcraft")
    @discord.option("region", description="The region of the guild in World of Warcraft")
    async def set_wow_guild(self, ctx: Context, name: str, realm: str, region: str):
        """Sets the World of Warcraft guild"""
        pass

    @guild.command(name="show")
    async def show_guild(self, ctx: Context):
        """Show the World of Warcraft guild"""
        pass

    @commands.Cog.listener()
    async def on_guild_join(self, ctx: Context, guild: discord.Guild):
        """Creates the Server model when bot joins the server"""
        exists = await ServerModel.exists(discord_guild_id=guild.id)
        if exists:
            return

        db_guild = await ServerModel.create(discord_guild_id=guild.id)
        await db_guild.save()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """Delete the associated server model for this server"""
        pass


def setup(bot):
    bot.add_cog(Server(bot))
