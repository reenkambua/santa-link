from rest_framework import serializers
from .models import User, Group, Pair, WishlistItem, GroupMessage
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']



class GroupSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    members = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'admin', 'members', 'created_at']



class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'user', 'group', 'name', 'description']



class GroupMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupMessage
        fields = ['id', 'user', 'group', 'content', 'timestamp']



class PairSerializer(serializers.ModelSerializer):
    giver = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Pair
        fields = ['id', 'group', 'giver', 'receiver']
