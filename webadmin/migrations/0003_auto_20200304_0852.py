# Generated by Django 2.1.8 on 2020-03-04 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webadmin', '0002_checkfile_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitFileBack',
            fields=[
                ('path', models.CharField(max_length=600, primary_key=True, serialize=False, verbose_name='文件路径')),
                ('stat', models.CharField(default='', max_length=200, verbose_name='文件的属性')),
                ('MD5', models.CharField(default='', max_length=32, verbose_name='文件MD5值')),
                ('ruleType', models.CharField(max_length=64, verbose_name='文件所属规则')),
                ('ruleCheck', models.CharField(max_length=20, verbose_name='文件检查项')),
                ('record', models.CharField(max_length=1, verbose_name='文件记录')),
            ],
            options={
                'verbose_name': '文件属性备份表',
            },
        ),
        migrations.AlterModelOptions(
            name='checkfile',
            options={'verbose_name': '文件属性检查表'},
        ),
    ]
