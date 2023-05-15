from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.text import slugify 
import random
import string

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


class AccCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(AccCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
# Create your models here.

class AccGame(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    sale = models.DecimalField(max_digits=10, decimal_places=3, default=50.000)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    image1 = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    image2 = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    image3 = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    timeUpload = models.DateTimeField(default=datetime.now, blank=True) 
    product = models.BooleanField(default=True)
    username = models.CharField(max_length=255, default=generate_random_string(10))
    password = models.CharField(max_length=255, default=generate_random_string(8))
    category = models.ForeignKey(AccCategory, on_delete=models.CASCADE, blank=True, null=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(AccGame, self).save(*args, **kwargs)

    def __str__(self):
        return self.name








