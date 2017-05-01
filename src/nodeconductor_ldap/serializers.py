from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework import serializers

from nodeconductor.core import serializers as core_serializers, validators as core_validators
from nodeconductor.structure import serializers as structure_serializers

from . import models


class ServiceSerializer(core_serializers.ExtraFieldOptionsMixin,
                        core_serializers.RequiredFieldsMixin,
                        structure_serializers.BaseServiceSerializer):

    backend_url = serializers.CharField(allow_null=True, write_only=True,
                                        required=False, validators=[core_validators.LDAPURLValidator])

    SERVICE_ACCOUNT_FIELDS = {
        'backend_url': _('LDAP URL (e.g. ldap://ipa.example.com/).'),
        'username': _('Administrative user UID (e.g. admin).'),
        'password': _('Administrative user password.'),
    }
    SERVICE_ACCOUNT_EXTRA_FIELDS = {
        'user_base_dn': _('Forms the DN of users (e.g. cn=users,cn=accounts,dc=example,dc=com).'),
    }

    class Meta(structure_serializers.BaseServiceSerializer.Meta):
        model = models.LDAPService
        required_fields = ('backend_url', 'username', 'password', 'user_base_dn')
        extra_field_options = {
            'backend_url': {
                'label': 'LDAP URL',
                'placeholder': 'ldap://ipa.example.com',
            },
            'username': {
                'label': 'User UID',
                'placeholder': 'admin',
            },
            'user_base_dn': {
                'label': 'LDAP user base DN',
                'placeholder': 'cn=users,cn=accounts,dc=example,dc=com',
            },
        }


class ServiceProjectLinkSerializer(structure_serializers.BaseServiceProjectLinkSerializer):

    class Meta(structure_serializers.BaseServiceProjectLinkSerializer.Meta):
        model = models.LDAPServiceProjectLink
        extra_kwargs = {
            'service': {'lookup_field': 'uuid', 'view_name': 'ldap-detail'},
        }


class LDAPUserSerializer(structure_serializers.BaseResourceSerializer):
    service = serializers.HyperlinkedRelatedField(
        source='service_project_link.service',
        view_name='ldap-detail',
        read_only=True,
        lookup_field='uuid')
    service_project_link = serializers.HyperlinkedRelatedField(
        view_name='ldap-spl-detail',
        queryset=models.LDAPServiceProjectLink.objects.all())
    agree_with_policy = serializers.BooleanField(write_only=True, help_text='User must agree with the policy.')
    attributes = core_serializers.JSONField(default={})

    class Meta(structure_serializers.BaseResourceSerializer.Meta):
        model = models.LDAPUser
        fields = structure_serializers.BaseResourceSerializer.Meta.fields + (
            'user', 'ssh_public_key', 'agree_with_policy', 'attributes',
        )
        protected_fields = structure_serializers.BaseResourceSerializer.Meta.protected_fields + (
            'user', 'ssh_public_key', 'agree_with_policy', 'attributes', 'name',
        )
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'user': {'lookup_field': 'uuid'},
            'ssh_public_key': {'lookup_field': 'uuid'},
        }

    def validate_agree_with_policy(self, value):
        if not value:
            raise serializers.ValidationError(_('User must agree with the policy.'))

        return value

    def validate(self, attrs):
        if self.instance:
            return attrs

        user = attrs['user']
        ssh_key = attrs.get('ssh_public_key')
        if ssh_key is not None and ssh_key.user != user:
            raise serializers.ValidationError(_('SSH key must belong to the same user.'))

        name = attrs['name']
        service_project_link = attrs['service_project_link']
        if models.LDAPUser.objects.filter(
            name=name,
            service_project_link__service__settings=service_project_link.service.settings,
        ).exists():
            raise serializers.ValidationError({'name': _('User with such name already exists.')})

        return attrs

    def create(self, validated_data):
        for object_class in settings.NODECONDUCTOR_LDAP.get('user_object_classes', []):
            if object_class not in validated_data['attributes'].setdefault('objectclass', []):
                validated_data['attributes']['objectclass'].append(object_class)

        if validated_data.get('ssh_public_key') is not None:
            validated_data['attributes']['ipaSshPubKey'] = validated_data['ssh_public_key'].public_key

        return super(LDAPUserSerializer, self).create(validated_data)
