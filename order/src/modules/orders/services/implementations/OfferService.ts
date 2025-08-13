import BaseService from "@src/core/services/BaseService";
import { SurpriseBagOfferCreateInput, SurpriseBagOfferModel, SurpriseBagOfferUpdateInput } from "../../models/surpriseBagOffer.models";
import ISurpriseBagOfferRepository from "../../repositories/interfaces/ISurpriseBagOfferRepository";
import IOfferService from "../interfaces/IOfferService";
import getAcrossDistance from "../../utils/getAcrossDistance";
import { RestaurantModel } from "@src/modules/restaurants/models/restaurant.models";
import IRestaurantRepository from "@src/modules/restaurants/repositories/interfaces/IRestaurantRepository";

export default class OfferService extends BaseService implements IOfferService {
  constructor(
    protected surpriseBagOfferRepository: ISurpriseBagOfferRepository,
    protected restaurantRepository: IRestaurantRepository,
  ) { super() }

  public async listRestaurantOffers(restaurantId: bigint): Promise<SurpriseBagOfferModel[]> {
    return this.surpriseBagOfferRepository.getRestaurantOffers(restaurantId, true)
  }

  public async createOffer(data: SurpriseBagOfferCreateInput): Promise<SurpriseBagOfferModel> {
    if (!this.restaurantManager) throw new Error("Permission denied")
    if (data.restaurantId !== this.restaurantManager.restaurantId) throw new Error("Ownership error")
    if (data.quantityTotal < 1) throw new Error("Quantity must be >= 1")
    
    // Calculate discount percentage for Indian market display
    const discountPercentage = Math.round(((data.originalValue - data.price) / data.originalValue) * 100)
    
    const createData: SurpriseBagOfferCreateInput = {
      ...data,
      quantityAvailable: data.quantityAvailable ?? data.quantityTotal,
      isActive: true,
    }
    
    // @ts-ignore - Add calculated discount percentage for Indian market
    const createDataWithDiscount = {
      ...createData,
      discountPercentage
    }
    
    return this.surpriseBagOfferRepository.create(createDataWithDiscount as any)
  }

  public async updateOffer(id: bigint, data: SurpriseBagOfferUpdateInput): Promise<SurpriseBagOfferModel> {
    if (!this.restaurantManager) throw new Error("Permission denied")
    // naive: rely on repo to check existence; real impl would fetch and assert ownership
    // @ts-ignore
    return this.surpriseBagOfferRepository.update(id, data as any)
  }

  public async listNearbyOffers(
    lat: number, 
    lng: number, 
    radiusKm: number, 
    filters?: { 
      veg?: boolean; 
      cuisine?: string;
      spiceLevel?: 'MILD' | 'MEDIUM' | 'SPICY';
      isJain?: boolean;
      isVegan?: boolean;
      foodCategory?: 'BREAKFAST' | 'LUNCH' | 'DINNER' | 'SNACKS' | 'SWEETS' | 'BEVERAGES';
      maxPrice?: number;
      minDiscount?: number;
    }
  ): Promise<SurpriseBagOfferModel[]> {
    // naive in-memory filter; production: SQL geospatial or WHERE by bounds
    const activeOffers = await (this.surpriseBagOfferRepository as any).listActive()
    const restaurants = await Promise.all(activeOffers.map(async (o: SurpriseBagOfferModel) => {
      const r = await this.restaurantRepository?.getOne(o.restaurantId)
      return [o, r] as [SurpriseBagOfferModel, RestaurantModel | null]
    }))
    const coords = { latitude: lat, longitude: lng }
    const filtered = restaurants
      .filter(([o, r]) => !!r && r?.latitude !== null && r?.longitude !== null)
      // Distance filter
      .filter(([o, r]) => getAcrossDistance(coords, { latitude: r!.latitude as number, longitude: r!.longitude as number }) <= radiusKm)
      // Indian market specific filters
      .filter(([o]) => (filters?.veg === undefined ? true : !!o.isVegetarian === !!filters?.veg))
      .filter(([o]) => (filters?.isJain === undefined ? true : !!o.isJain === !!filters?.isJain))
      .filter(([o]) => (filters?.isVegan === undefined ? true : !!o.isVegan === !!filters?.isVegan))
      .filter(([o]) => (filters?.cuisine ? (o.cuisine || '').toLowerCase() === filters.cuisine.toLowerCase() : true))
      .filter(([o]) => (filters?.spiceLevel ? o.spiceLevel === filters.spiceLevel : true))
      .filter(([o]) => (filters?.foodCategory ? o.foodCategory === filters.foodCategory : true))
      .filter(([o]) => (filters?.maxPrice ? o.price <= filters.maxPrice : true))
      .filter(([o]) => (filters?.minDiscount ? (o.discountPercentage || 0) >= filters.minDiscount : true))
      .map(([o]) => o)
      // Sort by discount percentage (highest first) for Indian market appeal
      .sort((a, b) => (b.discountPercentage || 0) - (a.discountPercentage || 0))
    
    return filtered
  }

  // New method for getting offers by food category (popular in Indian market)
  public async getOffersByCategory(
    category: 'BREAKFAST' | 'LUNCH' | 'DINNER' | 'SNACKS' | 'SWEETS' | 'BEVERAGES'
  ): Promise<SurpriseBagOfferModel[]> {
    const activeOffers = await (this.surpriseBagOfferRepository as any).listActive()
    return activeOffers
      .filter((o: SurpriseBagOfferModel) => o.foodCategory === category)
      .sort((a: SurpriseBagOfferModel, b: SurpriseBagOfferModel) => (b.discountPercentage || 0) - (a.discountPercentage || 0))
  }

  // Get vegetarian-only offers (very important for Indian market)
  public async getVegetarianOffers(): Promise<SurpriseBagOfferModel[]> {
    const activeOffers = await (this.surpriseBagOfferRepository as any).listActive()
    return activeOffers
      .filter((o: SurpriseBagOfferModel) => o.isVegetarian === true)
      .sort((a: SurpriseBagOfferModel, b: SurpriseBagOfferModel) => (b.discountPercentage || 0) - (a.discountPercentage || 0))
  }
}


