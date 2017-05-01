from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from nodeconductor.core import models as core_models
from nodeconductor.quotas.fields import CounterQuotaField
from nodeconductor.quotas.models import QuotaModelMixin
from nodeconductor.structure import models as structure_models


class LDAPService(structure_models.Service):
    projects = models.ManyToManyField(
        structure_models.Project, related_name='ldap_service', through='LDAPServiceProjectLink')

    class Meta:
        unique_together = ('customer', 'settings')
        verbose_name = _('LDAP provider')
        verbose_name_plural = _('LDAP providers')

    class Quotas(QuotaModelMixin.Quotas):
        user_count = CounterQuotaField(
            target_models=lambda: [LDAPUser],
            path_to_scope='service_project_link.service'
        )

    @classmethod
    def get_url_name(cls):
        return 'ldap'


class LDAPServiceProjectLink(structure_models.ServiceProjectLink):
    service = models.ForeignKey(LDAPService)

    class Meta(structure_models.ServiceProjectLink.Meta):
        verbose_name = _('LDAP provider project link')
        verbose_name_plural = _('LDAP provider project links')

    @classmethod
    def get_url_name(cls):
        return 'ldap-spl'


class LDAPUser(structure_models.NewResource):
    service_project_link = models.ForeignKey(
        LDAPServiceProjectLink, related_name='users', on_delete=models.PROTECT)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    ssh_public_key = models.ForeignKey(
        core_models.SshPublicKey, blank=True, null=True, help_text=_('SSH public key to propagate to the LDAP User.'))
    attributes = JSONField(default={}, help_text=_('LDAP entry attributes'))

    class Meta:
        unique_together = ('service_project_link', 'user')
        verbose_name = _('LDAP User')
        verbose_name_plural = _('LDAP User')

    @classmethod
    def get_url_name(cls):
        return 'ldap-user'
