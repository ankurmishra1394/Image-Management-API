from ApiBaseException import ApiBaseException

class UnauthorizedException(ApiBaseException):
	status_code = 401
	error_code = 'CODE_API_401'
	payload = (['hint','Unauthorized User'],)

	def __init__(self, params={}, payload=None):
		if payload is not None:
			self.payload = payload
		self.message = "Unauthorized Request"