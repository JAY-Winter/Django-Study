# Generated by Django 4.2.1 on 2023-05-29 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0009_alter_diagnosis_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]