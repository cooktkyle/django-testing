# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Feature(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    percent = models.IntegerField()
    enabled = models.BooleanField()
