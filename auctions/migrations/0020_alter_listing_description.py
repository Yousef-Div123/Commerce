# Generated by Django 4.0 on 2022-01-25 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_comments_listing_alter_comments_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(help_text='Write the your description here'),
        ),
    ]
