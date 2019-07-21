# Generated by Django 2.2.1 on 2019-06-26 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_currencysocial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_usd', models.FloatField(blank=True, null=True, verbose_name='price USD')),
                ('price_btc', models.FloatField(blank=True, null=True, verbose_name='price BTC')),
                ('price_usd_delta_24', models.FloatField(blank=True, null=True, verbose_name='price usd delta 24')),
                ('price_btc_delta_24', models.FloatField(blank=True, null=True, verbose_name='price btc delta 24')),
                ('yielded', models.FloatField(blank=True, null=True, verbose_name='yielded')),
                ('market_cap', models.FloatField(blank=True, null=True, verbose_name='marketCap')),
                ('circulating_supply', models.FloatField(blank=True, null=True, verbose_name='circulating supply')),
                ('staking_rate', models.FloatField(blank=True, null=True, verbose_name='staking rate')),
                ('unbonding_period', models.FloatField(blank=True, null=True, verbose_name='unbonding period')),
                ('second_backend_update_datetime', models.DateTimeField(verbose_name='second backend update datetime')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='update datetime')),
                ('currency', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='wallet.Currency')),
            ],
            options={
                'verbose_name': 'currency statistics',
                'verbose_name_plural': 'currencies statistics',
            },
        ),
    ]