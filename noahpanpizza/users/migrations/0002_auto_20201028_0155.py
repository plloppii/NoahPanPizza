# Generated by Django 3.0.2 on 2020-10-28 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='users/default.jpg', upload_to='users'),
        ),
    ]