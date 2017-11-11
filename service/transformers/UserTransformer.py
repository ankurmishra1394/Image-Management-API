def transform(user, only_meta = False):
	result = {
		'id' : user.id,
		'email' : user.email,
		'accessToken' : user.token,
		'joinedOn' : user.created_at
	}
	if only_meta:
		del result['accessToken']
	
	return result