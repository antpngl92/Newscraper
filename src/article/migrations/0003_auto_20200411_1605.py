# Generated by Django 3.0.3 on 2020-04-11 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20200411_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.CharField(max_length=200),
        ),
    ]
