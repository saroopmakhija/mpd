import { PrismaClient } from "@prisma/client"
import getLogger from "@src/core/setup/logger"

const logger = getLogger(module)

export function startSchedulers(prisma: PrismaClient) {
  // Every minute: expire reservations past pickup window and restock
  setInterval(async () => {
    try {
      const now = new Date()
      const overdue = await prisma.order.findMany({
        where: {
          status: "RESERVED",
          pickupWindowEnd: { lt: now }
        },
        select: { id: true, offerId: true }
      })

      for (const o of overdue) {
        await prisma.$transaction(async (tx) => {
          await tx.order.update({ where: { id: o.id }, data: { status: "EXPIRED" } })
          if (o.offerId) {
            await tx.surpriseBagOffer.update({ where: { id: o.offerId }, data: { quantityAvailable: { increment: 1 } } })
          }
        })
        logger.info(`Expired reservation order=${o.id} and restocked offer=${o.offerId}`)
      }
    } catch (err) {
      logger.error(`Scheduler error: ${(err as Error).message}`)
    }
  }, 60_000)
}


