import Razorpay from "razorpay";
import crypto from "crypto";

let client: Razorpay | null = null;

export default function getRazorpay() {
  if (!client) {
    client = new Razorpay({
      key_id: process.env.RAZORPAY_KEY_ID || "dummy",
      key_secret: process.env.RAZORPAY_KEY_SECRET || "dummy",
    });
  }
  return client;
}

// Verify Razorpay payment signature
export function verifyRazorpaySignature(
  orderId: string,
  paymentId: string,
  signature: string,
  secret: string = process.env.RAZORPAY_KEY_SECRET || "dummy"
): boolean {
  const expectedSignature = crypto
    .createHmac("sha256", secret)
    .update(`${orderId}|${paymentId}`)
    .digest("hex");
  
  return expectedSignature === signature;
}

// Create order with Indian market optimizations
export async function createRazorpayOrder(
  amount: number, // in INR paise (multiply by 100)
  currency: string = "INR",
  receipt: string,
  notes?: Record<string, string>
) {
  const razorpay = getRazorpay();
  
  return await razorpay.orders.create({
    amount: Math.round(amount * 100), // Convert to paise
    currency,
    receipt,
    notes: {
      purpose: "MealPeDeal Mystery Bag Purchase",
      platform: "mealpedealing",
      ...notes
    },
    payment_capture: 1 // Auto capture payments
  });
}

// Get payment details
export async function getPaymentDetails(paymentId: string) {
  const razorpay = getRazorpay();
  return await razorpay.payments.fetch(paymentId);
}

// Refund payment (for cancellations)
export async function createRefund(paymentId: string, amount?: number) {
  const razorpay = getRazorpay();
  return await razorpay.payments.refund(paymentId, {
    amount: amount ? Math.round(amount * 100) : undefined, // Full refund if amount not specified
    speed: "normal",
    notes: {
      reason: "MealPeDeal order cancellation"
    }
  });
}


