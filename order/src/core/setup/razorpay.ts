import Razorpay from "razorpay";

let client: Razorpay | null = null

export default function getRazorpay() {
  if (!client) {
    client = new Razorpay({
      key_id: process.env.RAZORPAY_KEY_ID || "dummy",
      key_secret: process.env.RAZORPAY_KEY_SECRET || "dummy",
    })
  }
  return client
}


