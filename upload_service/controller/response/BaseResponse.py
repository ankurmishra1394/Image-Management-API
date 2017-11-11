from django.http import JsonResponse

class BaseResponse(object):

	hint = 'success'
	message = 'Response sent successfully'
	response_type = 'success'
	api_code = 'CODE_API_200'
	status_code = 200
	data = 'Response Success'

	def handle(self):
		result = {}
		result['data'] = self.data

		result['notification'] = {}
		result['notification']['apiCode'] = self.api_code
		result['notification']['message'] = self.message
		result['notification']['type'] = self.response_type
		result['notification']['hint'] = self.hint

		return JsonResponse(result, status=self.status_code, content_type='application/json')