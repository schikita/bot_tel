import uuid

from pymorphy3 import MorphAnalyzer
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
        table = "channels_channel"


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
        table = "channels_post"
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
        table = "users_admin"


class SearchWord(Model):
    id = fields.IntField(pk=True)
    word = fields.CharField(max_length=255, unique=True)
    lemma = fields.CharField(max_length=255, null=True, blank=True)

    class Meta:
        table = "users_searchword"


async def add_or_update_keyword(word: str):
    """Добавить или обновить ключевое слово и его лемму."""
    existing_word = await SearchWord.filter(word=word).first()

    if existing_word:
        if not existing_word.lemma:
            existing_word.lemma = lemmatize_word(word)
            await existing_word.save()
        return existing_word
    lemma = lemmatize_word(word)
    new_word = await SearchWord.create(word=word, lemma=lemma)
    return new_word


class AdminSearchWord(Model):
    admin = fields.ForeignKeyField("models.Admin", on_delete=fields.CASCADE)
    search_word = fields.ForeignKeyField("models.SearchWord", on_delete=fields.CASCADE)

    class Meta:
        table = "users_admin_searchwords"


class AdminChannel(Model):
    admin = fields.ForeignKeyField("models.Admin", on_delete=fields.CASCADE)
    channel = fields.ForeignKeyField("models.Channel", on_delete=fields.CASCADE)

    class Meta:
        table = "users_admin_channels"


morph = MorphAnalyzer()


async def get_keywords():
    """Получить все ключевые слова и их леммы из базы данных."""
    keywords = await SearchWord.all().values_list("word", "lemma")
    print(keywords)
    print(keywords)
    print(keywords)
    print(keywords)
    print(keywords)
    print(keywords)
    return keywords


def lemmatize_word(word: str) -> str:
    """Лемматизация слова с использованием pymorphy3."""
    return morph.parse(word)[0].normal_form
