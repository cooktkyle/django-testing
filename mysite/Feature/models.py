# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Feature(models.Model):

    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(unique=True, max_length=100)
    percent = models.IntegerField()
    enabled = models.BooleanField()

    def __str__(self):
        return '[' +self.id +'] ' +self.name