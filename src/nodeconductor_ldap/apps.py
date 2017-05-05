from django.apps import AppConfig


class LDAPConfig(AppConfig):
    name = 'nodeconductor_ldap'
    verbose_name = 'LDAP'
    service_name = 'LDAP'

    def ready(self):
        from nodeconductor.structure import SupportedServices

        from .backend import LDAPBackend
        SupportedServices.register_backend(LDAPBackend)
