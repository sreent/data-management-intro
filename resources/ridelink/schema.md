# RideLink Super-App — Document Schema Model

The canonical document schema used across Chapters 1, 6, and 11. Chapter 1 introduces RideLink as a failure scenario; Chapter 6 designs the personalisation layer as aggregate-shaped documents; Chapter 11 revisits RideLink in the capstone multi-model architecture.

**2 collections (Design A)** | **8 collections (Design B)** | **RideLink super-app domain** | **MongoDB 4.4+**

---

## 1. Design A — Aggregate-First (Embedded)

### Collection diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  users  (one document per user, all roles in same collection)   │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │  passenger    │  │  driver      │  │  merchant             │  │
│  │              │  │              │  │                       │  │
│  │ savedPlaces[]│  │ vehicle{}    │  │ menu[]                │  │
│  │ paymentMeth[]│  │ license{}    │  │   └─customisations[]  │  │
│  │ ridePrefs{}  │  │ preferences{}│  │ operatingHours{}      │  │
│  │ rewardPoints │  │ earnings{}   │  │ promotions[]          │  │
│  │              │  │ paymentMeth[]│  │                       │  │
│  │ [premium]    │  │              │  │                       │  │
│  │ loyaltyTier  │  │ [grabcar]    │  │                       │  │
│  │ loungeAccess │  │ vehicle{}    │  │                       │  │
│  │ subscription │  │              │  │                       │  │
│  │   Snapshot{} │  │ [grabfood]   │  │                       │  │
│  │              │  │ bike{}       │  │                       │  │
│  │              │  │ thermalBag   │  │                       │  │
│  │              │  │ deliveryZone │  │                       │  │
│  │              │  │              │  │                       │  │
│  │              │  │ subscription │  │ subscription           │  │
│  │              │  │   Snapshot{} │  │   Snapshot{}           │  │
│  └──────────────┘  └──────────────┘  └───────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐
│  plans  (shared reference data)      │
│                                      │
│  planId, name, commissionRate,       │
│  features[], monthlyPrice, tier      │
└──────────────────────────────────────┘

  users.subscriptionSnapshot ─ ─ ─ ─ ─▶ plans (snapshot, not live reference)
  (immutable copy at sign-up)            (editable truth)
```

### `users` collection — document shapes by role

All roles share a common set of fields (`userId`, `displayName`, `phone`, `email`, `role`). Role-specific fields vary — this is structural variation as data, not schema change.

#### Common fields (all roles)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `userId` | string | Yes | Business key (e.g., `"passenger-1001"`) |
| `displayName` | string | Yes | |
| `phone` | string | Yes | Singapore format `+65XXXXXXXX` |
| `email` | string | Yes | |
| `role` | string | Yes | `"passenger"` \| `"driver"` \| `"merchant"` |

#### Passenger-specific fields

| Field | Type | Bounded? | Notes |
|-------|------|----------|-------|
| `tier` | string | — | `"standard"` \| `"premium"` |
| `savedPlaces[]` | array of objects | max 10 | Each: `{label, address, lat, lng, frequency, lastUsed}` |
| `paymentMethods[]` | array of objects | max 5 | Each: `{type, last4/balance, isDefault}` |
| `ridePreferences` | object | — | `{vehicleType, quietRide, temperature}` |
| `rewardPoints` | integer | — | |
| `loyaltyTier` | string | — | Premium only: `"gold"` \| `"platinum"` |
| `loungeAccess` | boolean | — | Premium only |
| `subscriptionSnapshot` | object | — | Premium only: `{planNameAtSignUp, priceAtSignUp, signUpDate}` |

#### Driver-specific fields

| Field | Type | Bounded? | Notes |
|-------|------|----------|-------|
| `driverType` | string | — | `"grabcar"` \| `"grabfood"` |
| `vehicle` | object | — | GrabCar only: `{make, model, year, plateNumber, vehicleType}` |
| `bike` | object | — | GrabFood only: `{type, model, plateNumber}` |
| `thermalBagCertified` | boolean | — | GrabFood only |
| `deliveryZone` | string | — | GrabFood only |
| `license` | object | — | `{licenseNumber, expiryDate, vocationalLicenseExpiry}` |
| `preferences` | object | — | `{maxDistance, preferredZones[], autoAccept}` |
| `preferences.preferredZones[]` | array of strings | max 5 | Singapore zones: central, east, west, north, northeast |
| `earnings` | object | — | `{currentWeek, incentiveProgress: {ridesCompleted, target, bonus}}`. GrabFood drivers use `deliveriesCompleted` instead of `ridesCompleted` — structural variation within the role. |
| `paymentMethods[]` | array of objects | max 5 | Typically bank transfer for drivers |
| `subscriptionSnapshot` | object | — | `{planNameAtSignUp, commissionRateAtSignUp, signUpDate}` |

#### Merchant-specific fields

| Field | Type | Bounded? | Notes |
|-------|------|----------|-------|
| `businessName` | string | — | |
| `cuisine` | string | — | e.g., Chinese, Malay, Indian, Beverages |
| `operatingHours` | object | — | Keys: `monday`–`sunday`, value: `{open, close}` or `null` (closed) |
| `menu[]` | array of objects | max 100 | Each: `{itemName, price, category, customisations[]}` |
| `menu[].customisations[]` | array of objects | max 10 | Each: `{name, price}` |
| `promotions[]` | array of objects | max 10 | Each: `{code, discount, validUntil}` |
| `subscriptionSnapshot` | object | — | `{planNameAtSignUp, commissionRateAtSignUp, signUpDate}` |

### `plans` collection

| Field | Type | Notes |
|-------|------|-------|
| `planId` | string | Business key (e.g., `"plan-premium"`) |
| `name` | string | Display name (e.g., `"GrabCar Premium"`) |
| `commissionRate` | number | Decimal 0–1 (e.g., `0.20` = 20%) |
| `features` | array of strings | Feature flags |
| `monthlyPrice` | number | 0.00 for free plans |
| `tier` | string | `"premium"` \| `"standard"` \| `"partner"` |

---

## 2. Design B — Reference-Heavy (Microservices Decomposition)

### Collection diagram

```
┌──────────────┐     ┌─────────────────┐     ┌───────────────┐
│  users_b     │     │  savedPlaces_b  │     │ preferences_b │
│  (core ID)   │◄────│  userId (ref)   │     │ userId (ref)  │
│              │◄────│                 │     │               │
│  userId      │     └─────────────────┘     └───────────────┘
│  displayName │          │
│  phone       │     ┌────┴────────────┐     ┌───────────────┐
│  email       │     │  vehicles_b     │     │  earnings_b   │
│  role        │◄────│  userId (ref)   │     │  userId (ref) │
│              │     │  vehicle/bike   │     │  earnings     │
└──────────────┘     │  license        │     └───────────────┘
       │             └─────────────────┘
       │
       │             ┌─────────────────┐     ┌───────────────┐
       │             │ paymentMethods_b│     │  menuItems_b  │
       └─────────────│  userId (ref)   │     │ merchantId    │
                     └─────────────────┘     │  (ref)        │
                                             └───────────────┘

┌──────────────────────────────────────┐
│  plans  (shared — same as Design A)  │
└──────────────────────────────────────┘
```

### Collection summary

| Collection | Documents (slide-ready) | Documents (lab) | Referenced by |
|-----------|------------------------|-----------------|---------------|
| `users_b` | 7 | ~200 | — (root) |
| `savedPlaces_b` | 5 | ~350 | `userId` → `users_b` |
| `preferences_b` | 7 | ~200 | `userId` → `users_b` |
| `vehicles_b` | 2 | ~50 | `userId` → `users_b` |
| `earnings_b` | 2 | ~50 | `userId` → `users_b` |
| `paymentMethods_b` | 4 | ~285 | `userId` → `users_b` |
| `menuItems_b` | 9 | ~325 | `merchantId` → `users_b` |
| `plans` | 4 | 10 | — (shared) |

---

## 3. Embed-or-Reference Decisions

| Related entity | Decision | Condition tested | Justification |
|---------------|----------|-----------------|---------------|
| Vehicle details | **Embed** | None triggered | Retrieved with profile, one per driver, no independent lifecycle |
| Licence info | **Embed** | None triggered | Retrieved with profile, one per driver |
| Saved places | **Embed** | None triggered | Retrieved every session, bounded (max 10) |
| Payment methods | **Embed** | None triggered | Retrieved every session, bounded (max 5) |
| Menu items | **Embed** | None triggered | Retrieved with dashboard, bounded (max 100) |
| Customisations | **Embed** (nested) | None triggered | Always retrieved with menu item, bounded (max 10) |
| Subscription plan | **Reference** | Shared data, independent lifecycle | Thousands of users share same plan; plan updated independently |
| Subscription snapshot | **Embed** | None triggered | Immutable historical fact, read with profile |
| Ride/order history | **Reference** | Unbounded growth | Daily commuter generates thousands over years |
| Platform-wide promotions | **Reference** | Shared data | Managed centrally, applied to many merchants |

---

## 4. Bounded-Growth Rules

| Array | Upper bound | Business rule | Fallback |
|-------|------------|---------------|----------|
| `savedPlaces[]` | max 10 | App UI disables add-place button at limit | Remove one before adding |
| `paymentMethods[]` | max 5 | App limits payment methods per user | Remove one before adding |
| `menu[]` | max 100 | Merchant portal enforces item limit | Move to `menuItems` collection, reference by merchantId |
| `menu[].customisations[]` | max 10 per item | Portal enforces per-item limit | Unlikely to exceed |
| `promotions[]` | max 10 | Marketing limits concurrent promos | Archive expired promos |
| `preferences.preferredZones[]` | max 5 | Equal to total number of Singapore zones | Cannot exceed |

---

## 5. Snapshot Fields (Truth Map)

| Field | Editable truth | Snapshot location | Mutability |
|-------|---------------|-------------------|------------|
| Plan name | `plans.name` | `users.subscriptionSnapshot.planNameAtSignUp` | Immutable (historical) |
| Commission rate | `plans.commissionRate` | `users.subscriptionSnapshot.commissionRateAtSignUp` | Immutable (contractual) |
| Monthly price | `plans.monthlyPrice` | `users.subscriptionSnapshot.priceAtSignUp` | Immutable (historical) |

**Rule:** The snapshot records the terms at sign-up. When the plan changes (e.g., commission rate 0.20 → 0.18), the snapshot is untouched. New users signing up after the change get the new rate in their snapshot; existing users keep the old rate.

---

## 6. Validation Rules

### Optional `$jsonSchema` validation (schema-on-read → partial schema-on-write)

```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["userId", "role"],
    "properties": {
      "userId": { "bsonType": "string" },
      "role": { "enum": ["passenger", "driver", "merchant"] }
    }
  }
}
```

**What this validates:**
- `userId` must be present and a string
- `role` must be present and one of the three allowed values

**What this does NOT validate:**
- Role-specific required fields (e.g., `license` for drivers)
- Bounded-growth limits (e.g., max 10 saved places)
- Referential integrity (e.g., plan referenced actually exists)
- Data types within nested objects (e.g., `price` is a number)

**Enforcement spectrum position:** "Nothing rejects" by default; the `$jsonSchema` rule shifts it partially toward "validator rejects" for the two critical fields. Full enforcement would require application-level validation.

---

## 7. Index Strategy

| Index | Fields | Purpose | Selectivity |
|-------|--------|---------|-------------|
| Default `_id` | `_id` (auto) | Internal document lookup | Unique |
| User lookup | `{"userId": 1}` | Profile load by business key | Unique |
| Phone lookup | `{"phone": 1}` | Login by phone | Unique |
| Role filter | `{"role": 1}` | Filter by user type | Low (60%/25%/15%) |
| Licence expiry | `{"role": 1, "license.expiryDate": 1}` | Drivers with expiring licences | Compound — role narrows, then date range |
| Menu category | `{"menu.category": 1}` | Merchants by food type | Multikey (indexes each array element) |

---

## 8. Trade-Off Ledger

| Guarantee | Relational (Chapters 2–5) | Document model (Chapter 6) | Status | Management strategy |
|-----------|--------------------------|---------------------------|--------|-------------------|
| Row/document uniqueness | PRIMARY KEY | `_id` unique per collection | **Preserved** | — |
| Referential integrity | FOREIGN KEY | Not enforced | **Lost** | Application validates references on write |
| Cross-entity constraints | CHECK, UNIQUE across tables | Within single document only | **Partially lost** | Application-level validation |
| Multi-step atomicity | BEGIN/COMMIT transactions | Single-document atomic; multi-doc costly | **Preserved within aggregate** | Costly across aggregates; saga pattern for cross-model |
| No redundancy | BCNF by design | Deliberate duplication (snapshots) | **Shifted** | Snapshot discipline: label copy, identify truth, never update snapshot |
| Ad-hoc joins | JOIN on any FK path | `$lookup` in pipeline | **Available but costlier** | Design aggregates for dominant reads; accept `$lookup` cost for analytics |
| Schema enforcement | DDL + constraints reject bad data | Schema-on-read by default | **Shifted** | Opt-in via `$jsonSchema`; application validates role-specific fields |

---

## 9. Cross-Model Comparison

| Concept | Relational (Chapters 2–5) | Document (Chapter 6) |
|---------|--------------------------|---------------------|
| Unit of storage | Row (flat, fixed columns) | Document (nested, flexible fields) |
| Schema posture | Schema-on-write (DDL before insert) | Schema-on-read (structure in data) |
| Identity | Auto-increment PK or natural key | `_id` (auto `ObjectId` or natural key) |
| Relationships | JOIN on FK paths | Embed (nesting) or reference (`$lookup`) |
| Structural variation | ALTER TABLE / subtype tables | Different fields per document |
| Aggregation | `GROUP BY` + functions (FWGHOS) | Pipeline: `$match`, `$unwind`, `$group`, `$sort` |
| LEFT JOIN equivalent | `LEFT JOIN ... ON` | `$lookup` (preserves left, empty array for no match) |
| Enforcement | Engine rejects (DDL) | Nothing rejects (opt-in `$jsonSchema`) |
| Snapshot pattern | Denormalised columns with documented justification | Embedded snapshot fields with truth map |

---

## 10. Design Comparison Summary

| Dimension | Design A (aggregate-first) | Design B (reference-heavy) |
|-----------|---------------------------|---------------------------|
| Profile load | 1 `findOne` | 1 `$match` + 4 `$lookup` |
| Nested field query | Dot notation directly | Query satellite, then `$lookup` for identity |
| Within-aggregate analytics | `$unwind` + `$group` (5 stages) | `$group` directly (3 stages, no `$unwind`) |
| Cross-aggregate analytics | Add `$lookup` to pipeline | Same |
| Single-field update | 1 `updateOne` | 1 `updateOne` (same) |
| Structural variation | Natural (different fields per document) | Requires new satellite collection per concern |
| Bounded-growth risk | Document growth if bounds exceeded | No growth risk (each item is a document) |
| **Best for** | **Aggregate-read personalisation** | **Microservices with independent scaling** |
