# Generated by Django 2.1.3 on 2018-11-29 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_staffinfo_bztime'),
    ]

    operations = [
        migrations.AddField(
            model_name='sport_staff_request',
            name='failreason',
            field=models.TextField(blank=True, null=True),
        ),
    ]