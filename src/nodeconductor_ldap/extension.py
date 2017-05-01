from __future__ import unicode_literals

from nodeconductor.core import NodeConductorExtension


class LDAPExtension(NodeConductorExtension):
    class Settings:
        NODECONDUCTOR_LDAP = {
            'user_object_classes': ['top', 'inetuser', 'ipasshuser', 'ipaobject', 'ipaSshGroupOfPubKeys'],
        }

    @staticmethod
    def django_app():
        return 'nodeconductor_ldap'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in
