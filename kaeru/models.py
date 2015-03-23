from django.db import models
from django.contrib.auth.models import User

VERSIONMAJOR=1
VERSIONMINOR=0
VERSION=('%d.%d' % (VERSIONMAJOR, VERSIONMINOR))

class Project(models.Model):
	creator = models.ForeignKey(User, default=None, related_name="project_creator") # Original creator
	contributors = models.ManyToManyField(User, related_name="project_contributors") # Contributors to the project
	hidden = models.BooleanField(default=False) # Public/Private Visibility
	create_date = models.DateTimeField('date created') # Creation date
