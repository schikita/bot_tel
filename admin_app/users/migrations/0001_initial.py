import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('telegram_id', models.CharField(max_length=255, unique=True, verbose_name='Telegram ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя администратора')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
            ],
        ),
        migrations.CreateModel(
            name='SearchWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255, unique=True, verbose_name='Ключевое слово')),
                ('lemma', models.CharField(blank=True, max_length=255, null=True, verbose_name='Лемма слова')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.admin', verbose_name='Админ')),
            ],
        ),
    ]
