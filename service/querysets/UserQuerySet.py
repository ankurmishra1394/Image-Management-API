from django.db import models

class UserQuerySet(models.QuerySet):
	
	def filter_user(self, filter_by):
		return self.filter(**filter_by)

	def update_user(self, filter_by, update_with):
		return self.filter(**filter_by).update(**update_with)

	def validate_token(self, token):
		import datetime
		return self.filter(token=token, expires_at__gte=datetime.datetime.now())