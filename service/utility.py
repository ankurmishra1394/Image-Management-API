'''

Utilities are basically the helper file containing helper functions.
This file contains all functions which will be used by local_upload package for processing
uploads.

'''

## 
# For Getting File Details
# @param file object
# @response dict
##
def get_file_details(file, request, upload_id=None):
	from werkzeug.utils import secure_filename

	filename = secure_filename(file.name)
	if upload_id:
		unique_id = upload_id
	else:
		unique_id = str(generate_uuid())
	data = {
		'id' : unique_id,
		'local_name' : unique_id+get_extension(filename),
		'original_name' : filename,
		'title' : get_title(filename),
		'extension': get_extension(filename),
		'mime' : get_mime_type(file),
		'user_id' : auth(request).id,
	}
	data['path'] = get_path(data['local_name'])
	data['self_link'] = self_link(data['local_name'])

	return data

def generate_uuid():
	import uuid
	return uuid.uuid4()

def get_title(filename):
	import os
	return os.path.splitext(filename)[0]

def get_extension(filename):
	import os
	return os.path.splitext(filename)[1]

def get_mime_type(file):
	return file.content_type

def get_path(temp_name):
	import os
	return os.environ['UPLOAD_FOLDER']+'/'+temp_name

def hash(password):
	import bcrypt
	return bcrypt.hashpw(password, bcrypt.gensalt())

def validate_password(requested, present):
	import bcrypt
	return bcrypt.checkpw(requested, present)

def format_on_user_registration(request):
	import json
	data = json.loads(request.body)
	
	return {
		'id' : str(generate_uuid()),
		'email' : data['email'],
		'password' : hash(str(data['password'])),
		'token' : hash(str(generate_uuid()))
	}

def auth(request):
	from models import Users
	return Users.manager.validate_token(request.META['HTTP_ACCESS_TOKEN'])[0]

def self_link(temp_name):
	from env import HOST
	if HOST == 'localhost':
		HOST = '127.0.0.1:8000'
	return "http://"+HOST+"/service/image?file="+temp_name

def load_file(file):
	with open(file, 'r') as file:
		return file.read()

def get_mime_from_path(filepath):
	import magic
	
	mime = magic.Magic(mime=True)
	return mime.from_file(filepath)

def format_on_user_login(request):
	import json
	data = json.loads(request.body)
	
	token = {
		'token' : hash(str(generate_uuid()))
	}
	filter_on = {
		'email' : data['email']
	}
	return token, filter_on

def delete_file(filepath):
	import os
	return os.remove(filepath)
