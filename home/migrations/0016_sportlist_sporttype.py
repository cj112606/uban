# Generated by Django 2.1.3 on 2018-11-29 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_sport_staff_request_failreason'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportlist',
            name='sporttype',
            field=models.TextField(blank=True, null=True),
        ),
    ]