# Generated by Django 2.1.7 on 2020-02-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categeory', models.CharField(max_length=250)),
                ('fee', models.DecimalField(decimal_places=2, max_digits=5)),
                ('categeory_pic', models.CharField(max_length=1000)),
            ],
        ),
    ]
