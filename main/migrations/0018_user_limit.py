# Generated by Django 2.1 on 2019-06-29 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20190627_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='limit',
            field=models.IntegerField(db_index=True, default=300, verbose_name='Запрашиваемый лимит'),
        ),
    ]
