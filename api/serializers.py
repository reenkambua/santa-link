from rest_framework import serializers
from .models import User, Group

class RegisterSerializer(serializers.ModelSerializer):
    class meta:
        model=User
        fields=['id', 'username','email', 'password']
        extra_kwargs={'password':{'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'budget', 'admin']
        read_only_fields = ['admin']