from django.db import models
from django.contrib.auth.models import User
from functools import partial
from django.core.urlresolvers import reverse

# Create your models here.
FUTURE_ACTIVATION_CHOICES = (
    ('D', 'Death Activation'),

)

FUTURE_DELIVERY_CHOICES = (
    ('CB', 'Child Birth'),
    ('M', 'Marriage'),
    ('D', 'Death'),
    ('SD', 'Specific Date In Future'),
)

FUTURE_DELIVERY_DICT = {key: value for (key, value) in FUTURE_DELIVERY_CHOICES}


def make_rng_filename(field_name, instance, filename):  # Thank you StackOverflow, it's a wonderful idea
    '''
        Produces a unique file path for the upload_to of a FileField.

        The produced path is of the form:
        "[model name]/[field name]/[random name].[filename extension]".
    '''
    new_filename = "%s.%s" % (User.objects.make_random_password(10),
                              filename.split('.')[-1])
    return '/'.join([instance.__class__.__name__.lower(),
                     field_name, new_filename])


class Capsule(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField(max_length=1000, blank=True, default='')
    file = models.FileField(blank=True, upload_to=partial(make_rng_filename, 'files'), null=True)
    activation_type = models.CharField(max_length=10, choices=FUTURE_ACTIVATION_CHOICES, default='D')
    delivery_condition = models.CharField(max_length=10, choices=FUTURE_DELIVERY_CHOICES, default='D')
    delivery_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(User)
    is_active = models.BooleanField(default=False)
    is_deliverable = models.BooleanField(default=False)
    author_twitter = models.CharField(max_length=40, default='')
    target_twitter = models.CharField(max_length=40, default='')
    target_email = models.EmailField(blank=False, max_length=45, default='')
    target_firstname = models.CharField(blank=True,default='',max_length=30)
    retired = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " " + self.title + " By: " + self.owner.username

    def get_absolute_url(self):
        return reverse('capsule-detail',kwargs={'pk':self.pk})
