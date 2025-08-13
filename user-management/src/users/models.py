from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field import modelfields
from .managers import UserManager
from .roles import UserRole


class User(AbstractBaseUser, PermissionsMixin):
    """User model for authentication without username field"""

    email = models.EmailField(max_length=254, unique=True)

    role = models.CharField(
        max_length=2,
        choices=UserRole.choices
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    
    # Indian market specific fields
    is_phone_verified = models.BooleanField(default=False)  # Phone verification is critical in India
    preferred_language = models.CharField(
        max_length=5, 
        choices=[('en', 'English'), ('hi', 'Hindi')], 
        default='en'
    )
    
    # Marketing preferences for Indian market
    accepts_whatsapp_notifications = models.BooleanField(default=True)
    accepts_sms_notifications = models.BooleanField(default=True)
    accepts_promotional_messages = models.BooleanField(default=True)

    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # Location for nearby offers discovery
    last_known_latitude = models.FloatField(null=True, blank=True)
    last_known_longitude = models.FloatField(null=True, blank=True)
    last_known_city = models.CharField(max_length=100, null=True, blank=True)
    last_known_state = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % self.pk


class UserProfile(models.Model):
    """Model, which contains common user personal data"""

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name='user_profile'
    )

    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    image_url = models.URLField(blank=True, null=True)  # Make optional
    phone = modelfields.PhoneNumberField()
    birth_date = models.DateField(null=True, blank=True)  # Make optional for quick signup
    
    # Indian market specific dietary preferences (very important for food platforms)
    is_vegetarian = models.BooleanField(default=False)
    is_jain = models.BooleanField(default=False)  # Jain dietary restrictions (no root vegetables)
    is_vegan = models.BooleanField(default=False)
    avoids_alcohol = models.BooleanField(default=False)
    
    # Spice preference (important for Indian cuisine)
    spice_preference = models.CharField(
        max_length=10,
        choices=[
            ('MILD', 'Mild'),
            ('MEDIUM', 'Medium'),
            ('SPICY', 'Spicy'),
            ('ANY', 'Any')
        ],
        default='ANY'
    )
    
    # Cuisine preferences for better recommendations
    preferred_cuisines = models.JSONField(default=list, blank=True)  # List of preferred cuisines
    
    # Address for deliveries and pickup preferences
    default_address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)  # Indian PIN codes are 6 digits
    
    # Environmental impact tracking (gamification for Indian market)
    total_meals_saved = models.PositiveIntegerField(default=0)
    total_money_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_co2_saved = models.FloatField(default=0.0)  # in kg CO2 equivalent
    
    # Referral system for Indian market growth
    referral_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='referrals'
    )
    
    # Engagement metrics
    favorite_restaurants = models.JSONField(default=list, blank=True)  # List of restaurant IDs
    last_order_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def environmental_impact_summary(self):
        """Summary of user's environmental impact for gamification"""
        return {
            'meals_saved': self.total_meals_saved,
            'money_saved': float(self.total_money_saved),
            'co2_saved_kg': self.total_co2_saved,
            'equivalent_trees': round(self.total_co2_saved / 21.77, 1),  # 1 tree absorbs ~22kg CO2/year
        }


class UserNotificationPreferences(models.Model):
    """Detailed notification preferences for Indian market channels"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # WhatsApp notifications (very popular in India)
    whatsapp_order_updates = models.BooleanField(default=True)
    whatsapp_pickup_reminders = models.BooleanField(default=True)
    whatsapp_daily_deals = models.BooleanField(default=True)
    whatsapp_environmental_updates = models.BooleanField(default=False)
    
    # SMS notifications (backup for WhatsApp)
    sms_order_updates = models.BooleanField(default=True)
    sms_pickup_reminders = models.BooleanField(default=True)
    sms_emergency_notifications = models.BooleanField(default=True)
    
    # Email notifications
    email_weekly_summary = models.BooleanField(default=True)
    email_monthly_impact_report = models.BooleanField(default=True)
    email_new_restaurant_alerts = models.BooleanField(default=False)
    
    # Push notifications (for mobile app)
    push_nearby_deals = models.BooleanField(default=True)
    push_favorite_restaurant_offers = models.BooleanField(default=True)
    push_pickup_time_reminders = models.BooleanField(default=True)
    
    # Marketing preferences
    promotional_offers = models.BooleanField(default=True)
    seasonal_campaigns = models.BooleanField(default=False)
    referral_program_updates = models.BooleanField(default=True)
    
    # Timing preferences for notifications
    quiet_hours_start = models.TimeField(default='22:00')  # 10 PM
    quiet_hours_end = models.TimeField(default='08:00')   # 8 AM
    
    def __str__(self):
        return f"Notification preferences for {self.user.email}"
