# Generated by Django 2.2.1 on 2019-06-20 16:07

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


def create_users(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    OldUser = apps.get_model('auth', 'User')
    User = apps.get_model('account', 'User')

    print(User.objects.values('id'))
    print('pizda vonuchaya')
    users = [
        User(
            id=old_user.id,
            email=old_user.email,
            password=old_user.password
        )
        for old_user in OldUser.objects.all()
    ]
    User.objects.bulk_create(users)


def delete_users(apps, schema_editor):
    User = apps.get_model('account', 'User')
    User.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20190531_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email', unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RunPython(create_users, delete_users),
    ]