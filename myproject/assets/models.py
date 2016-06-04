# -*- coding: utf-8 -*-

import os
from time import strftime
from django.db import models
from django.contrib.auth.models import User

from binascii import hexlify

def upload_to(instance, filename):
    return  'documents/%s/%s/%s' % (instance.user.username, strftime('%Y/%m/%d'), filename)

def _createId():
    return hexlify(os.urandom(16))

class Document(models.Model):
    title = models.CharField(max_length=50)
    docfile = models.FileField(upload_to=upload_to)

    doc_id = models.CharField(max_length=32, primary_key=True, default=_createId)
    user = models.ForeignKey(User, editable=False)
    converted = models.BooleanField(default=False)

    txtfile = models.CharField(max_length=1024, null=True)
    format_type = models.CharField(max_length=50, null=True)
    language = models.CharField(max_length=50, null=True)
    size = models.IntegerField(null=True)

    def __unicode__(self):
        return self.title
