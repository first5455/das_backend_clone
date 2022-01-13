from django.db import models


class Port(models.Model):
    port = models.IntegerField(unique=True)
    appName = models.CharField(max_length=254)
    namespace = models.CharField(max_length=254)
