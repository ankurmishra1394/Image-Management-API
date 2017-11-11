from ApiBaseException import ApiBaseException

class NotFoundException(ApiBaseException):
	status_code = 404
	error_code = 'CODE_API_404'
	payload = (['hint','Not Found'],)

	def __init__(self, params={}, payload=None, error_code=None):
		if payload is not None:
			self.payload = payload
		if error_code is not None:
			self.error_code = error_code
		self.message = "Not found: %s" % ', '.join(params)