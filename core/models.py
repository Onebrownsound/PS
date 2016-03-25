from django.db import models
from django.contrib.auth.models import User

# Create your models here.
FUTURE_ACTIVATION_CHOICES = (
    ('D', 'Death Activation'),
    ('T', 'Time Activation'),

)

FUTURE_DELIVERY_CHOICES = (
    ('SD', 'Specific Date In Future'),
    ('W', 'Wedding'),
    ('CB', 'Child Birth'),

)


class Capsule(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField(max_length=10000, blank=True, default='')
    file = models.FileField(blank=True)
    activation = models.CharField(max_length=10, choices=FUTURE_ACTIVATION_CHOICES, default='D')
    time_activation = models.DateTimeField(blank=True)
    delivery = models.CharField(max_length=10, choices=FUTURE_DELIVERY_CHOICES, default='SD')
    time_delivery = models.DateTimeField(blank=True)
    owner = models.ForeignKey('auth.User', related_name='capsules')

