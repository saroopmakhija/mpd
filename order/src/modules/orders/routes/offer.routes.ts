import { Router } from "express";
import { asyncHandler } from "@src/core/utils/asyncHandler";
import IOfferService from "../services/interfaces/IOfferService";

export const offerRouter = Router()

export default function buildOfferRoutes(offerService: IOfferService) {
  offerRouter.get("/restaurants/:restaurantId/offers", asyncHandler(async (req, res) => {
    const restaurantId = BigInt(req.params.restaurantId)
    const offers = await offerService.listRestaurantOffers(restaurantId)
    res.json(offers)
  }))

  // For managers
  offerRouter.post("/restaurants/:restaurantId/offers", asyncHandler(async (req, res) => {
    const restaurantId = BigInt(req.params.restaurantId)
    const payload = { ...req.body, restaurantId }
    const created = await offerService.createOffer(payload)
    res.status(201).json(created)
  }))

  offerRouter.patch("/offers/:offerId", asyncHandler(async (req, res) => {
    const offerId = BigInt(req.params.offerId)
    const updated = await offerService.updateOffer(offerId, req.body)
    res.json(updated)
  }))

  offerRouter.get("/nearby", asyncHandler(async (req, res) => {
    const lat = Number(req.query.lat)
    const lng = Number(req.query.lng)
    const radiusKm = Number(req.query.radiusKm || 5)
    
    // Parse Indian market specific filters
    const veg = req.query.veg === 'true' ? true : req.query.veg === 'false' ? false : undefined
    const isJain = req.query.isJain === 'true' ? true : req.query.isJain === 'false' ? false : undefined
    const isVegan = req.query.isVegan === 'true' ? true : req.query.isVegan === 'false' ? false : undefined
    const cuisine = typeof req.query.cuisine === 'string' ? req.query.cuisine : undefined
    const spiceLevel = ['MILD', 'MEDIUM', 'SPICY'].includes(req.query.spiceLevel as string) 
      ? req.query.spiceLevel as 'MILD' | 'MEDIUM' | 'SPICY' : undefined
    const foodCategory = ['BREAKFAST', 'LUNCH', 'DINNER', 'SNACKS', 'SWEETS', 'BEVERAGES'].includes(req.query.foodCategory as string)
      ? req.query.foodCategory as 'BREAKFAST' | 'LUNCH' | 'DINNER' | 'SNACKS' | 'SWEETS' | 'BEVERAGES' : undefined
    const maxPrice = req.query.maxPrice ? Number(req.query.maxPrice) : undefined
    const minDiscount = req.query.minDiscount ? Number(req.query.minDiscount) : undefined
    
    const offers = await offerService.listNearbyOffers(lat, lng, radiusKm, { 
      veg, 
      cuisine, 
      spiceLevel, 
      isJain, 
      isVegan, 
      foodCategory, 
      maxPrice, 
      minDiscount 
    })
    res.json(offers)
  }))

  // Indian market specific endpoints
  offerRouter.get("/vegetarian", asyncHandler(async (req, res) => {
    const offers = await offerService.getVegetarianOffers()
    res.json(offers)
  }))

  offerRouter.get("/category/:category", asyncHandler(async (req, res) => {
    const category = req.params.category as 'BREAKFAST' | 'LUNCH' | 'DINNER' | 'SNACKS' | 'SWEETS' | 'BEVERAGES'
    
    if (!['BREAKFAST', 'LUNCH', 'DINNER', 'SNACKS', 'SWEETS', 'BEVERAGES'].includes(category)) {
      return res.status(400).json({ error: "Invalid food category" })
    }
    
    const offers = await offerService.getOffersByCategory(category)
    res.json(offers)
  }))

  return offerRouter
}


