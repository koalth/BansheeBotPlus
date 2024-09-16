from os import getenv
import dotenv

from typing import Optional

import discord
from discord import ApplicationContext, Color, Embed
from discord.utils import utcnow

from .api import LichClient, CharacterProfileResponse


class Context(ApplicationContext):

    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> CharacterProfileResponse:
        client_id = getenv("BLIZZARD_CLIENT_ID")
        client_secret = getenv("BLIZZARD_CLIENT_SECRET")

        client = LichClient(client_id, client_secret)

        profile = await client.getCharacterProfile(name, realm, region)

        return profile

    def _get_role_name_or_empty(self, role_id: Optional[int]) -> str:
        if role_id is None:
            return "`None`"

        role = self.guild.get_role()

        if role is None:
            return "`None`"

        return f"`{role.name}`"

    async def success(self, title: str, description: str | None = None, **kwargs):
        embed = Embed(
            title=title,
            description=description,
            timestamp=utcnow(),
            color=Color.green(),
        )

        return await self.respond(embed=embed, **kwargs)

    async def exception(self, title: str, description: str | None = None, **kwargs):
        embed = Embed(
            title=title, description=description, timestamp=utcnow(), color=Color.red()
        )

        return await self.respond(embed=embed, **kwargs)

    async def info(self, title: str, description: str | None = None, **kwargs):
        embed = Embed(
            title=title, description=description, timestamp=utcnow(), color=Color.blue()
        )

        return await self.respond(embed=embed, **kwargs)
