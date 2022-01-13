from rest_framework import serializers

from ..models.User import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'namespace', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.namespace = validated_data.get('namespace', instance.namespace)
        instance.role = validated_data.get('role', instance.role)
        password = validated_data.get('password', None)
        if instance.password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class RoleSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role"]

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
