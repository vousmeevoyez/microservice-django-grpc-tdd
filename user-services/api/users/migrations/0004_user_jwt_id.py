# Generated by Django 3.0.5 on 2020-04-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='jwt_id',
            field=models.UUIDField(null=True),
        ),
    ]