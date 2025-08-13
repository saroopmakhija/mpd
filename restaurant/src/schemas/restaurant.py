from abc import ABC
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

from .hours import WorkingHoursRetrieveOut

__all__ = [
    "RestaurantBase",
    "RestaurantBaseOut",
    "RestaurantRetrieveOut",
    "RestaurantCreateIn",
    "RestaurantUpdateIn",
    "RestaurantComplianceIn",
    "RestaurantLocationIn", 
    "RestaurantMysteryBagConfigIn",
    "EnvironmentalImpactOut",
    "ComplianceStatusOut",
    "DietaryOptionsOut"
]


# Base

class RestaurantBase(BaseModel, ABC):
    """
    Base schema class for a restaurant.
    """

    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1, max_length=1000)
    address: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=1, max_length=30)
    email: str = Field(min_length=1, max_length=50)


class RestaurantBaseOut(RestaurantBase, ABC):
    """
    Base schema class for output representation of a restaurant.
    """

    id: int = Field(ge=0)
    rating: Optional[float]
    reviews_count: int
    image_url: str = Field(min_length=1, max_length=1000)
    is_active: bool
    
    # Geolocation fields
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: str = "India"
    
    # MealPeDeal specific fields
    mystery_bag_enabled: bool = True
    pickup_counter_info: Optional[str] = None
    pickup_instructions: Optional[str] = None
    average_pickup_time: Optional[int] = None
    contact_phone: Optional[str] = None
    
    # Dietary options
    serves_vegetarian: bool = True
    serves_non_vegetarian: bool = True
    serves_jain: bool = False
    serves_vegan: bool = False
    halal_certified: bool = False
    serves_alcohol: bool = False
    
    # Cuisine information
    cuisine_types: Optional[List[str]] = None
    
    # Operational metrics
    total_mystery_bags_sold: int = 0
    total_food_waste_saved_kg: float = 0.0
    average_discount_percentage: Optional[int] = None
    customer_satisfaction_score: Optional[float] = None
    
    # Verification status
    is_verified: bool = False
    verification_date: Optional[datetime] = None
    partnership_start_date: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# Retrieve

class RestaurantRetrieveOut(RestaurantBaseOut):
    """
    Schema class for output representation of a retrieved restaurant.
    """

    working_hours: List[WorkingHoursRetrieveOut]
    
    # Compliance information (only for restaurant managers/moderators)
    gst_number: Optional[str] = None
    fssai_license: Optional[str] = None
    pan_number: Optional[str] = None
    trade_license_number: Optional[str] = None
    
    # Notification preferences
    whatsapp_notifications: bool = True
    sms_notifications: bool = True
    email_notifications: bool = True
    
    # Additional operational fields
    minimum_preparation_time: int = 15
    promotional_message: Optional[str] = None
    featured_until: Optional[datetime] = None
    
    # Sustainability information
    sustainability_practices: Optional[List[str]] = None
    organic_certified: bool = False
    local_sourcing: bool = False


# Create

class RestaurantCreateIn(RestaurantBase):
    """
    Schema class for input data when creating a restaurant.
    """
    
    # Required location information for Indian market
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100) 
    pincode: Optional[str] = Field(None, regex=r'^\d{6}$')  # Indian PIN code validation
    
    # Compliance information (required for onboarding)
    gst_number: Optional[str] = Field(None, regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')
    fssai_license: Optional[str] = Field(None, regex=r'^\d{14}$')  # 14-digit FSSAI license
    pan_number: Optional[str] = Field(None, regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')  # PAN card format
    trade_license_number: Optional[str] = Field(None, min_length=1, max_length=50)
    
    # MealPeDeal configuration
    mystery_bag_enabled: bool = True
    pickup_counter_info: Optional[str] = Field(None, max_length=500)
    pickup_instructions: Optional[str] = Field(None, max_length=1000)
    contact_phone: Optional[str] = Field(None, regex=r'^\+91[0-9]{10}$')  # Indian phone format
    
    # Dietary options (important for Indian market)
    serves_vegetarian: bool = True
    serves_non_vegetarian: bool = True
    serves_jain: bool = False
    serves_vegan: bool = False
    halal_certified: bool = False
    serves_alcohol: bool = False
    
    # Cuisine types
    cuisine_types: Optional[List[str]] = Field(None, max_items=10)
    
    # Notification preferences
    whatsapp_notifications: bool = True
    sms_notifications: bool = True
    email_notifications: bool = True
    
    # Sustainability practices
    sustainability_practices: Optional[List[str]] = Field(None, max_items=20)
    organic_certified: bool = False
    local_sourcing: bool = False
    
    @validator('cuisine_types')
    def validate_cuisine_types(cls, v):
        if v:
            allowed_cuisines = [
                'North Indian', 'South Indian', 'Punjabi', 'Bengali', 'Gujarati', 'Maharashtrian',
                'Rajasthani', 'Tamil', 'Telugu', 'Kashmiri', 'Chinese', 'Italian', 'Continental',
                'Mexican', 'Thai', 'Japanese', 'Korean', 'Mediterranean', 'Lebanese', 'American',
                'Fast Food', 'Street Food', 'Desserts', 'Beverages', 'Bakery', 'Cafe'
            ]
            for cuisine in v:
                if cuisine not in allowed_cuisines:
                    raise ValueError(f'Invalid cuisine type: {cuisine}')
        return v


# Update
class RestaurantUpdateIn(BaseModel):
    """
    Schema class for input data when updating a restaurant.
    """
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    address: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=1, max_length=30)
    email: Optional[str] = Field(None, min_length=1, max_length=50)
    
    # Location updates
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    pincode: Optional[str] = Field(None, regex=r'^\d{6}$')
    
    # MealPeDeal settings
    mystery_bag_enabled: Optional[bool] = None
    pickup_counter_info: Optional[str] = Field(None, max_length=500)
    pickup_instructions: Optional[str] = Field(None, max_length=1000)
    contact_phone: Optional[str] = Field(None, regex=r'^\+91[0-9]{10}$')
    average_pickup_time: Optional[int] = Field(None, ge=5, le=120)  # 5 to 120 minutes
    
    # Dietary options
    serves_vegetarian: Optional[bool] = None
    serves_non_vegetarian: Optional[bool] = None
    serves_jain: Optional[bool] = None
    serves_vegan: Optional[bool] = None
    halal_certified: Optional[bool] = None
    serves_alcohol: Optional[bool] = None
    
    # Cuisine and operational
    cuisine_types: Optional[List[str]] = Field(None, max_items=10)
    minimum_preparation_time: Optional[int] = Field(None, ge=5, le=60)
    promotional_message: Optional[str] = Field(None, max_length=200)
    
    # Notification preferences
    whatsapp_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    email_notifications: Optional[bool] = None
    
    # Sustainability
    sustainability_practices: Optional[List[str]] = Field(None, max_items=20)
    organic_certified: Optional[bool] = None
    local_sourcing: Optional[bool] = None


# Specialized input schemas for specific operations

class RestaurantComplianceIn(BaseModel):
    """
    Schema for updating restaurant compliance information.
    """
    
    gst_number: Optional[str] = Field(None, regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')
    fssai_license: Optional[str] = Field(None, regex=r'^\d{14}$')
    pan_number: Optional[str] = Field(None, regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
    trade_license_number: Optional[str] = Field(None, min_length=1, max_length=50)


class RestaurantLocationIn(BaseModel):
    """
    Schema for updating restaurant location information.
    """
    
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    address: str = Field(min_length=1, max_length=200)
    city: str = Field(min_length=1, max_length=100)
    state: str = Field(min_length=1, max_length=100)
    pincode: str = Field(regex=r'^\d{6}$')


class RestaurantMysteryBagConfigIn(BaseModel):
    """
    Schema for configuring mystery bag settings.
    """
    
    mystery_bag_enabled: bool
    pickup_counter_info: Optional[str] = Field(None, max_length=500)
    pickup_instructions: Optional[str] = Field(None, max_length=1000)
    average_pickup_time: Optional[int] = Field(None, ge=5, le=120)
    minimum_preparation_time: Optional[int] = Field(None, ge=5, le=60)


# Output schemas for specific data

class EnvironmentalImpactOut(BaseModel):
    """
    Schema for environmental impact metrics.
    """
    
    total_meals_saved: int
    food_waste_saved_kg: float
    co2_saved_kg: float
    equivalent_trees: float


class ComplianceStatusOut(BaseModel):
    """
    Schema for compliance status information.
    """
    
    gst_registered: bool
    fssai_licensed: bool
    trade_licensed: bool
    pan_verified: bool
    fully_compliant: bool


class DietaryOptionsOut(BaseModel):
    """
    Schema for dietary options summary.
    """
    
    vegetarian: bool
    non_vegetarian: bool
    jain: bool
    vegan: bool
    halal: bool
    alcohol: bool


class RestaurantUpdateOut(RestaurantBaseOut):
    """
    Schema class for output representation of an updated restaurant.
    """

    pass
