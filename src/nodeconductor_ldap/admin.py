from django.contrib import admin

from nodeconductor.structure import admin as structure_admin

from . import models

admin.site.register(models.LDAPService, structure_admin.ServiceAdmin)
admin.site.register(models.LDAPServiceProjectLink, structure_admin.ServiceProjectLinkAdmin)
admin.site.register(models.LDAPUser, structure_admin.ResourceAdmin)
