# Generated by Django 3.0.14 on 2022-03-18 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220225_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(choices=[('ikoyi', 'Ikoyi'), ('vi', 'VI'), ('lekki', 'Lekki'), ('surulere', 'Surulere'), ('yaba', 'Yaba')], default='ikoyi', max_length=200),
        ),
    ]