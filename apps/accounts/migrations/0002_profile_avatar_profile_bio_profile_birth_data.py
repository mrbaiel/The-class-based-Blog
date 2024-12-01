# Generated by Django 5.1.3 on 2024-12-01 13:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="images/avatars/default.jpg",
                upload_to="images/avatars/%Y/%m/%d/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpeg", "png", "jpg"]
                    )
                ],
                verbose_name="Аватарка",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(
                blank=True, max_length=500, verbose_name="Информация о себе"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="birth_data",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Дата рождения"
            ),
        ),
    ]
