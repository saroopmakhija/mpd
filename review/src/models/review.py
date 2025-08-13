from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta

from .base import Base


@dataclass
class ReviewBaseModel(ABC):
    """
    Base model for a review.
    """

    rating: int
    comment: Optional[str]


@dataclass
class ReviewModel(ReviewBaseModel):
    """
    Model for a review.
    """

    id: int
    customer_id: int
    customer_full_name: str
    customer_image_url: str
    order_id: Optional[int]
    restaurant_id: Optional[int]
    menu_item_id: Optional[int]
    created_at: datetime


@dataclass
class ReviewCreateModel(ReviewBaseModel):
    """
    Model for creating a review.
    """

    customer_id: int
    order_id: Optional[int] = None
    restaurant_id: Optional[int] = None
    menu_item_id: Optional[int] = None


@dataclass
class ReviewUpdateModel(ReviewBaseModel):
    """
    Model for updating a review.
    """

    pass


class RestaurantReview(Base):
    """
    Restaurant reviews for MealPeDeal - optimized for Indian market.
    Includes specific categories important for Indian food and service expectations.
    """
    __tablename__ = 'restaurant_reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # References to other microservices
    restaurant_id = Column(Integer, nullable=False)  # Reference to restaurant service
    customer_id = Column(Integer, nullable=False)    # Reference to user-management service
    order_id = Column(Integer, nullable=True)        # Reference to order service (if applicable)
    
    # Overall rating and review
    overall_rating = Column(Integer, nullable=False)  # 1-5 stars
    review_text = Column(Text, nullable=True)
    review_title = Column(String(200), nullable=True)
    
    # Indian market specific rating categories
    food_quality_rating = Column(Integer, nullable=True)      # 1-5: Taste, freshness, authenticity
    value_for_money_rating = Column(Integer, nullable=True)   # 1-5: Price vs quantity/quality
    service_rating = Column(Integer, nullable=True)          # 1-5: Staff behavior, responsiveness
    hygiene_rating = Column(Integer, nullable=True)          # 1-5: Cleanliness (very important in India)
    pickup_experience_rating = Column(Integer, nullable=True) # 1-5: For mystery bag pickup
    authenticity_rating = Column(Integer, nullable=True)     # 1-5: How authentic the cuisine is
    spice_level_accuracy = Column(Integer, nullable=True)    # 1-5: Did spice level match expectation
    
    # Specific feedback for Indian market
    was_food_fresh = Column(Boolean, nullable=True)
    was_spice_level_accurate = Column(Boolean, nullable=True)
    was_quantity_adequate = Column(Boolean, nullable=True)
    was_packaging_good = Column(Boolean, nullable=True)      # Important for takeout/pickup
    would_recommend = Column(Boolean, nullable=True)
    
    # Experience type
    experience_type = Column(String(50), nullable=True)  # MYSTERY_BAG, REGULAR_ORDER, DINE_IN
    meal_category = Column(String(50), nullable=True)    # BREAKFAST, LUNCH, DINNER, SNACKS
    
    # Trust and verification
    is_verified_purchase = Column(Boolean, default=True)
    has_photos = Column(Boolean, default=False)
    photo_urls = Column(JSON, nullable=True)  # List of review photo URLs
    
    # Helpfulness and moderation
    helpful_votes = Column(Integer, default=0)
    unhelpful_votes = Column(Integer, default=0)
    is_flagged = Column(Boolean, default=False)
    flag_reason = Column(String(100), nullable=True)
    is_approved = Column(Boolean, default=True)
    moderated_at = Column(DateTime, nullable=True)
    
    # Language support for Indian market
    language = Column(String(10), default='en')  # 'en', 'hi', etc.
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Restaurant response (important for customer service)
    restaurant_response = Column(Text, nullable=True)
    restaurant_responded_at = Column(DateTime, nullable=True)
    
    @property
    def average_category_rating(self):
        """Calculate average of all category ratings"""
        ratings = [
            r for r in [
                self.food_quality_rating, self.value_for_money_rating,
                self.service_rating, self.hygiene_rating, self.pickup_experience_rating,
                self.authenticity_rating, self.spice_level_accuracy
            ] if r is not None
        ]
        return sum(ratings) / len(ratings) if ratings else None
    
    @property
    def is_recent(self):
        """Check if review is from last 30 days"""
        return self.created_at > datetime.utcnow() - timedelta(days=30)
    
    @property
    def helpfulness_score(self):
        """Calculate helpfulness score"""
        total_votes = self.helpful_votes + self.unhelpful_votes
        if total_votes == 0:
            return 0
        return (self.helpful_votes / total_votes) * 100

    def __str__(self):
        return f"Review for Restaurant {self.restaurant_id} - {self.overall_rating}★"


class MysteryBagReview(Base):
    """
    Specific reviews for mystery bags - core feature of MealPeDeal.
    Focuses on surprise factor, value, and overall mystery bag experience.
    """
    __tablename__ = 'mystery_bag_reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # References
    mystery_bag_id = Column(Integer, nullable=False)  # Reference to menu service mystery bag
    restaurant_id = Column(Integer, nullable=False)   # Reference to restaurant service
    customer_id = Column(Integer, nullable=False)     # Reference to user-management service
    order_id = Column(Integer, nullable=False)        # Reference to order service
    
    # Overall mystery bag experience
    overall_rating = Column(Integer, nullable=False)  # 1-5 stars
    review_text = Column(Text, nullable=True)
    
    # Mystery bag specific ratings
    value_for_money_rating = Column(Integer, nullable=False)     # 1-5: Was it worth the price?
    food_quality_rating = Column(Integer, nullable=False)       # 1-5: Quality of food received
    quantity_rating = Column(Integer, nullable=False)           # 1-5: Was quantity satisfactory?
    variety_rating = Column(Integer, nullable=False)            # 1-5: Good variety of items?
    surprise_factor_rating = Column(Integer, nullable=False)    # 1-5: How surprising was it?
    freshness_rating = Column(Integer, nullable=False)          # 1-5: Freshness of food
    packaging_rating = Column(Integer, nullable=True)           # 1-5: Quality of packaging
    pickup_experience_rating = Column(Integer, nullable=True)   # 1-5: Pickup process experience
    
    # Specific mystery bag feedback
    items_received = Column(JSON, nullable=True)        # List of items received
    expected_vs_actual = Column(Text, nullable=True)    # Expectations vs reality
    would_buy_again = Column(Boolean, nullable=True)
    would_recommend_to_others = Column(Boolean, nullable=True)
    
    # Indian market specific feedback
    dietary_requirements_met = Column(Boolean, nullable=True)  # Were veg/jain/etc. requirements met?
    spice_level_appropriate = Column(Boolean, nullable=True)   # Was spice level suitable?
    cultural_authenticity = Column(Integer, nullable=True)     # 1-5: Authenticity of cuisine
    
    # Environmental consciousness (important for MealPeDeal's mission)
    environmental_satisfaction = Column(Integer, nullable=True)  # 1-5: Happy about reducing waste?
    
    # Trust and verification
    is_verified_purchase = Column(Boolean, default=True)
    has_photos = Column(Boolean, default=False)
    photo_urls = Column(JSON, nullable=True)
    
    # Moderation
    helpful_votes = Column(Integer, default=0)
    is_flagged = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    
    # Language and timestamps
    language = Column(String(10), default='en')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    @property
    def average_rating(self):
        """Calculate average of all rating categories"""
        ratings = [
            self.value_for_money_rating, self.food_quality_rating,
            self.quantity_rating, self.variety_rating, self.surprise_factor_rating,
            self.freshness_rating
        ]
        optional_ratings = [
            r for r in [self.packaging_rating, self.pickup_experience_rating, 
                       self.cultural_authenticity, self.environmental_satisfaction]
            if r is not None
        ]
        all_ratings = ratings + optional_ratings
        return sum(all_ratings) / len(all_ratings)
    
    def __str__(self):
        return f"Mystery Bag Review {self.mystery_bag_id} - {self.overall_rating}★"


class ReviewHelpfulness(Base):
    """
    Track which users found reviews helpful - important for review credibility.
    """
    __tablename__ = 'review_helpfulness'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    review_id = Column(Integer, nullable=False)      # Can reference any review table
    review_type = Column(String(50), nullable=False) # 'restaurant', 'mystery_bag'
    customer_id = Column(Integer, nullable=False)    # User who voted
    
    is_helpful = Column(Boolean, nullable=False)     # True = helpful, False = not helpful
    created_at = Column(DateTime, default=func.now())
    
    def __str__(self):
        helpful_text = "helpful" if self.is_helpful else "not helpful"
        return f"Review {self.review_id} marked as {helpful_text}"


class ReviewFlag(Base):
    """
    User-reported flags for inappropriate reviews - important for content moderation.
    """
    __tablename__ = 'review_flags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    review_id = Column(Integer, nullable=False)
    review_type = Column(String(50), nullable=False)  # 'restaurant', 'mystery_bag'
    flagger_customer_id = Column(Integer, nullable=False)
    
    flag_reason = Column(String(100), nullable=False)  # 'spam', 'inappropriate', 'fake', 'offensive'
    flag_description = Column(Text, nullable=True)
    
    is_reviewed = Column(Boolean, default=False)
    moderator_action = Column(String(50), nullable=True)  # 'approved', 'removed', 'warned'
    moderator_notes = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    def __str__(self):
        return f"Flag for review {self.review_id} - {self.flag_reason}"


class RestaurantResponseToReview(Base):
    """
    Restaurant responses to customer reviews - important for customer service in Indian market.
    """
    __tablename__ = 'restaurant_responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    review_id = Column(Integer, nullable=False)
    review_type = Column(String(50), nullable=False)  # 'restaurant', 'mystery_bag'
    restaurant_id = Column(Integer, nullable=False)
    responder_id = Column(Integer, nullable=False)    # Restaurant manager/owner ID
    
    response_text = Column(Text, nullable=False)
    language = Column(String(10), default='en')      # Support for Hindi/English responses
    
    is_public = Column(Boolean, default=True)        # Public response vs private message
    is_approved = Column(Boolean, default=True)      # Moderation for public responses
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __str__(self):
        return f"Restaurant response to review {self.review_id}"


class ReviewAnalytics(Base):
    """
    Analytics data for reviews - helps restaurants understand feedback trends.
    """
    __tablename__ = 'review_analytics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    restaurant_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    
    # Daily aggregated statistics
    total_reviews = Column(Integer, default=0)
    total_mystery_bag_reviews = Column(Integer, default=0)
    
    # Average ratings
    avg_overall_rating = Column(Float, nullable=True)
    avg_food_quality = Column(Float, nullable=True)
    avg_value_for_money = Column(Float, nullable=True)
    avg_service_rating = Column(Float, nullable=True)
    avg_hygiene_rating = Column(Float, nullable=True)
    
    # Indian market specific metrics
    vegetarian_reviews_count = Column(Integer, default=0)
    jain_reviews_count = Column(Integer, default=0)
    spice_level_complaints = Column(Integer, default=0)
    authenticity_score = Column(Float, nullable=True)
    
    # Mystery bag specific metrics
    avg_mystery_bag_rating = Column(Float, nullable=True)
    avg_surprise_factor = Column(Float, nullable=True)
    mystery_bag_repeat_customers = Column(Integer, default=0)
    
    # Response metrics
    response_rate = Column(Float, nullable=True)      # % of reviews responded to
    avg_response_time_hours = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    def __str__(self):
        return f"Analytics for restaurant {self.restaurant_id} on {self.date.date()}"
