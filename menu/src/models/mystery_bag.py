from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from .base import CustomBase


class MysteryBag(CustomBase):
    """
    Mystery Bag model for MealPeDeal - Too Good To Go alternative for Indian market.
    
    This model represents surprise food packages that restaurants offer at discounted prices
    to reduce food waste. Optimized for Indian market preferences and dietary requirements.
    """
    __tablename__ = 'mystery_bags'

    # Basic information
    title = Column(String(200), nullable=False)  # e.g., "South Indian Lunch Mystery Bag"
    description = Column(Text, nullable=True)  # Detailed description of what might be included
    image_url = Column(String(500), nullable=True)  # Image showcasing the mystery bag
    
    # Restaurant relationship
    restaurant_id = Column(Integer, ForeignKey('restaurants.id', name='fk_restaurant_id'), nullable=False)
    
    # Pricing information (in INR paise for precision)
    original_value = Column(Integer, nullable=False)  # Original estimated value in paise
    selling_price = Column(Integer, nullable=False)   # Discounted selling price in paise
    discount_percentage = Column(Integer, nullable=True)  # Calculated discount percentage
    
    # Inventory and availability
    total_quantity = Column(Integer, nullable=False, default=1)
    available_quantity = Column(Integer, nullable=False, default=1)
    
    # Pickup time window
    pickup_start_time = Column(DateTime, nullable=False)  # When pickup becomes available
    pickup_end_time = Column(DateTime, nullable=False)    # When pickup window closes
    
    # Indian market specific dietary information (crucial for Indian customers)
    is_vegetarian = Column(Boolean, nullable=False, default=True)
    is_jain = Column(Boolean, nullable=False, default=False)  # Jain dietary restrictions
    is_vegan = Column(Boolean, nullable=False, default=False)
    contains_dairy = Column(Boolean, nullable=False, default=True)
    contains_nuts = Column(Boolean, nullable=False, default=False)
    contains_gluten = Column(Boolean, nullable=False, default=True)
    is_halal = Column(Boolean, nullable=False, default=False)
    contains_alcohol = Column(Boolean, nullable=False, default=False)
    
    # Spice level (important for Indian cuisine)
    spice_level = Column(String(20), nullable=True)  # MILD, MEDIUM, SPICY, EXTRA_SPICY
    
    # Food category and meal type
    meal_category = Column(String(50), nullable=True)  # BREAKFAST, LUNCH, DINNER, SNACKS, DESSERTS, BEVERAGES
    cuisine_type = Column(String(100), nullable=True)  # North Indian, South Indian, Chinese, etc.
    food_type = Column(String(50), nullable=True)     # MAIN_COURSE, APPETIZER, DESSERT, COMBO
    
    # Additional dietary and allergen information
    allergens = Column(JSON, nullable=True)  # List of allergens: ["nuts", "dairy", "soy", etc.]
    ingredients_excluded = Column(JSON, nullable=True)  # For Jain: ["onion", "garlic", "potato", etc.]
    
    # Preparation and pickup information
    preparation_time_minutes = Column(Integer, nullable=False, default=15)  # Time needed to prepare
    pickup_instructions = Column(Text, nullable=True)  # Special pickup instructions
    estimated_weight_grams = Column(Integer, nullable=True)  # Estimated food weight
    
    # Marketing and appeal
    surprise_factor = Column(String(50), nullable=True)  # HIGH, MEDIUM, LOW - how much variety to expect
    value_proposition = Column(Text, nullable=True)     # Marketing description of value
    
    # Operational status
    is_active = Column(Boolean, nullable=False, default=True)
    is_featured = Column(Boolean, nullable=False, default=False)  # Featured mystery bag
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Environmental impact tracking
    estimated_food_waste_saved_grams = Column(Integer, nullable=True)
    
    # Rating and feedback (calculated from reviews)
    average_rating = Column(Float, nullable=True)
    total_reviews = Column(Integer, default=0)
    
    # Relationships
    restaurant = relationship("Restaurant", uselist=False)
    
    @property
    def original_value_inr(self):
        """Convert original value from paise to INR"""
        return self.original_value / 100
    
    @property
    def selling_price_inr(self):
        """Convert selling price from paise to INR"""
        return self.selling_price / 100
    
    @property
    def savings_inr(self):
        """Calculate savings in INR"""
        return (self.original_value - self.selling_price) / 100
    
    @property
    def calculated_discount_percentage(self):
        """Calculate discount percentage"""
        if self.original_value > 0:
            return int(((self.original_value - self.selling_price) / self.original_value) * 100)
        return 0
    
    @property
    def is_available(self):
        """Check if mystery bag is currently available"""
        now = datetime.utcnow()
        return (
            self.is_active and 
            self.available_quantity > 0 and 
            self.pickup_start_time <= now <= self.pickup_end_time
        )
    
    @property
    def dietary_summary(self):
        """Summary of dietary options for quick filtering"""
        return {
            'vegetarian': self.is_vegetarian,
            'jain': self.is_jain,
            'vegan': self.is_vegan,
            'halal': self.is_halal,
            'contains_dairy': self.contains_dairy,
            'contains_nuts': self.contains_nuts,
            'contains_gluten': self.contains_gluten,
            'contains_alcohol': self.contains_alcohol,
            'spice_level': self.spice_level
        }
    
    @property
    def meal_info(self):
        """Meal information summary"""
        return {
            'category': self.meal_category,
            'cuisine': self.cuisine_type,
            'type': self.food_type,
            'preparation_time': self.preparation_time_minutes
        }
    
    def __str__(self):
        return f"{self.title} - ₹{self.selling_price_inr} (Save ₹{self.savings_inr})"


class MysteryBagReview(CustomBase):
    """
    Reviews and ratings for mystery bags to help customers make informed decisions.
    Important for building trust in the Indian market.
    """
    __tablename__ = 'mystery_bag_reviews'
    
    mystery_bag_id = Column(Integer, ForeignKey('mystery_bags.id', name='fk_mystery_bag_id'), nullable=False)
    customer_id = Column(Integer, nullable=False)  # Reference to customer from user-management service
    
    # Rating and review
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review_text = Column(Text, nullable=True)
    
    # Specific feedback categories (important for mystery bags)
    value_for_money_rating = Column(Integer, nullable=True)  # 1-5 rating for value
    food_quality_rating = Column(Integer, nullable=True)     # 1-5 rating for quality
    quantity_satisfaction_rating = Column(Integer, nullable=True)  # 1-5 rating for quantity
    surprise_satisfaction_rating = Column(Integer, nullable=True)  # 1-5 rating for surprise factor
    
    # Verification
    is_verified_purchase = Column(Boolean, default=True)  # Only customers who bought can review
    
    # Helpful votes from other customers
    helpful_votes = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    mystery_bag = relationship("MysteryBag", uselist=False)
    
    def __str__(self):
        return f"Review for {self.mystery_bag.title} - {self.rating}★"


class MysteryBagTemplate(CustomBase):
    """
    Templates for restaurants to quickly create recurring mystery bags.
    Helps restaurants efficiently manage daily/weekly mystery bag offerings.
    """
    __tablename__ = 'mystery_bag_templates'
    
    restaurant_id = Column(Integer, ForeignKey('restaurants.id', name='fk_restaurant_id'), nullable=False)
    
    # Template information
    template_name = Column(String(200), nullable=False)  # e.g., "Daily Lunch Special"
    description = Column(Text, nullable=True)
    
    # Default pricing
    default_original_value = Column(Integer, nullable=False)
    default_selling_price = Column(Integer, nullable=False)
    
    # Default dietary information
    default_is_vegetarian = Column(Boolean, default=True)
    default_is_jain = Column(Boolean, default=False)
    default_spice_level = Column(String(20), nullable=True)
    default_meal_category = Column(String(50), nullable=True)
    default_cuisine_type = Column(String(100), nullable=True)
    
    # Recurrence settings
    is_recurring = Column(Boolean, default=False)
    recurring_days = Column(JSON, nullable=True)  # ["monday", "tuesday", etc.]
    default_pickup_duration_hours = Column(Integer, default=2)  # Default pickup window
    
    # Usage tracking
    times_used = Column(Integer, default=0)
    last_used_at = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    restaurant = relationship("Restaurant", uselist=False)
    
    def __str__(self):
        return f"{self.template_name} - ₹{self.default_selling_price/100}"