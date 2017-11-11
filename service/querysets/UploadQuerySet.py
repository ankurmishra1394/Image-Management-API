from django.db import models

class UploadQuerySet(models.QuerySet):
	
	def filterUpload(self, filter_by):
		return self.filter(**filter_by)

	def deleteUpload(self, filter_by):
		return self.filter(**filter_by).delete()