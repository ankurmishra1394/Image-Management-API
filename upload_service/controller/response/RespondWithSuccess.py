from BaseResponse import BaseResponse

class RespondWithSuccess(BaseResponse):
	def transform(self, status_code=None, message=None, api_code=None, hint=None):
		BaseResponse.data = 'Success'
		
		if status_code:
			BaseResponse.status_code = status_code

		if hint:
			BaseResponse.hint = hint

		if message:
			BaseResponse.message = message

		if api_code:
			BaseResponse.api_code = api_code

		return self.handle()