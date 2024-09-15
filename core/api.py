from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import List, Optional
from datetime import datetime
import statistics
import math


class Base(BaseModel):
    model_config = ConfigDict(extra="ignore")


class CharacterResponse(Base):
    name: str


class ItemLevelResponse(Base):
    value: int


class ItemSlotResponse(Base):
    type: str


class ItemResponse(Base):
    level: ItemLevelResponse
    slot: ItemSlotResponse


class BlizzardCharacterEquipmentResponse(Base):
    character: CharacterResponse
    equipped_items: List[ItemResponse]

    @computed_field()
    @property
    def item_level(self) -> int:
        slots_to_not_check = set(["TABARD", "SHIRT"])
        item_levels = [
            item.level.value
            for item in self.equipped_items
            if item.slot.type not in slots_to_not_check
        ]
        return int(math.floor(statistics.fmean(item_levels)))


class CharacterGenderResponse(Base):
    name: str


class CharacterFactionResponse(Base):
    name: str


class CharacterRaceResponse(Base):
    name: str


class CharacterClassResponse(Base):
    name: str


class CharacterActiveSpecResponse(Base):
    name: str


class CharacterRealmResponse(Base):
    name: str


class CharacterGuildResponse(Base):
    name: str
    id: int


class BlizzardCharacterProfileResponse(Base):
    id: int
    name: str
    level: int
    average_item_level: int
    equipped_item_level: int

    guild: CharacterGuildResponse
    realm: CharacterRealmResponse
    active_spec: CharacterActiveSpecResponse
    character_class: CharacterClassResponse
    race: CharacterRaceResponse
    faction: CharacterFactionResponse
    gender: CharacterGenderResponse


class CharacterProfileResponse(BaseModel):
    name: str
    realm: str
    region: str

    class_name: str
    active_spec: str
    race: str
    faction: str
    gender: str

    item_level: int
    last_crawled_at: datetime = Field(default=datetime.now())


from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Auth
import httpx
import json
from typing import TypeVar, Type, Optional

ModelT = TypeVar("ModelT", bound=Base)


class BlizzardClient:

    api_url: str = "https://us.api.blizzard.com"
    auth_url: str = "https://oauth.battle.net/token"

    auth_client: AsyncOAuth2Client
    auth: Optional[OAuth2Auth]

    client: Optional[httpx.AsyncClient]

    def __init__(self, client_id: Optional[str], client_secret: Optional[str]) -> None:
        if client_id is None:
            raise Exception("Client ID is None")

        if client_secret is None:
            raise Exception("Client Secret is None")

        self.client_id = client_id
        self.client_secret = client_secret

        self.client = None
        self.access_token = None
        self.auth = None

    async def __aenter__(self):
        await self.authenticate()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        if self.client is None:
            raise Exception("Client is not initilized")

        await self.client.aclose()

    async def authenticate(self):
        async with AsyncOAuth2Client(
            client_id=self.client_id, client_secret=self.client_secret
        ) as oauth:
            access_token = await oauth.fetch_token(self.auth_url)  # type: ignore
            self.auth = OAuth2Auth(token=access_token)

        self.client = httpx.AsyncClient(base_url=self.api_url, auth=self.auth)

    async def _get(self, endpoint: str, data_cls: Type[ModelT]) -> ModelT:
        if self.client is None:
            raise Exception("Client is not initalized")
        response = await self.client.get(endpoint)
        if not response.is_success:
            raise Exception(f"Response did not succeed: {response.text}")

        json_data = json.dumps(response.json())
        return data_cls.model_validate_json(json_data)

    async def get_character_profile(
        self, name: str, realm: str, region: str
    ) -> BlizzardCharacterProfileResponse:
        endpoint = f"/profile/wow/character/{realm.lower()}/{name.lower()}?namespace=profile-us&locale=en_US"
        return await self._get(endpoint, BlizzardCharacterProfileResponse)

    async def get_character_equipment(
        self, name: str, realm: str
    ) -> BlizzardCharacterEquipmentResponse:
        endpoint = f"/profile/wow/character/{realm.lower()}/{name.lower()}/equipment?namespace=profile-us"
        return await self._get(endpoint, BlizzardCharacterEquipmentResponse)


from abc import ABC, abstractmethod


class ILichClient(ABC):

    @abstractmethod
    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> CharacterProfileResponse:
        raise NotImplementedError()


class LichClient(ILichClient):

    client_id: str
    client_secret: str

    def __init__(self, client_id: Optional[str], client_secret: Optional[str]):
        if client_id is None:
            raise Exception("Client ID is None")

        if client_secret is None:
            raise Exception("Client Secret is None")

        self.client_id = client_id
        self.client_secret = client_secret

    async def getCharacterProfile(
        self, name: str, realm: str, region: str
    ) -> CharacterProfileResponse:
        async with BlizzardClient(self.client_id, self.client_secret) as client:
            response = await client.get_character_profile(name, realm, region="us")
            return CharacterProfileResponse(
                name=response.name,
                realm=response.realm.name,
                region=region,
                item_level=response.average_item_level,
                class_name=response.character_class.name,
                active_spec=response.active_spec.name,
                faction=response.faction.name,
                race=response.race.name,
                gender=response.gender.name,
            )
