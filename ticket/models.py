from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    STATUS_CHOICES = (
        ('Upcoming', 'Upcoming'),
        ('Cancelled', 'Cancelled'),
        ('Happening', 'Happening'),
    )
    title = models.CharField(max_length=255)
    descritpion = models.TextField()
    date = models.DateField()
    capacity = models.IntegerField()
    ticket_price = models.FloatField()
    status = models.CharField(max_length=255,choices=STATUS_CHOICES,default="Upcoming")

    def __str__(self):
        return self.title
    
class Ticket(models.Model):
    TICKET_TYPE_CHOICES = (
        ('VIP', 'VIP'),
        ('Regular', 'Regular'),
    )
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=255,choices=TICKET_TYPE_CHOICES)
    price = models.FloatField()

    def __str__(self):
        return self.ticket_type


class Booking(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=255,default='Pending')
    quantity = models.IntegerField(default=0)
    total_price = models.FloatField(default=0)
    # booked_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.user.username} - {self.ticket} x {self.quantity}"