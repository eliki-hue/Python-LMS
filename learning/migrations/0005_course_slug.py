# Generated by Django 5.2.1 on 2025-06-25 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0004_chatlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
