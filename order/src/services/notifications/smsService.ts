// SMS Service for Indian Market - MealPeDeal
import axios from 'axios';
import { formatIndianPhone } from '../../utils/localization';

export interface SMSMessage {
  to: string;
  message: string;
  template?: string;
  variables?: Record<string, string>;
}

export interface SMSResponse {
  success: boolean;
  messageId?: string;
  error?: string;
}

export abstract class BaseSMSProvider {
  abstract sendSMS(message: SMSMessage): Promise<SMSResponse>;
}

// MSG91 - Popular Indian SMS provider
export class MSG91Provider extends BaseSMSProvider {
  private apiKey: string;
  private senderId: string;

  constructor(apiKey: string, senderId: string = 'MEALPE') {
    super();
    this.apiKey = apiKey;
    this.senderId = senderId;
  }

  async sendSMS(message: SMSMessage): Promise<SMSResponse> {
    try {
      const phone = formatIndianPhone(message.to).replace(/\D/g, ''); // Remove all non-digits
      
      const response = await axios.post('https://api.msg91.com/api/v5/flow/', {
        flow_id: message.template || 'default',
        sender: this.senderId,
        mobiles: `91${phone.substring(phone.length - 10)}`, // Ensure 10 digits with country code
        VAR1: message.variables?.customerName || '',
        VAR2: message.variables?.orderCode || '',
        VAR3: message.variables?.restaurantName || '',
        VAR4: message.variables?.amount || '',
        VAR5: message.variables?.time || '',
      }, {
        headers: {
          'authkey': this.apiKey,
          'Content-Type': 'application/json'
        }
      });

      return {
        success: response.data.type === 'success',
        messageId: response.data.message,
        error: response.data.type !== 'success' ? response.data.message : undefined
      };
    } catch (error) {
      return {
        success: false,
        error: (error as Error).message
      };
    }
  }
}

// TextLocal - Another popular Indian SMS provider
export class TextLocalProvider extends BaseSMSProvider {
  private apiKey: string;
  private sender: string;

  constructor(apiKey: string, sender: string = 'MEALPE') {
    super();
    this.apiKey = apiKey;
    this.sender = sender;
  }

  async sendSMS(message: SMSMessage): Promise<SMSResponse> {
    try {
      const phone = formatIndianPhone(message.to).replace(/\D/g, '');
      
      const params = new URLSearchParams({
        apikey: this.apiKey,
        numbers: `91${phone.substring(phone.length - 10)}`,
        message: message.message,
        sender: this.sender
      });

      const response = await axios.post('https://api.textlocal.in/send/', params);

      return {
        success: response.data.status === 'success',
        messageId: response.data.messages?.[0]?.id,
        error: response.data.status !== 'success' ? response.data.errors?.[0]?.message : undefined
      };
    } catch (error) {
      return {
        success: false,
        error: (error as Error).message
      };
    }
  }
}

// Twilio - International provider (backup option)
export class TwilioProvider extends BaseSMSProvider {
  private accountSid: string;
  private authToken: string;
  private phoneNumber: string;

  constructor(accountSid: string, authToken: string, phoneNumber: string) {
    super();
    this.accountSid = accountSid;
    this.authToken = authToken;
    this.phoneNumber = phoneNumber;
  }

  async sendSMS(message: SMSMessage): Promise<SMSResponse> {
    try {
      const phone = formatIndianPhone(message.to);
      
      const auth = Buffer.from(`${this.accountSid}:${this.authToken}`).toString('base64');
      
      const response = await axios.post(
        `https://api.twilio.com/2010-04-01/Accounts/${this.accountSid}/Messages.json`,
        new URLSearchParams({
          From: this.phoneNumber,
          To: phone,
          Body: message.message
        }),
        {
          headers: {
            'Authorization': `Basic ${auth}`,
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );

      return {
        success: true,
        messageId: response.data.sid
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || error.message
      };
    }
  }
}

// SMS Service class to manage providers
export class SMSService {
  private provider: BaseSMSProvider;

  constructor(provider: BaseSMSProvider) {
    this.provider = provider;
  }

  // Send mystery bag reservation confirmation
  async sendReservationConfirmation(
    phone: string,
    customerName: string,
    restaurantName: string,
    pickupCode: string,
    pickupTime: string,
    amount: number
  ): Promise<SMSResponse> {
    const message = `Hi ${customerName}! Your MealPeDeal mystery bag from ${restaurantName} is confirmed. Pickup code: ${pickupCode}. Pickup time: ${pickupTime}. Amount: ₹${amount}. Show this SMS at pickup.`;
    
    return this.provider.sendSMS({
      to: phone,
      message,
      template: 'reservation_confirmation',
      variables: {
        customerName,
        restaurantName,
        orderCode: pickupCode,
        time: pickupTime,
        amount: amount.toString()
      }
    });
  }

  // Send pickup reminder
  async sendPickupReminder(
    phone: string,
    customerName: string,
    restaurantName: string,
    pickupCode: string,
    timeRemaining: string
  ): Promise<SMSResponse> {
    const message = `${customerName}, your MealPeDeal bag from ${restaurantName} is ready! Pickup in ${timeRemaining}. Code: ${pickupCode}. Address & directions: bit.ly/mealpe-${pickupCode}`;
    
    return this.provider.sendSMS({
      to: phone,
      message,
      template: 'pickup_reminder',
      variables: {
        customerName,
        restaurantName,
        orderCode: pickupCode,
        time: timeRemaining
      }
    });
  }

  // Send pickup ready notification
  async sendPickupReady(
    phone: string,
    customerName: string,
    restaurantName: string,
    pickupCode: string
  ): Promise<SMSResponse> {
    const message = `${customerName}, your mystery bag from ${restaurantName} is ready for pickup! Show code ${pickupCode} to collect. Happy eating! - MealPeDeal`;
    
    return this.provider.sendSMS({
      to: phone,
      message,
      template: 'pickup_ready',
      variables: {
        customerName,
        restaurantName,
        orderCode: pickupCode
      }
    });
  }

  // Send cancellation notification
  async sendCancellationNotification(
    phone: string,
    customerName: string,
    restaurantName: string,
    refundAmount: number
  ): Promise<SMSResponse> {
    const message = `${customerName}, your MealPeDeal order from ${restaurantName} has been cancelled. Refund of ₹${refundAmount} will be credited in 3-5 working days. Thank you!`;
    
    return this.provider.sendSMS({
      to: phone,
      message,
      template: 'cancellation',
      variables: {
        customerName,
        restaurantName,
        amount: refundAmount.toString()
      }
    });
  }
}

// Factory function to create SMS service based on environment
export function createSMSService(): SMSService {
  const provider = process.env.SMS_PROVIDER || 'msg91';
  
  switch (provider.toLowerCase()) {
    case 'msg91':
      if (!process.env.MSG91_API_KEY) {
        throw new Error('MSG91_API_KEY is required for MSG91 SMS provider');
      }
      return new SMSService(new MSG91Provider(
        process.env.MSG91_API_KEY,
        process.env.MSG91_SENDER_ID || 'MEALPE'
      ));
      
    case 'textlocal':
      if (!process.env.TEXTLOCAL_API_KEY) {
        throw new Error('TEXTLOCAL_API_KEY is required for TextLocal SMS provider');
      }
      return new SMSService(new TextLocalProvider(
        process.env.TEXTLOCAL_API_KEY,
        process.env.TEXTLOCAL_SENDER || 'MEALPE'
      ));
      
    case 'twilio':
      if (!process.env.TWILIO_ACCOUNT_SID || !process.env.TWILIO_AUTH_TOKEN || !process.env.TWILIO_PHONE_NUMBER) {
        throw new Error('TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER are required for Twilio');
      }
      return new SMSService(new TwilioProvider(
        process.env.TWILIO_ACCOUNT_SID,
        process.env.TWILIO_AUTH_TOKEN,
        process.env.TWILIO_PHONE_NUMBER
      ));
      
    default:
      throw new Error(`Unsupported SMS provider: ${provider}`);
  }
}