# Generated by Django 2.1 on 2019-06-18 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20190618_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fieldbalance',
            options={'verbose_name': 'Баланс по месторождению', 'verbose_name_plural': 'Баланс по месторождениям'},
        ),
        migrations.AlterModelOptions(
            name='wellmatrix',
            options={'verbose_name': 'Матрица скважины', 'verbose_name_plural': 'Матрица скважин'},
        ),
    ]
