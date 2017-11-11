from BaseResponse import BaseResponse

class RespondWithList(BaseResponse):
	def transform(self, result, transformer, status_code=None, message=None, api_code=None):
		if status_code:
			BaseResponse.status_code = status_code

		if message:
			BaseResponse.message = message

		if api_code:
			BaseResponse.api_code = api_code

		new_result = []
		if len(result):
			for data in result:
				new_result.append(transformer.transform(data))
		BaseResponse.data = new_result
		return self.handle()