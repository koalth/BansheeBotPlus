from tortoise import Tortoise, fields
from tortoise.models import Model

""" Represents the discord server and the World of Warcraft Guild tied to the Discord server"""


class ServerModel(Model):
    id = fields.IntField(primary_key=True)
    discord_guild_id = fields.IntField(unique=True)

    manager_role_id = fields.IntField(null=True)
    raid_role_id = fields.IntField(null=True)
    raid_roster_channel_id = fields.IntField(null=True)
    raid_roster_item_level_requirement = fields.IntField(null=True)

    guild: fields.ReverseRelation["GuildModel"]
    raiders: fields.ReverseRelation["CharacterModel"]

    class Meta:
        table = "servers"


""" Represents the World of Warcraft Guild tied to the server"""


class GuildModel(Model):
    id = fields.IntField(primary_key=True)

    name = fields.TextField()
    realm = fields.TextField()
    region = fields.TextField()

    server: fields.OneToOneNullableRelation[ServerModel] = fields.OneToOneField(
        "models.ServerModel",
        on_delete=fields.OnDelete.CASCADE,
        related_name="guild",
        to_field="discord_guild_id",
    )


""" Represents the World of Warcraft Character tied to a user """


class CharacterModel(Model):
    id = fields.IntField(primary_key=True)
    discord_user_id = fields.IntField()

    name = fields.TextField()
    realm = fields.TextField()
    region = fields.TextField()

    item_level = fields.IntField()
    class_name = fields.TextField()
    spec_name = fields.TextField()
    profile_url = fields.TextField()
    thumbnail_url = fields.TextField()

    raid_roster: fields.ForeignKeyNullableRelation[ServerModel] = (
        fields.ForeignKeyField("models.ServerModel", related_name="raiders")
    )

    class Meta:
        table = "characters"
