# Generated by Django 3.0.3 on 2020-04-06 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200310_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='source1',
            field=models.BooleanField(default=False),
        ),
    ]
