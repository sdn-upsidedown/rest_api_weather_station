from django.db import models

# Create your models here.

class WeatherData(models.Model):
    humidity = models.PositiveSmallIntegerField(null=True)
    pressure = models.PositiveSmallIntegerField(null=True)
    temperature = models.SmallIntegerField(null=True)
    light = models.PositiveSmallIntegerField(null=True)
    date = models.DateTimeField()

    def __str__(self):
        return "{}".format(self.date)

# class StationController(models.Model):
#     power = models.PositiveSmallIntegerField(null=True)
#     sleep_mode = models.BooleanField(default=True)