# app/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer
import uuid
from django.shortcuts import get_object_or_404
def generate_unique_user_id():
    return str(uuid.uuid4())


from rest_framework import permissions

class IsAuthenticatedCustom(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data.copy()
    if 'userId' not in data:
        data['userId'] = generate_unique_user_id()

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'success',
            'message': 'Registration successful',
            'data': {
                'accessToken': str(refresh.access_token),
                'user': serializer.data
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'Bad request',
        'message': 'Registration unsuccessful',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'accessToken': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
        }, status=status.HTTP_200_OK)
    return Response({
        'status': 'Bad request',
        'message': 'Authentication failed',
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_details(request, userId):
    try:
        user = User.objects.get(userId=userId)
    except User.DoesNotExist:
        return Response({
            'status': 'Not found',
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'Error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = UserSerializer(user)
    return Response({
        'status': 'success',
        'message': 'User details fetched successfully',
        'data': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_organisations(request):
    user = request.user
    organisations = Organisation.objects.filter(users=user) | Organisation.objects.filter(created_by=user)
    serializer = OrganisationSerializer(organisations, many=True)
    return Response({
        'status': 'success',
        'message': 'Organisations fetched successfully',
        'data': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_organisation_details(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId)
    except Organisation.DoesNotExist:
        return Response({
            'status': 'Not found',
            'message': 'Organisation not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'Error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = OrganisationSerializer(organisation)
    return Response({
        'status': 'success',
        'message': 'Organisation details fetched successfully',
        'data': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])  # À ajuster en fonction de vos besoins d'authentification
def create_organisation(request):
    # Récupérer l'utilisateur actuellement authentifié
    user = request.user  # Assurez-vous que cela récupère correctement l'utilisateur authentifié
    
    # Ajouter l'utilisateur à la requête si nécessaire
    request.data['created_by'] = user.id
    
    serializer = OrganisationSerializer(data=request.data)
    if serializer.is_valid():
        organisation = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_user_to_organisation(request, orgId):
    try:
        organisation = get_object_or_404(Organisation, orgId=orgId)
        userId = request.data.get('userId')
        user = get_object_or_404(User, userId=userId)
        
        organisation.users.add(user)
        
        return Response({
            'status': 'success',
            'message': 'User added to organisation successfully',
        }, status=status.HTTP_200_OK)
    except Organisation.DoesNotExist:
        return Response({
            'status': 'Not found',
            'message': 'Organisation not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({
            'status': 'Not found',
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'Error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_user_ids(request):
    try:
        users = User.objects.all()
        user_ids = [user.userId for user in users]
        return Response({
            'status': 'success',
            'message': 'User IDs fetched successfully',
            'data': user_ids
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'Error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
