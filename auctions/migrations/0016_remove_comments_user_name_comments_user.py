# Generated by Django 4.0 on 2022-01-22 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_bid_biders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='user_name',
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='auctions.user'),
        ),
    ]