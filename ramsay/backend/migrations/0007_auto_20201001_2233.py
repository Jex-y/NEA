# Generated by Django 2.2.16 on 2020-10-01 21:33

import backend.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20200930_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=backend.models.Image.get_upload_name)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Image'),
        ),
        migrations.AlterField(
            model_name='weeklymenu',
            name='end_day',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]),
        ),
        migrations.AlterField(
            model_name='weeklymenu',
            name='start_day',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]),
        ),
    ]
