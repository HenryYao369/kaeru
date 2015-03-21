from django.db import models

VERSIONMAJOR=1
VERSIONMINOR=0
VERSION=('%d.%d' % (VERSIONMAJOR, VERSIONMINOR))

# use django.contrib.auth.models.User

class Project(models.Model):
    # creator = models.ForeignKey(User) # Original creator
    # contributors = models.ManyToManyField(User) # Contributors to the project
	hidden = models.BooleanField() # Public/Private Visibility
	create_date = models.DateTimeField('date created') # Creation date