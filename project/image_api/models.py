from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from upload_validator import FileTypeValidator
import random
import string


class Height(models.Model):
    height = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return str(self.height)


class Plan(models.Model):
    name = models.CharField(max_length=100)
    height = models.ManyToManyField(Height)
    original_image = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, blank=True, null=True)


class Image(models.Model):
    image = models.ImageField(blank=False, upload_to='images', validators=[FileTypeValidator(
                              allowed_types=['image/jpeg', 'image/png'])])
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    time = models.IntegerField(default=300, validators=[MinValueValidator(300), MaxValueValidator(30000)])
    created_on = models.DateTimeField(auto_now_add=True)
    expiring_link = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        characters = string.ascii_letters + string.digits
        self.expiring_link = ''.join(random.choice(characters) for i in range(10))
        super().save(*args, **kwargs)
