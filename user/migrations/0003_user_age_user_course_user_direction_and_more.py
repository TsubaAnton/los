# Generated by Django 4.2.4 on 2024-04-07 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_country_user_tg_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='course',
            field=models.CharField(max_length=255, null=True, verbose_name='курс'),
        ),
        migrations.AddField(
            model_name='user',
            name='direction',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255, null=True, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tg_link',
            field=models.CharField(max_length=255, null=True, verbose_name='ник в телеграм'),
        ),
    ]
