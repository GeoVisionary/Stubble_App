# Generated by Django 5.1.2 on 2024-10-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Point",
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
                ("geolocation", models.CharField(max_length=100)),
                ("date", models.DateField()),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("length", models.FloatField(blank=True, null=True)),
                ("width", models.FloatField(blank=True, null=True)),
                (
                    "fire_status",
                    models.CharField(
                        choices=[
                            ("biomass", "Biomass"),
                            ("active", "Active Burning"),
                            ("burnt", "Already Burnt"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]
