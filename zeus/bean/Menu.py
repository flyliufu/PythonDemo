from django.db import models


class Menu(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=16)
    key = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    media_id = models.CharField(max_length=256)
    appid = models.CharField(max_length=256)
    pagepath = models.CharField(max_length=256)
