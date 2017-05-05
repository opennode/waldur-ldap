from nodeconductor.core import executors as core_executors
from nodeconductor.core import validators as core_validators
from nodeconductor.structure import views as structure_views

from . import models, serializers, filters, executors


class LDAPServiceViewSet(structure_views.BaseServiceViewSet):
    queryset = models.LDAPService.objects.all()
    serializer_class = serializers.ServiceSerializer


class LDAPServiceProjectLinkViewSet(structure_views.BaseServiceProjectLinkViewSet):
    queryset = models.LDAPServiceProjectLink.objects.all()
    serializer_class = serializers.ServiceProjectLinkSerializer
    filter_class = filters.LDAPServiceProjectLinkFilter


class LDAPUserViewSet(structure_views.ResourceViewSet):
    queryset = models.LDAPUser.objects.all()
    serializer_class = serializers.LDAPUserSerializer

    create_executor = executors.LDAPUserCreateExecutor
    update_executor = core_executors.EmptyExecutor
    delete_executor = executors.LDAPUserDeleteExecutor
    destroy_validators = [core_validators.StateValidator(models.LDAPUser.States.OK, models.LDAPUser.States.ERRED)]
