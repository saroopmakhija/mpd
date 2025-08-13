import abc
import logging

from django.utils.http import urlsafe_base64_decode
from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.db import transaction
from django.core.cache import cache
from django.utils import timezone
from decimal import Decimal
import random
import string

from tokens.generators import email_verification_token_generator
from tokens.utils import set_jwt_cookies
from .models import User, UserRole, UserProfile, UserNotificationPreferences
from .serializers import (
    UserRegistrationSerializer, UserSerializer, UserProfileSerializer,
    NotificationPreferencesSerializer, UserLocationUpdateSerializer,
    DietaryPreferencesSerializer, PhoneVerificationSerializer,
    ReferralCodeSerializer, LoginSerializer, EnvironmentalImpactSerializer
)
from .permissions import IsModerator, IsEmailVerified
from .services import UserService
from .utils import send_verification_email, send_customer_verification_email, send_courier_verification_email, \
    send_restaurant_manager_verification_email

logger = logging.getLogger(__name__)


# Generic API Views #
class BaseCreateUserView(CreateAPIView, abc.ABC):
    """Base view for registering user's account"""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        expires_session = serializer.validated_data.pop('expires_session')

        user = serializer.save()
        headers = self.get_success_headers(serializer.data)

        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        set_jwt_cookies(response, user, expires_session)

        return response


class CreateCustomerView(BaseCreateUserView):
    """View for registering customer's account (no permissions)"""

    serializer_class = CustomerPostSerializer


class CreateCourierView(BaseCreateUserView):
    """View for registering courier's account (no permissions)"""

    serializer_class = CourierPostSerializer


class CreateRestaurantManagerView(BaseCreateUserView):
    """View for registering restaurant manager's account (no permissions)"""

    serializer_class = RestaurantManagerPostSerializer


class CreateModeratorView(BaseCreateUserView):
    """View for registering moderator's account (IsModerator permission)"""
    permission_classes = [IsModerator]

    serializer_class = ModeratorPostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        headers = self.get_success_headers(serializer.data)

        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return response


class RetrieveUpdateCurrentUserView(RetrieveUpdateAPIView):
    """View for retrieving (IsAuthenticated permission)
    or updating authenticated user account's common information (IsAuthenticated permission)"""

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserOutSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=False)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)


class ListUsersView(ListAPIView):
    """View for getting list of users (IsModerator permission).
    Supports query param 'role' for getting only:
        customers (role=cu)
        couriers (role=co)
        restaurant managers (role=rm)
    """

    serializer_class = UserOutSerializer
    permission_classes = [IsModerator]

    def get_queryset(self):
        role = self.request.query_params.get('role', None)
        queryset = User.objects.exclude(role=UserRole.MODERATOR)

        if role:
            if role == 'cu':
                queryset = queryset.filter(role=UserRole.CUSTOMER)
            elif role == 'co':
                queryset = queryset.filter(role=UserRole.COURIER)
            elif role == 'rm':
                queryset = queryset.filter(role=UserRole.RESTAURANT_MANAGER)

        return queryset.order_by('id')


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    """View for retrieving user (AllowAny permission)
    or updating any user account's information (IsModerator permission)"""

    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsModerator()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateModeratorSerializer
        return UserOutSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=False)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)


class UploadUserImageView(UpdateAPIView):
    permission_classes = [IsModerator]
    serializer_class = UserUploadImageSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=False)


class UploadCurrentUserImageView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUploadImageSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=False)


# API Views #

class SendVerificationEmailView(APIView):
    """View for sending the email for it's verification"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user

        if user.is_email_verified:
            logger.warning(f"Attempted to send verification email for already verified user: {user}")

            return Response({'detail': 'Email has already been verified'}, status=status.HTTP_400_BAD_REQUEST)

        # Send the verification email
        if user.role == UserRole.CUSTOMER:
            send_customer_verification_email(user)
        elif user.role == UserRole.COURIER:
            send_courier_verification_email(user)
        elif user.role == UserRole.RESTAURANT_MANAGER:
            send_restaurant_manager_verification_email(user)

        return Response({'detail': 'Verification email sent successfully'}, status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
    """View for email verification of user's account"""

    def get(self, request, uidb64: str, verification_token: str):

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            logger.warning(f"Invalid uidb64: {uidb64}")
            return Response({'detail': 'Given uidb64 is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.warning(f"User with uidb64 not found: {uidb64}")
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user is not None and email_verification_token_generator.check_token(user, verification_token):
            UserService.verify_email(user=user)
            return Response({'detail': 'Email has been successfully verified'}, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Email verification failed for user: {user}. "
                           f"Invalid or already used token: {verification_token}")
            return Response({'detail': 'Email has already been verified or token is invalid'},
                            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    """Enhanced user management for Indian market"""
    
    queryset = User.objects.select_related('user_profile', 'notification_preferences')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'me':
            return User.objects.filter(id=self.request.user.id)
        return super().get_queryset()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Update user profile information"""
        try:
            profile = request.user.user_profile
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['patch'])
    def update_location(self, request):
        """Update user location for nearby offers discovery"""
        serializer = UserLocationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.last_known_latitude = serializer.validated_data['latitude']
            user.last_known_longitude = serializer.validated_data['longitude']
            user.last_known_city = serializer.validated_data.get('city')
            user.last_known_state = serializer.validated_data.get('state')
            user.save()
            
            return Response({'message': 'Location updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['patch'])
    def update_dietary_preferences(self, request):
        """Update dietary preferences for better recommendations"""
        try:
            profile = request.user.user_profile
            serializer = DietaryPreferencesSerializer(data=request.data)
            if serializer.is_valid():
                for field, value in serializer.validated_data.items():
                    setattr(profile, field, value)
                profile.save()
                return Response({'message': 'Dietary preferences updated successfully'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get', 'patch'])
    def notification_preferences(self, request):
        """Get or update notification preferences"""
        try:
            preferences = request.user.notification_preferences
            
            if request.method == 'GET':
                serializer = NotificationPreferencesSerializer(preferences)
                return Response(serializer.data)
            
            elif request.method == 'PATCH':
                serializer = NotificationPreferencesSerializer(
                    preferences, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except UserNotificationPreferences.DoesNotExist:
            return Response(
                {'error': 'Notification preferences not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def environmental_impact(self, request):
        """Get user's environmental impact metrics for gamification"""
        try:
            profile = request.user.user_profile
            impact_data = profile.environmental_impact_summary
            
            # Add ranking within city (simplified calculation)
            city_users = UserProfile.objects.filter(
                default_address__icontains=profile.user.last_known_city or ''
            ).order_by('-total_meals_saved')
            
            try:
                rank = list(city_users.values_list('user_id', flat=True)).index(request.user.id) + 1
                impact_data['rank_in_city'] = rank
                impact_data['total_users_in_city'] = city_users.count()
            except ValueError:
                impact_data['rank_in_city'] = None
                impact_data['total_users_in_city'] = 0
            
            serializer = EnvironmentalImpactSerializer(impact_data)
            return Response(serializer.data)
            
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def add_favorite_restaurant(self, request):
        """Add restaurant to user's favorites"""
        restaurant_id = request.data.get('restaurant_id')
        if not restaurant_id:
            return Response(
                {'error': 'restaurant_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            profile = request.user.user_profile
            favorites = profile.favorite_restaurants or []
            
            if restaurant_id not in favorites:
                favorites.append(restaurant_id)
                profile.favorite_restaurants = favorites
                profile.save()
                
            return Response({'message': 'Restaurant added to favorites'})
            
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['delete'])
    def remove_favorite_restaurant(self, request):
        """Remove restaurant from user's favorites"""
        restaurant_id = request.data.get('restaurant_id')
        if not restaurant_id:
            return Response(
                {'error': 'restaurant_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            profile = request.user.user_profile
            favorites = profile.favorite_restaurants or []
            
            if restaurant_id in favorites:
                favorites.remove(restaurant_id)
                profile.favorite_restaurants = favorites
                profile.save()
                
            return Response({'message': 'Restaurant removed from favorites'})
            
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Enhanced user registration for Indian market"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({
                'message': 'Registration successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': access_token,
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    """Enhanced login with Indian market considerations"""
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Update last login
        user.last_login = timezone.now()
        user.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'access': access_token,
                'refresh': str(refresh)
            }
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_phone_otp(request):
    """Send OTP for phone verification (Indian market)"""
    serializer = PhoneVerificationSerializer(data=request.data)
    if serializer.is_valid():
        phone = str(serializer.validated_data['phone'])
        
        # Generate 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))
        
        # Store OTP in cache for 5 minutes
        cache_key = f"phone_otp_{phone}"
        cache.set(cache_key, otp, timeout=300)  # 5 minutes
        
        # In production, integrate with SMS provider (MSG91, TextLocal, etc.)
        # For now, return OTP in response (remove in production)
        return Response({
            'message': 'OTP sent successfully',
            'otp': otp  # Remove this in production
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_phone_otp(request):
    """Verify phone OTP and mark phone as verified"""
    serializer = PhoneVerificationSerializer(data=request.data)
    if serializer.is_valid():
        phone = str(serializer.validated_data['phone'])
        otp = serializer.validated_data.get('otp')
        
        if not otp:
            return Response(
                {'error': 'OTP is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check OTP from cache
        cache_key = f"phone_otp_{phone}"
        stored_otp = cache.get(cache_key)
        
        if not stored_otp or stored_otp != otp:
            return Response(
                {'error': 'Invalid or expired OTP'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark phone as verified
        user = request.user
        user.is_phone_verified = True
        user.save()
        
        # Update profile phone if needed
        try:
            profile = user.user_profile
            profile.phone = phone
            profile.save()
        except UserProfile.DoesNotExist:
            pass
        
        # Clear OTP from cache
        cache.delete(cache_key)
        
        return Response({'message': 'Phone verified successfully'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def apply_referral_code(request):
    """Apply referral code for new users"""
    serializer = ReferralCodeSerializer(data=request.data)
    if serializer.is_valid():
        referral_code = serializer.validated_data['referral_code']
        
        try:
            user_profile = request.user.user_profile
            
            # Check if user already has a referrer
            if user_profile.referred_by:
                return Response(
                    {'error': 'Referral code already applied'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Find referrer
            referrer_profile = UserProfile.objects.get(referral_code=referral_code)
            
            # Check user isn't referring themselves
            if referrer_profile.user_id == request.user.id:
                return Response(
                    {'error': 'Cannot use your own referral code'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Apply referral
            user_profile.referred_by = referrer_profile
            user_profile.save()
            
            # Add bonus for both users (simplified - in production, integrate with rewards system)
            bonus_amount = Decimal('50.00')  # ₹50 bonus
            user_profile.total_money_saved += bonus_amount
            referrer_profile.total_money_saved += bonus_amount
            user_profile.save()
            referrer_profile.save()
            
            return Response({
                'message': 'Referral code applied successfully',
                'bonus_amount': float(bonus_amount),
                'referrer_name': referrer_profile.first_name
            })
            
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Invalid referral code'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_referral_stats(request):
    """Get user's referral statistics"""
    try:
        profile = request.user.user_profile
        referrals = UserProfile.objects.filter(referred_by=profile)
        
        return Response({
            'referral_code': profile.referral_code,
            'total_referrals': referrals.count(),
            'referrals': [
                {
                    'name': ref.first_name,
                    'date_joined': ref.user.date_joined,
                    'total_orders': 0  # Can be calculated from order service
                }
                for ref in referrals[:10]  # Limit to recent 10
            ]
        })
        
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'User profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
