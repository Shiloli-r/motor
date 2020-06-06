# Generated by Django 3.0.5 on 2020-05-30 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motorhub', '0002_auto_20200529_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateTimeField()),
                ('read', models.BooleanField(default=False)),
            ],
        ),
    ]
