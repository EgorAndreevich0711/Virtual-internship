
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    fam = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    otc = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fam} {self.name} {self.otc}"


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    def __str__(self):
        return f"Широта: {self.latitude}, Долгота: {self.longitude}, Высота: {self.height}"


class Level(models.Model):
    LEVEL_CHOICES = [
        ('1A', '1A'),
        ('2A', '2A'),
        ('3A', '3A'),
        ('4A', '4A'),
    ]

    winter = models.CharField(max_length=2, choices=LEVEL_CHOICES, blank=True)
    summer = models.CharField(max_length=2, choices=LEVEL_CHOICES, blank=True)
    autumn = models.CharField(max_length=2, choices=LEVEL_CHOICES, blank=True)
    spring = models.CharField(max_length=2, choices=LEVEL_CHOICES, blank=True)

    def __str__(self):
        return f"Зима: {self.winter}, Лето: {self.summer}, Осень: {self.autumn}, Весна: {self.spring}"


class MountainPass(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('pending', 'В работе'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
    ]

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Image(models.Model):
    mountain_pass = models.ForeignKey(MountainPass, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='mountain_passes/')

    def __str__(self):
        return self.title