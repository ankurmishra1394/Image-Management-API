class ApiBaseException(Exception):

	message = 'we messed up!'
	status_code = 500
	payload = ({'hint','Internal Server Error'},)
	error_code = 'CODE_API_500'

	def __init__(self, message=None, status_code=None, payload=None, error_code=None):
		if message is not None:
			self.message = message
		if status_code is not None:
			self.status_code = status_code
		if payload is not None:
			self.payload = payload
		if error_code is not None:
			self.error_code = error_code