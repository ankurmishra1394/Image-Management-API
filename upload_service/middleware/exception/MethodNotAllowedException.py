from ApiBaseException import ApiBaseException

class MethodNotAllowedException(ApiBaseException):
	status_code = 405
	error_code = 'CODE_API_400'
	payload = (['hint','Method not allowed'],)

	def __init__(self, params={}, payload=None, error_code=None):
		if payload is not None:
			self.payload = payload
		if error_code is not None:
			self.error_code = error_code
		self.message = "Method is not allowed: %s" % ', '.join(params)