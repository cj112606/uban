# Generated by Django 2.1.3 on 2018-11-24 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20181123_2217'),
    ]

    operations = [
        migrations.CreateModel(
            name='deptment_staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deptmentnumber', models.CharField(blank=True, max_length=300, null=True)),
                ('staffnumber', models.CharField(blank=True, max_length=300, null=True)),
                ('staffclass', models.CharField(blank=True, max_length=300, null=True)),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('isfail', models.CharField(blank=True, max_length=2, null=True)),
                ('failtime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestnumber', models.CharField(blank=True, max_length=300, null=True)),
                ('requestname', models.CharField(blank=True, max_length=300, null=True)),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_top', models.TextField(blank=True, null=True)),
                ('toptime', models.DateTimeField(auto_now_add=True, null=True)),
                ('topcycle', models.TextField(blank=True, null=True)),
                ('isfail', models.CharField(blank=True, max_length=2, null=True)),
                ('failtime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='sport_staff_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sportnumber', models.CharField(blank=True, max_length=300, null=True)),
                ('staffnumber', models.CharField(blank=True, max_length=300, null=True)),
                ('requestnumber', models.CharField(blank=True, max_length=300, null=True)),
                ('ssport_staff_request_info', models.CharField(blank=True, max_length=300, null=True)),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('isfail', models.CharField(blank=True, max_length=2, null=True)),
                ('failtime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='sportlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sportnumber', models.CharField(blank=True, max_length=300, null=True)),
                ('sportname', models.TextField(blank=True, null=True)),
                ('sportcontent', models.TextField(blank=True, null=True)),
                ('sportlink', models.TextField(blank=True, null=True)),
                ('is_top', models.TextField(blank=True, null=True)),
                ('toptime', models.DateTimeField(auto_now_add=True, null=True)),
                ('topcycle', models.TextField(blank=True, null=True)),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('isfail', models.CharField(blank=True, max_length=2, null=True)),
                ('failtime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='deptment',
            old_name='deptmentnamePinyin',
            new_name='deptmentname',
        ),
        migrations.RemoveField(
            model_name='deptment',
            name='sdeptmentname',
        ),
        migrations.RemoveField(
            model_name='deptment',
            name='sdeptmentnamePinyinab',
        ),
    ]
