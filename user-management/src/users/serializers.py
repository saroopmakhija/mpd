from rest_framework import serializers
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User, UserProfile, UserNotificationPreferences
import random
import string


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Enhanced user registration for Indian market"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    phone = PhoneNumberField(write_only=True)
    first_name = serializers.CharField(max_length=254)
    last_name = serializers.CharField(max_length=254)
    
    # Optional Indian market fields
    preferred_language = serializers.ChoiceField(
        choices=[('en', 'English'), ('hi', 'Hindi')], 
        default='en'
    )
    is_vegetarian = serializers.BooleanField(default=False)
    is_jain = serializers.BooleanField(default=False)
    spice_preference = serializers.ChoiceField(
        choices=[('MILD', 'Mild'), ('MEDIUM', 'Medium'), ('SPICY', 'Spicy'), ('ANY', 'Any')],
        default='ANY'
    )
    pincode = serializers.CharField(max_length=6, required=False, allow_blank=True)
    
    # Marketing consent
    accepts_whatsapp_notifications = serializers.BooleanField(default=True)
    accepts_sms_notifications = serializers.BooleanField(default=True)
    accepts_promotional_messages = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'confirm_password', 'phone', 'first_name', 'last_name',
            'preferred_language', 'is_vegetarian', 'is_jain', 'spice_preference', 'pincode',
            'accepts_whatsapp_notifications', 'accepts_sms_notifications', 'accepts_promotional_messages'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def validate_pincode(self, value):
        if value and (not value.isdigit() or len(value) != 6):
            raise serializers.ValidationError("PIN code must be exactly 6 digits.")
        return value

    def create(self, validated_data):
        # Extract profile and phone data
        phone = validated_data.pop('phone')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        is_vegetarian = validated_data.pop('is_vegetarian', False)
        is_jain = validated_data.pop('is_jain', False)
        spice_preference = validated_data.pop('spice_preference', 'ANY')
        pincode = validated_data.pop('pincode', '')
        
        # Remove confirm_password
        validated_data.pop('confirm_password')
        
        # Create user
        user = User.objects.create_user(**validated_data)
        
        # Generate referral code
        referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while UserProfile.objects.filter(referral_code=referral_code).exists():
            referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_vegetarian=is_vegetarian,
            is_jain=is_jain,
            spice_preference=spice_preference,
            pincode=pincode,
            referral_code=referral_code
        )
        
        # Create notification preferences
        UserNotificationPreferences.objects.create(user=user)
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer with Indian market specific fields"""
    
    full_name = serializers.ReadOnlyField()
    environmental_impact_summary = serializers.ReadOnlyField()
    phone = PhoneNumberField()
    
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'full_name', 'image_url', 'phone', 'birth_date',
            'is_vegetarian', 'is_jain', 'is_vegan', 'avoids_alcohol', 'spice_preference',
            'preferred_cuisines', 'default_address', 'pincode', 'environmental_impact_summary',
            'total_meals_saved', 'total_money_saved', 'total_co2_saved', 'referral_code',
            'favorite_restaurants', 'last_order_date'
        ]
        read_only_fields = [
            'total_meals_saved', 'total_money_saved', 'total_co2_saved', 'referral_code',
            'last_order_date'
        ]


class UserSerializer(serializers.ModelSerializer):
    """Complete user serializer including profile data"""
    
    user_profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'role', 'is_active', 'is_email_verified', 'is_phone_verified',
            'preferred_language', 'accepts_whatsapp_notifications', 'accepts_sms_notifications',
            'accepts_promotional_messages', 'last_known_city', 'last_known_state',
            'date_joined', 'last_login', 'user_profile'
        ]
        read_only_fields = ['id', 'date_joined']


class NotificationPreferencesSerializer(serializers.ModelSerializer):
    """Notification preferences serializer for Indian market channels"""
    
    class Meta:
        model = UserNotificationPreferences
        exclude = ['user']


class UserLocationUpdateSerializer(serializers.Serializer):
    """Serializer for updating user location for nearby offers"""
    
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    city = serializers.CharField(max_length=100, required=False)
    state = serializers.CharField(max_length=100, required=False)


class DietaryPreferencesSerializer(serializers.Serializer):
    """Quick update serializer for dietary preferences"""
    
    is_vegetarian = serializers.BooleanField()
    is_jain = serializers.BooleanField()
    is_vegan = serializers.BooleanField()
    avoids_alcohol = serializers.BooleanField()
    spice_preference = serializers.ChoiceField(
        choices=[('MILD', 'Mild'), ('MEDIUM', 'Medium'), ('SPICY', 'Spicy'), ('ANY', 'Any')]
    )


class PhoneVerificationSerializer(serializers.Serializer):
    """Serializer for phone number verification via OTP"""
    
    phone = PhoneNumberField()
    otp = serializers.CharField(max_length=6, min_length=6, required=False)
    
    def validate_otp(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("OTP must contain only digits.")
        return value


class ReferralCodeSerializer(serializers.Serializer):
    """Serializer for applying referral codes"""
    
    referral_code = serializers.CharField(max_length=10)
    
    def validate_referral_code(self, value):
        try:
            UserProfile.objects.get(referral_code=value.upper())
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Invalid referral code.")
        return value.upper()


class LoginSerializer(serializers.Serializer):
    """Enhanced login serializer with Indian market considerations"""
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                               email=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
                
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include "email" and "password".')


class EnvironmentalImpactSerializer(serializers.Serializer):
    """Serializer for displaying environmental impact metrics"""
    
    meals_saved = serializers.IntegerField()
    money_saved = serializers.DecimalField(max_digits=10, decimal_places=2)
    co2_saved_kg = serializers.FloatField()
    equivalent_trees = serializers.FloatField()
    rank_in_city = serializers.IntegerField(required=False)
    total_users_in_city = serializers.IntegerField(required=False)
