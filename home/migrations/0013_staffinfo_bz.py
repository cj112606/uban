# Generated by Django 2.1.3 on 2018-11-29 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_sportlist_sportauthor'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffinfo',
            name='bz',
            field=models.TextField(blank=True, null=True),
        ),
    ]