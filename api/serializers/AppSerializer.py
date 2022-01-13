from rest_framework import serializers

from ..models.App import Port


class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = ['port', 'appName', 'namespace']


class EnvSerializer(serializers.Serializer):
    key = serializers.CharField(required=False)
    value = serializers.CharField(required=False)


class LogSerializer(serializers.Serializer):
    podname = serializers.CharField(required=False)
    logs = serializers.CharField(required=False)


class UpdateReplica(serializers.Serializer):
    replicas = serializers.IntegerField()


class UpdateLimitAutoscaler(serializers.Serializer):
    max = serializers.IntegerField(required=False)
    min = serializers.IntegerField(required=False)
    cpu = serializers.IntegerField(required=False)
