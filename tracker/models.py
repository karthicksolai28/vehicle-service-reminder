from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):
    TYPE_CHOICES = [
        ('Bike', 'Bike'),
        ('Car', 'Car'),
    ]

    SERVICE_GAP_DAYS = 90
    SERVICE_GAP_KM = 3000

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.number})"

    @property
    def last_service(self):
        return self.records.first()

    @property
    def next_due_date(self):
        last = self.last_service
        if last:
            return last.service_date + timedelta(days=self.SERVICE_GAP_DAYS)
        return None

    @property
    def next_due_km(self):
        last = self.last_service
        if last:
            return last.km_reading + self.SERVICE_GAP_KM
        return None

    @property
    def status(self):
        due = self.next_due_date
        if due is None:
            return 'No service yet'
        days_left = (due - date.today()).days
        if days_left < 0:
            return 'Overdue'
        if days_left <= 10:
            return 'Due soon'
        return 'OK'

    @property
    def days_left(self):
        due = self.next_due_date
        if due is None:
            return None
        return (due - date.today()).days


class ServiceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='records')
    service_date = models.DateField()
    km_reading = models.IntegerField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-service_date']

    def __str__(self):
        return f"{self.vehicle.name} - {self.service_date}"