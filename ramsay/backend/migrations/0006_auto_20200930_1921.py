# Generated by Django 2.2.16 on 2020-09-30 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d'),
        ),
    ]
