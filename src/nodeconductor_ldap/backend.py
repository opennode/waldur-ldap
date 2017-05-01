import logging

import collections
import ldap
import six

from django.conf import settings as django_settings
from ldap import modlist

from nodeconductor.structure import ServiceBackend, ServiceBackendError


logger = logging.getLogger(__name__)


class LDAPBackendError(ServiceBackendError):
    pass


class UnauthorizedError(LDAPBackendError):
    pass


class LDAPBackend(ServiceBackend):
    """
    Interface to LDAP API.
    https://www.python-ldap.org/doc/html/
    """

    def __init__(self, settings):
        self.settings = settings
        self.user_base_dn = settings.options.get('user_base_dn', '')
        self.client = self._get_client()

    def _get_client(self):
        username = ','.join(['uid=%s' % self.settings.username, self.user_base_dn])
        try:
            client = ldap.initialize(self.settings.backend_url)
            client.simple_bind_s(username, self.settings.password)
        except ldap.LDAPError as e:
            six.reraise(UnauthorizedError, e)

        return client

    def ping(self, raise_exception=False):
        tries_count = 3
        for _ in range(tries_count):
            try:
                self.client.search_s(self.user_base_dn, ldap.SCOPE_SUBTREE)
            except ldap.LDAPError as e:
                if raise_exception:
                    six.reraise(LDAPBackendError, e)
            else:
                return True
        return False

    def sync(self):
        pass

    def create_ldap_user(self, ldap_user):
        dn = ('uid=%s,' % ldap_user.name) + self.user_base_dn
        data = modlist.addModlist(self._get_backend_user_attributes(ldap_user))

        try:
            self.client.add_s(dn, data)
        except ldap.LDAPError as e:
            six.reraise(LDAPBackendError, e)
        else:
            ldap_user.backend_id = dn
            ldap_user.save(update_fields=['backend_id'])

    def delete_ldap_user(self, ldap_user):
        dn = ldap_user.backend_id
        try:
            self.client.delete_s(dn)
        except ldap.LDAPError as e:
            six.reraise(LDAPBackendError, e)

    def _get_backend_user_attributes(self, ldap_user):
        attrs = ldap_user.attributes

        for object_class in django_settings.NODECONDUCTOR_LDAP.get('user_object_classes', []):
            if object_class not in attrs.setdefault('objectclass', []):
                attrs['objectclass'].append(object_class)

        if ldap_user.ssh_public_key is not None:
            attrs['ipaSshPubKey'] = ldap_user.ssh_public_key.public_key

        # python-ldap rises TypeError if unicode strings are used.
        return self._unicode_to_string(attrs)

    def _unicode_to_string(self, data):
        # http://stackoverflow.com/a/1254499/4591416
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(self._unicode_to_string, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(self._unicode_to_string, data))
        else:
            return data
