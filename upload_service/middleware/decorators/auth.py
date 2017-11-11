from service.models import Users
import datetime

def auth_middleware(function):
	def wrap(cls, request, *args, **kwargs):
		if 'HTTP_ACCESS_TOKEN' in request.META:
			token = Users.manager.validate_token(request.META['HTTP_ACCESS_TOKEN'])
			if len(token):
				return function(cls, request, *args, **kwargs)
		from upload_service.middleware.exception.UnauthorizedException import UnauthorizedException
		raise UnauthorizedException(payload=(['hint',"Invalid Token Provided"],))
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap