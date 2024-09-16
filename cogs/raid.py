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
        assert ctx.guild_id

        server = await ServerModel.get(discord_guild_id=ctx.guild_id).prefetch_related(
            "raiders"
        )

        raider_names = "\n".join([raider.name for raider in server.raiders])
        class_specs = "\n".join([f"{raider.class_name}" for raider in server.raiders])

        embed = discord.Embed(title="Raid Roster", color=discord.Color.blue())

        embed.add_field(name="Raiders", value=raider_names, inline=True)
        embed.add_field(name="Class", value=class_specs, inline=True)

        return await ctx.respond(embed=embed)

    @discord.command(
        name="readycheck",
        description="Checks all registered characters for raid requirements",
    )
    async def readycheck(self, ctx: Context):

        assert ctx.guild_id
        server = await ServerModel.get(discord_guild_id=ctx.guild_id).prefetch_related(
            "raiders"
        )

        if server.raid_roster_item_level_requirement is None:
            return await ctx.respond("The item level requirements are not set")

        item_levels_pre = []
        for raider in server.raiders:
            item_levels_pre.append(
                f"{str(raider.item_level)} {'✅' if raider.item_level >= server.raid_roster_item_level_requirement else '❌'}"
            )

        item_levels = "\n".join(item_levels_pre)
        raider_names = "\n".join([raider.name for raider in server.raiders])
        class_specs = "\n".join(
            [f"{raider.class_name}/{raider.spec_name}" for raider in server.raiders]
        )

        embed = discord.Embed(
            title="Raid Roster Ready Check!", color=discord.Color.red()
        )

        embed.add_field(name="Members", value=raider_names, inline=True)
        embed.add_field(name="Item Level", value=item_levels, inline=True)
        embed.add_field(name="Class/Spec", value=class_specs, inline=True)

        return await ctx.respond(embed=embed)

    @discord.command(
        name="register", description="Register a World of Warcraft character"
    )
    @discord.option(name="name", description="Name of the World of Warcraft character")
    @discord.option(
        name="realm", description="Realm of the World of Warcraft character"
    )
    @discord.option(
        name="region",
        description="Region of the World of Warcraft character",
        choices=["us"],
    )
    async def register(
        self,
        ctx: Context,
        name: str,
        realm: str,
        region: str,
    ):

        # check if character already exists
        exists = await CharacterModel.exists(name=name, realm=realm)

        if exists:
            return ctx.respond(f"`{name}` has already been registered")

        assert ctx.guild_id
        profile = await ctx.getCharacterProfile(name, realm, region)

        server = await ServerModel.get(discord_guild_id=ctx.guild_id)

        discord_id = ctx.author.id

        character = CharacterModel(
            discord_user_id=discord_id,
            name=profile.name,
            realm=profile.realm,
            region=profile.region,
            item_level=profile.item_level,
            raid_roster_id=server.id,
            class_name=profile.class_name,
            spec_name=profile.active_spec,
        )

        await character.save()

        return await ctx.respond(
            f"`{character.name}`-`{character.realm}` has been registered!"
        )


def setup(bot):
    bot.add_cog(Raid(bot))
