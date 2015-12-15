from django.apps import AppConfig


class ldapsyncConfig(AppConfig):
    name = 'nodeconductor_ldapsync'
    verbose_name = 'ldapsync'

    def ready(self):
        pass
