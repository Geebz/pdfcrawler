# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Document(models.Model):
    name = models.CharField(max_length=32)


class URL(models.Model):
    name = models.CharField(max_length=256)
    document = models.ForeignKey(Document)
