from django.http import JsonResponse

class ExceptionMiddleware(object):

	def __init__(self, get_response=None):
		self.get_response = get_response
		super(ExceptionMiddleware, self).__init__()

	def __call__(self, request):
		return self.get_response(request)

	def process_exception(self, request, exception):
		try:
			exception.payload
		except Exception:
			exception.message = 'Internal Server Error'
			exception.payload = (['hint','Something Went Wrong.'],)
			exception.error_code = 'CODE_API_500'
			exception.status_code = 500
		
		response = {}
		response['data'] = exception.message

		response['notification'] = {}
		response['notification'] = dict(exception.payload or ())
		response['notification']['message'] = 'Failed to respond'
		response['notification']['type'] = 'error'
		response['notification']['errorCode'] = exception.error_code

		return JsonResponse(response, status=exception.status_code)