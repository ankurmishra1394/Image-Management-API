from upload_service.middleware.decorators.auth import auth_middleware
from custom_view import CustomView

class ServiceView(CustomView):
	
	def dispatch(self, request, *args, **kwars):
		pass

	def userSignup(self, request):
		from user import user_register
		from upload_service.controller.response.RespondWithSuccess import RespondWithSuccess
		
		result = user_register(request)
		return RespondWithSuccess().transform(message='User Registered Successfully', status_code=201)

	def userSignIn(self, request):
		from user import user_login
		from upload_service.controller.response.RespondWithItem import RespondWithItem
		from transformers import UserTransformer

		result = user_login(request)
		return RespondWithItem().transform(result, UserTransformer, message='Logged in successfully', status_code=200)

	@auth_middleware
	def listUserUploads(self, request):
		from user import get_uploads
		from upload_service.controller.response.RespondWithList import RespondWithList
		from transformers import UploadTransformer

		result = get_uploads(request)
		return RespondWithList().transform(result, UploadTransformer, message='Response sent successfully', status_code=200)

	@auth_middleware
	def uploadImage(self, request):

		from service import LocalUploader
		from upload_service.controller.response.RespondWithList import RespondWithList
		from transformers import UploadTransformer
		
		result = LocalUploader().upload(request)
		return RespondWithList().transform(result, UploadTransformer, message='File Uploaded Successfully', status_code=201)

	# @auth_middleware
	def viewImage(self, request, filename):
		from django.shortcuts import HttpResponse
		from service import LocalUploader
		from transformers import UploadTransformer

		file, mimetype = LocalUploader().accessFile(request, filename)
		response = HttpResponse(file, content_type=mimetype)
		return response

	@auth_middleware
	def updateImage(self, request, upload_id):

		if request.method == 'DELETE':
			return self.deleteImage(request, upload_id)

		from service import LocalUploader
		from transformers import UploadTransformer

		from upload_service.controller.response.RespondWithItem import RespondWithItem

		request.method = 'POST'
		result = LocalUploader().update(request, upload_id)
		if result:
			return RespondWithItem().transform(result, UploadTransformer, message='File Updated Successfully', status_code=200)
		
		from upload_service.middleware.exception.ApiBaseException import ApiBaseException
		raise ApiBaseException(message='Failed to upload. Something Went Wrong')
	
	@auth_middleware
	def deleteImage(self, request, upload_id):
		from upload_service.controller.response.RespondWithSuccess import RespondWithSuccess
		from service import LocalUploader

		result = LocalUploader().delete(request, upload_id)
		if result[0]:
			return RespondWithSuccess().transform(message='File deleted successfully', status_code=200)
		
		from upload_service.middleware.exception.InvalidRequestException import InvalidRequestException
		raise InvalidRequestException(params={'upload-id'}, payload=(['hint','Failed to delete file.'],))
