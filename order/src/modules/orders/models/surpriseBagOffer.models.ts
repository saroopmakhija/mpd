export type SurpriseBagOfferModel = {
  id: bigint
  restaurantId: bigint
  title: string
  description?: string | null
  imageUrl?: string | null
  originalValue: number
  price: number
  quantityTotal: number
  quantityAvailable: number
  pickupWindowStart: Date
  pickupWindowEnd: Date
  isActive: boolean
  createdAt: Date
  updatedAt: Date
  isVegetarian?: boolean | null
  cuisine?: string | null
}

export type SurpriseBagOfferCreateInput = {
  restaurantId: bigint
  title: string
  description?: string | null
  imageUrl?: string | null
  originalValue: number
  price: number
  quantityTotal: number
  quantityAvailable?: number
  pickupWindowStart: Date
  pickupWindowEnd: Date
  isActive?: boolean
  isVegetarian?: boolean | null
  cuisine?: string | null
}

export type SurpriseBagOfferUpdateInput = Partial<SurpriseBagOfferCreateInput>


