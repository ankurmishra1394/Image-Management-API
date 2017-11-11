from __future__ import unicode_literals

from service.querysets.UserQuerySet import UserQuerySet
from django.db import models

class UsersManager(models.Manager):

	def queryset(self):
		return UserQuerySet(self.model, using=self._db)

	def filter_user(self, filter_by):
		return self.queryset().filter_user(filter_by)

	def update_user(self, filter_by, update_with):
		return self.queryset().update_user(filter_by, update_with)

	def validate_token(self, token):
		return self.queryset().validate_token(token)