from django.db import models

class Technology(models.Model)
	name = models.CharField(max_length=100)

class Client(models.Model)
	name = models.CharField(max_length=1000)

class Project(models.Model):
	name =  models.CharField(max_length=100)
	client = models.ManyToManyField(Client)
	slug = models.SlugField()
	notes = models.TextField()
	technologies = models.ManyToManyField(Technology)	
	team_members = models.ManyToManyField(settings.AUTH_USER_MODEL)
	start_date = models.DateField()
	end_date = models.DateField()
	project_lead = models.ManyToManyField(settings.AUTH_USER_MODEL)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL)





	

