export type OrderStatus =
  | "PLACING"
  | "PENDING"
  | "PREPARING"
  | "READY"
  | "DELIVERING"
  | "DELIVERED"
  | "CANCELLED"
  // Pickup/reservation flow statuses
  | "RESERVED"
  | "COLLECTED"
  | "EXPIRED"