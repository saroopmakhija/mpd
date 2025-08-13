# IMPORTANT FOR ALEMBIC'S DETECTION OF TABLES #
# IMPORT ALL MODELS HERE #
from .base import Base, CustomBase
from .menu import Menu
from .category import MenuCategory
from .item import MenuItem
from .restaurant import Restaurant
from .manager import RestaurantManager
from .mystery_bag import MysteryBag, MysteryBagReview, MysteryBagTemplate

__all__ = [
    'Base', 'CustomBase', 'Menu', 'MenuCategory', 'MenuItem', 
    'Restaurant', 'RestaurantManager',
    'MysteryBag', 'MysteryBagReview', 'MysteryBagTemplate'
]
