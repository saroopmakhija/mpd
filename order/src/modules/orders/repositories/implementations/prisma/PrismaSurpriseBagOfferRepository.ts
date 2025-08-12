import { PrismaClient } from "@prisma/client";
import PrismaBaseRepository from "@src/core/repositories/prisma/PrismaBaseRepository";
import { SurpriseBagOfferCreateInput, SurpriseBagOfferModel, SurpriseBagOfferUpdateInput } from "../../../models/surpriseBagOffer.models";
import ISurpriseBagOfferRepository from "../../interfaces/ISurpriseBagOfferRepository";
import { SurpriseBagOfferDelegate } from "./delegates";

export default class PrismaSurpriseBagOfferRepository extends PrismaBaseRepository<SurpriseBagOfferDelegate, SurpriseBagOfferModel, SurpriseBagOfferCreateInput, SurpriseBagOfferUpdateInput> implements ISurpriseBagOfferRepository {

  constructor(prisma: PrismaClient) {
    super(prisma.surpriseBagOffer)
  }

  public async getOne(id: bigint): Promise<SurpriseBagOfferModel | null> {
    return this.delegate.findFirst({ where: { id } })
  }

  public async getRestaurantOffers(restaurantId: bigint, onlyActive: boolean = true): Promise<SurpriseBagOfferModel[]> {
    return this.delegate.findMany({ where: { restaurantId, isActive: onlyActive } })
  }

  public async create(data: SurpriseBagOfferCreateInput): Promise<SurpriseBagOfferModel> {
    // @ts-ignore - Prisma types generated map
    return this.delegate.create({ data: data as any })
  }

  public async update(id: bigint, data: SurpriseBagOfferUpdateInput): Promise<SurpriseBagOfferModel | null> {
    // @ts-ignore
    return this.delegate.update({ where: { id }, data: data as any }).catch(() => null)
  }

  public async listActive(): Promise<SurpriseBagOfferModel[]> {
    const now = new Date()
    return this.delegate.findMany({
      where: {
        isActive: true,
        pickupWindowEnd: { gt: now }
      }
    })
  }

  public async reserveAtomic(id: bigint, quantity: number): Promise<SurpriseBagOfferModel | null> {
    // @ts-ignore
    return (this.delegate as any).update({
      where: { id, quantityAvailable: { gte: quantity } },
      data: { quantityAvailable: { decrement: quantity } },
    }).catch(() => null)
  }

  public async restoreAtomic(id: bigint, quantity: number): Promise<SurpriseBagOfferModel | null> {
    // @ts-ignore
    return (this.delegate as any).update({
      where: { id },
      data: { quantityAvailable: { increment: quantity } },
    }).catch(() => null)
  }
}


