import discord
from discord.utils import get
from discord.ext import commands
from discord import guild_only

from typing import Optional

from core import Cog, Context, ServerModel


class Server(Cog):
    """Commands related to server settings"""

    @discord.command(name="show", description="Show the current server settings")
    @guild_only()
    async def show(self, ctx: Context):
        """Show the settings for this server."""
        assert ctx.guild_id
        server = await ServerModel.get(discord_guild_id=ctx.guild_id)

        embed = discord.Embed(title=f"Server Settings", color=discord.Color.blurple())

        embed.add_field(
            name="Manager Role",
            value=ctx._get_role_name_or_empty(server.manager_role_id),
        )

        embed.add_field(
            name="Raid Role",
            value=ctx._get_role_name_or_empty(server.raid_role_id),
        )

        return await ctx.respond(embed=embed)

    @discord.command(
        name="setmanagerrole",
        description="Sets the manager role for the server. Managers can use admin commands within the bot",
    )
    @guild_only()
    async def set_manager_role(self, ctx: Context, role: discord.Role):
        """Set the manager role"""
        assert ctx.guild_id
        await ServerModel.filter(discord_guild_id=ctx.guild_id).update(
            manager_role_id=role.id
        )

    @discord.command(
        name="setraiderrole", description="Set the raider role for the server"
    )
    @guild_only()
    async def set_raider_role(self, ctx: Context, role: discord.Role):
        """Set the raider role"""
        assert ctx.guild_id
        await ServerModel.filter(discord_guild_id=ctx.guild_id).update(
            raid_role_id=role.id
        )

    @discord.command(
        name="setitemlevel",
        description="Set the item level requirement for the raid roster",
    )
    @guild_only()
    async def set_item_level_requirement(self, ctx: Context, item_level: int):
        assert ctx.guild_id
        await ServerModel.filter(discord_guild_id=ctx.guild_id).update(
            raid_roster_item_level_requirement=item_level
        )

    guild = discord.SlashCommandGroup(
        "guild",
        "Commands related to the World of Warcraft guild.",
        default_member_permissions=discord.Permissions(manage_guild=True),
    )

    @guild.command(name="set")
    @guild_only()
    @discord.option("name", description="The name of the guild in World of Warcraft")
    @discord.option("realm", description="The realm of the guild in World of Warcraft")
    @discord.option(
        "region", description="The region of the guild in World of Warcraft"
    )
    async def set_wow_guild(self, ctx: Context, name: str, realm: str, region: str):
        """Sets the World of Warcraft guild"""
        pass

    @guild.command(name="show")
    async def show_guild(self, ctx: Context):
        """Show the World of Warcraft guild"""
        pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Creates the Server model when bot joins the server"""
        exists = await ServerModel.exists(discord_guild_id=guild.id)
        if exists:
            return

        db_guild = await ServerModel.create(discord_guild_id=guild.id)
        await db_guild.save()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """Delete the associated server model for this server"""
        db_guild = await ServerModel.get(iscord_guild_id=guild.id)
        await ServerModel.delete(db_guild)


def setup(bot):
    bot.add_cog(Server(bot))
