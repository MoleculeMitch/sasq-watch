from django.db import models
from apps.accounts.models import User
from django.db.models.deletion import CASCADE
import hashlib
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
    location = models.TextField(default='')
    observed = models.TextField(default='')
    notes = models.TextField(default='')
    special_number = models.IntegerField(default='')


    ##### speak with headmaster michael about this curious conundrum #####
        # solution would be null = true, default = None
        # or restart data base and clear all migrations and migrate all at once
    def get_gravatar(self):
        # This is the example code found online for Gravatar, which will
        # randomly generate avatars based on email (we'll use user.username in
        # this case).
        email = self.user.username
        encoded = hashlib.md5(email.encode('utf8')).hexdigest()
        gravatar_url = "http://www.gravatar.com/avatar/%s?d=identicon" % encoded
        return gravatar_url