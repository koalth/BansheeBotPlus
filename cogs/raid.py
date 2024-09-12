import discord
from discord.utils import get

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
    
    unlinked = raid.create_subgroup(
        name="unlinked",
        description="Commands related to unlinked raid members"
    )
    
    @unlinked.command(name="list", description="List the unlinked members with the raider role")
    async def list_unlinked(self, ctx: Context):
        pass
    
    @unlinked.command(name="message", description="Message the unlinked members with the raider role")
    async def message_unlinked(self, ctx: Context):
        pass
    
    linked = raid.create_subgroup(
        name="linked",
        description="Commands related to linked raid members"
    )
    
    @linked.command(name="list", description="List the linked members with the raid roles")
    async def list_linked(self, ctx: Context):
        pass
    
    @linked.command(name="message", description="Message the linked members with raid roles")
    async def message_linked(self, ctx: Context):
        pass