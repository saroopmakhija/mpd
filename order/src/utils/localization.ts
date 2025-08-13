// Indian Localization Utilities for MealPeDeal

export interface IndianAddress {
  addressLine1: string;
  addressLine2?: string;
  landmark?: string;
  area: string;
  city: string;
  state: string;
  pincode: string;
  country: 'India' | 'IN';
}

// Indian currency formatting
export function formatINR(amount: number): string {
  // Format number in Indian numbering system with commas
  const formatted = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
  
  return formatted;
}

// Format amount in paise (for Razorpay)
export function toINRPaise(rupees: number): number {
  return Math.round(rupees * 100);
}

// Convert paise to rupees
export function fromINRPaise(paise: number): number {
  return paise / 100;
}

// Format Indian address for display
export function formatIndianAddress(address: IndianAddress): string {
  const parts = [
    address.addressLine1,
    address.addressLine2,
    address.landmark ? `Near ${address.landmark}` : null,
    address.area,
    `${address.city}, ${address.state}`,
    `PIN: ${address.pincode}`
  ].filter(Boolean);
  
  return parts.join(', ');
}

// Validate Indian PIN code
export function isValidPincode(pincode: string): boolean {
  return /^[1-9][0-9]{5}$/.test(pincode);
}

// Indian phone number validation
export function isValidIndianPhone(phone: string): boolean {
  // Matches: +91xxxxxxxxxx, 91xxxxxxxxxx, xxxxxxxxxx (10 digits)
  return /^(\+91|91)?[6-9]\d{9}$/.test(phone.replace(/\s+/g, ''));
}

// Format Indian phone number
export function formatIndianPhone(phone: string): string {
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.length === 10) {
    return `+91 ${cleaned.substring(0, 5)} ${cleaned.substring(5)}`;
  } else if (cleaned.length === 12 && cleaned.startsWith('91')) {
    const number = cleaned.substring(2);
    return `+91 ${number.substring(0, 5)} ${number.substring(5)}`;
  }
  
  return phone; // Return as-is if format is unclear
}

// Indian state list
export const INDIAN_STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
  'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
  'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
  'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
  'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
];

// Major Indian cities
export const MAJOR_INDIAN_CITIES = [
  'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Chennai',
  'Kolkata', 'Surat', 'Pune', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur',
  'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad',
  'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik',
  'Faridabad', 'Meerut', 'Rajkot', 'Kalyan-Dombivli', 'Vasai-Virar',
  'Varanasi', 'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar',
  'Navi Mumbai', 'Allahabad', 'Howrah', 'Ranchi', 'Gwalior'
];

// Popular Indian cuisines for mystery bags
export const INDIAN_CUISINES = [
  'North Indian', 'South Indian', 'Bengali', 'Gujarati', 'Punjabi',
  'Rajasthani', 'Maharashtrian', 'Tamil', 'Kerala', 'Hyderabadi',
  'Mughlai', 'Street Food', 'Chinese', 'Continental', 'Italian',
  'Fast Food', 'Bakery', 'Desserts', 'Beverages'
];

// Time zone utilities for India
export function getIndianTime(): Date {
  return new Date(new Date().toLocaleString("en-US", {timeZone: "Asia/Kolkata"}));
}

export function formatIndianDateTime(date: Date): string {
  return date.toLocaleString('en-IN', {
    timeZone: 'Asia/Kolkata',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  });
}

// GST calculation utilities
export function calculateGST(amount: number, gstRate: number = 5): { baseAmount: number; gstAmount: number; totalAmount: number } {
  const baseAmount = amount / (1 + gstRate / 100);
  const gstAmount = amount - baseAmount;
  
  return {
    baseAmount: Math.round(baseAmount * 100) / 100,
    gstAmount: Math.round(gstAmount * 100) / 100,
    totalAmount: amount
  };
}

// Common Indian food allergens
export const INDIAN_ALLERGENS = [
  'Dairy', 'Gluten', 'Nuts', 'Soy', 'Sesame', 'Eggs', 'Fish', 'Shellfish'
];

// Vegetarian symbols for Indian market
export const VEG_SYMBOLS = {
  VEGETARIAN: '🟢', // Green dot
  NON_VEGETARIAN: '🔴', // Red dot
  JAIN: '🟡', // Yellow dot
  VEGAN: '🌱' // Plant symbol
};