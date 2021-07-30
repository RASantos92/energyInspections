from django.db import models
import re
import bcrypt

class ClientManager(models.Manager):
	def loginValidator(self, postData):
		loginErrors = {}
		clientsWithEmail = Client.objects.filter(email=postData['email'])
		if len(postData['password']) == 0:
			loginErrors['passwordReq'] = "A password is required to login"
		if len(postData['email']) == 0:
			loginErrors['emailReq'] = "A email is required to login"
		elif len(clientsWithEmail) == 0:
			loginErrors['emailNotFound'] = "Email is not found please register to login"
		else:
			clientToCheck = clientsWithEmail[0]
			if bcrypt.checkpw(postData['password'].encode(), clientsWithEmail[0].password.encode()):
				print("password matches")
			else:
				loginErrors['pwmatch'] = "Password Incorrect"
		return loginErrors
	
	

	def editValidator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['fullName']) < 2:
			errors["fullName"] = "user name should be at least 2 characters"
		if len(postData['zipCode']) < 5:
			errors['zipLen'] = "zipCode needs to be at least 5 numbers"
		if len(postData['state']) != "Texas":
			errors['stateVal'] = "sorry but we dont do buisness outside of Texas"
		if len(postData['email']) == 0:
			errors['emailreq'] = "Email is required"
		elif not EMAIL_REGEX.match(postData['email']):
			errors['invalidEmail'] = "This email is not real"
		else:
			repeatEmail = User.objects.filter(email = postData['email'])
			if len(repeatEmail)> 0 and postData['email'] != postData['userEmail']:
				errors['invalidEmail'] = "This email is already taken"
		if len(postData['password']) < 4:
			errors['passwordReq'] = "password must be at least 4 characters"
		if postData['password'] != postData['cPassword']:
			errors['password'] = ("Passwords do not match")
		return errors

	def clientValidator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['fullName']) < 2:
			errors["fullName"] = "user name should be at least 2 characters"
		if len(postData['zipCode']) < 3:
			errors['zipLen'] = "zipCode needs to be valid"
		if len(postData['email']) == 0:
			errors['emailreq'] = "Email is required"
		elif not EMAIL_REGEX.match(postData['email']):
			errors['invalidEmail'] = "This email is not real"
		else:
			repeatEmail = Client.objects.filter(email = postData['email'])
			if len(repeatEmail)> 0:
				errors['invalidEmail'] = "This email is already taken"
		if len(postData['password']) < 4:
			errors['passwordReq'] = "password must be at least 4 characters"
		if postData['password'] != postData['cPassword']:
			errors['password'] = ("Passwords do not match")
		return errors

class WorkRequestManager(models.Manager):
	def workRequestValidator(self, postData):
		errors = {}
		if len(postData['jobLocation']) <= 0:
			errors["jobLocation"] = "Job location is required"
		if len(postData['phone']) <= 0:
			errors['phone'] = "Please enter a phone number or email to be contacted at"
		return errors

class AdminManager(models.Manager):
	def adminValidator(self, postData):
		loginErrors = {}
		admin = Admin.objects.filter(fullName=postData['fullName'])
		if len(postData['password']) == 0:
			loginErrors['passwordReq'] = "A password is required to login"
		if len(postData['fullName']) == 0:
			loginErrors['nameReq'] = "A email is required to login"
		elif len(admin) == 0:
			loginErrors['adminNotFound'] = "This admin name was not found"
		else:
			clientToCheck = admin[0]
			if bcrypt.checkpw(postData['password'].encode(), admin[0].password.encode()):
				print("password matches")
			else:
				loginErrors['pwmatch'] = "Password Incorrect"
		return loginErrors

class Client(models.Model):
	fullName= models.CharField(max_length=45)
	companyName= models.CharField(max_length=45)
	streetAddress= models.CharField(max_length=120)
	email= models.CharField(max_length=45)
	zipCode= models.CharField(max_length=10)
	city= models.CharField(max_length=20)
	phone= models.CharField(max_length=12)
	password = models.CharField(max_length=45, null=True)
	created_at= models.DateTimeField(auto_now_add=True)
	updated_at= models.DateTimeField(auto_now=True)
	objects= ClientManager()

class WorkRequest(models.Model):
	client = models.ForeignKey(Client, related_name="workRequests", on_delete = models.CASCADE)
	jobLocation = models.CharField(max_length=45)
	phone = models.CharField(max_length = 13,null = True)
	prefferedInspectionDate = models.DateTimeField()
	comment = models.CharField(max_length = 300)
	reviewed = models.BooleanField(default=False)
	created_at= models.DateTimeField(auto_now_add=True)
	updated_at= models.DateTimeField(auto_now=True)
	objects = WorkRequestManager()

class Admin(models.Model):
	fullName= models.CharField(max_length=40,null=True)
	password= models.CharField(max_length=45, null=True)
	missionS= models.CharField(max_length=1000, null=True)
	whyLife = models.CharField(max_length=1000, null=True)
	OurGuarantee = models.CharField(max_length=1000, null=True)
	tailorFit = models.CharField(max_length=1000, null=True)
	objects = AdminManager()

