# Generated by Django 3.0.2 on 2020-11-14 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20201028_0155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=50)),
                ('expiration_date', models.DateTimeField()),
                ('discount', models.IntegerField(default=1)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, default='store/thumbnails/default.jpg', upload_to='store/thumbnails'),
        ),
    ]
