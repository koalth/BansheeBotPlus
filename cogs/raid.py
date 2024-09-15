import discord
from discord.utils import get

from typing import Optional

from core import Cog, Context, ServerModel, CharacterModel


class Raid(Cog):
    """Commands related to the raid roster"""

    @discord.command(
        name="roster", description="Displays the roster of all registered characters"
    )
    async def roster(self, ctx: Context):
        pass

    @discord.command(
        name="readycheck",
        description="Checks all registered characters for raid requirements",
    )
    async def readycheck(self, ctx: Context):
        pass

    @discord.command(
        name="register", description="Register a World of Warcraft character"
    )
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
    async def register(
        self,
        ctx: Context,
        name: str,
        realm: str,
        region: str,
        member: Optional[discord.Member],
    ):
        assert ctx.guild_id
        profile = await ctx.getCharacterProfile(name, realm, region)

        server = await ServerModel.get(discord_guild_id=ctx.guild_id)

        discord_id = ctx.author.id
        if member is not None:
            discord_id = member.id

        character = CharacterModel(
            discord_user_id=discord_id,
            name=profile.name,
            realm=profile.realm,
            region=profile.region,
            item_level=profile.item_level,
            raid_roster=server.id,
        )

        await character.save()

        return await ctx.respond(
            f"`{character.name}`-`{character.realm}` has been registered!"
        )


def setup(bot):
    bot.add_cog(Raid(bot))
