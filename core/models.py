from django.db import models
from django.contrib.auth.models import User

# Create your models here.
FUTURE_ACTIVATION_CHOICES = (
    ('D', 'Death Activation'),

)

FUTURE_DELIVERY_CHOICES = (
    ('SD', 'Specific Date In Future'),
    ('W', 'Wedding'),
    ('CB', 'Child Birth'),
    ('M', 'Marriage')

)

FUTURE_DELIVERY_DICT = {key: value for (key, value) in FUTURE_DELIVERY_CHOICES}


class Capsule(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField(max_length=1000, blank=True, default='')
    file = models.FileField(blank=True)
    activation_type = models.CharField(max_length=10, choices=FUTURE_ACTIVATION_CHOICES, default='D')
    delivery_condition = models.CharField(max_length=10, choices=FUTURE_DELIVERY_CHOICES, default='SD')
    time_delivery = models.DateField(blank=True)
    owner = models.ForeignKey(User)
    is_active = models.BooleanField(default=False)
    is_deliverable = models.BooleanField(default=False)
    author_twitter = models.CharField(max_length=40, default='')
    target_twitter = models.CharField(max_length=40, default='')
