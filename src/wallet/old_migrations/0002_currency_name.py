# Generated by Django 2.2.1 on 2019-05-19 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='name',
            field=models.CharField(default='', max_length=30, verbose_name='name'),
            preserve_default=False,
        ),
    ]
