# MealPeDeal MVP Development Checklist

## Overview
This checklist outlines the minimum viable product (MVP) requirements to transform the existing food delivery backend into a Too Good To Go clone for the Indian market. Focus is on core functionality to get to market quickly.

## Phase 1: Core Infrastructure Changes

### 1.1 Database Schema Updates
- [ ] **Update Prisma Schema** (`order/prisma/schema.prisma`)
  - [ ] Add `MysteryBag` model with basic fields:
    - `id`, `restaurantId`, `name`, `description`
    - `originalValue`, `salePrice`, `availableQuantity`
    - `pickupTimeStart`, `pickupTimeEnd`, `isActive`
    - `createdAt`, `updatedAt`
  - [ ] Add `BagReservation` model:
    - `id`, `customerId`, `mysteryBagId`, `reservedAt`
    - `pickupSlot`, `status` (RESERVED, PICKED_UP, CANCELLED, NO_SHOW)
  - [ ] Modify `Order` model:
    - Add `mysteryBagId` field (optional)
    - Add `pickupConfirmedAt` field
    - Remove delivery-related fields for bag orders
  - [ ] Update `Restaurant` model:
    - Add `mysteryBagEnabled` boolean
    - Add `pickupInstructions` text field
  - [ ] Run database migration

### 1.2 Remove Delivery System
- [ ] **Remove Courier Functionality**
  - [ ] Remove courier role from user management service
  - [ ] Remove delivery-related APIs from order service
  - [ ] Remove courier authentication flows
  - [ ] Update role-based permissions

### 1.3 Environment Configuration
- [ ] **Update Environment Variables** (`.env`)
  - [ ] Update database connection strings for new schema
  - [ ] Add mystery bag configuration variables:
    - `MYSTERY_BAG_DEFAULT_DISCOUNT_PERCENT=67`
    - `PICKUP_WINDOW_HOURS=2`
    - `MAX_BAGS_PER_RESTAURANT=50`
  - [ ] Add Indian payment gateway credentials:
    - `RAZORPAY_KEY_ID=your_key_id`
    - `RAZORPAY_KEY_SECRET=your_secret`
    - `PAYU_MERCHANT_KEY=your_merchant_key`
    - `PAYU_SALT=your_salt`
  - [ ] Add Indian localization settings:
    - `DEFAULT_CURRENCY=INR`
    - `DEFAULT_TIMEZONE=Asia/Kolkata`
    - `GST_RATE=5` (for food service)

## Phase 2: Core Mystery Bag System

### 2.1 Mystery Bag Management APIs
- [ ] **Create Mystery Bag Service** (`order/src/modules/mysteryBags/`)
  - [ ] `models/mysteryBag.models.ts`
  - [ ] `repositories/mysteryBag.repository.ts`
  - [ ] `services/mysteryBag.service.ts`
  - [ ] `controllers/mysteryBag.controller.ts`
  - [ ] `routes/mysteryBag.routes.ts`

- [ ] **Core API Endpoints**
  - [ ] `GET /api/mystery-bags` - List available bags (with basic filtering)
  - [ ] `GET /api/mystery-bags/:id` - Get bag details
  - [ ] `POST /api/mystery-bags` - Restaurant creates bag
  - [ ] `PUT /api/mystery-bags/:id` - Update bag
  - [ ] `DELETE /api/mystery-bags/:id` - Remove bag
  - [ ] `POST /api/mystery-bags/:id/reserve` - Customer reserves bag
  - [ ] `PATCH /api/mystery-bags/:id/pickup` - Confirm pickup

### 2.2 Restaurant Mystery Bag Management
- [ ] **Restaurant Dashboard APIs**
  - [ ] `GET /api/restaurants/current/mystery-bags` - List restaurant's bags
  - [ ] `GET /api/restaurants/current/reservations` - View reservations
  - [ ] `POST /api/restaurants/current/mystery-bags/bulk-create` - Quick bag creation

### 2.3 Customer Experience
- [ ] **Customer APIs**
  - [ ] `GET /api/customers/current/reservations` - My reservations
  - [ ] `GET /api/customers/current/pickup-history` - Past pickups
  - [ ] `PATCH /api/reservations/:id/cancel` - Cancel reservation

## Phase 3: Basic Discovery & Search

### 3.1 Simple Search Functionality
- [ ] **Search APIs** (basic, no geolocation initially)
  - [ ] `GET /api/mystery-bags/search?restaurant_name=X&available=true`
  - [ ] `GET /api/restaurants/search?has_mystery_bags=true`
  - [ ] Add basic filtering by:
    - Restaurant name
    - Bag availability
    - Price range
    - Pickup time

### 3.2 Restaurant Listing Updates
- [ ] **Update Restaurant APIs**
  - [ ] Modify restaurant listing to show mystery bag availability
  - [ ] Add pickup instructions display
  - [ ] Show current available bags count

## Phase 4: Order Flow Modification

### 4.1 Update Order System
- [ ] **Modify Order Service** (`order/src/modules/orders/`)
  - [ ] Update order creation for mystery bags
  - [ ] Remove delivery logic for bag orders
  - [ ] Add pickup time slot validation
  - [ ] Implement pickup confirmation workflow

### 4.2 Payment Integration (Indian Market Focus)
- [ ] **Integrate Indian Payment Methods**
  - [ ] **UPI Integration** (Primary for Indian market)
    - [ ] Add Razorpay/PayU integration for UPI payments
    - [ ] Support major UPI apps (GPay, PhonePe, Paytm, BHIM)
    - [ ] UPI QR code generation for quick payments
  - [ ] **Credit/Debit Cards**
    - [ ] RuPay card support (Indian domestic)
    - [ ] Visa/Mastercard support
    - [ ] EMI options for higher-value orders
  - [ ] **Digital Wallets**
    - [ ] Paytm Wallet integration
    - [ ] Amazon Pay integration
    - [ ] PhonePe wallet support
  - [ ] **Net Banking**
    - [ ] Major Indian banks (SBI, HDFC, ICICI, Axis, etc.)
    - [ ] Regional bank support
- [ ] **Update Payment Flow**
  - [ ] Replace/supplement Stripe with Indian payment gateway (Razorpay/PayU)
  - [ ] Add pre-authorization for no-show protection
  - [ ] Update pricing calculation for discounted bags
  - [ ] Currency conversion to INR
  - [ ] GST calculation and invoice generation
  - [ ] Refund processing for Indian payment methods

## Phase 5: Basic Authentication & Authorization

### 5.1 User Role Updates
- [ ] **Update User Management Service**
  - [ ] Remove courier role completely
  - [ ] Update customer model with basic mystery bag preferences
  - [ ] Update restaurant manager permissions for bag management

### 5.2 Permission System
- [ ] **Update Authorization**
  - [ ] Restaurant managers can create/manage mystery bags
  - [ ] Customers can reserve and pickup bags
  - [ ] Remove all courier-related permissions

## Phase 6: Basic UI/UX Requirements

### 6.1 Essential Frontend Updates
- [ ] **Customer Interface**
  - [ ] Mystery bag listing page
  - [ ] Bag detail page with pickup instructions
  - [ ] Reservation confirmation page
  - [ ] Basic pickup history

- [ ] **Restaurant Interface**
  - [ ] Simple bag creation form
  - [ ] Reservation management dashboard
  - [ ] Basic pickup queue view

### 6.2 Mobile Considerations (Indian Market Focus)
- [ ] **Responsive Design**
  - [ ] Ensure mobile-friendly mystery bag browsing
  - [ ] Simple pickup confirmation flow
  - [ ] Basic navigation to restaurant location
- [ ] **Indian UX Patterns**
  - [ ] UPI payment flow optimized for mobile
  - [ ] Support for regional languages (Hindi + local languages)
  - [ ] WhatsApp integration for order updates
  - [ ] SMS notifications for users without smartphones

## Phase 7: Basic Notifications

### 7.1 Essential Notifications (Indian Market Focus)
- [ ] **Multi-Channel Notifications**
  - [ ] **Email Notifications**
    - [ ] Reservation confirmation with GST invoice
    - [ ] Pickup reminders (1 hour before)
    - [ ] Bag ready for pickup
    - [ ] Reservation cancellation with refund details
  - [ ] **SMS Notifications** (Critical for Indian market)
    - [ ] Reservation confirmation SMS
    - [ ] Pickup time reminders
    - [ ] Payment confirmation SMS
  - [ ] **WhatsApp Integration** (Preferred in India)
    - [ ] Order status updates via WhatsApp Business API
    - [ ] Pickup instructions and restaurant contact
    - [ ] Payment receipts and invoices

### 7.2 Restaurant Notifications
- [ ] **Restaurant Alerts**
  - [ ] New reservation notification (SMS + Email)
  - [ ] No-show alerts
  - [ ] Daily summary with GST reports
  - [ ] Payment settlement notifications

## Phase 8: Quality Assurance & Testing

### 8.1 Core Testing
- [ ] **Unit Tests**
  - [ ] Mystery bag service tests
  - [ ] Reservation workflow tests
  - [ ] Indian payment integration tests (UPI, Cards, Wallets)
  - [ ] GST calculation tests
  - [ ] Currency formatting tests (INR)

### 8.2 Integration Testing
- [ ] **End-to-End Testing**
  - [ ] Complete customer journey (browse → reserve → pickup)
  - [ ] Restaurant bag creation workflow
  - [ ] Payment and cancellation flows with Indian gateways
  - [ ] Multi-language support testing
  - [ ] SMS/WhatsApp notification delivery
  - [ ] Mobile responsiveness across devices

## Phase 9: Production Deployment

### 9.1 Infrastructure Setup
- [ ] **Production Environment**
  - [ ] Database migration scripts
  - [ ] Environment variable configuration for Indian services
  - [ ] Payment gateway sandbox → production migration
  - [ ] SMS/WhatsApp API credentials setup
  - [ ] CDN setup for Indian geography
  - [ ] Basic monitoring setup

### 9.2 Launch Preparation
- [ ] **Go-Live Checklist**
  - [ ] Partner restaurant onboarding process (India-specific)
  - [ ] Customer acquisition strategy for Indian market
  - [ ] Multi-language support documentation
  - [ ] Customer support in Hindi/English
  - [ ] Error monitoring and logging
  - [ ] Compliance with Indian data protection laws
  - [ ] GST registration and tax compliance

## Post-MVP Features (Future Releases)

### Not Required for MVP Launch
- ❌ ML-based content recommendation
- ❌ Advanced geolocation with maps
- ❌ Sustainability metrics and gamification
- ❌ Complex pickup time optimization
- ❌ Advanced analytics dashboard
- ❌ Push notifications
- ❌ Social features and community challenges
- ❌ Carbon footprint tracking
- ❌ Advanced search filters

## Success Metrics for MVP

### Key Performance Indicators
- [ ] **Technical Metrics**
  - [ ] 99% uptime for core APIs
  - [ ] < 2 second response time for bag listing
  - [ ] Zero payment processing errors

- [ ] **Business Metrics**
  - [ ] 10+ restaurant partners at launch
  - [ ] 100+ successful bag pickups in first month
  - [ ] < 20% no-show rate
  - [ ] Positive customer feedback (4+ stars)

## Estimated Timeline
- **Phase 1-2**: 4-6 weeks (Core infrastructure + Mystery bag system)
- **Phase 3-4**: 3-4 weeks (Search + Order flow)
- **Phase 5-6**: 2-3 weeks (Auth + Basic UI)
- **Phase 7-9**: 2-3 weeks (Notifications + Deployment)

**Total MVP Timeline: 11-16 weeks**

## Team Assignment Recommendations
- **Backend Developer**: Phases 1-5, 7 (Focus on payment gateway integration)
- **Frontend Developer**: Phase 6 (Multi-language UI, mobile-first design)
- **DevOps Engineer**: Phases 1, 9 (Indian cloud providers, compliance)
- **QA Engineer**: Phase 8 (Payment testing, regional testing)
- **Product Manager**: All phases coordination + restaurant partnerships
- **Payment Integration Specialist**: Phase 4 (UPI, digital wallets, compliance)
- **Localization Expert**: Phases 6-7 (Regional languages, cultural adaptation)

---

**Note**: This MVP focuses on core functionality to validate the market quickly. Advanced features like ML recommendations, detailed analytics, and sophisticated gamification can be added in subsequent releases based on user feedback and market response.