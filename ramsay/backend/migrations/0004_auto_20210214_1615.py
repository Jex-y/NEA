# Generated by Django 2.2.17 on 2021-02-14 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20210214_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='notes',
        ),
        migrations.AddField(
            model_name='itemorder',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='itemorder',
            name='notes',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
