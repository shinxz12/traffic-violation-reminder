# Generated by Django 5.0.4 on 2024-04-16 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("CAR", "CAR"),
                            ("MOTO_BIKE", "MOTO_BIKE"),
                            ("ELECTRIC_BIKE", "ELECTRIC_BIKE"),
                        ],
                        max_length=32,
                    ),
                ),
                ("number_plate", models.CharField(max_length=32, unique=True)),
                ("email", models.CharField(max_length=255)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
            ],
        ),
    ]