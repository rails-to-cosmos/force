from __future__ import unicode_literals

from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=255, unique=True)

    # menu fetching strategy
    mfs = models.CharField(max_length=1024, blank=True)
    wc = models.TextField('w3p config')

    urls = models.TextField('urls')
    emails = models.TextField('emails')
    phones = models.TextField('phone numbers')
    tags = models.TextField('tags')
