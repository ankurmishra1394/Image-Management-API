from django.core.management import BaseCommand

class Command(BaseCommand):
	
	# Show this when the user types help
	help = "This will help you in generating access-token by after verifying \
			the credentials you entered."

	def handle(self, *args, **options):
		
		user_email = ''
		while len(user_email) < 5:
			user_email = raw_input("Enter your email : ")
		
		user_password = ''
		while len(user_password) < 5:
			user_password = raw_input("Enter your password(minimum of 6) : ")

		user = self.validate_and_respond(user_email, user_password)
		print "\n Your access-token token is : \n"+user.token+"\n"
		print "Please set this access-token in header before sending requests \n"

	def validate_and_respond(self, email, password):
		import sys
		try:
			from django.core.validators import validate_email
			from django.core.exceptions import ValidationError
			validate_email(email)
		except ValidationError:
			print '\n ** Invalid email provided. Please provide a valid email ! ** \n'
			sys.exit()

		from service.models import Users
		user = Users.manager.filter_user({'email' : email})
		if not len(user):
			answer = ""
			while answer not in ["y", "n"]:
				answer = raw_input("You are not registered with us. Do you want us to register you\
					[Y/N]? ").lower()
			if answer == 'y':
				return register_user(email, password)
		from service.utility import validate_password
		if not validate_password(str(password), str(user[0].password)):
			print "\n ** Email and password not matched. Please try again ! ** \n"
			sys.exit()
		return user[0]

	def register_user(email, password):
		from service.models import Users
		from service.utility import generate_uuid, hash
		data = {
			'id' : str(generate_uuid()),
			'email' : email,
			'password' : hash(str(password)),
			'token' : hash(str(generate_uuid()))
		}
		user = Users(**data).save()
		return user


