from __future__ import unicode_literals

from django.db import models

##
# Users Model
# For Storing User's name, hashed-password, access-token and tokers
##
class Users(models.Model):
	import datetime
	from manager.UsersManager import UsersManager
	from django.db import IntegrityError, transaction

	id = models.CharField(primary_key=True, max_length=255)
	email = models.CharField(max_length=255, unique=True)
	password = models.CharField(max_length=200)
	token = models.CharField(max_length=255, unique=True)
	expires_at = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=2))
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	manager = UsersManager()

	class Meta:
		db_table = 'users'
		app_label = 'service'

	def save(self, *args, **kwargs):
		from django.db import IntegrityError, transaction

		try:
			with transaction.atomic():
				new = super(Users, self).save(*args, **kwargs)
				return self
		except IntegrityError as error:
			if 'UNIQUE constraint' in error.message:
				from upload_service.middleware.exception.InvalidRequestException import InvalidRequestException
				raise InvalidRequestException(params={'email'}, payload=(['hint','Email already exists. Please Login.'],))
			from upload_service.middleware.exception.ApiBaseException import ApiBaseException
			raise ApiBaseException(message=str(error.message))

##
# Uploads Model
# For Storing the records of all uploaded files with the actor
##
class Uploads(models.Model):
	from manager.UploadManager import UploadManager

	id = models.CharField(primary_key=True, max_length=255)
	original_name = models.CharField(max_length=255)
	local_name = models.CharField(max_length=255)
	extension = models.CharField(max_length=10)
	title = models.CharField(max_length=255)
	mime = models.CharField(max_length=20)
	path = models.CharField(max_length=255)
	user = models.ForeignKey(
		'Users',
		on_delete=models.CASCADE,
		verbose_name="related to unique user's id"
		)
	self_link = models.URLField(max_length=255, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	manager = UploadManager()

	class Meta:
		db_table = 'uploads'
		app_label = 'service'

	def save(self, *args, **kwargs):
		from django.db import transaction

		try:
			with transaction.atomic():
				new = super(Uploads, self).save(*args, **kwargs)
				return self
		except Exception as error:
			from upload_service.middleware.exception.ApiBaseException import ApiBaseException
			raise ApiBaseException(message=str(error.message))
