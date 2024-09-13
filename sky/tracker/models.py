from django.db import models
from django.contrib.auth.models import User

class FavoriteAircraft(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с моделью пользователя
    aircraft_id = models.CharField(max_length=255)  # ID воздушного судна
    country = models.CharField(max_length=255)  # Страна происхождения воздушного судна
    latitude = models.FloatField()  # Широта
    longitude = models.FloatField()  # Долгота

    def __str__(self):
        return f'Aircraft ID: {self.aircraft_id}, Country: {self.country}'


class SavedFilter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, blank=True, null=True)
    min_latitude = models.FloatField(blank=True, null=True)
    max_latitude = models.FloatField(blank=True, null=True)
    min_longitude = models.FloatField(blank=True, null=True)
    max_longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Фильтр для {self.user.username}"