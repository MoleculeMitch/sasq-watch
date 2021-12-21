from django.db import models
from apps.accounts.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Bookmark (models.Model):

    logged_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=160)
