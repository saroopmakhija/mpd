import { SurpriseBagOfferCreateInput, SurpriseBagOfferModel, SurpriseBagOfferUpdateInput } from "../../models/surpriseBagOffer.models";

export default interface ISurpriseBagOfferRepository {
  getOne(id: bigint): Promise<SurpriseBagOfferModel | null>
  getRestaurantOffers(restaurantId: bigint, onlyActive?: boolean): Promise<SurpriseBagOfferModel[]>
  create(data: SurpriseBagOfferCreateInput): Promise<SurpriseBagOfferModel>
  update(id: bigint, data: SurpriseBagOfferUpdateInput): Promise<SurpriseBagOfferModel | null>
  reserveAtomic(id: bigint, quantity: number): Promise<SurpriseBagOfferModel | null>
  restoreAtomic(id: bigint, quantity: number): Promise<SurpriseBagOfferModel | null>
}


