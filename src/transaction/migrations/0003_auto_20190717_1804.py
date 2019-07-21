# Generated by Django 2.2.1 on 2019-07-17 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20190628_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='mission',
            field=models.CharField(choices=[('supplement', 'supplement'), ('conclusion', 'conclusion'), ('delegation', 'delegation'), ('delegate_change', 'delegate change'), ('delegate_remove', 'delegate remove'), ('payment', 'payment'), ('approved_payment', 'approved payment')], db_index=True, max_length=20, verbose_name='mission'),
        ),
    ]