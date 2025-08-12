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
    const veg = req.query.veg === 'true' ? true : req.query.veg === 'false' ? false : undefined
    const cuisine = typeof req.query.cuisine === 'string' ? req.query.cuisine : undefined
    const offers = await offerService.listNearbyOffers(lat, lng, radiusKm, { veg, cuisine })
    res.json(offers)
  }))

  return offerRouter
}


