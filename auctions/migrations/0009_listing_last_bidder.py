# Generated by Django 4.0 on 2022-01-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='last_bidder',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]