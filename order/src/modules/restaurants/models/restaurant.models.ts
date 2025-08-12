export type RestaurantModel = {
    id: bigint
    address: string
    isActive: boolean
    latitude?: number | null
    longitude?: number | null
    city?: string | null
    state?: string | null
    pincode?: string | null
    country?: string | null
}

export type RestaurantCreateInput = {
    id: bigint
    address: string
    isActive: boolean
    latitude?: number | null
    longitude?: number | null
    city?: string | null
    state?: string | null
    pincode?: string | null
    country?: string | null
}

export type RestaurantUpdateInput = {
    id?: bigint
    address?: string
    isActive?: boolean
    latitude?: number | null
    longitude?: number | null
    city?: string | null
    state?: string | null
    pincode?: string | null
    country?: string | null
}