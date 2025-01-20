import uuid

from tortoise import fields
from tortoise.models import Model


class Channel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255, null=True)
    url = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)
    interval_minutes = fields.IntField(default=2)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table_name = "channels_channel"


class Post(Model):
    id = fields.IntField(pk=True)
    channel = fields.ForeignKeyField(
        "models.Channel",
        related_name="posts",
        on_delete=fields.CASCADE,
    )
    post_id = fields.IntField()
    text = fields.TextField(null=True, blank=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    published_at = fields.DatetimeField(null=True)
    last_parsed_at = fields.DatetimeField(null=True, auto_now_add=True)
    next_parse_at = fields.DatetimeField(null=True, db_index=True)

    class Meta:
        table_name = "channels_post"
        unique_together = ("post_id", "channel")


class Admin(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    telegram_id = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255, null=True, blank=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    words = fields.ManyToManyField(
        "models.SearchWord",
        related_name="users_admin_searchwords",
        through="admin_searchword",
    )
    channels = fields.ManyToManyField(
        "models.Channel",
        related_name="admins",
        through="users_admin_channels",
    )

    class Meta:
        table_name = "users_admin"


class SearchWord(Model):
    id = fields.IntField(pk=True)
    word = fields.CharField(max_length=255, unique=True)
    lemma = fields.CharField(max_length=255, null=True, blank=True)

    class Meta:
        table_name = "users_searchword"


class AdminSearchWord(Model):
    admin = fields.ForeignKeyField("models.Admin", on_delete=fields.CASCADE)
    search_word = fields.ForeignKeyField("models.SearchWord", on_delete=fields.CASCADE)

    class Meta:
        table_name = "users_admin_searchwords"


class AdminChannel(Model):
    admin = fields.ForeignKeyField("models.Admin", on_delete=fields.CASCADE)
    channel = fields.ForeignKeyField("models.Channel", on_delete=fields.CASCADE)

    class Meta:
        table_name = "users_admin_channels"
