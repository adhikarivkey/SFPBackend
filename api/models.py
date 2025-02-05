from django.db import models

# Create your models here.


class GasStation(models.Model):
    truckstop_id = models.IntegerField(unique=True)
    rack_id = models.IntegerField()
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    price = models.FloatField()
    map_address = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    comment = models.CharField(max_length=10, default='Not Found')

    def save(self, *args, **kwargs):
        self.state = self.state.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.state} (${self.price})"
