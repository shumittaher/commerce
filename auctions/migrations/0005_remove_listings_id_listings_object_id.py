# Generated by Django 5.0.4 on 2024-04-23 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_object_piccture_listings_object_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='id',
        ),
        migrations.AddField(
            model_name='listings',
            name='object_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]