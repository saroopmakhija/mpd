import { Router } from "express"
import crypto from "crypto"
import { PrismaClient } from "@prisma/client"
import getLogger from "@src/core/setup/logger"

export const razorpayRouter = Router()
const logger = getLogger(module)
const prisma = new PrismaClient()

// Enhanced webhook handler for MealPeDeal payment processing
razorpayRouter.post("/", async (req, res) => {
  try {
    const signature = req.headers["x-razorpay-signature"] as string
    const secret = process.env.RAZORPAY_WEBHOOK_SECRET || "dummy"
    const body = JSON.stringify(req.body)
    const expected = crypto.createHmac("sha256", secret).update(body).digest("hex")
    
    if (signature !== expected) {
      logger.warn("Invalid Razorpay webhook signature")
      return res.status(400).json({ success: false, error: "Invalid signature" })
    }

    const event = req.body
    logger.info(`Razorpay webhook received: ${event.event}`)

    switch (event.event) {
      case "payment.captured":
        await handlePaymentCaptured(event.payload.payment.entity)
        break
      case "payment.failed":
        await handlePaymentFailed(event.payload.payment.entity)
        break
      case "order.paid":
        await handleOrderPaid(event.payload.order.entity)
        break
      default:
        logger.info(`Unhandled Razorpay event: ${event.event}`)
    }

    return res.json({ success: true })
  } catch (e) {
    logger.error(`Razorpay webhook error: ${(e as Error).message}`)
    return res.status(500).json({ success: false, error: "Internal server error" })
  }
})

async function handlePaymentCaptured(payment: any) {
  try {
    // Find order by payment intent ID
    const order = await prisma.order.findFirst({
      where: {
        paymentInformation: {
          paymentIntentId: payment.order_id
        }
      },
      include: {
        paymentInformation: true,
        offer: true
      }
    })

    if (!order) {
      logger.warn(`Order not found for payment ID: ${payment.id}`)
      return
    }

    // Update order status to PENDING (payment confirmed)
    await prisma.order.update({
      where: { id: order.id },
      data: { status: "PENDING" }
    })

    // If it's a mystery bag order, confirm the reservation
    if (order.offerId) {
      await prisma.order.update({
        where: { id: order.id },
        data: { status: "RESERVED" }
      })
    }

    logger.info(`Payment captured for order ${order.id}`)
  } catch (error) {
    logger.error(`Error handling payment captured: ${(error as Error).message}`)
  }
}

async function handlePaymentFailed(payment: any) {
  try {
    // Find order by payment intent ID
    const order = await prisma.order.findFirst({
      where: {
        paymentInformation: {
          paymentIntentId: payment.order_id
        }
      },
      include: {
        offer: true
      }
    })

    if (!order) {
      logger.warn(`Order not found for failed payment ID: ${payment.id}`)
      return
    }

    // Cancel the order
    await prisma.order.update({
      where: { id: order.id },
      data: { status: "CANCELLED" }
    })

    // If it's a mystery bag order, restore inventory
    if (order.offerId && order.offer) {
      await prisma.surpriseBagOffer.update({
        where: { id: order.offerId },
        data: {
          quantityAvailable: {
            increment: 1
          }
        }
      })
    }

    logger.info(`Payment failed for order ${order.id}, order cancelled`)
  } catch (error) {
    logger.error(`Error handling payment failed: ${(error as Error).message}`)
  }
}

async function handleOrderPaid(orderData: any) {
  try {
    logger.info(`Order paid webhook received for order: ${orderData.id}`)
    // Additional order-level payment processing if needed
  } catch (error) {
    logger.error(`Error handling order paid: ${(error as Error).message}`)
  }
}


