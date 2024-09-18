from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_migrate

GENDERS = [("Male", "Male"), ("Female", "Female")]

TEMPERAMENTS = [
    ("Friendly", "Friendly"),
    ("Playful", "Playful"),
    ("Loyal", "Loyal"),
    ("Protective", "Protective"),
    ("Energetic", "Energetic"),
    ("Calm", "Calm"),
    ("Independent", "Independent"),
    ("Intelligent", "Intelligent"),
    ("Stubborn", "Stubborn"),
    ("Affectionate", "Affectionate"),
    ("Anxious", "Anxious"),
    ("Aggressive", "Aggressive"),
    ("Gentle", "Gentle"),
    ("Adventurous", "Adventurous"),
    ("Shy", "Shy"),
    ("Sociable", "Sociable"),
    ("Well-Balanced", "Well-Balanced"),
]

PET_TYPES = [
    ("Dog", "Dog"),
    ("Cat", "Cat"),
    ("Bird", "Bird"),
    ("Reptile", "Reptile"),
    ("Other", "Other"),
]

PET_SIZES = [
    ("Small", "Small"),
    ("Medium", "Medium"),
    ("Large", "Large"),
]


class Breed(models.Model):
    name = models.CharField(
        max_length=100, unique=True, help_text="The name of the breed"
    )
    size = models.CharField(
        max_length=20, choices=PET_SIZES, help_text="The size of the breed"
    )
    exercise_needs = models.IntegerField(help_text="Exercise needs in minutes per day")
    grooming_requirements = models.IntegerField(help_text="Grooming frequency in days")
    coat_length = models.CharField(max_length=50)
    sheds = models.BooleanField(default=True)
    lifespan = models.IntegerField(help_text="The lifespan of the breed in years")
    min_weight = models.FloatField(help_text="The minimum weight of the breed in Lbs")
    max_weight = models.FloatField(help_text="The maximum weight of the breed in Lbs")
    min_height = models.FloatField(
        help_text="The minimum height of the breed in inches"
    )
    max_height = models.FloatField(
        help_text="The maximum height of the breed in inches"
    )

    def __str__(self):
        return self.name


class Temperament(models.Model):
    name = models.CharField(
        max_length=50, choices=TEMPERAMENTS, help_text="The name of the temperament"
    )

    def __str__(self):
        return self.name


class Pet(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The owner of the pet"
    )
    type = models.CharField(
        max_length=20, choices=PET_TYPES, help_text="The type of the pet"
    )
    avatar = models.ImageField(
        upload_to="pets", null=True, blank=True, help_text="The avatar of the pet"
    )
    name = models.CharField(
        max_length=50, null=True, blank=True, help_text="The name of the pet"
    )
    breed = models.ForeignKey(
        Breed,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The breed of the pet",
    )
    birth_year = models.IntegerField(
        null=True, blank=True, help_text="The birth year of the pet"
    )
    birth_month = models.IntegerField(  # type: ignore
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 13)],  # type: ignore
        help_text="The birth month of the pet",
    )
    birth_day = models.IntegerField(  # type: ignore
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 32)],  # type: ignore
        help_text="The birth day of the pet",
    )
    sex = models.CharField(null=True, blank=True, max_length=6, choices=GENDERS)
    is_neutered = models.BooleanField(
        default=False, help_text="Whether the pet is neutered"
    )
    weight = models.FloatField(null=True, blank=True, help_text="The weight of the pet")
    temperament = models.ManyToManyField(
        "Temperament", blank=True, help_text="The temperament of the pet"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the pet was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The date and time the pet was last updated"
    )

    def get_date_of_birth(self):
        if self.birth_year and self.birth_month and self.birth_day:
            return f"{self.birth_year}-{self.birth_month}-{self.birth_day}"
        elif self.birth_year and self.birth_month:
            return f"{self.birth_year}-{self.birth_month}"
        elif self.birth_year:
            return f"{self.birth_year}"
        else:
            return None

    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = "Pets"

    def __str__(self):
        return self.name if self.name else "Pet"


@receiver(post_migrate)
def create_default_breed(sender, **kwargs):
    """
    Creates default breeds if the Breed table is empty.
    """
    if not Breed.objects.exists():
        breeds = [
            {
                "name": "Labrador Retriever",
                "size": "Large",
                "exercise_needs": 120,  # Более 2 часов
                "grooming_requirements": 7,  # Раз в неделю
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 10,
                "min_weight": 49,
                "max_weight": 77,
                "min_height": 21,
                "max_height": 24,
            },
            {
                "name": "French Bulldog",
                "size": "Small",
                "exercise_needs": 60,  # До 1 часа
                "grooming_requirements": 7,  # Раз в неделю
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 10,
                "min_weight": 19,
                "max_weight": 34,
                "min_height": 12,
                "max_height": 13,
            },
            {
                "name": "German Shepherd",
                "size": "Large",
                "exercise_needs": 120,
                "grooming_requirements": 4,  # Более одного раза в неделю
                "coat_length": "Short & long",
                "sheds": True,
                "lifespan": 10,
                "min_weight": 48,
                "max_weight": 97,
                "min_height": 22,
                "max_height": 26,
            },
            {
                "name": "Golden Retriever",
                "size": "Large",
                "exercise_needs": 120,
                "grooming_requirements": 4,
                "coat_length": "Medium",
                "sheds": True,
                "lifespan": 10,
                "min_weight": 46,
                "max_weight": 80,
                "min_height": 20,
                "max_height": 24,
            },
            {
                "name": "Bulldog",
                "size": "Medium",
                "exercise_needs": 60,
                "grooming_requirements": 7,
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 9,
                "min_weight": 55,
                "max_weight": 99,
                "min_height": 18,
                "max_height": 26,
            },
            {
                "name": "Poodle",
                "size": "Medium",
                "exercise_needs": 60,
                "grooming_requirements": 1,  # Каждый день
                "coat_length": "Medium",
                "sheds": False,
                "lifespan": 12,
                "min_weight": 15,
                "max_weight": 69,
                "min_height": 14,
                "max_height": 24,
            },
            {
                "name": "Poodle Toy",
                "size": "Small",
                "exercise_needs": 60,
                "grooming_requirements": 1,
                "coat_length": "Medium",
                "sheds": False,
                "lifespan": 12,
                "min_weight": 7,
                "max_weight": 28,
                "min_height": 8,
                "max_height": 15,
            },
            {
                "name": "Beagle",
                "size": "Small",
                "exercise_needs": 60,
                "grooming_requirements": 7,
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 12,
                "min_weight": 17,
                "max_weight": 37,
                "min_height": 13,
                "max_height": 16,
            },
            {
                "name": "Rottweiler",
                "size": "Large",
                "exercise_needs": 120,
                "grooming_requirements": 7,
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 9,
                "min_weight": 72,
                "max_weight": 132,
                "min_height": 23,
                "max_height": 27,
            },
            {
                "name": "German Shorthaired Pointer",
                "size": "Medium",
                "exercise_needs": 120,
                "grooming_requirements": 7,
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 10,
                "min_weight": 42,
                "max_weight": 79,
                "min_height": 21,
                "max_height": 25,
            },
            {
                "name": "Dachshund",
                "size": "Small",
                "exercise_needs": 60,
                "grooming_requirements": 7,
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 12,
                "min_weight": 5,
                "max_weight": 32,
                "min_height": 5,
                "max_height": 11,
            },
            {
                "name": "Boxer",
                "size": "Large",
                "exercise_needs": 120,
                "grooming_requirements": 7,
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 10,
                "min_weight": 49,
                "max_weight": 77,
                "min_height": 21,
                "max_height": 25,
            },
            {
                "name": "Siberian Husky",
                "size": "Medium",
                "exercise_needs": 120,
                "grooming_requirements": 4,
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 10,
                "min_weight": 34,
                "max_weight": 67,
                "min_height": 21,
                "max_height": 23,
            },
            {
                "name": "Cavalier King Charles Spaniel",
                "size": "Small",
                "exercise_needs": 60,
                "grooming_requirements": 4,
                "coat_length": "Medium",
                "sheds": True,
                "lifespan": 12,
                "min_weight": 11,
                "max_weight": 23,
                "min_height": 12,
                "max_height": 13,
            },
            {
                "name": "Doberman Pinscher",
                "size": "Medium",
                "exercise_needs": 60,
                "grooming_requirements": 7,
                "coat_length": "Short",
                "sheds": True,
                "lifespan": 10,
                "min_weight": 60,
                "max_weight": 117,
                "min_height": 24,
                "max_height": 28,
            },
        ]
        for breed in breeds:
            Breed.objects.create(**breed)
