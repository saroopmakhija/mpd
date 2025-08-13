import { SurpriseBagOfferCreateInput, SurpriseBagOfferModel, SurpriseBagOfferUpdateInput } from "../../models/surpriseBagOffer.models";

export default interface IOfferService {
  listRestaurantOffers(restaurantId: bigint): Promise<SurpriseBagOfferModel[]>
  createOffer(data: SurpriseBagOfferCreateInput): Promise<SurpriseBagOfferModel>
  updateOffer(id: bigint, data: SurpriseBagOfferUpdateInput): Promise<SurpriseBagOfferModel>
  listNearbyOffers(
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
  ): Promise<SurpriseBagOfferModel[]>
  
  // Indian market specific methods
  getOffersByCategory(
    category: 'BREAKFAST' | 'LUNCH' | 'DINNER' | 'SNACKS' | 'SWEETS' | 'BEVERAGES'
  ): Promise<SurpriseBagOfferModel[]>
  getVegetarianOffers(): Promise<SurpriseBagOfferModel[]>
}


