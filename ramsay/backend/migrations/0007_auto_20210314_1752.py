# Generated by Django 2.2.17 on 2021-03-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20210314_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, to='backend.Item'),
        ),
    ]
