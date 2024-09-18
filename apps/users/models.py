from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from PIL import Image
from django.utils.timezone import now
from django.utils.crypto import get_random_string
import os


def user_avatar_upload_path(instance, filename):
    year = now().strftime("%Y")
    unique_filename = f"{get_random_string(10)}_{filename}"
    return os.path.join(f"avatars/{year}", unique_filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=user_avatar_upload_path, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.username if self.user.username else "UserProfile"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def save(self, *args, **kwargs):
        # Проверяем, изменился ли аватар
        if self.pk:  # если объект уже существует в базе
            previous = UserProfile.objects.get(pk=self.pk)
            if previous.avatar == self.avatar:
                super().save(*args, **kwargs)
                return

        super().save(*args, **kwargs)
        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                max_size = (300, 300)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img.save(self.avatar.path, quality=85, optimize=True)
            except FileNotFoundError:
                self.avatar = None
                self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
