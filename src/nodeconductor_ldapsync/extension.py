from __future__ import unicode_literals

from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
import ldap

from nodeconductor.core import NodeConductorExtension


class LDAPSyncExtension(NodeConductorExtension):

    class Settings(object):
        # LDAP
        # Tested on FreeIPA.
        #See also: https://pythonhosted.org/django-auth-ldap/
        AUTH_LDAP_SERVER_URI = "ldap://ldap.example.com/"
        AUTH_LDAP_BASE = "cn=accounts,dc=example,dc=com"
        AUTH_LDAP_USER_BASE = "cn=users," + AUTH_LDAP_BASE
        AUTH_LDAP_BIND_DN = "uid=BINDUSERNAME," + AUTH_LDAP_USER_BASE
        AUTH_LDAP_BIND_PASSWORD = "BINDPASSWORD"

        # LDAP user settings
        AUTH_LDAP_USER_FILTER = "(uid=%(user)s)"
        AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_USER_BASE,
                    ldap.SCOPE_SUBTREE, AUTH_LDAP_USER_FILTER)

        # Populate the Django user from the LDAP directory
        AUTH_LDAP_USER_ATTR_MAP = {
            "first_name": "givenName",
            "last_name": "sn",
            "email": "mail"
        }

        # LDAP group settings
        #
        AUTH_LDAP_GROUP_BASE = "cn=groups," + AUTH_LDAP_BASE
        AUTH_LDAP_GROUP_FILTER = "(objectClass=groupOfNames)"
        AUTH_LDAP_GROUP_SEARCH = LDAPSearch(AUTH_LDAP_GROUP_BASE,
            ldap.SCOPE_SUBTREE, AUTH_LDAP_GROUP_FILTER
        )
        AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

        # Cache group memberships for an 10 mins to minimize LDAP traffic
        AUTH_LDAP_CACHE_GROUPS = True
        AUTH_LDAP_GROUP_CACHE_TIMEOUT = 600


    @staticmethod
    def django_app():
        return 'nodeconductor_ldapsync'

