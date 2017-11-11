from django.utils.decorators import classonlymethod

class CustomView(object):

	@classonlymethod
	def as_view(cls, def_name, method=['GET'], **initkwargs):
		def view(request, *args, **kwargs):

			if request.method.upper() not in method:
				from upload_service.middleware.exception.MethodNotAllowedException import MethodNotAllowedException
				raise MethodNotAllowedException(params={request.method.upper()})

			if len(initkwargs):
				self = cls(initkwargs)
			else:
				self = cls()
			self.dispatch(request, *args, **kwargs)
			handler = getattr(self, def_name)
			return handler(request, *args, **kwargs)

		return view