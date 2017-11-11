from service.transformers import UserTransformer

def transform(upload):
	return {
		'id' : upload.id,
		'name' : upload.original_name,
		'title' : upload.title,
		'extension' : upload.extension,
		'mimeType' : upload.mime,
		'actor' : UserTransformer.transform(upload.user, only_meta=True),
		'selfLink' : upload.self_link
	}