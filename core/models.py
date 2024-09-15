from tortoise import Tortoise, fields
from tortoise.models import Model

""" Represents the discord server and the World of Warcraft Guild tied to the Discord server"""
class ServerModel(Model):
    id = fields.IntField(primary_key=True)
    discord_guild_id = fields.IntField(unique=True)
    
    name = fields.TextField(null=True)
    realm = fields.TextField(null=True)
    region = fields.TextField(null=True)
    
    manager_role_id = fields.IntField(null=True)
    raid_role_id = fields.IntField(null=True)
    raid_roster_channel_id = fields.IntField(null=True)
    raid_roster_item_level_requirement = fields.IntField(null=True)
    
    raiders: fields.ReverseRelation["CharacterModel"]
    
    def __str__(self):
        return f"<ServerModel(name={self.name}, realm={self.region}, region={self.region})>"
    
    class Meta:
        table = "servers"

""" Represents the World of Warcraft Character tied to a user """
class CharacterModel(Model):
    id = fields.IntField(primary_key=True)
    discord_user_id = fields.IntField()

    name = fields.TextField()
    realm = fields.TextField()
    region = fields.TextField()

    item_level = fields.IntField()

    raid_roster: fields.ForeignKeyNullableRelation[ServerModel] = fields.ForeignKeyField(
        "models.ServerModel", related_name="raiders"
    )

    class Meta:
        table = "characters"
