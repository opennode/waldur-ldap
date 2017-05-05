from . import views


def register_in(router):
    router.register(r'ldap', views.LDAPServiceViewSet, base_name='ldap')
    router.register(r'ldap-service-project-link', views.LDAPServiceProjectLinkViewSet, base_name='ldap-spl')
    router.register(r'ldap-users', views.LDAPUserViewSet, base_name='ldap-user')
