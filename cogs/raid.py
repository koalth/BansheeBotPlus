import discord
from discord.utils import get

from typing import Optional

from core import Cog, Context, ServerModel, CharacterModel


class Raid(Cog):
    """Commands related to the raid roster"""

    raid = discord.SlashCommandGroup(
        name="raid",
        description="Commands related to raid roster",
        guild_only=True
    )

    @raid.command(name="show", description="Show the raid roster")
    async def show_raid(self, ctx: Context):
        pass

    @raid.command(name="refresh", description="Refresh the character data of the raiders")
    async def refresh_raid(self, ctx: Context):
        pass

    @raid.command(name="add", description="Add a character to be tracked")
    @discord.option(name="name", description="Name of the World of Warcraft character")
    @discord.option(
        name="realm", description="Realm of the World of Warcraft character"
    )
    @discord.option(
        name="region", description="Region of the World of Warcraft character"
    )
    @discord.option(
        name="member",
        input_type=discord.Member,
        description="Server member that the character belongs to. Default is the member who used this command",
    )
    async def add_raid(
        self,
        ctx: Context,
        name: str,
        realm: str,
        region: str,
        member: Optional[discord.Member],
    ):
        pass


def setup(bot):
    bot.add_cog(Raid(bot))
