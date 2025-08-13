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
  
  // Indian market specific fields
  isVegetarian?: boolean | null  // Critical for Indian customers
  cuisine?: string | null        // Indian, Chinese, Italian, etc.
  spiceLevel?: 'MILD' | 'MEDIUM' | 'SPICY' | null  // Important for Indian palate
  isJain?: boolean | null        // Jain dietary requirements
  isVegan?: boolean | null       // Growing vegan community in India
  containsAlcohol?: boolean | null // For legal compliance in some Indian states
  
  // Discount and pricing
  discountPercentage?: number | null  // Calculated discount % for marketing
  
  // Additional metadata for Indian market
  foodCategory?: 'BREAKFAST' | 'LUNCH' | 'DINNER' | 'SNACKS' | 'SWEETS' | 'BEVERAGES' | null
  preparationTime?: number | null     // Minutes - for customer expectations
  allergens?: string | null           // Comma separated list of allergens
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
  
  // Indian market specific fields
  isVegetarian?: boolean | null
  cuisine?: string | null
  spiceLevel?: 'MILD' | 'MEDIUM' | 'SPICY' | null
  isJain?: boolean | null
  isVegan?: boolean | null
  containsAlcohol?: boolean | null
  foodCategory?: 'BREAKFAST' | 'LUNCH' | 'DINNER' | 'SNACKS' | 'SWEETS' | 'BEVERAGES' | null
  preparationTime?: number | null
  allergens?: string | null
}

export type SurpriseBagOfferUpdateInput = Partial<SurpriseBagOfferCreateInput>


