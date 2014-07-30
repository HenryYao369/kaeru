from django.db import models

VERSIONMAJOR=1
VERSIONMINOR=0
VERSION=('%d.%d' % (VERSIONMAJOR, VERSIONMINOR))

class User(models.Model):
    name           = models.CharField(max_length=80)
    favorite_color = models.CharField(max_length=40)
    email          = models.EmailField()
    create_date    = models.DateTimeField('date created')
    login_date     = models.DateTimeField('date of most recent login')

    def __unicode__(self):
        return self.name
