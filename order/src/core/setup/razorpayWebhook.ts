import { Router } from "express"
import crypto from "crypto"
import { PrismaClient } from "@prisma/client"
import getLogger from "@src/core/setup/logger"

export const razorpayRouter = Router()
const logger = getLogger(module)

// Minimal webhook: verify signature and mark payment info as paid (placeholder)
razorpayRouter.post("/", async (req, res) => {
  try {
    const signature = req.headers["x-razorpay-signature"] as string
    const secret = process.env.RAZORPAY_WEBHOOK_SECRET || "dummy"
    const body = JSON.stringify(req.body)
    const expected = crypto.createHmac("sha256", secret).update(body).digest("hex")
    if (signature !== expected) {
      logger.warn("Invalid Razorpay signature")
      return res.status(400).json({ ok: false })
    }
    const prisma = new PrismaClient()
    // In a real implementation, look up order by payload and mark as paid
    logger.info("Razorpay webhook received and verified")
    return res.json({ ok: true })
  } catch (e) {
    logger.error(`Razorpay webhook error: ${(e as Error).message}`)
    return res.status(500).json({ ok: false })
  }
})


