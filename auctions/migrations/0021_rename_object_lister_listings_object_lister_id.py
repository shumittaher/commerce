# Generated by Django 5.0.4 on 2024-05-05 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_rename_object_lister_id_listings_object_lister'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listings',
            old_name='object_lister',
            new_name='object_lister_id',
        ),
    ]
