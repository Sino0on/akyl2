from django.contrib.auth.models import AbstractUser
from django.db import models
import json

class Bus(models.Model):
    bus_number = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Bus {self.bus_number}"

class User(AbstractUser):
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)

    def is_driver(self):
        return self.bus is not None

class BusRoute(models.Model):
    bus = models.OneToOneField(Bus, on_delete=models.CASCADE)
    route_json = models.TextField(help_text="JSON with list of coordinates: [[lat, lng], [lat, lng], ...]")
    stops_json = models.TextField(help_text="JSON with list of stops: [{\"name\": \"Stop A\", \"lat\": ..., \"lng\": ...}, ...]")

    def __str__(self):
        return f"Route for Bus {self.bus.bus_number}"

    def get_route(self):
        return json.loads(self.route_json)

    def get_stops(self):
        return json.loads(self.stops_json)


from django.utils import timezone

class BusEntry(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.bus.bus_number} — {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
