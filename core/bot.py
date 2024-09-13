from os import environ, getenv
from glob import glob

import discord
from discord.ext import commands
from tortoise import Tortoise

from .context import Context
from .models import ServerModel, CharacterModel

class BansheeBot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(
            intents=discord.Intents(
                members=True,
                messages=True,
                message_content=True,
                guilds=True
            )
        )

    async def setup_tortoise(self) -> None:
        await Tortoise.init(
            db_url="sqlite://data/database.db", modules={"models": ["core.models"]}
        )
        await Tortoise.generate_schemas()

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        await self.setup_tortoise()
        return await super().start(token, reconnect=reconnect)

    async def close(self) -> None:
        await Tortoise.close_connections()
        return await super().close()

    async def get_application_context(
        self, interaction: discord.Interaction
    ) -> Context:
        return Context(self, interaction)

    def run(self, debug: bool = False, cogs: list[str] | None = None) -> None:
        default_cog_list = ["cogs.raid", "cogs.server"]
        for cog in default_cog_list:
            self.load_extension(cog)

        if debug:
            return super().run(getenv("DEBUG_TOKEN", getenv("TOKEN")))

        super().run(getenv("TOKEN"))

    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        await ctx.respond(
            embed=discord.Embed(
                title=error.__class__.__name__,
                description=str(error),
                color=discord.Color.red()
            )
        )
