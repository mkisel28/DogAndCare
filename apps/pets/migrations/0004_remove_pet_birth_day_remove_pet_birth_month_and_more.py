# Generated by Django 5.1.1 on 2024-09-27 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pets", "0003_rename_gender_pet_sex"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pet",
            name="birth_day",
        ),
        migrations.RemoveField(
            model_name="pet",
            name="birth_month",
        ),
        migrations.RemoveField(
            model_name="pet",
            name="birth_year",
        ),
        migrations.RemoveField(
            model_name="pet",
            name="temperament",
        ),
        migrations.AddField(
            model_name="pet",
            name="birth_date",
            field=models.DateField(
                blank=True, help_text="The birth date of the pet", null=True
            ),
        ),
        migrations.AlterField(
            model_name="pet",
            name="is_neutered",
            field=models.BooleanField(
                blank=True, help_text="Whether the pet is neutered", null=True
            ),
        ),
        migrations.AlterField(
            model_name="pet",
            name="type",
            field=models.CharField(
                choices=[
                    ("Dog", "Dog"),
                    ("Cat", "Cat"),
                    ("Bird", "Bird"),
                    ("Reptile", "Reptile"),
                    ("Other", "Other"),
                ],
                default="Dog",
                help_text="The type of the pet",
                max_length=20,
            ),
        ),
    ]