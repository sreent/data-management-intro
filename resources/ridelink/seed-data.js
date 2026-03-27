// ============================================================
// RideLink Super-App — Slide-Ready Seed Data
// MongoDB 4.4+
// ============================================================
// Small enough to trace by hand on teaching slides.
// 3 passengers | 2 drivers | 2 merchants | 4 plans
//
// Two designs: Design A (aggregate-first, embedded) and
// Design B (reference-heavy, microservices decomposition).
// ============================================================

// ------------------------------------------------------------
// Design A — Aggregate-First (Embedded)
// ------------------------------------------------------------

// ── Plans (shared across both designs) ──
db.plans.insertMany([
    {
        "planId": "plan-premium",
        "name": "GrabCar Premium",
        "commissionRate": 0.20,
        "features": ["priority-matching", "lounge-access", "premium-support"],
        "monthlyPrice": 29.99,
        "tier": "premium"
    },
    {
        "planId": "plan-standard",
        "name": "GrabCar Standard",
        "commissionRate": 0.25,
        "features": ["standard-matching"],
        "monthlyPrice": 0.00,
        "tier": "standard"
    },
    {
        "planId": "plan-grabfood-partner",
        "name": "GrabFood Partner",
        "commissionRate": 0.30,
        "features": ["food-delivery", "merchant-dashboard"],
        "monthlyPrice": 0.00,
        "tier": "partner"
    },
    {
        "planId": "plan-grabfood-standard",
        "name": "GrabFood Standard",
        "commissionRate": 0.35,
        "features": ["food-delivery"],
        "monthlyPrice": 0.00,
        "tier": "standard"
    }
]);

// ── Users (Design A: 7 documents, all roles in one collection) ──
db.users.insertMany([
    // ── Passenger 1: Sarah (standard, $elemMatch demo) ──
    {
        "userId": "passenger-1001",
        "displayName": "Sarah Tan",
        "phone": "+6591234567",
        "email": "sarah@example.com",
        "role": "passenger",
        "tier": "standard",
        "savedPlaces": [
            {"label": "Home",   "address": "123 Clementi Ave 3", "lat": 1.315, "lng": 103.765, "frequency": "daily",   "lastUsed": "2025-01-20"},
            {"label": "Office", "address": "1 Raffles Place",     "lat": 1.284, "lng": 103.851, "frequency": "weekday", "lastUsed": "2024-12-10"}
        ],
        "paymentMethods": [
            {"type": "card", "last4": "4242", "isDefault": true},
            {"type": "grabpay", "balance": 45.00}
        ],
        "ridePreferences": {"vehicleType": "JustGrab", "quietRide": false, "temperature": "normal"},
        "rewardPoints": 2840
    },

    // ── Passenger 2: Wei Ming (premium, snapshot + structural variation) ──
    {
        "userId": "passenger-1002",
        "displayName": "Wei Ming Lim",
        "phone": "+6598761234",
        "email": "weiming@example.com",
        "role": "passenger",
        "tier": "premium",
        "savedPlaces": [
            {"label": "Home",    "address": "88 Bukit Timah Rd",   "lat": 1.328, "lng": 103.797, "frequency": "daily",   "lastUsed": "2025-01-18"},
            {"label": "Gym",     "address": "10 Bayfront Ave",     "lat": 1.283, "lng": 103.860, "frequency": "weekly",  "lastUsed": "2025-01-15"},
            {"label": "Parents", "address": "45 Ang Mo Kio Ave 6", "lat": 1.370, "lng": 103.837, "frequency": "monthly", "lastUsed": "2024-12-25"}
        ],
        "paymentMethods": [
            {"type": "card", "last4": "8888", "isDefault": true}
        ],
        "ridePreferences": {"vehicleType": "GrabCar Premium", "quietRide": true, "temperature": "cold"},
        "loyaltyTier": "platinum",
        "loungeAccess": true,
        "rewardPoints": 15200,
        "subscriptionSnapshot": {
            "planNameAtSignUp": "GrabCar Premium",
            "priceAtSignUp": 29.99,
            "signUpDate": "2023-06-01"
        }
    },

    // ── Passenger 3: Rani (standard, empty saved places) ──
    {
        "userId": "passenger-1003",
        "displayName": "Rani Devi",
        "phone": "+6587001234",
        "email": "rani@example.com",
        "role": "passenger",
        "tier": "standard",
        "savedPlaces": [],
        "paymentMethods": [
            {"type": "grabpay", "balance": 120.00}
        ],
        "ridePreferences": {"vehicleType": "GrabShare", "quietRide": false, "temperature": "normal"},
        "rewardPoints": 450
    },

    // ── Driver 1: Ahmad (GrabCar, licence 2026, shape alignment exemplar) ──
    {
        "userId": "driver-5582",
        "displayName": "Ahmad Ibrahim",
        "phone": "+6598765432",
        "email": "ahmad@example.com",
        "role": "driver",
        "driverType": "grabcar",
        "vehicle": {
            "make": "Toyota", "model": "Prius", "year": 2022,
            "plateNumber": "SBA1234X", "vehicleType": "standard"
        },
        "license": {
            "licenseNumber": "S1234567A",
            "expiryDate": "2026-08-15",
            "vocationalLicenseExpiry": "2025-12-31"
        },
        "preferences": {
            "maxDistance": 25,
            "preferredZones": ["central", "east"],
            "autoAccept": false
        },
        "earnings": {
            "currentWeek": 1240.50,
            "incentiveProgress": {"ridesCompleted": 42, "target": 50, "bonus": 120.00}
        },
        "subscriptionSnapshot": {
            "planNameAtSignUp": "GrabCar Premium",
            "commissionRateAtSignUp": 0.20,
            "signUpDate": "2024-01-15"
        }
    },

    // ── Driver 2: Priya (GrabFood, licence 2025, within-role variation) ──
    {
        "userId": "driver-5583",
        "displayName": "Priya Nair",
        "phone": "+6587654321",
        "email": "priya@example.com",
        "role": "driver",
        "driverType": "grabfood",
        "bike": {
            "type": "electric_scooter", "model": "Niu NQi GTS",
            "plateNumber": "FBA5678Y"
        },
        "thermalBagCertified": true,
        "deliveryZone": "central",
        "license": {
            "licenseNumber": "S7654321B",
            "expiryDate": "2025-06-30",
            "vocationalLicenseExpiry": "2025-06-30"
        },
        "preferences": {
            "maxDistance": 10,
            "preferredZones": ["central"],
            "autoAccept": true
        },
        "earnings": {
            "currentWeek": 680.00,
            "incentiveProgress": {"deliveriesCompleted": 95, "target": 100, "bonus": 50.00}
        },
        "subscriptionSnapshot": {
            "planNameAtSignUp": "GrabFood Partner",
            "commissionRateAtSignUp": 0.30,
            "signUpDate": "2024-03-10"
        }
    },

    // ── Merchant 1: Ah Huat (chicken rice, $elemMatch + $unwind demo) ──
    {
        "userId": "merchant-0891",
        "displayName": "Ah Huat",
        "phone": "+6562345678",
        "email": "ahhuat@example.com",
        "role": "merchant",
        "businessName": "Ah Huat Chicken Rice",
        "cuisine": "Chinese",
        "operatingHours": {
            "monday":    {"open": "10:00", "close": "21:00"},
            "tuesday":   {"open": "10:00", "close": "21:00"},
            "wednesday": {"open": "10:00", "close": "21:00"},
            "thursday":  {"open": "10:00", "close": "21:00"},
            "friday":    {"open": "10:00", "close": "22:00"},
            "saturday":  {"open": "09:00", "close": "22:00"},
            "sunday":    null
        },
        "menu": [
            {"itemName": "Roasted Chicken Rice", "price": 5.50, "category": "mains", "customisations": [{"name": "Extra rice", "price": 0.50}, {"name": "Add egg", "price": 1.00}]},
            {"itemName": "Steamed Chicken Rice", "price": 5.00, "category": "mains", "customisations": [{"name": "Extra rice", "price": 0.50}]},
            {"itemName": "Char Siew Rice",       "price": 6.00, "category": "mains", "customisations": [{"name": "Extra rice", "price": 0.50}]},
            {"itemName": "Iced Barley",          "price": 1.50, "category": "drinks", "customisations": []},
            {"itemName": "Hot Tea",              "price": 1.20, "category": "drinks", "customisations": []}
        ],
        "promotions": [
            {"code": "AHHUAT10", "discount": 0.10, "validUntil": "2025-03-31"}
        ],
        "subscriptionSnapshot": {
            "planNameAtSignUp": "GrabFood Partner",
            "commissionRateAtSignUp": 0.30,
            "signUpDate": "2023-11-01"
        }
    },

    // ── Merchant 2: Tiger Sugar (bubble tea, different cuisine) ──
    {
        "userId": "merchant-0892",
        "displayName": "Jia Yi",
        "phone": "+6563456789",
        "email": "jiayi@example.com",
        "role": "merchant",
        "businessName": "Tiger Sugar Toa Payoh",
        "cuisine": "Beverages",
        "operatingHours": {
            "monday":    {"open": "11:00", "close": "22:00"},
            "tuesday":   {"open": "11:00", "close": "22:00"},
            "wednesday": {"open": "11:00", "close": "22:00"},
            "thursday":  {"open": "11:00", "close": "22:00"},
            "friday":    {"open": "11:00", "close": "23:00"},
            "saturday":  {"open": "10:00", "close": "23:00"},
            "sunday":    {"open": "10:00", "close": "21:00"}
        },
        "menu": [
            {"itemName": "Brown Sugar Boba Milk", "price": 6.90, "category": "signature", "customisations": [{"name": "Less sugar", "price": 0.00}, {"name": "Extra boba", "price": 1.00}]},
            {"itemName": "Tiger Black Sugar",     "price": 5.90, "category": "signature", "customisations": [{"name": "Less sugar", "price": 0.00}]},
            {"itemName": "Oolong Tea Latte",      "price": 5.50, "category": "tea",       "customisations": [{"name": "Less sugar", "price": 0.00}, {"name": "Oat milk", "price": 0.80}]},
            {"itemName": "Matcha Latte",          "price": 6.50, "category": "tea",       "customisations": [{"name": "Less sugar", "price": 0.00}]}
        ],
        "promotions": [],
        "subscriptionSnapshot": {
            "planNameAtSignUp": "GrabFood Standard",
            "commissionRateAtSignUp": 0.35,
            "signUpDate": "2024-02-15"
        }
    }
]);


// ------------------------------------------------------------
// Design B — Reference-Heavy (Microservices Decomposition)
// ------------------------------------------------------------

// ── Core identity ──
db.users_b.insertMany([
    {"userId": "passenger-1001", "displayName": "Sarah Tan",      "phone": "+6591234567", "email": "sarah@example.com",    "role": "passenger", "tier": "standard"},
    {"userId": "passenger-1002", "displayName": "Wei Ming Lim",   "phone": "+6598761234", "email": "weiming@example.com",  "role": "passenger", "tier": "premium"},
    {"userId": "passenger-1003", "displayName": "Rani Devi",      "phone": "+6587001234", "email": "rani@example.com",     "role": "passenger", "tier": "standard"},
    {"userId": "driver-5582",    "displayName": "Ahmad Ibrahim",  "phone": "+6598765432", "email": "ahmad@example.com",    "role": "driver",    "driverType": "grabcar"},
    {"userId": "driver-5583",    "displayName": "Priya Nair",     "phone": "+6587654321", "email": "priya@example.com",    "role": "driver",    "driverType": "grabfood"},
    {"userId": "merchant-0891",  "displayName": "Ah Huat",        "phone": "+6562345678", "email": "ahhuat@example.com",   "role": "merchant",  "businessName": "Ah Huat Chicken Rice"},
    {"userId": "merchant-0892",  "displayName": "Jia Yi",         "phone": "+6563456789", "email": "jiayi@example.com",    "role": "merchant",  "businessName": "Tiger Sugar Toa Payoh"}
]);

// ── Saved places ──
db.savedPlaces_b.insertMany([
    {"userId": "passenger-1001", "label": "Home",    "address": "123 Clementi Ave 3",  "lat": 1.315, "lng": 103.765, "frequency": "daily",   "lastUsed": "2025-01-20"},
    {"userId": "passenger-1001", "label": "Office",  "address": "1 Raffles Place",      "lat": 1.284, "lng": 103.851, "frequency": "weekday", "lastUsed": "2024-12-10"},
    {"userId": "passenger-1002", "label": "Home",    "address": "88 Bukit Timah Rd",    "lat": 1.328, "lng": 103.797, "frequency": "daily",   "lastUsed": "2025-01-18"},
    {"userId": "passenger-1002", "label": "Gym",     "address": "10 Bayfront Ave",      "lat": 1.283, "lng": 103.860, "frequency": "weekly",  "lastUsed": "2025-01-15"},
    {"userId": "passenger-1002", "label": "Parents", "address": "45 Ang Mo Kio Ave 6",  "lat": 1.370, "lng": 103.837, "frequency": "monthly", "lastUsed": "2024-12-25"}
]);

// ── Preferences ──
db.preferences_b.insertMany([
    {"userId": "passenger-1001", "ridePreferences": {"vehicleType": "JustGrab", "quietRide": false, "temperature": "normal"}},
    {"userId": "passenger-1002", "ridePreferences": {"vehicleType": "GrabCar Premium", "quietRide": true, "temperature": "cold"}},
    {"userId": "passenger-1003", "ridePreferences": {"vehicleType": "GrabShare", "quietRide": false, "temperature": "normal"}},
    {"userId": "driver-5582",    "preferences": {"maxDistance": 25, "preferredZones": ["central", "east"], "autoAccept": false}},
    {"userId": "driver-5583",    "preferences": {"maxDistance": 10, "preferredZones": ["central"], "autoAccept": true}},
    {"userId": "merchant-0891",  "operatingHours": {"monday": {"open": "10:00", "close": "21:00"}, "tuesday": {"open": "10:00", "close": "21:00"}, "wednesday": {"open": "10:00", "close": "21:00"}, "thursday": {"open": "10:00", "close": "21:00"}, "friday": {"open": "10:00", "close": "22:00"}, "saturday": {"open": "09:00", "close": "22:00"}, "sunday": null}},
    {"userId": "merchant-0892",  "operatingHours": {"monday": {"open": "11:00", "close": "22:00"}, "tuesday": {"open": "11:00", "close": "22:00"}, "wednesday": {"open": "11:00", "close": "22:00"}, "thursday": {"open": "11:00", "close": "22:00"}, "friday": {"open": "11:00", "close": "23:00"}, "saturday": {"open": "10:00", "close": "23:00"}, "sunday": {"open": "10:00", "close": "21:00"}}}
]);

// ── Vehicles and licences (drivers only) ──
db.vehicles_b.insertMany([
    {"userId": "driver-5582", "vehicle": {"make": "Toyota", "model": "Prius", "year": 2022, "plateNumber": "SBA1234X", "vehicleType": "standard"}, "license": {"licenseNumber": "S1234567A", "expiryDate": "2026-08-15", "vocationalLicenseExpiry": "2025-12-31"}},
    {"userId": "driver-5583", "bike": {"type": "electric_scooter", "model": "Niu NQi GTS", "plateNumber": "FBA5678Y"}, "thermalBagCertified": true, "deliveryZone": "central", "license": {"licenseNumber": "S7654321B", "expiryDate": "2025-06-30", "vocationalLicenseExpiry": "2025-06-30"}}
]);

// ── Earnings (drivers only) ──
db.earnings_b.insertMany([
    {"userId": "driver-5582", "earnings": {"currentWeek": 1240.50, "incentiveProgress": {"ridesCompleted": 42, "target": 50, "bonus": 120.00}}},
    {"userId": "driver-5583", "earnings": {"currentWeek": 680.00, "incentiveProgress": {"deliveriesCompleted": 95, "target": 100, "bonus": 50.00}}}
]);

// ── Payment methods ──
db.paymentMethods_b.insertMany([
    {"userId": "passenger-1001", "type": "card",    "last4": "4242", "isDefault": true},
    {"userId": "passenger-1001", "type": "grabpay", "balance": 45.00, "isDefault": false},
    {"userId": "passenger-1002", "type": "card",    "last4": "8888", "isDefault": true},
    {"userId": "passenger-1003", "type": "grabpay", "balance": 120.00, "isDefault": true}
]);

// ── Menu items (merchants only, each item a separate document) ──
db.menuItems_b.insertMany([
    {"merchantId": "merchant-0891", "itemName": "Roasted Chicken Rice", "price": 5.50, "category": "mains", "customisations": [{"name": "Extra rice", "price": 0.50}, {"name": "Add egg", "price": 1.00}]},
    {"merchantId": "merchant-0891", "itemName": "Steamed Chicken Rice", "price": 5.00, "category": "mains", "customisations": [{"name": "Extra rice", "price": 0.50}]},
    {"merchantId": "merchant-0891", "itemName": "Char Siew Rice",       "price": 6.00, "category": "mains", "customisations": [{"name": "Extra rice", "price": 0.50}]},
    {"merchantId": "merchant-0891", "itemName": "Iced Barley",          "price": 1.50, "category": "drinks", "customisations": []},
    {"merchantId": "merchant-0891", "itemName": "Hot Tea",              "price": 1.20, "category": "drinks", "customisations": []},
    {"merchantId": "merchant-0892", "itemName": "Brown Sugar Boba Milk","price": 6.90, "category": "signature", "customisations": [{"name": "Less sugar", "price": 0.00}, {"name": "Extra boba", "price": 1.00}]},
    {"merchantId": "merchant-0892", "itemName": "Tiger Black Sugar",    "price": 5.90, "category": "signature", "customisations": [{"name": "Less sugar", "price": 0.00}]},
    {"merchantId": "merchant-0892", "itemName": "Oolong Tea Latte",     "price": 5.50, "category": "tea",       "customisations": [{"name": "Less sugar", "price": 0.00}, {"name": "Oat milk", "price": 0.80}]},
    {"merchantId": "merchant-0892", "itemName": "Matcha Latte",         "price": 6.50, "category": "tea",       "customisations": [{"name": "Less sugar", "price": 0.00}]}
]);
