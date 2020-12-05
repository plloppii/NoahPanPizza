# Generated by Django 3.0.2 on 2020-02-06 01:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300)),
                ('date_posted', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('image', models.ImageField(default='', upload_to='profile_pics')),
                ('content', models.TextField()),
            ],
        ),
    ]
