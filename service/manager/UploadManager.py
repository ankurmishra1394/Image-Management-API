from __future__ import unicode_literals

from service.querysets.UploadQuerySet import UploadQuerySet
from django.db import models

class UploadManager(models.Manager):

	def queryset(self):
		return UploadQuerySet(self.model, using=self._db)

	def filterUpload(self, filter_by):
		return self.queryset().filterUpload(filter_by)

	def deleteUpload(self, filter_by):
		return self.queryset().deleteUpload(filter_by)