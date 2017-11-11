from ApiBaseException import ApiBaseException

class MissingRequiredParameterException(ApiBaseException):
	status_code = 400
	error_code = 'CODE_API_400'
	payload = (['hint','missing parameters'],)

	def __init__(self, params={}, payload=None):
		if payload is not None:
			self.payload = payload
		self.message = "Missing required parameters: %s" % ', '.join(params)