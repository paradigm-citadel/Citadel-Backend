# Generated by Django 2.2.1 on 2019-05-27 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_auto_20190526_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='transactions_detail',
            field=models.TextField(default='', verbose_name='Transactions update detail'),
        ),
        migrations.AddField(
            model_name='wallet',
            name='transactions_updated',
            field=models.DateTimeField(blank=True, null=True, verbose_name='transactions updated'),
        ),
    ]