# Generated by Django 5.1.1 on 2024-10-10 10:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0004_alter_guest_email_alter_guest_phone'),
        ('memories', '0003_alter_memories_guest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memories',
            options={},
        ),
        migrations.AlterField(
            model_name='memories',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guests.guest'),
        ),
        migrations.AlterField(
            model_name='memories',
            name='memory_text',
            field=models.TextField(),
        ),
    ]
