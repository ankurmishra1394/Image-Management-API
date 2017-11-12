import json
from upload_service.middleware.exception.MissingRequiredParameter import MissingRequiredParameterException

def on_user_registration(request):

	data = json.loads(request.body)
	if 'email' not in data or('email' in data and data['email'] == ''):
		raise MissingRequiredParameterException(params={'email'}, payload=(['hint','Please provide email'],))
	if 'password' not in data or('password' in data and data['password'] == ''):
		raise MissingRequiredParameterException(params={'password'}, payload=(['hint','Please provide a password.'],))
	try:
		from django.core.validators import validate_email
		from django.core.exceptions import ValidationError
		validate_email(data['email'])
	except ValidationError:
		from upload_service.middleware.exception.InvalidRequestException import InvalidRequestException
		raise InvalidRequestException(params={'email'}, payload=(['hint','Please provide a valid email id'],))
	return True

def on_user_login(request):
	data = json.loads(request.body)
	if 'email' not in data or('email' in data and len(data['email']) < 5):
		raise MissingRequiredParameterException(params={'email'}, payload=(['hint','Please provide email'],))
	if 'password' not in data or('password' in data and len(data['password']) < 5):
		raise MissingRequiredParameterException(params={'password'}, payload=(['hint','Please provide a password.'],))
	
	try:
		from django.core.validators import validate_email
		from django.core.exceptions import ValidationError
		validate_email(data['email'])
	except ValidationError:
		from upload_service.middleware.exception.InvalidRequestException import InvalidRequestException
		raise InvalidRequestException(params={'email'}, payload=(['hint','Please provide a valid email id'],))

	from models import Users
	from upload_service.middleware.exception.UnauthorizedException import UnauthorizedException
	user = Users.manager.filter_user({'email' : data['email']})
	if not len(user):
		raise UnauthorizedException(payload=(['hint','Please register the email first.'],))

	from utility import validate_password
	if not validate_password(str(data['password']), str(user[0].password)):
		raise UnauthorizedException(payload=(['hint','Email and password not matched. Please try login again.'],))

	return True

def on_upload_request(request):
	files = request.FILES.getlist('files[]')
	if not len(files):
		raise MissingRequiredParameterException(params={'files[]'}, payload=(['hint','Please upload some files.'],))
	for file in files:
		if 'image/' not in file.content_type:
			from upload_service.middleware.exception.InvalidRequestException import InvalidRequestException
			raise InvalidRequestException(params={'files[]'}, payload=(['hint','Please upload only images.'],))

def on_upload_update_request(request, upload_id):
	files = request.FILES.getlist('files[]')
	if not len(files):
		raise MissingRequiredParameterException(params={'files[]'}, payload=(['hint','Please upload some files.'],))
	if len(files) > 1:
		from upload_service.middleware.exception.InvalidRequestException import InvalidRequestException
		raise InvalidRequestException(params={'files[]'}, payload=(['hint','Please upload only one file.'],))
	for file in files:
		if 'image/' not in file.content_type:
			from upload_service.middleware.exception.InvalidRequestException import InvalidRequestException
			raise InvalidRequestException(params={'files[]'}, payload=(['hint','Please upload only images.'],))
	from models import Uploads
	from utility import auth, delete_file
	upload = Uploads.manager.filterUpload({'id':upload_id, 'user_id':auth(request).id})
	if not len(upload):
		from upload_service.middleware.exception.UnauthorizedException import UnauthorizedException
		raise UnauthorizedException(payload=(['hint',"You don't have permission to update this file"],))
	else:
		delete_file(upload[0].path)
	return True

def on_upload_access_request(filename):
	import os

	file_exists = os.path.exists(os.environ['UPLOAD_FOLDER']+'/'+filename)
	if not file_exists:
		from upload_service.middleware.exception.InvalidRequestException import InvalidRequestException
		raise InvalidRequestException(params={'file'}, payload=(['hint','Please validate file name first.'],))
	return True
