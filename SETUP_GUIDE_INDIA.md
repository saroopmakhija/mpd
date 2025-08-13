# MealPeDeal India Setup Guide

This guide will help you set up **MealPeDeal** - India's premier food waste reduction platform, modeled after Too Good To Go but optimized for the Indian market.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Indian Market Integrations](#indian-market-integrations)
4. [Database Configuration](#database-configuration)
5. [API Configuration](#api-configuration)
6. [Payment Gateway Setup](#payment-gateway-setup)
7. [Notification Services](#notification-services)
8. [Production Deployment](#production-deployment)
9. [Indian Compliance](#indian-compliance)
10. [Testing](#testing)

## Prerequisites

### System Requirements

- Node.js 18+ (LTS recommended)
- Python 3.9+
- PostgreSQL 14+
- Redis 6+ (for caching)
- Docker & Docker Compose (optional)

### Indian Market Accounts

1. **Razorpay Account** (Payment Gateway)
   - Sign up at [dashboard.razorpay.com](https://dashboard.razorpay.com)
   - Complete KYC verification
   - Get API keys for live/test mode

2. **Google Cloud Platform** (Maps API)
   - Create project at [console.cloud.google.com](https://console.cloud.google.com)
   - Enable Maps JavaScript API, Geocoding API, Distance Matrix API
   - Generate API key with IP/domain restrictions

3. **SMS Provider** (Choose one)
   - **MSG91**: Indian SMS provider - [msg91.com](https://msg91.com)
   - **TextLocal**: Alternative Indian provider - [textlocal.in](https://textlocal.in)
   - **Twilio**: International backup - [twilio.com](https://twilio.com)

4. **WhatsApp Business API** (Recommended)
   - Apply at [business.whatsapp.com](https://business.whatsapp.com)
   - Complete Facebook Business verification
   - Set up webhook endpoints

## Local Development Setup

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone https://github.com/your-org/mealpedealing-backend.git
cd mealpedealing-backend

# Install dependencies for each service
cd order && npm install && cd ..
cd user-management && pip install -r requirements.txt && cd ..
cd restaurant && pip install -r requirements.txt && cd ..
cd menu && pip install -r requirements.txt && cd ..
```

### 2. Environment Configuration

```bash
# Copy example environment files
cp order/env/.env.india.example order/env/.env.dev
cp user-management/.env.example user-management/.env
cp restaurant/.env.example restaurant/.env
cp menu/.env.example menu/.env

# Edit each .env file with your credentials
```

### 3. Database Setup

```bash
# Start PostgreSQL (local or Docker)
docker run --name mealpedealing-postgres \
  -e POSTGRES_DB=mealpedealing_db \
  -e POSTGRES_USER=mealpedealing_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 -d postgres:14

# Run database migrations
cd order && npm run migrate:dev && cd ..
```

### 4. Start Development Services

```bash
# Start Kafka (required for microservices communication)
cd docker && docker-compose up -d && cd ..

# Start each microservice in separate terminals
cd order && npm run start:dev
cd user-management && python -m uvicorn main:app --reload --port 8001
cd restaurant && python -m uvicorn main:app --reload --port 8002
cd menu && python -m uvicorn main:app --reload --port 8003
```

## Indian Market Integrations

### Razorpay Payment Gateway

1. **Test Credentials Setup**
```bash
# In order/env/.env.dev
RAZORPAY_KEY_ID=rzp_test_your_test_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
```

2. **Webhook Configuration**
```bash
# Razorpay webhook URL (for local testing use ngrok)
ngrok http 3000
# Add webhook URL: https://your-ngrok-url.ngrok.io/webhooks/razorpay
```

3. **Supported Payment Methods**
   - UPI (GPay, PhonePe, Paytm, BHIM)
   - Credit/Debit Cards (Visa, Mastercard, RuPay)
   - Net Banking (All major Indian banks)
   - Digital Wallets (Paytm, Amazon Pay)

### Google Maps Integration

1. **API Key Setup**
```bash
# In order/env/.env.dev
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

2. **API Restrictions** (Recommended)
   - Restrict by IP addresses for server keys
   - Restrict by HTTP referrers for client keys
   - Enable only required APIs

3. **Indian Optimization**
   - Region biasing set to 'in'
   - Language preference: English with Hindi fallback
   - Support for Indian address formats

## Database Configuration

### Mystery Bag Schema Updates

The database has been updated for Indian market requirements:

```sql
-- New Indian-specific fields in surprise_bag_offers
ALTER TABLE surprise_bag_offers ADD COLUMN is_jain BOOLEAN;
ALTER TABLE surprise_bag_offers ADD COLUMN is_vegan BOOLEAN;
ALTER TABLE surprise_bag_offers ADD COLUMN contains_alcohol BOOLEAN;
ALTER TABLE surprise_bag_offers ADD COLUMN spice_level VARCHAR(20);
ALTER TABLE surprise_bag_offers ADD COLUMN food_category VARCHAR(50);
ALTER TABLE surprise_bag_offers ADD COLUMN discount_percentage INTEGER;

-- Restaurant compliance fields
ALTER TABLE restaurants ADD COLUMN gst_number VARCHAR(15);
ALTER TABLE restaurants ADD COLUMN fssai_license VARCHAR(14);
ALTER TABLE restaurants ADD COLUMN pickup_instructions TEXT;
ALTER TABLE restaurants ADD COLUMN contact_phone VARCHAR(15);
```

### Run Migrations

```bash
cd order
npm run migrate:dev  # Development
npm run migrate:prod # Production
```

## API Configuration

### Indian Market Endpoints

New endpoints specifically for Indian market:

#### Mystery Bags
```bash
# Get vegetarian-only offers
GET /api/offers/vegetarian

# Get offers by meal category
GET /api/offers/category/{BREAKFAST|LUNCH|DINNER|SNACKS|SWEETS|BEVERAGES}

# Search with Indian filters
GET /api/offers/nearby?lat=28.6139&lng=77.2090&veg=true&isJain=true&spiceLevel=MILD&maxPrice=200
```

#### Payment
```bash
# Razorpay webhook
POST /api/webhooks/razorpay

# Create mystery bag reservation with Razorpay
POST /api/orders/mystery-bag-reservation
```

## Payment Gateway Setup

### Razorpay Integration

1. **Create Razorpay Orders**
```javascript
// Example: Reserve mystery bag
const order = await razorpay.orders.create({
  amount: Math.round(bagPrice * 100), // Amount in paise
  currency: 'INR',
  receipt: `mysteryBag_${offerId}_${Date.now()}`,
  notes: {
    customer_id: customerId,
    offer_id: offerId,
    type: 'mystery_bag'
  }
});
```

2. **Webhook Handling**
- Payment captured → Order status: RESERVED
- Payment failed → Order cancelled, inventory restored
- Auto-refunds for cancellations

3. **Indian Compliance**
- GST calculation (5% for food services)
- TDS handling for restaurant partners
- Digital payment receipts

## Notification Services

### SMS Integration

Choose one provider:

**Option 1: MSG91 (Recommended for India)**
```bash
SMS_PROVIDER=msg91
MSG91_API_KEY=your_msg91_api_key
MSG91_SENDER_ID=MEALPE
```

**Option 2: TextLocal**
```bash
SMS_PROVIDER=textlocal
TEXTLOCAL_API_KEY=your_textlocal_api_key
TEXTLOCAL_SENDER=MEALPE
```

### WhatsApp Business Integration

1. **Setup WhatsApp Business Account**
   - Complete Facebook Business verification
   - Add phone number to WhatsApp Business
   - Create message templates

2. **Required Templates**
   - `reservation_confirmation`
   - `pickup_reminder`
   - `pickup_ready`
   - `order_cancellation`
   - `welcome_message_english`
   - `welcome_message_hindi`

3. **Configuration**
```bash
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_BUSINESS_PHONE_ID=your_phone_number_id
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_verify_token
```

## Production Deployment

### 1. Cloud Infrastructure (Recommended: AWS Mumbai Region)

```bash
# EC2 instances
- Application servers: t3.medium (2 instances for HA)
- Database: RDS PostgreSQL db.t3.medium
- Cache: ElastiCache Redis cache.t3.micro
- Load Balancer: Application Load Balancer

# S3 buckets
- mealpedealing-images (restaurant/bag photos)
- mealpedealing-backups (database backups)
```

### 2. Environment Variables

```bash
# Production environment
NODE_ENV=production
DATABASE_URL=postgresql://username:password@prod-rds-endpoint:5432/mealpedealing_prod

# Security
JWT_SECRET=your_strong_jwt_secret_32_chars_min
ENCRYPTION_KEY=your_32_character_encryption_key

# Monitoring
SENTRY_DSN=your_sentry_dsn
GRAYLOG_HOST=your_graylog_endpoint
```

### 3. SSL/TLS Setup

```bash
# Use Let's Encrypt with Nginx
sudo certbot --nginx -d api.mealpedealing.com -d app.mealpedealing.com
```

### 4. Monitoring Setup

```bash
# Health check endpoints
GET /api/health
GET /api/health/db
GET /api/health/redis

# Metrics collection
- Application metrics: Prometheus + Grafana
- Error tracking: Sentry
- Log aggregation: ELK Stack or Graylog
```

## Indian Compliance

### 1. Legal Requirements

- **GST Registration**: Required for marketplace operations
- **FSSAI License**: Food safety compliance
- **Digital India**: Compliance with IT Act 2000
- **RBI Guidelines**: Payment aggregator compliance

### 2. Data Protection

- **Personal Data Protection Bill**: Implement data minimization
- **Payment Card Industry (PCI)**: DSS compliance via Razorpay
- **Customer consent**: Clear opt-in for notifications

### 3. Restaurant Partner Compliance

```javascript
// Validate restaurant documents
const requiredDocs = [
  'fssaiLicense',    // FSSAI registration
  'gstNumber',       // GST registration
  'panCard',         // PAN card
  'bankAccount'      // Bank account details
];
```

## Testing

### 1. Unit Tests

```bash
cd order && npm test
cd user-management && python -m pytest
cd restaurant && python -m pytest
cd menu && python -m pytest
```

### 2. Integration Tests

```bash
# Test payment flow with Razorpay test cards
curl -X POST http://localhost:3000/api/orders/mystery-bag-reservation \
  -H "Content-Type: application/json" \
  -d '{
    "offerId": 1,
    "quantity": 1,
    "customerPhone": "+91-9876543210"
  }'
```

### 3. Indian Market Testing

- **Payment Methods**: Test UPI, cards, net banking, wallets
- **Phone Numbers**: Use Indian phone number formats
- **Addresses**: Test with Indian address formats and PIN codes
- **Languages**: Test Hindi/English content
- **Time Zones**: Verify IST (Asia/Kolkata) handling

### 4. Load Testing

```bash
# Use artillery.js for load testing
artillery run --target http://localhost:3000 test-scenarios.yml
```

## Post-Deployment Checklist

### 1. Restaurant Onboarding

- [ ] Create restaurant partner application form
- [ ] Document verification process
- [ ] Training materials for mystery bag creation
- [ ] Pickup process guidelines

### 2. Customer Acquisition

- [ ] Referral program setup
- [ ] Social media integration
- [ ] App store submissions (iOS/Android)
- [ ] Marketing campaigns for Indian market

### 3. Operations

- [ ] Customer support setup (Hindi/English)
- [ ] Restaurant support helpline
- [ ] Daily monitoring dashboards
- [ ] Backup and disaster recovery procedures

### 4. Legal and Compliance

- [ ] Terms of service (India-specific)
- [ ] Privacy policy (PDPB compliant)
- [ ] Refund and cancellation policy
- [ ] Restaurant partner agreements

## Troubleshooting

### Common Issues

1. **Razorpay Webhook Failures**
   - Check webhook URL accessibility
   - Verify signature validation
   - Monitor webhook logs

2. **SMS Delivery Issues**
   - Verify sender ID approval
   - Check DND preferences
   - Monitor delivery reports

3. **Google Maps API Errors**
   - Check API key restrictions
   - Verify billing account
   - Monitor quota usage

4. **Database Performance**
   - Add indexes for Indian city/state queries
   - Optimize geospatial queries
   - Monitor connection pools

### Support Contacts

- **Technical Support**: tech@mealpedealing.com
- **Business Queries**: business@mealpedealing.com
- **Restaurant Partners**: partners@mealpedealing.com

---

## Next Steps

After successful setup:

1. **Pilot Launch**: Start with 10-15 restaurants in one city
2. **Customer Feedback**: Collect and iterate on user experience
3. **Scale Gradually**: Expand to nearby areas
4. **Marketing Campaign**: Launch awareness campaigns
5. **Feature Enhancement**: Add reviews, loyalty programs, etc.

For additional support or customization requests, please contact our development team.

---

*MealPeDeal - Save Money, Save Food, Save Earth! 🌱*