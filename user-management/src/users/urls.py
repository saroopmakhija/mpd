from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # Include router URLs
    path('api/', include(router.urls)),
    
    # Authentication endpoints for Indian market
    path('api/auth/register/', views.register, name='register'),
    path('api/auth/login/', views.login_user, name='login'),
    
    # Phone verification (critical for Indian market)
    path('api/auth/send-otp/', views.send_phone_otp, name='send_phone_otp'),
    path('api/auth/verify-otp/', views.verify_phone_otp, name='verify_phone_otp'),
    
    # Referral system (important for growth in Indian market)
    path('api/referrals/apply/', views.apply_referral_code, name='apply_referral'),
    path('api/referrals/stats/', views.get_referral_stats, name='referral_stats'),
    
    # Legacy authentication endpoints (maintain backward compatibility)
    path('auth/customers/', views.CustomerRegistrationView.as_view(), name='customer-registration'),
    path('auth/couriers/', views.CourierRegistrationView.as_view(), name='courier-registration'),
    path('auth/restaurant-managers/', views.RestaurantManagerRegistrationView.as_view(), name='restaurant-manager-registration'),
    path('auth/moderators/', views.ModeratorRegistrationView.as_view(), name='moderator-registration'),
    path('auth/email-verification/<str:verification_token>/', views.EmailVerificationView.as_view(), name='email-verification'),
    
    # Legacy user management endpoints (maintain backward compatibility)
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerUpdateDeleteView.as_view(), name='customer-update-delete'),
    path('customers/upload-avatar/', views.CustomerUploadAvatarView.as_view(), name='customer-upload-avatar'),
    
    path('couriers/', views.CourierListView.as_view(), name='courier-list'),
    path('couriers/<int:pk>/', views.CourierUpdateDeleteView.as_view(), name='courier-update-delete'),
    path('couriers/upload-avatar/', views.CourierUploadAvatarView.as_view(), name='courier-upload-avatar'),
    
    path('restaurant-managers/', views.RestaurantManagerListView.as_view(), name='restaurant-manager-list'),
    path('restaurant-managers/<int:pk>/', views.RestaurantManagerUpdateDeleteView.as_view(), name='restaurant-manager-update-delete'),
    path('restaurant-managers/upload-avatar/', views.RestaurantManagerUploadAvatarView.as_view(), name='restaurant-manager-upload-avatar'),
    
    path('moderators/', views.ModeratorListView.as_view(), name='moderator-list'),
    path('moderators/<int:pk>/', views.ModeratorUpdateDeleteView.as_view(), name='moderator-update-delete'),
]

# New API endpoints are available at:
# - /api/users/ - User management (CRUD)
# - /api/users/me/ - Current user profile
# - /api/users/update_profile/ - Update profile
# - /api/users/update_location/ - Update location for nearby offers
# - /api/users/update_dietary_preferences/ - Update dietary preferences
# - /api/users/notification_preferences/ - Manage notification settings
# - /api/users/environmental_impact/ - View environmental impact metrics
# - /api/users/add_favorite_restaurant/ - Add favorite restaurant
# - /api/users/remove_favorite_restaurant/ - Remove favorite restaurant
# - /api/auth/register/ - Enhanced registration
# - /api/auth/login/ - Enhanced login
# - /api/auth/send-otp/ - Send phone OTP
# - /api/auth/verify-otp/ - Verify phone OTP
# - /api/referrals/apply/ - Apply referral code
# - /api/referrals/stats/ - Get referral statistics
