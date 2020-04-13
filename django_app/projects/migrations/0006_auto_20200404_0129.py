# Generated by Django 3.0.2 on 2020-04-04 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20200403_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='images',
            field=models.ImageField(blank=True, default='', upload_to='project_pics'),
        ),
    ]
