import os
import dotenv

from discord import ApplicationContext, Color, Embed
from discord.utils import utcnow

from ..api import LichClient, CharacterProfileResponse

class Context(ApplicationContext):

    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> CharacterProfileResponse:
        client_id = ""
        client_secret = ""

        client = LichClient(client_id, client_secret)

        profile = await client.getCharacterProfile(name, realm, region)

        return profile

    async def success(self, title: str, description: str | None = None, **kwargs):
        embed = Embed(
            title=title,
            description=description,
            timestamp=utcnow(),
            color=Color.green()
        )

        return await self.respond(embed=embed, **kwargs)

    async def exception(self, title: str, description: str | None = None, **kwargs):
        embed = Embed(
            title=title,
            description=description,
            timestamp=utcnow(),
            color=Color.red()
        )

        return await self.respond(embed=embed, **kwargs)

    async def info(self, title: str, description: str | None = None, **kwargs):
        embed = Embed(
            title=title,
            description=description,
            timestamp=utcnow(),
            color=Color.blue()
        )

        return await self.respond(embed=embed, **kwargs)
