from django.db import models
from apps.accounts.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Bookmark (models.Model):

    logged_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    year = models.CharField(max_length=160, default='')
    season = models.CharField(max_length=160, default='')
    month = models.CharField(max_length=160, default='')
    state = models.CharField(max_length=160, default='')
    county = models.CharField(max_length=160, default='')
    location = models.CharField(max_length=160, default='')
    observed = models.CharField(max_length=160, default='')
