# app/serializers.py

from rest_framework import serializers
from .models import User, Organisation
import uuid
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True},
            'userId': {'required': False},
        }

    def create(self, validated_data):
        validated_data['userId'] = uuid.uuid4().hex  # Génère une userId unique
        user = User.objects.create_user(**validated_data)
        return user

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description', 'users', 'created_by']
        read_only_fields = ['orgId', 'created_by'] 

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description', 'users', 'created_by']
        read_only_fields = ['orgId', 'created_by']

    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, many=True)
