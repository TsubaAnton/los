# Generated by Django 4.2.4 on 2024-04-07 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('los', '0002_event_attendees'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('img', models.ImageField(null=True, upload_to='articles/')),
            ],
        ),
    ]
