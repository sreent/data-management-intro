# RideLink Super-App — Slide-Ready Seed Data

A minimal dataset for the Chapter 6 Document Modelling topic, small enough to trace by hand on teaching slides. Designed to demonstrate key concepts: structural variation, shape alignment, embed vs reference, `$elemMatch`, dot notation, aggregation pipelines, snapshot discipline, and bounded growth.

**3 passengers | 2 drivers | 2 merchants | 4 plans**

---

## Design A — Aggregate-First (Embedded)

### `users` Collection (7 documents)

#### Passenger 1 — Sarah (standard, $elemMatch demo)

```json
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
}
```

> Sarah's saved places are the **`$elemMatch` counterexample**: Home is "daily" but recent (2025-01-20); Office is "weekday" but old (2024-12-10). A query for "daily AND lastUsed before 2025-01-01" matches *without* `$elemMatch` (Home=daily, Office=old) but fails *with* `$elemMatch` (no single place is both daily and old).

#### Passenger 2 — Wei Ming (premium, snapshot demo)

```json
{
  "userId": "passenger-1002",
  "displayName": "Wei Ming Lim",
  "phone": "+6598761234",
  "email": "weiming@example.com",
  "role": "passenger",
  "tier": "premium",
  "savedPlaces": [
    {"label": "Home",    "address": "88 Bukit Timah Rd",  "lat": 1.328, "lng": 103.797, "frequency": "daily",   "lastUsed": "2025-01-18"},
    {"label": "Gym",     "address": "10 Bayfront Ave",    "lat": 1.283, "lng": 103.860, "frequency": "weekly",  "lastUsed": "2025-01-15"},
    {"label": "Parents", "address": "45 Ang Mo Kio Ave 6","lat": 1.370, "lng": 103.837, "frequency": "monthly", "lastUsed": "2024-12-25"}
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
}
```

> Wei Ming is a **premium passenger** — extra fields (`loyaltyTier`, `loungeAccess`, `subscriptionSnapshot`) that a standard passenger does not have. Demonstrates **structural variation** within the same collection. Also has 3 saved places with distinct frequencies for `$elemMatch` exercises.

#### Passenger 3 — Rani (standard, no saved places)

```json
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
}
```

> Rani has **no saved places** (empty array). Tests queries against empty embedded arrays — `$elemMatch` on an empty array returns no match.

#### Driver 1 — Ahmad (GrabCar, licence expiring 2026)

```json
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
}
```

> Ahmad is the **shape-alignment exemplar** — his document is exactly what the API returns. Also the **snapshot discipline** demo: his `commissionRateAtSignUp` (0.20) does not change when the plan's current rate changes.

#### Driver 2 — Priya (GrabFood, licence expiring 2025)

```json
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
}
```

> Priya is a **GrabFood delivery rider** — different shape from Ahmad (has `bike` instead of `vehicle`, `thermalBagCertified`, `deliveryZone`). Demonstrates **structural variation within the same role**. Licence expires 2025-06-30 — matches the "expiring before 2026-01-01" **dot notation** query. Ahmad's does not (2026-08-15).

#### Merchant 1 — Ah Huat (chicken rice, `$elemMatch` + `$unwind` demo)

```json
{
  "userId": "merchant-0891",
  "displayName": "Ah Huat",
  "phone": "+6562345678",
  "email": "ahhuat@example.com",
  "role": "merchant",
  "businessName": "Ah Huat Chicken Rice",
  "cuisine": "Chinese",
  "operatingHours": {
    "monday": {"open": "10:00", "close": "21:00"},
    "tuesday": {"open": "10:00", "close": "21:00"},
    "wednesday": {"open": "10:00", "close": "21:00"},
    "thursday": {"open": "10:00", "close": "21:00"},
    "friday": {"open": "10:00", "close": "22:00"},
    "saturday": {"open": "09:00", "close": "22:00"},
    "sunday": null
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
}
```

> Ah Huat has **5 menu items** (3 mains, 2 drinks). Key for `$unwind` demo: unwinding produces 5 documents. Also key for `$group` by category: mains count = 3, drinks count = 2. Also the **`$elemMatch` menu counterexample**: all 3 mains items are priced ≥ 5.00, so a query for "mains AND price < 5.00" with `$elemMatch` returns no match — but *without* `$elemMatch` it matches (some item is "mains", some item is < 5.00 — the drinks).

#### Merchant 2 — Tiger Sugar (bubble tea, different cuisine)

```json
{
  "userId": "merchant-0892",
  "displayName": "Jia Yi",
  "phone": "+6563456789",
  "email": "jiayi@example.com",
  "role": "merchant",
  "businessName": "Tiger Sugar Toa Payoh",
  "cuisine": "Beverages",
  "operatingHours": {
    "monday": {"open": "11:00", "close": "22:00"},
    "tuesday": {"open": "11:00", "close": "22:00"},
    "wednesday": {"open": "11:00", "close": "22:00"},
    "thursday": {"open": "11:00", "close": "22:00"},
    "friday": {"open": "11:00", "close": "23:00"},
    "saturday": {"open": "10:00", "close": "23:00"},
    "sunday": {"open": "10:00", "close": "21:00"}
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
```

> Tiger Sugar has **4 menu items** (2 signature, 2 tea). Combined with Ah Huat's 5 items, unwinding both merchants produces 9 item-documents. Grouped by category: mains=3, drinks=2, signature=2, tea=2. Different plan from Ah Huat — demonstrates `$lookup` to `plans` for cross-aggregate analytics.

---

### `plans` Collection (4 documents)

| planId | name | commissionRate | features | monthlyPrice | tier |
|--------|------|----------------|----------|--------------|------|
| plan-premium | GrabCar Premium | 0.20 | priority-matching, lounge-access, premium-support | 29.99 | premium |
| plan-standard | GrabCar Standard | 0.25 | standard-matching | 0.00 | standard |
| plan-grabfood-partner | GrabFood Partner | 0.30 | food-delivery, merchant-dashboard | 0.00 | partner |
| plan-grabfood-standard | GrabFood Standard | 0.35 | food-delivery | 0.00 | standard |

```json
[
  {"planId": "plan-premium",          "name": "GrabCar Premium",   "commissionRate": 0.20, "features": ["priority-matching", "lounge-access", "premium-support"], "monthlyPrice": 29.99, "tier": "premium"},
  {"planId": "plan-standard",         "name": "GrabCar Standard",  "commissionRate": 0.25, "features": ["standard-matching"], "monthlyPrice": 0.00, "tier": "standard"},
  {"planId": "plan-grabfood-partner", "name": "GrabFood Partner",  "commissionRate": 0.30, "features": ["food-delivery", "merchant-dashboard"], "monthlyPrice": 0.00, "tier": "partner"},
  {"planId": "plan-grabfood-standard","name": "GrabFood Standard", "commissionRate": 0.35, "features": ["food-delivery"], "monthlyPrice": 0.00, "tier": "standard"}
]
```

> Plans are a **separate collection** (shared data, independent lifecycle). Users embed only a snapshot of plan terms at sign-up. The `plans` collection is the editable truth.

---

## Design B — Reference-Heavy (Microservices Decomposition)

Same 7 users, decomposed across separate collections.

### `users_b` (7 documents — core identity only)

| userId | displayName | phone | role | tier/driverType/businessName |
|--------|------------|-------|------|------------------------------|
| passenger-1001 | Sarah Tan | +6591234567 | passenger | tier: standard |
| passenger-1002 | Wei Ming Lim | +6598761234 | passenger | tier: premium |
| passenger-1003 | Rani Devi | +6587001234 | passenger | tier: standard |
| driver-5582 | Ahmad Ibrahim | +6598765432 | driver | driverType: grabcar |
| driver-5583 | Priya Nair | +6587654321 | driver | driverType: grabfood |
| merchant-0891 | Ah Huat | +6562345678 | merchant | businessName: Ah Huat Chicken Rice |
| merchant-0892 | Jia Yi | +6563456789 | merchant | businessName: Tiger Sugar Toa Payoh |

### `savedPlaces_b` (5 documents)

| userId | label | frequency | lastUsed |
|--------|-------|-----------|----------|
| passenger-1001 | Home | daily | 2025-01-20 |
| passenger-1001 | Office | weekday | 2024-12-10 |
| passenger-1002 | Home | daily | 2025-01-18 |
| passenger-1002 | Gym | weekly | 2025-01-15 |
| passenger-1002 | Parents | monthly | 2024-12-25 |

> Rani has **no saved places** — no rows in `savedPlaces_b` for passenger-1003.

### `preferences_b` (7 documents)

One per user: ride preferences for passengers, zone preferences for drivers.

### `vehicles_b` (2 documents)

| userId | vehicle/bike | license.expiryDate |
|--------|-------------|-------------------|
| driver-5582 | Toyota Prius (SBA1234X) | 2026-08-15 |
| driver-5583 | Niu NQi GTS (FBA5678Y) | 2025-06-30 |

### `earnings_b` (2 documents)

| userId | currentWeek | incentiveProgress |
|--------|------------|-------------------|
| driver-5582 | 1240.50 | 42/50 rides, $120 bonus |
| driver-5583 | 680.00 | 95/100 deliveries, $50 bonus |

### `paymentMethods_b` (4 documents)

| userId | type | last4/balance |
|--------|------|---------------|
| passenger-1001 | card | 4242 |
| passenger-1001 | grabpay | $45.00 |
| passenger-1002 | card | 8888 |
| passenger-1003 | grabpay | $120.00 |

### `menuItems_b` (9 documents)

| merchantId | itemName | price | category |
|-----------|----------|-------|----------|
| merchant-0891 | Roasted Chicken Rice | 5.50 | mains |
| merchant-0891 | Steamed Chicken Rice | 5.00 | mains |
| merchant-0891 | Char Siew Rice | 6.00 | mains |
| merchant-0891 | Iced Barley | 1.50 | drinks |
| merchant-0891 | Hot Tea | 1.20 | drinks |
| merchant-0892 | Brown Sugar Boba Milk | 6.90 | signature |
| merchant-0892 | Tiger Black Sugar | 5.90 | signature |
| merchant-0892 | Oolong Tea Latte | 5.50 | tea |
| merchant-0892 | Matcha Latte | 6.50 | tea |

---

## Data Summary — Counts for Hand-Tracing

| Collection (Design A) | Documents |
|----------------------|-----------|
| `users` | 7 (3 passengers + 2 drivers + 2 merchants) |
| `plans` | 4 |

| Collection (Design B) | Documents |
|----------------------|-----------|
| `users_b` | 7 |
| `savedPlaces_b` | 5 |
| `preferences_b` | 7 |
| `vehicles_b` | 2 |
| `earnings_b` | 2 |
| `paymentMethods_b` | 4 |
| `menuItems_b` | 9 |
| `plans` | 4 (shared) |

---

## Teaching Scenarios Supported

| Scenario | Concept | What to show on slide |
|----------|---------|----------------------|
| **Structural variation** | Schema-on-read | Sarah (passenger) has `savedPlaces`, `ridePreferences`. Ahmad (driver) has `vehicle`, `license`, `earnings`. Ah Huat (merchant) has `menu`, `operatingHours`. All in the same collection, no NULLs. |
| **Within-role variation** | Schema-on-read | Wei Ming (premium passenger) has `loyaltyTier`, `loungeAccess`, `subscriptionSnapshot` that Sarah (standard) does not. Priya (GrabFood) has `bike`, `thermalBagCertified` that Ahmad (GrabCar) does not. No schema change needed. |
| **Shape alignment** | Aggregate design | Ahmad's document IS the API response. `db.users.findOne({"userId": "driver-5582"})` returns the complete profile. No join, no re-nesting. |
| **Dot notation** | Nested queries | `{"license.expiryDate": {"$lt": "2026-01-01"}}` — matches Priya (2025-06-30), not Ahmad (2026-08-15). Trace: navigate into `license` object, compare string dates. |
| **`$elemMatch` (saved places)** | Array queries | Sarah: Home="daily"/2025-01-20, Office="weekday"/2024-12-10. Query "daily AND before 2025-01-01": without `$elemMatch` → matches (Home=daily + Office=old). With `$elemMatch` → no match (no single place is both). |
| **`$elemMatch` (menu)** | Array queries | Ah Huat: mains at 5.00–6.00, drinks at 1.20–1.50. Query "mains AND price < 5.00": without `$elemMatch` → matches (some item=mains + drinks<5.00). With `$elemMatch` → no match (no single item is mains AND <5.00). |
| **`$unwind` + `$group`** | Aggregation pipeline | `$unwind: "$menu"` on both merchants → 9 documents. `$group by category`: mains=3 (avg $5.50), drinks=2 (avg $1.35), signature=2 (avg $6.40), tea=2 (avg $6.00). Trace each stage on slide. |
| **`$lookup` (cross-aggregate)** | Pipeline joins | "Avg price by plan tier" requires `$lookup` from `users` to `plans`. Ah Huat signed up under "GrabFood Partner" (tier: partner); Tiger Sugar under "GrabFood Standard" (tier: standard). The `$lookup` adds one pipeline stage. |
| **Snapshot discipline** | Update fan-out | Plan "GrabCar Premium" commission changes 0.20 → 0.18. Ahmad's `commissionRateAtSignUp` stays 0.20 (historical fact). Only `plans` collection updated (1 doc). Without snapshots: both Ahmad and Wei Ming would need updates (fan-out). |
| **Embed-or-reference** | Design decisions | Plans: referenced (shared, independent lifecycle). Saved places: embedded (bounded ≤10, read together). Ride history: referenced (unbounded growth). |
| **Profile load comparison** | Design A vs B | Design A: 1 `findOne`. Design B: 1 `$match` + 4 `$lookup` stages. Design A returns nested JSON directly; Design B assembles it from fragments. |
| **Empty array** | Edge cases | Rani has `savedPlaces: []`. `$elemMatch` on an empty array → no match. `savedPlaces.label` exists query → no match. But the document is valid (schema-on-read accepts it). |
| **Regex** | Pattern matching | `{"phone": /^\+65/}` → all 7 users (anchored, index-friendly). `{"businessName": /chicken rice/i}` → Ah Huat only (unanchored, requires scan). |
| **Selectivity** | Index trade-offs | `{"role": "passenger"}` matches 3/7 (43%). `{"role": "merchant"}` matches 2/7 (29%). `{"phone": "+6591234567"}` matches 1/7 (14%). Phone index is most selective. |

---

## Hand-Trace Walkthroughs

### Walkthrough 1 — `$unwind` then `$group` (9 items → 4 categories)

**Input:** 2 merchant documents with embedded `menu[]` arrays.

**Stage 1 — `$match: {"role": "merchant"}`:** Keeps Ah Huat and Tiger Sugar (2 documents).

**Stage 2 — `$unwind: "$menu"`:** Produces 9 documents:

| # | merchantId | menu.itemName | menu.price | menu.category |
|---|-----------|--------------|------------|---------------|
| 1 | merchant-0891 | Roasted Chicken Rice | 5.50 | mains |
| 2 | merchant-0891 | Steamed Chicken Rice | 5.00 | mains |
| 3 | merchant-0891 | Char Siew Rice | 6.00 | mains |
| 4 | merchant-0891 | Iced Barley | 1.50 | drinks |
| 5 | merchant-0891 | Hot Tea | 1.20 | drinks |
| 6 | merchant-0892 | Brown Sugar Boba Milk | 6.90 | signature |
| 7 | merchant-0892 | Tiger Black Sugar | 5.90 | signature |
| 8 | merchant-0892 | Oolong Tea Latte | 5.50 | tea |
| 9 | merchant-0892 | Matcha Latte | 6.50 | tea |

**Stage 3 — `$group by "$menu.category"`:** Produces 4 documents:

| _id (category) | itemCount | avgPrice |
|----------------|-----------|----------|
| mains | 3 | (5.50 + 5.00 + 6.00) / 3 = **5.50** |
| drinks | 2 | (1.50 + 1.20) / 2 = **1.35** |
| signature | 2 | (6.90 + 5.90) / 2 = **6.40** |
| tea | 2 | (5.50 + 6.50) / 2 = **6.00** |

**Stage 4 — `$sort: {"itemCount": -1}`:** mains (3), then drinks/signature/tea (2 each, order depends on insertion).

**Stage 5 — `$limit: 5`:** All 4 categories pass (fewer than limit).

### Walkthrough 2 — `$elemMatch` counterexample (Sarah's saved places)

**Sarah's saved places array:**

| Element | label | frequency | lastUsed |
|---------|-------|-----------|----------|
| [0] | Home | daily | 2025-01-20 |
| [1] | Office | weekday | 2024-12-10 |

**Query A (without `$elemMatch`):**
```json
{"savedPlaces.frequency": "daily", "savedPlaces.lastUsed": {"$lt": "2025-01-01"}}
```
- Does any element have `frequency: "daily"`? Yes — element [0] (Home).
- Does any element have `lastUsed < "2025-01-01"`? Yes — element [1] (Office, 2024-12-10).
- Both conditions satisfied (by different elements). **Result: MATCH.**

**Query B (with `$elemMatch`):**
```json
{"savedPlaces": {"$elemMatch": {"frequency": "daily", "lastUsed": {"$lt": "2025-01-01"}}}}
```
- Element [0]: frequency="daily" ✓, lastUsed="2025-01-20" — NOT < 2025-01-01 ✗. Fails.
- Element [1]: frequency="weekday" ✗. Fails.
- No single element satisfies both. **Result: NO MATCH.**

### Walkthrough 3 — Snapshot discipline (commission rate change)

**Before change:**
- `plans` collection: "GrabCar Premium" has `commissionRate: 0.20`
- Ahmad's profile: `subscriptionSnapshot.commissionRateAtSignUp: 0.20`

**Change:** Company updates GrabCar Premium rate to 0.18.

**With snapshot design (Design A):**
- Update `plans` collection: 1 document updated (`commissionRate: 0.18`)
- Ahmad's profile: `commissionRateAtSignUp` stays 0.20 (immutable historical fact)
- **Total writes: 1**

**Without snapshot (hypothetical — embedded current plan data):**
- Update `plans` collection: 1 document
- Update every user who embeds data from that plan: Ahmad (driver-5582, has `commissionRate`) + Wei Ming (passenger-1002, has `monthlyPrice`) = 2 user documents
- **Total writes: 3** (and scales to thousands with more users on the plan)

### Walkthrough 4 — Profile load comparison (driver-5582)

**Design A:** `db.users.findOne({"userId": "driver-5582"})` → returns complete document with `vehicle`, `license`, `preferences`, `earnings`, `subscriptionSnapshot`. **1 read.**

**Design B:**
1. `db.users_b.findOne({"userId": "driver-5582"})` → core identity
2. `db.vehicles_b.findOne({"userId": "driver-5582"})` → vehicle + license
3. `db.preferences_b.findOne({"userId": "driver-5582"})` → preferences
4. `db.earnings_b.findOne({"userId": "driver-5582"})` → earnings
5. `db.paymentMethods_b.find({"userId": "driver-5582"})` → payment methods

**5 reads** (or 1 `$match` + 4 `$lookup` stages in a pipeline). Application must then assemble these into a single nested response.

---

## MongoDB Insert Statements

See `seed-data.js` for the complete `insertMany` statements for both designs.
