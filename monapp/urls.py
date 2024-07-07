# app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register_user, name='register_user'),
    path('auth/login/', views.login_user, name='login_user'),
    path('api/users/<str:userId>/', views.get_user_details, name='get_user_details'),
    path('api/organisations/', views.get_organisations, name='get_organisations'),
    path('api/organisations/<str:orgId>/', views.get_organisation_details, name='get_organisation_details'),
    path('api/organisationscreate/', views.create_organisation, name='create_organisation'),
    path('api/organisations/<str:orgId>/users/', views.add_user_to_organisation, name='add_user_to_organisation'),
    # Add more URL patterns as needed
]
