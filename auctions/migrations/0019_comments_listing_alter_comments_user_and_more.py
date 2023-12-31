# Generated by Django 4.0 on 2022-01-22 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_comments_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_listing', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='auctions.user'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='listing_comment', to='auctions.Comments'),
        ),
    ]
