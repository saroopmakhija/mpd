from sqlalchemy import Column, String, Boolean, Float, Integer, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import CustomBase

__all__ = ["Restaurant"]


class Restaurant(CustomBase):
    __tablename__ = 'restaurants'

    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(String)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    rating = Column(Float(decimal_return_scale=2), nullable=True)
    reviews_count = Column(Integer, nullable=False, default=0)

    is_active = Column(Boolean, nullable=False, default=True)
    
    # Geolocation fields for Indian market (essential for location-based discovery)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(6), nullable=True)  # Indian PIN codes are 6 digits
    country = Column(String(50), default='India')
    
    # Indian market compliance and legal requirements
    gst_number = Column(String(15), nullable=True)  # GST registration number (15 characters)
    fssai_license = Column(String(14), nullable=True)  # FSSAI food license number (14 digits)
    pan_number = Column(String(10), nullable=True)  # PAN card number for tax compliance
    trade_license_number = Column(String(50), nullable=True)  # Local trade license
    
    # MealPeDeal specific fields for mystery bag operations
    mystery_bag_enabled = Column(Boolean, default=True)  # Restaurant participates in mystery bags
    pickup_counter_info = Column(Text, nullable=True)  # Information about pickup location within restaurant
    pickup_instructions = Column(Text, nullable=True)  # Special instructions for customers
    average_pickup_time = Column(Integer, nullable=True)  # Average pickup time in minutes
    contact_phone = Column(String(15), nullable=True)  # Dedicated contact for pickup coordination
    
    # Operating hours flexibility for Indian market
    pickup_hours_different = Column(Boolean, default=False)  # If pickup hours differ from regular hours
    
    # Food and cuisine information (important for Indian market)
    cuisine_types = Column(JSON, nullable=True)  # List of cuisine types: ["North Indian", "South Indian", "Chinese", etc.]
    serves_vegetarian = Column(Boolean, default=True)  # Very important in Indian market
    serves_non_vegetarian = Column(Boolean, default=True)
    serves_jain = Column(Boolean, default=False)  # Jain dietary requirements
    serves_vegan = Column(Boolean, default=False)  # Growing vegan market in India
    halal_certified = Column(Boolean, default=False)  # Important for Muslim customers
    serves_alcohol = Column(Boolean, default=False)  # Important for compliance in some Indian states
    
    # Operational metrics for MealPeDeal
    total_mystery_bags_sold = Column(Integer, default=0)
    total_food_waste_saved_kg = Column(Float, default=0.0)  # Environmental impact tracking
    average_discount_percentage = Column(Integer, nullable=True)  # Average discount offered
    customer_satisfaction_score = Column(Float, nullable=True)  # Based on pickup experience
    
    # Business verification and trust indicators
    is_verified = Column(Boolean, default=False)  # MealPeDeal verification status
    verification_date = Column(DateTime, nullable=True)
    partnership_start_date = Column(DateTime, default=func.now())
    
    # Notification preferences for restaurant
    whatsapp_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    
    # Peak hours and demand management
    peak_hours = Column(JSON, nullable=True)  # Peak hours configuration for better mystery bag planning
    minimum_preparation_time = Column(Integer, default=15)  # Minimum time needed to prepare mystery bags
    
    # Marketing and promotional fields
    promotional_message = Column(Text, nullable=True)  # Custom message for customers
    featured_until = Column(DateTime, nullable=True)  # Featured restaurant status
    
    # Sustainability credentials (important for environmentally conscious Indian market)
    sustainability_practices = Column(JSON, nullable=True)  # List of green practices
    organic_certified = Column(Boolean, default=False)
    local_sourcing = Column(Boolean, default=False)
    
    working_hours = relationship("WorkingHours", back_populates="restaurant", uselist=True)
    
    @property
    def environmental_impact_summary(self):
        """Calculate environmental impact metrics"""
        return {
            'total_meals_saved': self.total_mystery_bags_sold,
            'food_waste_saved_kg': self.total_food_waste_saved_kg,
            'co2_saved_kg': self.total_food_waste_saved_kg * 3.3,  # Rough estimate: 1kg food waste = 3.3kg CO2
            'equivalent_trees': round((self.total_food_waste_saved_kg * 3.3) / 21.77, 1),  # 1 tree absorbs ~22kg CO2/year
        }
    
    @property
    def dietary_options_summary(self):
        """Summary of dietary options for quick filtering"""
        return {
            'vegetarian': self.serves_vegetarian,
            'non_vegetarian': self.serves_non_vegetarian,
            'jain': self.serves_jain,
            'vegan': self.serves_vegan,
            'halal': self.halal_certified,
            'alcohol': self.serves_alcohol
        }
    
    @property
    def compliance_status(self):
        """Check compliance status for Indian regulations"""
        return {
            'gst_registered': bool(self.gst_number),
            'fssai_licensed': bool(self.fssai_license),
            'trade_licensed': bool(self.trade_license_number),
            'pan_verified': bool(self.pan_number),
            'fully_compliant': all([self.gst_number, self.fssai_license, self.trade_license_number, self.pan_number])
        }
