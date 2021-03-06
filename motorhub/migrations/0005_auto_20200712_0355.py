# Generated by Django 3.0.2 on 2020-07-12 00:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motorhub', '0004_auto_20200712_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='date_due',
            field=models.DateField(default=datetime.datetime(2020, 7, 19, 3, 55, 1, 456007)),
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=250)),
                ('notification', models.CharField(max_length=255)),
                ('read', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motorhub.Customers')),
            ],
        ),
    ]
