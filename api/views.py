from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import random

from .models import User, Group, Pair, WishlistItem, GroupMessage
from .serializers import (
    RegisterSerializer, UserSerializer,
    GroupSerializer, PairSerializer,
    WishlistSerializer, GroupMessageSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.groups.all()

    def perform_create(self, serializer):
        group = serializer.save(admin=self.request.user)
        group.members.add(self.request.user)

class JoinGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        group.members.add(request.user)
        return Response({"detail": f"{request.user.username} joined {group.name}"})

class GeneratePairsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)

        if request.user != group.admin:
            return Response({"detail": "Only admin can generate pairs."}, status=403)

        members = list(group.members.all())
        if len(members) < 2:
            return Response({"detail": "Not enough members."}, status=400)

        group.pairs.all().delete()

        shuffled = members[:]
        random.shuffle(shuffled)

        for i in range(len(shuffled)):
            giver = shuffled[i]
            receiver = shuffled[(i + 1) % len(shuffled)]
            Pair.objects.create(group=group, giver=giver, receiver=receiver)

        return Response({"detail": "Pairs generated and emails sent!"})



class MyPairView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        try:
            pair = Pair.objects.get(group=group, giver=request.user)
            return Response({"your_recipient": pair.receiver.username})
        except Pair.DoesNotExist:
            return Response({"detail": "Pairing not generated yet."}, status=404)


class WishlistCreateView(generics.CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(Group, id=group_id)
        serializer.save(user=self.request.user, group=group)


class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        return WishlistItem.objects.filter(group__id=group_id)



class GroupMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        return GroupMessage.objects.filter(group__id=group_id)

    def perform_create(self, serializer):
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(Group, id=group_id)
        serializer.save(user=self.request.user, group=group)
