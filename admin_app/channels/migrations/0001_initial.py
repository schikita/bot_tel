# Generated by Django 5.1.4 on 2025-01-17 06:49

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Channel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Имя канала",
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        unique=True,
                        verbose_name="Ссылка на Telegram-канал",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активен"),
                ),
                (
                    "interval_minutes",
                    models.PositiveIntegerField(
                        default=2,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Интервал парсинга в минутах",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("post_id", models.PositiveIntegerField(verbose_name="ID поста")),
                (
                    "text",
                    models.TextField(blank=True, null=True, verbose_name="Текст поста"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Дата добавления в БД",
                    ),
                ),
                ("published_at", models.DateTimeField(verbose_name="Дата публикации")),
                (
                    "last_parsed_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        null=True,
                        verbose_name="Время последнего парсинга",
                    ),
                ),
                (
                    "next_parse_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Время начала следующего парсинга",
                    ),
                ),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to="channels.channel",
                        verbose_name="Канал",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
                "unique_together": {("post_id", "channel")},
            },
        ),
    ]
