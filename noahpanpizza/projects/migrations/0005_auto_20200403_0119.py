# Generated by Django 3.0.2 on 2020-04-03 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20200402_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='images',
            field=models.ImageField(default='', upload_to='project_pics'),
        ),
    ]