# MealPeDeal Backend Service

**MealPeDeal** is a modern backend service based on event-driven **Microservice** architecture 
designed to power India's premier food waste reduction platform - a Too Good To Go alternative for the Indian market.


# Project Description

The **MealPeDeal Backend Service** stands as a cutting-edge 
technological infrastructure, driving the operations of India's innovative 
food waste reduction platform. Its event-driven microservice architecture, 
coupled with a rich feature set, ensures a seamless experience 
for restaurants, customers, and the environment by connecting surplus food with conscious consumers. 




# Key Features

1. **Event-Driven Microservice Architecture**:
The service is architected around a powerful event-driven paradigm, 
where various microservices communicate via events. 
This design choice facilitates seamless integration and ensures 
that different components of the platform can react to events in real-time, 
enabling a highly responsive and efficient system.

2. **Scalability and Performance**:
The service is engineered to meet the demands of a high-traffic 
food waste reduction platform. It leverages horizontal scalability, 
allowing it to handle a large volume of concurrent users, mystery bag orders, 
and pickup transactions. This ensures a smooth and uninterrupted experience 
for customers and restaurant partners.

3. **Mystery Bag System**:
MealPeDeal's core feature revolves around "mystery bags" - surprise food packages 
from restaurants at heavily discounted prices. The system includes real-time inventory management, 
pickup time slots, reservation systems, and seamless payment processing tailored for the Indian market.

4. **Indian Market Optimization**:
Built specifically for the Indian market with UPI/Razorpay payments, 
multi-language support (Hindi + regional languages), WhatsApp/SMS notifications, 
INR currency handling, and compliance with Indian data protection laws.

5. **Secure Authentication and Authorization**:
A robust authentication and authorization system is integrated to 
safeguard user data and sensitive information. 
This ensures that only authenticated and authorized users have access 
to their respective accounts and functionalities within the platform.

# Microservices

Each microservice has its own documentation. You can get acquainted with it further.

1. [User Management Microservice](user-management). This Microservice handles authentication and user management for customers and restaurant partners.
2. [Menu Microservice](menu). This Microservice manages mystery bag creation and menu-related operations for **Restaurant Managers**.
3. [Restaurant Microservice](restaurant). This Microservice gives **Restaurant Managers** and **Moderators** ability to work with **Restaurant** data and pickup configurations.
4. [Order Microservice](order). This Microservice handles mystery bag reservations, pickup management, and payment processing with Razorpay integration.

# Docker

You can use docker files in [Docker directory](docker) to launch Kafka broker.

Clone the repository to your local machine

```bash
  git clone https://github.com/Ash1VT/food-delivery-backend
```

Create an **".env"** file.

Your **env** file should look like this:
```
  ZOOKEEPER_SERVER_USERS=admin
  ZOOKEEPER_SERVER_PASSWORDS=admin
  ZOOKEEPER_CLIENT_USER=admin
  ZOOKEEPER_CLIENT_PASSWORD=admin
  KAFKA_CLIENT_USERS=user
  KAFKA_CLIENT_PASSWORDS=admin
  KAFKA_INTER_BROKER_USER=kafka
  KAFKA_INTER_BROKER_PASSWORD=12345
```

Navigate to the [Docker directory](docker)
```bash
  cd docker
```

Build Docker web app image (don't forget to provide path to your **env** file)
```bash
  docker compose --env-file=../.env build
```

Run Docker containers (don't forget to provide path to your **env** file)
```bash
  docker compose --env-file=../.env up -d
```

To run test containers use following command
```bash
  docker compose --env-file=../.env -f docker-compose.test.yaml up -d
```

# Core Features (Implemented)

1. **Mystery Bag Management**. Restaurant partners can create surprise bags with surplus food at discounted prices.
2. **Reservation System**. Customers can browse and reserve mystery bags with specific pickup time slots.
3. **Pickup Management**. QR code-based pickup verification system for seamless collection.
4. **Payment Integration**. Complete Razorpay integration supporting UPI, cards, wallets, and net banking.
5. **Geolocation Services**. Google Maps integration for restaurant discovery and navigation.

# Future Enhancements

1. **Advanced Analytics**. Restaurant dashboard with food waste analytics, revenue insights, and sustainability metrics.
2. **Reviews and Ratings**. Customer feedback system for mystery bags and restaurant experiences.
3. **Gamification**. Environmental impact tracking, badges, and rewards for reducing food waste.
4. **AI Recommendations**. Machine learning-based mystery bag suggestions based on customer preferences.
5. **Social Features**. Community challenges, sharing food waste reduction achievements, and referral programs.
6. **Expansion Features**. Multi-city support, franchise management, and white-label solutions. 


# License

This project is provided with [MIT Licence](LICENSE).