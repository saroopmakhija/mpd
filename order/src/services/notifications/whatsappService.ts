// WhatsApp Business API Service for Indian Market - MealPeDeal
import axios from 'axios';
import { formatIndianPhone } from '../../utils/localization';

export interface WhatsAppMessage {
  to: string;
  templateName: string;
  languageCode: string;
  components?: Array<{
    type: 'header' | 'body' | 'button';
    parameters: Array<{
      type: 'text' | 'currency' | 'date_time';
      text?: string;
      currency?: {
        fallback_value: string;
        code: string;
        amount_1000: number;
      };
      date_time?: {
        fallback_value: string;
      };
    }>;
  }>;
}

export interface WhatsAppResponse {
  success: boolean;
  messageId?: string;
  error?: string;
}

export class WhatsAppService {
  private accessToken: string;
  private phoneNumberId: string;
  private baseUrl: string;

  constructor(accessToken: string, phoneNumberId: string) {
    this.accessToken = accessToken;
    this.phoneNumberId = phoneNumberId;
    this.baseUrl = `https://graph.facebook.com/v18.0/${phoneNumberId}/messages`;
  }

  private async sendTemplateMessage(message: WhatsAppMessage): Promise<WhatsAppResponse> {
    try {
      const phone = formatIndianPhone(message.to).replace(/\D/g, '');
      const formattedPhone = `91${phone.substring(phone.length - 10)}`;

      const payload = {
        messaging_product: 'whatsapp',
        to: formattedPhone,
        type: 'template',
        template: {
          name: message.templateName,
          language: {
            code: message.languageCode
          },
          components: message.components || []
        }
      };

      const response = await axios.post(this.baseUrl, payload, {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        }
      });

      return {
        success: true,
        messageId: response.data.messages?.[0]?.id
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error?.message || error.message
      };
    }
  }

  // Send reservation confirmation via WhatsApp
  async sendReservationConfirmation(
    phone: string,
    customerName: string,
    restaurantName: string,
    pickupCode: string,
    pickupTime: string,
    amount: number,
    restaurantAddress: string
  ): Promise<WhatsAppResponse> {
    return this.sendTemplateMessage({
      to: phone,
      templateName: 'reservation_confirmation',
      languageCode: 'en',
      components: [
        {
          type: 'body',
          parameters: [
            { type: 'text', text: customerName },
            { type: 'text', text: restaurantName },
            { type: 'text', text: pickupCode },
            { type: 'text', text: pickupTime },
            { 
              type: 'currency', 
              currency: {
                fallback_value: `₹${amount}`,
                code: 'INR',
                amount_1000: amount * 1000
              }
            },
            { type: 'text', text: restaurantAddress }
          ]
        }
      ]
    });
  }

  // Send pickup reminder via WhatsApp
  async sendPickupReminder(
    phone: string,
    customerName: string,
    restaurantName: string,
    pickupCode: string,
    timeRemaining: string,
    restaurantAddress: string
  ): Promise<WhatsAppResponse> {
    return this.sendTemplateMessage({
      to: phone,
      templateName: 'pickup_reminder',
      languageCode: 'en',
      components: [
        {
          type: 'body',
          parameters: [
            { type: 'text', text: customerName },
            { type: 'text', text: restaurantName },
            { type: 'text', text: timeRemaining },
            { type: 'text', text: pickupCode },
            { type: 'text', text: restaurantAddress }
          ]
        }
      ]
    });
  }

  // Send pickup ready notification via WhatsApp
  async sendPickupReady(
    phone: string,
    customerName: string,
    restaurantName: string,
    pickupCode: string,
    restaurantAddress: string,
    restaurantPhone: string
  ): Promise<WhatsAppResponse> {
    return this.sendTemplateMessage({
      to: phone,
      templateName: 'pickup_ready',
      languageCode: 'en',
      components: [
        {
          type: 'body',
          parameters: [
            { type: 'text', text: customerName },
            { type: 'text', text: restaurantName },
            { type: 'text', text: pickupCode },
            { type: 'text', text: restaurantAddress },
            { type: 'text', text: restaurantPhone }
          ]
        }
      ]
    });
  }

  // Send order cancellation via WhatsApp
  async sendCancellationNotification(
    phone: string,
    customerName: string,
    restaurantName: string,
    refundAmount: number,
    reason?: string
  ): Promise<WhatsAppResponse> {
    return this.sendTemplateMessage({
      to: phone,
      templateName: 'order_cancellation',
      languageCode: 'en',
      components: [
        {
          type: 'body',
          parameters: [
            { type: 'text', text: customerName },
            { type: 'text', text: restaurantName },
            { 
              type: 'currency', 
              currency: {
                fallback_value: `₹${refundAmount}`,
                code: 'INR',
                amount_1000: refundAmount * 1000
              }
            },
            { type: 'text', text: reason || 'restaurant unavailability' }
          ]
        }
      ]
    });
  }

  // Send welcome message to new customers (in Hindi/English)
  async sendWelcomeMessage(
    phone: string,
    customerName: string,
    language: 'en' | 'hi' = 'en'
  ): Promise<WhatsAppResponse> {
    return this.sendTemplateMessage({
      to: phone,
      templateName: language === 'hi' ? 'welcome_message_hindi' : 'welcome_message_english',
      languageCode: language,
      components: [
        {
          type: 'body',
          parameters: [
            { type: 'text', text: customerName }
          ]
        }
      ]
    });
  }

  // Send daily deals notification
  async sendDailyDeals(
    phone: string,
    customerName: string,
    nearbyRestaurantCount: number,
    bestDealDiscount: number,
    language: 'en' | 'hi' = 'en'
  ): Promise<WhatsAppResponse> {
    return this.sendTemplateMessage({
      to: phone,
      templateName: language === 'hi' ? 'daily_deals_hindi' : 'daily_deals_english',
      languageCode: language,
      components: [
        {
          type: 'body',
          parameters: [
            { type: 'text', text: customerName },
            { type: 'text', text: nearbyRestaurantCount.toString() },
            { type: 'text', text: `${bestDealDiscount}%` }
          ]
        }
      ]
    });
  }

  // Send environmental impact message (food waste saved)
  async sendEnvironmentalImpact(
    phone: string,
    customerName: string,
    totalMealsSaved: number,
    co2Saved: string,
    language: 'en' | 'hi' = 'en'
  ): Promise<WhatsAppResponse> {
    return this.sendTemplateMessage({
      to: phone,
      templateName: language === 'hi' ? 'environmental_impact_hindi' : 'environmental_impact_english',
      languageCode: language,
      components: [
        {
          type: 'body',
          parameters: [
            { type: 'text', text: customerName },
            { type: 'text', text: totalMealsSaved.toString() },
            { type: 'text', text: co2Saved }
          ]
        }
      ]
    });
  }

  // Send restaurant onboarding confirmation (for restaurant partners)
  async sendRestaurantOnboarding(
    phone: string,
    restaurantName: string,
    managerName: string,
    dashboardUrl: string
  ): Promise<WhatsAppResponse> {
    return this.sendTemplateMessage({
      to: phone,
      templateName: 'restaurant_onboarding',
      languageCode: 'en',
      components: [
        {
          type: 'body',
          parameters: [
            { type: 'text', text: managerName },
            { type: 'text', text: restaurantName },
            { type: 'text', text: dashboardUrl }
          ]
        }
      ]
    });
  }
}

// Factory function to create WhatsApp service
export function createWhatsAppService(): WhatsAppService | null {
  const accessToken = process.env.WHATSAPP_ACCESS_TOKEN;
  const phoneNumberId = process.env.WHATSAPP_BUSINESS_PHONE_ID;

  if (!accessToken || !phoneNumberId) {
    console.warn('WhatsApp credentials not configured. WhatsApp notifications will be disabled.');
    return null;
  }

  return new WhatsAppService(accessToken, phoneNumberId);
}

// WhatsApp template message examples for reference:
/*
Example templates you need to create in WhatsApp Business Manager:

1. reservation_confirmation:
"Hi {{1}}! 🎉 Your MealPeDeal mystery bag from *{{2}}* is confirmed!
📦 Pickup Code: *{{3}}*
⏰ Pickup Time: {{4}}
💰 Amount: {{5}}
📍 Address: {{6}}

Show this message when you arrive. Happy saving! 🌱"

2. pickup_reminder:
"{{1}}, your mystery bag from *{{2}}* is ready! ⏰ Pickup in {{3}}.
📦 Code: *{{4}}*
📍 {{5}}

Don't miss out on your delicious savings! 🍽️"

3. pickup_ready:
"{{1}}, your mystery bag from *{{2}}* is ready for pickup! 🎉
📦 Show code: *{{3}}*
📍 {{4}}
📞 Call: {{5}}

Happy eating! 🌟 #SaveFoodSaveEarth"

4. order_cancellation:
"Hi {{1}}, your MealPeDeal order from {{2}} has been cancelled due to {{4}}.
💰 Refund: {{3}} will be credited in 3-5 working days.
Sorry for the inconvenience! 🙏"

5. welcome_message_english:
"Welcome to MealPeDeal, {{1}}! 🌟
Save money, save food, save the planet! 🌱
Get mystery bags from top restaurants at 50-70% off.
Start exploring delicious deals near you! 🍽️"

6. welcome_message_hindi:
"MealPeDeal में आपका स्वागत है, {{1}}! 🌟
पैसे बचाएं, खाना बचाएं, धरती बचाएं! 🌱
टॉप रेस्टोरेंट से मिस्ट्री बैग 50-70% छूट पर पाएं।
अपने आस-पास के स्वादिष्ट डील एक्सप्लोर करना शुरू करें! 🍽️"
*/