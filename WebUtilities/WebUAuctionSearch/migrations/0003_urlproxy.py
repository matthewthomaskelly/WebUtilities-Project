# Generated by Django 2.0.1 on 2018-02-28 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebUAuctionSearch', '0002_auto_20180118_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlProxy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urlName', models.CharField(max_length=30)),
                ('httpProxy', models.GenericIPAddressField()),
                ('httpsProxy', models.GenericIPAddressField()),
            ],
        ),
    ]