# Generated by Django 3.0.2 on 2020-08-29 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20200419_0141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='images',
        ),
        migrations.AddField(
            model_name='project',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='thumbnails',
            field=models.ImageField(
                blank=True, default='', upload_to='project_thumbnails'),
        ),
    ]
