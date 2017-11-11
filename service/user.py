'''
user.py file is being used for processing requests related to user.
It contains some methods like user_register, user_login, get_uploads which queries into Users Model 
to complete the request.

'''

## 
# To Register a user
# @param request object
# @return bool
##
def user_register(request):
	from validator import on_user_registration
	from utility import format_on_user_registration
	from models import Users

	on_user_registration(request)
	data = format_on_user_registration(request)
	user = Users(**data).save()
	if user:
		return True
	else:
		from upload_service.middleware.exception.ApiBaseException import ApiBaseException
		raise ApiBaseException(message='Failed To Register User')

## 
# To Login a user with valid credentials
# @param request object
# @return Users-model-object
##
def user_login(request):
	from validator import on_user_login
	from utility import format_on_user_login
	from models import Users

	on_user_login(request)
	data, filter_key = format_on_user_login(request)
	print filter_key, data
	user_update = Users.manager.update_user(filter_key, data)
	print user_update
	if user_update:
		return Users.manager.filter_user(filter_key)[0]

	from upload_service.middleware.exception.ApiBaseException import ApiBaseException
	raise ApiBaseException(message='Failed To Login. Please Try Again')

## 
# To get all uploads by a user
# It gets all uploads by current auth user.
# @param request object
# @return Uploads-model-object
##
def get_uploads(request):
	from models import Uploads
	from utility import auth

	return Uploads.manager.filterUpload({'user_id':auth(request).id})