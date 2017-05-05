from nodeconductor.core import executors
from nodeconductor.core import tasks as core_tasks


class LDAPUserCreateExecutor(executors.CreateExecutor):

    @classmethod
    def get_task_signature(cls, ldap_user, serialized_ldap_user, **kwargs):
        return core_tasks.BackendMethodTask().si(
            serialized_ldap_user, 'create_ldap_user', state_transition='begin_creating')


class LDAPUserDeleteExecutor(executors.DeleteExecutor):

    @classmethod
    def get_task_signature(cls, ldap_user, serialized_ldap_user, **kwargs):
        if ldap_user.backend_id:
            return core_tasks.BackendMethodTask().si(
                serialized_ldap_user, 'delete_ldap_user', state_transition='begin_deleting')
        else:
            return core_tasks.StateTransitionTask().si(serialized_ldap_user, state_transition='begin_deleting')
