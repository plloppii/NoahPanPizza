# Generated by Django 3.0.2 on 2020-09-10 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20200910_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(
                blank=True,
                default='',
                upload_to='product_thumbnails'),
        ),
    ]
