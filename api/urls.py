from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, GroupListCreateView, JoinGroupView,
    GeneratePairsView, MyPairView,
    WishlistCreateView, WishlistListView,
    GroupMessageListCreateView
)

urlpatterns = [
    
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('groups/', GroupListCreateView.as_view(), name='group_list_create'),
    path('groups/<int:group_id>/join/', JoinGroupView.as_view(), name='join_group'),

    path('groups/<int:group_id>/generate_pairs/', GeneratePairsView.as_view(), name='generate_pairs'),
    path('groups/<int:group_id>/my_pair/', MyPairView.as_view(), name='my_pair'),

    path('groups/<int:group_id>/wishlist/', WishlistListView.as_view(), name='wishlist_list'),
    path('groups/<int:group_id>/wishlist/add/', WishlistCreateView.as_view(), name='wishlist_add'),

    path('groups/<int:group_id>/messages/', GroupMessageListCreateView.as_view(), name='group_messages'),
]
