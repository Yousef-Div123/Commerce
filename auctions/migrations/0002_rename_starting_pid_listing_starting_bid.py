# Generated by Django 4.0 on 2022-01-20 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='starting_pid',
            new_name='starting_bid',
        ),
    ]
