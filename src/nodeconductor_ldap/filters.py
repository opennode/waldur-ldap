from nodeconductor.core import filters as core_filters
from nodeconductor.structure import filters as structure_filters

from . import models


class LDAPServiceProjectLinkFilter(structure_filters.BaseServiceProjectLinkFilter):
    service = core_filters.URLFilter(view_name='ldap-detail', name='service__uuid')

    class Meta(object):
        model = models.LDAPServiceProjectLink
