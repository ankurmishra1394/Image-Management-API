'''

class-name LocalUploader

LocalUploader class is being used for storing the uploaded files on to the server
This class contains some methods for uploading, viewing, updating and deleting file from/on server.

'''
class LocalUploader(object):
	
	## 
	# To Upload Multiple Files onto the Server
	# @param request object
	# @return list[Uploads-model-object]
	##
	def upload(self, request):
		import os
		from models import Uploads
		from utility import get_file_details, generate_uuid
		from validator import on_upload_request
		from PIL import Image
		
		if not os.path.isdir(os.environ['UPLOAD_FOLDER']):
			os.mkdir(os.environ['UPLOAD_FOLDER'])

		on_upload_request(request)
		files = request.FILES.getlist('files[]')
		upload_response = []
		for file in files:
			file_detail = get_file_details(file, request)
			pil_image = Image.open(file, 'r')
			pil_image.save(os.path.join(os.environ['UPLOAD_FOLDER'], file_detail['local_name']), pil_image.format, quality=70)
			upload = Uploads(**file_detail).save()
			if upload:
				upload_response.append(upload)
		return upload_response

	## 
	# To View a file using the SelfLink, which is provided when user uploads a file
	# @param request object
	# @return file
	##
	def accessFile(self, request):
		import os
		from validator import on_upload_access_request
		from utility import load_file, get_mime_from_path

		if not os.path.isdir(os.environ['UPLOAD_FOLDER']):
			os.mkdir(os.environ['UPLOAD_FOLDER'])

		on_upload_access_request(request)
		filepath = os.path.join(os.environ['UPLOAD_FOLDER'], request.GET['file'])
		return load_file(filepath), get_mime_from_path(filepath)

	## 
	# To update a file with another using upload-id
	# A file can only be updated by the owner of the file.
	# @param request object, upload-id
	# @return Uploads-model-object
	##
	def update(self, request, upload_id):
		from validator import on_upload_update_request
		from models import Uploads
		from utility import get_file_details
		from PIL import Image
		import os

		on_upload_update_request(request, upload_id)
		file = request.FILES['files[]']
		file_detail = get_file_details(file, request, upload_id)
		pil_image = Image.open(file, 'r')
		pil_image.save(os.path.join(os.environ['UPLOAD_FOLDER'], file_detail['local_name']), pil_image.format, quality=70)
		return Uploads.manager.filterUpload({'id':upload_id})[0]

	## 
	# To delete a file with using upload-id
	# A file can only be deleted by the owner of the file.
	# @param request object, upload-id
	# @return bool
	##
	def delete(self, request, upload_id):
		from models import Uploads
		from utility import delete_file, auth

		upload = Uploads.manager.filterUpload({'id':upload_id, 'user_id':auth(request).id})
		if len(upload):
			delete_file(upload[0].path)
			return upload[0].delete()
		else:
			from upload_service.middleware.exception.NotFoundException import NotFoundException
			raise NotFoundException(params={'upload-id'}, payload=(['hint','Please provide a valid upload id'],))
