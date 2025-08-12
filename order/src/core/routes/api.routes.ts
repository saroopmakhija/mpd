import { addressRouter } from "@src/modules/addresses/routes/address.routes";
import { orderRouter } from "@src/modules/orders/routes/order.routes";
import { promocodeRouter } from "@src/modules/promotions/routes/promocode.routes";
import { restaurantRouter } from "@src/modules/restaurants/routes/restaurant.routes";
import { customerRouter } from "@src/modules/users/routes/customer.routes";
import { Router } from "express";
import buildOfferRoutes from "@src/modules/orders/routes/offer.routes";
import OfferService from "@src/modules/orders/services/implementations/OfferService";
import PrismaSurpriseBagOfferRepository from "@src/modules/orders/repositories/implementations/prisma/PrismaSurpriseBagOfferRepository";
import { getPrismaClient } from "@src/core/setup/prisma";
import PrismaRestaurantRepository from "@src/modules/restaurants/repositories/implementations/prisma/PrismaRestaurantRepository";

export const apiRouter = Router()

apiRouter.use("/orders", orderRouter)

apiRouter.use("/promocodes", promocodeRouter)

apiRouter.use("/restaurants", restaurantRouter)

apiRouter.use("/customers", customerRouter)

apiRouter.use("/addresses", addressRouter)

// Offers endpoints
const prisma = getPrismaClient()
const offerRepo = new PrismaSurpriseBagOfferRepository(prisma)
const restaurantRepo = new PrismaRestaurantRepository(prisma)
const offerService = new OfferService(offerRepo, restaurantRepo)
apiRouter.use("/offers", buildOfferRoutes(offerService))