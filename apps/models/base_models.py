from django.db import models


class Reporter(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

class Reporter2(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name