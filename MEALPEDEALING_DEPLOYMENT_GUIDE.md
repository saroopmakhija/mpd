# MealPeDeal - Complete Deployment Guide
## India's Premier Food Waste Reduction Platform

### 🌟 Overview

MealPeDeal is now fully optimized for the Indian market with comprehensive features including:

- **Mystery Bag System**: Complete Too Good To Go alternative with Indian dietary preferences
- **Indian Market Compliance**: GST, FSSAI, PAN integration for legal operations
- **Multi-language Support**: English and Hindi with WhatsApp/SMS notifications
- **Razorpay Integration**: Complete payment gateway with UPI, cards, wallets
- **Geolocation Services**: Google Maps integration for nearby restaurant discovery
- **Environmental Impact Tracking**: CO2 savings and gamification features
- **Comprehensive Review System**: Restaurant and mystery bag ratings

### 🏗️ Microservices Architecture

#### 1. **User Management Service** (Django + Python)
**Port: 8001**

**New Features:**
- Indian phone number verification with OTP
- Dietary preferences (Vegetarian, Jain, Vegan, Halal)
- Referral system with bonus rewards
- Environmental impact tracking per user
- Multi-language support (English/Hindi)
- Location-based nearby offers
- WhatsApp/SMS notification preferences

**Key Endpoints:**
```
POST /api/auth/register/ - Enhanced registration with dietary preferences
POST /api/auth/send-otp/ - Send phone verification OTP
POST /api/auth/verify-otp/ - Verify phone OTP
GET /api/users/me/ - Get current user profile
PATCH /api/users/update_dietary_preferences/ - Update food preferences
PATCH /api/users/update_location/ - Update location for nearby offers
GET /api/users/environmental_impact/ - Get sustainability metrics
POST /api/referrals/apply/ - Apply referral code
```

#### 2. **Restaurant Service** (FastAPI + Python)
**Port: 8002**

**New Features:**
- Indian compliance fields (GST, FSSAI, PAN, Trade License)
- Geolocation with city/state/PIN code
- Mystery bag configuration and pickup instructions
- Dietary options (Veg/Non-veg/Jain/Vegan/Halal)
- Cuisine types and regional food categories
- Environmental impact tracking per restaurant
- Verification system for trust building

**Key Endpoints:**
```
GET /restaurants/nearby/ - Find restaurants by location + dietary filters
PATCH /restaurants/{id}/compliance/ - Update Indian compliance info
PATCH /restaurants/{id}/mystery-bag-config/ - Configure mystery bag settings
GET /restaurants/{id}/environmental-impact/ - Restaurant sustainability metrics
PATCH /restaurants/{id}/verify/ - Verify restaurant for trust
GET /restaurants/analytics/top-performers/ - Top restaurants by metrics
```

#### 3. **Menu Service** (FastAPI + Python)
**Port: 8003**

**New Features:**
- **Mystery Bag Models**: Complete mystery bag system with Indian dietary filters
- **Enhanced Menu Items**: Spice levels, allergens, regional cuisine types
- **Mystery Bag Templates**: For recurring daily offers
- **Review Integration**: Mystery bag specific reviews
- Jain dietary restrictions support
- Nutritional information and health labels
- Cultural significance and regional origins

**New Models:**
- `MysteryBag`: Core mystery bag with Indian dietary preferences
- `MysteryBagReview`: Specific reviews for mystery bag experience
- `MysteryBagTemplate`: Templates for recurring offers

#### 4. **Order Service** (Node.js + TypeScript)
**Port: 3000**

**Enhanced Features:**
- **Razorpay Integration**: Complete Indian payment gateway
- **Pickup-only Model**: No delivery, only pickup for mystery bags
- **QR Code Pickup**: Contactless pickup verification
- **SMS/WhatsApp Notifications**: Indian market communication
- **Environmental Impact**: Track food waste saved per order
- Order status: RESERVED → READY → COLLECTED

**Key Features:**
- Mystery bag reservation and payment
- Pickup time slot management
- Indian phone number formats
- Webhook handling for payment confirmation
- Environmental impact calculation

#### 5. **Review Service** (FastAPI + Python)
**Port: 8004**

**New Features:**
- **Restaurant Reviews**: Indian market specific categories
- **Mystery Bag Reviews**: Surprise factor, value, freshness ratings
- **Multi-language Reviews**: English and Hindi support
- **Photo Reviews**: Visual feedback from customers
- **Restaurant Responses**: Public responses to reviews
- **Review Analytics**: Performance metrics for restaurants

**Key Models:**
- `RestaurantReview`: Comprehensive restaurant feedback
- `MysteryBagReview`: Mystery bag specific reviews
- `ReviewAnalytics`: Performance metrics and trends

### 🚀 Quick Start Deployment

#### Prerequisites
```bash
# System requirements
Node.js 18+ (for order service)
Python 3.9+ (for other services)
PostgreSQL 14+
Redis 6+
Docker & Docker Compose

# Indian Market Accounts Required
Razorpay account (KYC completed)
Google Cloud Platform (Maps API enabled)
SMS Provider (MSG91 recommended)
WhatsApp Business API (optional but recommended)
```

#### 1. Clone and Environment Setup
```bash
git clone <repository>
cd mealpedealing-backend

# Copy environment templates
cp order/env/.env.india.example order/env/.env.dev
cp user-management/.env.example user-management/.env
cp restaurant/.env.example restaurant/.env
cp menu/.env.example menu/.env
cp review/.env.example review/.env
```

#### 2. Configure Indian Market Integration

**Razorpay Configuration:**
```bash
# In order/env/.env.dev
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_secret_key
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
```

**SMS Configuration (MSG91 recommended):**
```bash
SMS_PROVIDER=msg91
MSG91_API_KEY=your_msg91_api_key
MSG91_SENDER_ID=MEALPE
```

**Google Maps Configuration:**
```bash
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

**WhatsApp Business API:**
```bash
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_BUSINESS_PHONE_ID=your_phone_number_id
```

#### 3. Database Setup
```bash
# Start PostgreSQL
docker run --name mealpedealing-postgres \
  -e POSTGRES_DB=mealpedealing_db \
  -e POSTGRES_USER=mealpedealing_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 -d postgres:14

# Run migrations for each service
cd order && npm run migrate:dev && cd ..
cd user-management && python manage.py migrate && cd ..
cd restaurant && alembic upgrade head && cd ..
cd menu && alembic upgrade head && cd ..
cd review && alembic upgrade head && cd ..
```

#### 4. Start Services
```bash
# Start Kafka for microservices communication
cd docker && docker-compose up -d && cd ..

# Install dependencies
cd order && npm install && cd ..
cd user-management && pip install -r requirements.txt && cd ..
cd restaurant && pip install -r requirements.txt && cd ..
cd menu && pip install -r requirements.txt && cd ..
cd review && pip install -r requirements.txt && cd ..

# Start each service (use separate terminals)
cd order && npm run start:dev
cd user-management && python manage.py runserver 8001
cd restaurant && python -m uvicorn main:app --reload --port 8002
cd menu && python -m uvicorn main:app --reload --port 8003
cd review && python -m uvicorn main:app --reload --port 8004
```

### 🇮🇳 Indian Market Features

#### Dietary Preferences Support
- **Vegetarian/Non-vegetarian**: Primary filter for Indian customers
- **Jain Dietary**: No root vegetables (onion, garlic, potato, etc.)
- **Vegan Options**: Plant-based alternatives
- **Halal Certification**: For Muslim customers
- **Allergen Information**: Nuts, dairy, gluten awareness

#### Payment Integration
- **UPI**: Google Pay, PhonePe, Paytm, BHIM
- **Cards**: Visa, Mastercard, RuPay
- **Net Banking**: All major Indian banks
- **Wallets**: Paytm, Amazon Pay, etc.

#### Compliance Features
- **GST Registration**: 15-character GST number validation
- **FSSAI License**: 14-digit food license validation
- **PAN Card**: Income tax compliance
- **Trade License**: Local authority permissions

#### Communication
- **SMS Notifications**: MSG91/TextLocal integration
- **WhatsApp Business**: Rich media messages
- **Multi-language**: English and Hindi support
- **Phone Verification**: OTP-based verification

### 📱 API Integration Examples

#### Customer Registration
```javascript
POST /api/auth/register/
{
  "email": "customer@example.com",
  "password": "securepassword",
  "first_name": "Raj",
  "last_name": "Sharma",
  "phone": "+919876543210",
  "preferred_language": "en",
  "is_vegetarian": true,
  "is_jain": false,
  "spice_preference": "MEDIUM",
  "pincode": "110001"
}
```

#### Mystery Bag Search
```javascript
GET /offers/nearby?lat=28.6139&lng=77.2090&veg=true&spiceLevel=MILD&maxPrice=200&foodCategory=LUNCH
```

#### Mystery Bag Reservation
```javascript
POST /api/orders/mystery-bag-reservation
{
  "offerId": 123,
  "quantity": 1,
  "customerPhone": "+919876543210",
  "paymentMethod": "upi"
}
```

### 🌱 Environmental Impact Features

#### For Customers
- Track meals saved and money saved
- CO2 emissions reduced calculation
- Equivalent trees planted metric
- City-wise leaderboard ranking

#### For Restaurants
- Total mystery bags sold
- Food waste saved in kg
- Environmental impact summary
- Sustainability badges

### 📊 Analytics and Insights

#### Restaurant Dashboard
- Daily mystery bag performance
- Customer dietary preference trends
- Peak hour analysis for offers
- Environmental impact metrics
- Review sentiment analysis

#### Customer Insights
- Favorite cuisine discovery
- Money saved over time
- Environmental contribution
- Referral program benefits

### 🔒 Security and Compliance

#### Data Protection
- Personal Data Protection Bill compliance
- Secure payment processing via Razorpay
- OTP-based phone verification
- JWT token authentication

#### Legal Compliance
- GST calculation and invoicing
- FSSAI compliance verification
- Digital payment receipts
- TDS handling for restaurants

### 🚀 Production Deployment

#### Recommended Infrastructure (AWS Mumbai)
```bash
# Application Servers
2x t3.medium EC2 instances (HA setup)

# Database
RDS PostgreSQL db.t3.medium

# Cache
ElastiCache Redis cache.t3.micro

# Load Balancer
Application Load Balancer with SSL

# Storage
S3 buckets for images and backups
```

#### Environment Variables (Production)
```bash
# Security
JWT_SECRET=your_strong_jwt_secret_32_chars_min
ENCRYPTION_KEY=your_32_character_encryption_key

# Database
DATABASE_URL=postgresql://username:password@prod-rds:5432/mealpedealing

# Monitoring
SENTRY_DSN=your_sentry_dsn
```

### 📞 Support and Maintenance

#### Health Check Endpoints
```bash
GET /api/health - Application health
GET /api/health/db - Database connectivity
GET /api/health/redis - Cache connectivity
```

#### Monitoring
- Application metrics: Prometheus + Grafana
- Error tracking: Sentry
- Log aggregation: ELK Stack

### 🎯 Next Steps

1. **Pilot Launch**: Start with 10-15 restaurants in one city
2. **Customer Acquisition**: Launch referral campaigns
3. **Marketing**: Focus on environmental consciousness
4. **Expansion**: Scale to nearby cities based on success
5. **Mobile Apps**: Develop iOS/Android applications

### 📧 Contact Information

- **Technical Support**: tech@mealpedealing.com
- **Business Queries**: business@mealpedealing.com
- **Restaurant Partners**: partners@mealpedealing.com

---

**MealPeDeal - Save Money, Save Food, Save Earth! 🌱**

*Transforming India's fight against food waste, one mystery bag at a time.*