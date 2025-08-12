import { SurpriseBagOfferCreateInput, SurpriseBagOfferModel, SurpriseBagOfferUpdateInput } from "../../models/surpriseBagOffer.models";

export default interface IOfferService {
  listRestaurantOffers(restaurantId: bigint): Promise<SurpriseBagOfferModel[]>
  createOffer(data: SurpriseBagOfferCreateInput): Promise<SurpriseBagOfferModel>
  updateOffer(id: bigint, data: SurpriseBagOfferUpdateInput): Promise<SurpriseBagOfferModel>
  listNearbyOffers(lat: number, lng: number, radiusKm: number, filters?: { veg?: boolean; cuisine?: string }): Promise<SurpriseBagOfferModel[]>
}


