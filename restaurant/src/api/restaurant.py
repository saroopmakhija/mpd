from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from geopy.distance import geodesic

from dependencies import get_uow, get_uow_with_commit, get_restaurant_service
from schemas.application import RestaurantApplicationCreateOut
from schemas.pagination import PaginatedResponse
from schemas.restaurant import (
    RestaurantRetrieveOut, RestaurantCreateIn, RestaurantUpdateIn, RestaurantUpdateOut,
    RestaurantComplianceIn, RestaurantLocationIn, RestaurantMysteryBagConfigIn,
    EnvironmentalImpactOut, ComplianceStatusOut, DietaryOptionsOut
)
from services import RestaurantService
from uow import SqlAlchemyUnitOfWork
from decorators import handle_app_errors

router = APIRouter(
    prefix='/restaurants'
)


@router.get('/', response_model=PaginatedResponse[RestaurantRetrieveOut])
@handle_app_errors
async def get_all_restaurants(service: RestaurantService = Depends(get_restaurant_service),
                              uow: SqlAlchemyUnitOfWork = Depends(get_uow),
                              name: Optional[str] = Query(default=None),
                              address: Optional[str] = Query(default=None),
                              city: Optional[str] = Query(default=None, description="Filter by city"),
                              state: Optional[str] = Query(default=None, description="Filter by state"),
                              pincode: Optional[str] = Query(default=None, description="Filter by PIN code"),
                              cuisine_type: Optional[str] = Query(default=None, description="Filter by cuisine type"),
                              # Indian market specific filters
                              vegetarian_only: Optional[bool] = Query(default=None, description="Show only vegetarian restaurants"),
                              jain_food: Optional[bool] = Query(default=None, description="Restaurants serving Jain food"),
                              vegan_options: Optional[bool] = Query(default=None, description="Restaurants with vegan options"),
                              halal_certified: Optional[bool] = Query(default=None, description="Halal certified restaurants"),
                              mystery_bag_enabled: Optional[bool] = Query(default=None, description="Restaurants offering mystery bags"),
                              verified_only: Optional[bool] = Query(default=None, description="Show only verified restaurants"),
                              order_by_rating: Optional[bool] = Query(default=False),
                              order_by_environmental_impact: Optional[bool] = Query(default=False, description="Order by food waste saved"),
                              limit: int = Query(100, ge=1),
                              offset: int = Query(0, ge=0)):
    return await service.list(
        uow, name=name, address=address, city=city, state=state, pincode=pincode,
        cuisine_type=cuisine_type, vegetarian_only=vegetarian_only, jain_food=jain_food,
        vegan_options=vegan_options, halal_certified=halal_certified, 
        mystery_bag_enabled=mystery_bag_enabled, verified_only=verified_only,
        order_by_rating=order_by_rating, order_by_environmental_impact=order_by_environmental_impact,
        limit=limit, offset=offset
    )


@router.get('/nearby/', response_model=List[RestaurantRetrieveOut])
@handle_app_errors
async def get_nearby_restaurants(lat: float = Query(..., description="Latitude"),
                                 lng: float = Query(..., description="Longitude"),
                                 radius_km: float = Query(5.0, description="Search radius in kilometers"),
                                 service: RestaurantService = Depends(get_restaurant_service),
                                 uow: SqlAlchemyUnitOfWork = Depends(get_uow),
                                 # Indian market specific filters
                                 vegetarian_only: Optional[bool] = Query(default=None),
                                 jain_food: Optional[bool] = Query(default=None),
                                 vegan_options: Optional[bool] = Query(default=None),
                                 halal_certified: Optional[bool] = Query(default=None),
                                 cuisine_type: Optional[str] = Query(default=None),
                                 mystery_bag_enabled: Optional[bool] = Query(default=True),
                                 limit: int = Query(20, ge=1, le=50)):
    """
    Find restaurants near a given location with Indian market specific filters.
    Essential for MealPeDeal's location-based mystery bag discovery.
    """
    return await service.get_nearby_restaurants(
        lat, lng, radius_km, uow,
        vegetarian_only=vegetarian_only, jain_food=jain_food, vegan_options=vegan_options,
        halal_certified=halal_certified, cuisine_type=cuisine_type,
        mystery_bag_enabled=mystery_bag_enabled, limit=limit
    )


@router.get('/current/', response_model=RestaurantRetrieveOut | None)
@handle_app_errors
async def get_current_restaurant(service: RestaurantService = Depends(get_restaurant_service),
                                 uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    return await service.retrieve_current_restaurant(uow)


@router.get('/{restaurant_id}/', response_model=RestaurantRetrieveOut)
@handle_app_errors
async def get_restaurant(restaurant_id: int,
                         service: RestaurantService = Depends(get_restaurant_service),
                         uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    return await service.retrieve(restaurant_id, uow)


@router.get('/{restaurant_id}/environmental-impact/', response_model=EnvironmentalImpactOut)
@handle_app_errors
async def get_restaurant_environmental_impact(restaurant_id: int,
                                              service: RestaurantService = Depends(get_restaurant_service),
                                              uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    """
    Get environmental impact metrics for a restaurant.
    Important for showcasing sustainability in Indian market.
    """
    return await service.get_environmental_impact(restaurant_id, uow)


@router.get('/{restaurant_id}/compliance-status/', response_model=ComplianceStatusOut)
@handle_app_errors
async def get_restaurant_compliance_status(restaurant_id: int,
                                           service: RestaurantService = Depends(get_restaurant_service),
                                           uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    """
    Check compliance status for Indian regulations (GST, FSSAI, etc.).
    Essential for legal operations in Indian market.
    """
    return await service.get_compliance_status(restaurant_id, uow)


@router.get('/{restaurant_id}/dietary-options/', response_model=DietaryOptionsOut)
@handle_app_errors
async def get_restaurant_dietary_options(restaurant_id: int,
                                         service: RestaurantService = Depends(get_restaurant_service),
                                         uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    """
    Get dietary options summary for a restaurant.
    Critical for Indian market dietary preferences.
    """
    return await service.get_dietary_options(restaurant_id, uow)


@router.post('/', response_model=RestaurantApplicationCreateOut)
@handle_app_errors
async def create_restaurant(restaurant: RestaurantCreateIn,
                            service: RestaurantService = Depends(get_restaurant_service),
                            uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    return await service.create(restaurant, uow)


@router.put('/{restaurant_id}/', response_model=RestaurantApplicationCreateOut)
@handle_app_errors
async def update_restaurant(restaurant_id: int,
                            restaurant: RestaurantUpdateIn,
                            service: RestaurantService = Depends(get_restaurant_service),
                            uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    return await service.update(restaurant_id, restaurant, uow)


@router.patch('/{restaurant_id}/compliance/', response_model=RestaurantUpdateOut)
@handle_app_errors
async def update_restaurant_compliance(restaurant_id: int,
                                       compliance_data: RestaurantComplianceIn,
                                       service: RestaurantService = Depends(get_restaurant_service),
                                       uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    """
    Update restaurant compliance information (GST, FSSAI, PAN, Trade License).
    Essential for Indian market legal compliance.
    """
    return await service.update_compliance(restaurant_id, compliance_data, uow)


@router.patch('/{restaurant_id}/location/', response_model=RestaurantUpdateOut)
@handle_app_errors
async def update_restaurant_location(restaurant_id: int,
                                     location_data: RestaurantLocationIn,
                                     service: RestaurantService = Depends(get_restaurant_service),
                                     uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    """
    Update restaurant location information for better discovery.
    Critical for location-based mystery bag offers.
    """
    return await service.update_location(restaurant_id, location_data, uow)


@router.patch('/{restaurant_id}/mystery-bag-config/', response_model=RestaurantUpdateOut)
@handle_app_errors
async def update_mystery_bag_config(restaurant_id: int,
                                    config_data: RestaurantMysteryBagConfigIn,
                                    service: RestaurantService = Depends(get_restaurant_service),
                                    uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    """
    Configure mystery bag settings for the restaurant.
    Core functionality for MealPeDeal platform.
    """
    return await service.update_mystery_bag_config(restaurant_id, config_data, uow)


@router.patch('/{restaurant_id}/activate/', response_model=RestaurantUpdateOut)
@handle_app_errors
async def activate_restaurant(restaurant_id: int,
                              service: RestaurantService = Depends(get_restaurant_service),
                              uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    return await service.activate_restaurant(restaurant_id, uow)


@router.patch('/{restaurant_id}/deactivate/', response_model=RestaurantUpdateOut)
@handle_app_errors
async def deactivate_restaurant(restaurant_id: int,
                                service: RestaurantService = Depends(get_restaurant_service),
                                uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    return await service.deactivate_restaurant(restaurant_id, uow)


@router.patch('/{restaurant_id}/verify/', response_model=RestaurantUpdateOut)
@handle_app_errors
async def verify_restaurant(restaurant_id: int,
                            service: RestaurantService = Depends(get_restaurant_service),
                            uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    """
    Verify restaurant for MealPeDeal platform.
    Important for building trust in Indian market.
    """
    return await service.verify_restaurant(restaurant_id, uow)


@router.patch('/{restaurant_id}/unverify/', response_model=RestaurantUpdateOut)
@handle_app_errors
async def unverify_restaurant(restaurant_id: int,
                              service: RestaurantService = Depends(get_restaurant_service),
                              uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    """
    Remove verification status from restaurant.
    """
    return await service.unverify_restaurant(restaurant_id, uow)


@router.put('/{restaurant_id}/image/', response_model=RestaurantUpdateOut)
@handle_app_errors
async def upload_restaurant_image(restaurant_id: int,
                                  image: UploadFile = File(...),
                                  service: RestaurantService = Depends(get_restaurant_service),
                                  uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    # Check if the uploaded file is an image
    if not image.content_type.startswith('image'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    return await service.upload_image(restaurant_id, image, uow)


@router.post('/{restaurant_id}/record-mystery-bag-sale/', response_model=RestaurantUpdateOut)
@handle_app_errors
async def record_mystery_bag_sale(restaurant_id: int,
                                  quantity: int = Query(..., description="Number of mystery bags sold"),
                                  food_weight_kg: float = Query(..., description="Weight of food saved in kg"),
                                  service: RestaurantService = Depends(get_restaurant_service),
                                  uow: SqlAlchemyUnitOfWork = Depends(get_uow_with_commit)):
    """
    Record mystery bag sale for environmental impact tracking.
    Essential for sustainability metrics in MealPeDeal.
    """
    return await service.record_mystery_bag_sale(restaurant_id, quantity, food_weight_kg, uow)


# Indian market specific analytics endpoints

@router.get('/analytics/top-performers/', response_model=List[RestaurantRetrieveOut])
@handle_app_errors
async def get_top_performing_restaurants(metric: str = Query("mystery_bags_sold", description="Metric to rank by"),
                                         city: Optional[str] = Query(default=None, description="Filter by city"),
                                         limit: int = Query(10, ge=1, le=50),
                                         service: RestaurantService = Depends(get_restaurant_service),
                                         uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    """
    Get top performing restaurants by various metrics.
    Useful for showcasing success stories in Indian market.
    """
    return await service.get_top_performers(metric, city, limit, uow)


@router.get('/analytics/cuisine-distribution/', response_model=dict)
@handle_app_errors
async def get_cuisine_distribution(city: Optional[str] = Query(default=None, description="Filter by city"),
                                   service: RestaurantService = Depends(get_restaurant_service),
                                   uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    """
    Get distribution of restaurants by cuisine type.
    Helpful for market analysis in Indian food ecosystem.
    """
    return await service.get_cuisine_distribution(city, uow)
