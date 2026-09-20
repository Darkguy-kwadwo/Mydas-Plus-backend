from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Agent, BlogPost, Property, Testimonial


def user_payload(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email or '',
        'firstName': user.first_name or '',
        'lastName': user.last_name or '',
        'isStaff': user.is_staff,
        'isSuperuser': user.is_superuser,
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = (request.data.get('username') or '').strip()
    password = request.data.get('password') or ''
    if not username or not password:
        return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.is_active:
        return Response({'detail': 'This account is disabled.'}, status=status.HTTP_403_FORBIDDEN)
    if not user.is_staff:
        return Response(
            {'detail': 'Only staff or admin accounts can sign in here.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_payload(user),
        }
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    if not request.user.is_staff:
        return Response({'detail': 'Staff access required.'}, status=status.HTTP_403_FORBIDDEN)
    return Response(user_payload(request.user))


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats_view(request):
    return Response(
        {
            'properties': Property.objects.count(),
            'agents': Agent.objects.count(),
            'blogPosts': BlogPost.objects.count(),
            'testimonials': Testimonial.objects.count(),
            'featured': Property.objects.filter(featured=True).count(),
            'forSale': Property.objects.filter(for_sale=True).count(),
            'forRent': Property.objects.filter(for_rent=True).count(),
        }
    )
