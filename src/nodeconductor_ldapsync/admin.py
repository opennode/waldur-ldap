from __future__ import unicode_literals

from django.contrib import admin

# Plugin admin site registrations should be here!
from nodeconductor_ldapsync import models

admin.site.register(models.LdapToGroup)
