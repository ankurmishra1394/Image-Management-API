from ApiBaseException import ApiBaseException

class InvalidRequestException(ApiBaseException):
	status_code = 400
	error_code = 'CODE_API_400'
	payload = (['hint','Request cannot be processed'],)

	def __init__(self, params={}, payload=None, error_code=None):
		if payload is not None:
			self.payload = payload
		if error_code is not None:
			self.error_code = error_code
		self.message = "Invalid request made for: %s" % ', '.join(params)