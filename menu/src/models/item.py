from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Text, JSON
from sqlalchemy.orm import relationship

from .base import CustomBase


class MenuItem(CustomBase):
    __tablename__ = 'menu_items'

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)  # Changed to Text for longer descriptions
    price = Column(Integer, nullable=False)  # Price in paise (INR subunit) for precision
    image_url = Column(String, nullable=False)

    rating = Column(Float(decimal_return_scale=2), nullable=True)
    reviews_count = Column(Integer, nullable=False, default=0)

    restaurant_id = Column(Integer, ForeignKey('restaurants.id', name='fk_restaurant_id'), nullable=False)
    
    # Indian market specific dietary information (critical for Indian customers)
    is_vegetarian = Column(Boolean, nullable=False, default=True)  # Most important filter in India
    is_jain = Column(Boolean, nullable=False, default=False)  # Jain dietary restrictions (no root vegetables)
    is_vegan = Column(Boolean, nullable=False, default=False)  # Growing vegan community
    contains_dairy = Column(Boolean, nullable=False, default=True)  # Important for lactose intolerant customers
    contains_eggs = Column(Boolean, nullable=False, default=False)  # Many vegetarians avoid eggs in India
    contains_nuts = Column(Boolean, nullable=False, default=False)  # Allergy information
    contains_gluten = Column(Boolean, nullable=False, default=True)  # Gluten-free awareness growing
    is_halal = Column(Boolean, nullable=False, default=False)  # Important for Muslim customers
    contains_alcohol = Column(Boolean, nullable=False, default=False)  # Religious/cultural considerations
    
    # Spice level (very important for Indian cuisine)
    spice_level = Column(String(20), nullable=True)  # MILD, MEDIUM, SPICY, EXTRA_SPICY, NONE
    
    # Cuisine and meal categorization
    cuisine_type = Column(String(100), nullable=True)  # North Indian, South Indian, Chinese, Continental, etc.
    meal_category = Column(String(50), nullable=True)  # BREAKFAST, LUNCH, DINNER, SNACKS, DESSERTS, BEVERAGES
    food_type = Column(String(50), nullable=True)     # MAIN_COURSE, APPETIZER, BREAD, RICE, CURRY, DESSERT, BEVERAGE
    
    # Additional allergen and ingredient information
    allergens = Column(JSON, nullable=True)  # Detailed list: ["peanuts", "tree nuts", "soy", "sesame", etc.]
    ingredients_excluded = Column(JSON, nullable=True)  # For Jain: ["onion", "garlic", "potato", "carrot", etc.]
    main_ingredients = Column(JSON, nullable=True)  # Primary ingredients for transparency
    
    # Preparation and serving information
    preparation_time_minutes = Column(Integer, nullable=True)  # Estimated preparation time
    serving_size = Column(String(50), nullable=True)  # "1 person", "2-3 people", etc.
    calories_per_serving = Column(Integer, nullable=True)  # Health-conscious customers
    
    # Availability and operational
    is_available = Column(Boolean, nullable=False, default=True)
    is_signature_dish = Column(Boolean, nullable=False, default=False)  # Restaurant's specialty
    is_seasonal = Column(Boolean, nullable=False, default=False)  # Seasonal availability
    
    # Pricing and offers
    original_price = Column(Integer, nullable=True)  # For showing discounts
    is_on_offer = Column(Boolean, nullable=False, default=False)
    offer_description = Column(String(200), nullable=True)  # "20% off", "Buy 1 Get 1", etc.
    
    # Nutritional information (growing health awareness in urban India)
    is_healthy_option = Column(Boolean, nullable=False, default=False)
    is_low_calorie = Column(Boolean, nullable=False, default=False)
    is_high_protein = Column(Boolean, nullable=False, default=False)
    is_organic = Column(Boolean, nullable=False, default=False)
    
    # Regional and cultural significance
    region_of_origin = Column(String(100), nullable=True)  # Punjab, Tamil Nadu, Bengal, etc.
    cultural_significance = Column(Text, nullable=True)  # Festival food, traditional recipe, etc.
    
    # Mystery bag eligibility
    can_be_in_mystery_bag = Column(Boolean, nullable=False, default=True)
    mystery_bag_category = Column(String(50), nullable=True)  # MAIN, SIDE, DESSERT, BEVERAGE

    restaurant = relationship("Restaurant", uselist=False)
    
    @property
    def price_inr(self):
        """Convert price from paise to INR"""
        return self.price / 100
    
    @property
    def original_price_inr(self):
        """Convert original price from paise to INR"""
        return self.original_price / 100 if self.original_price else None
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage if on offer"""
        if self.is_on_offer and self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0
    
    @property
    def dietary_summary(self):
        """Summary of dietary options for quick filtering"""
        return {
            'vegetarian': self.is_vegetarian,
            'jain': self.is_jain,
            'vegan': self.is_vegan,
            'halal': self.is_halal,
            'contains_dairy': self.contains_dairy,
            'contains_eggs': self.contains_eggs,
            'contains_nuts': self.contains_nuts,
            'contains_gluten': self.contains_gluten,
            'contains_alcohol': self.contains_alcohol,
            'spice_level': self.spice_level
        }
    
    @property
    def nutritional_highlights(self):
        """Nutritional highlights for health-conscious customers"""
        highlights = []
        if self.is_healthy_option:
            highlights.append("Healthy Choice")
        if self.is_low_calorie:
            highlights.append("Low Calorie")
        if self.is_high_protein:
            highlights.append("High Protein")
        if self.is_organic:
            highlights.append("Organic")
        if self.is_vegan:
            highlights.append("Vegan")
        return highlights
    
    @property
    def cultural_info(self):
        """Cultural and regional information"""
        return {
            'cuisine': self.cuisine_type,
            'region': self.region_of_origin,
            'significance': self.cultural_significance,
            'is_signature': self.is_signature_dish
        }

    def __str__(self):
        return f"{self.name} - ₹{self.price_inr}"
