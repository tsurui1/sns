# Generated by Django 4.2.1 on 2023-05-26 02:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('insta', '0007_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日'),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='コメント')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insta.post')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insta.chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
