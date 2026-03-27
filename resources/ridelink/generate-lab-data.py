#!/usr/bin/env python3
"""
RideLink Super-App — Lab Dataset Generator
============================================
Generates ~200 user profiles across both Design A (aggregate-first)
and Design B (reference-heavy) for the Chapter 6 MongoDB lab.

Usage:
    python3 generate-lab-data.py

Output:
    lab-data.js  (in the same directory)

The output file contains mongosh-compatible insertMany statements
that can be run directly in a mongo shell or pasted into %%mongodb
notebook cells.

Deterministic: random.seed(42) ensures identical output every run.
"""

import random
import json
import os

# ── Configuration ────────────────────────────────────────────
SEED = 42
random.seed(SEED)

NUM_PASSENGERS = 120
NUM_DRIVERS    = 50
NUM_MERCHANTS  = 30

# ── Reference Data ───────────────────────────────────────────

SG_ZONES = ["central", "east", "west", "north", "northeast"]

SG_STREETS = [
    "Orchard Rd", "Clementi Ave 3", "Tampines St 21", "Jurong East St 13",
    "Ang Mo Kio Ave 6", "Bedok North Rd", "Bukit Timah Rd", "Toa Payoh Lor 1",
    "Woodlands Ave 3", "Hougang Ave 8", "Serangoon Rd", "Queenstown Rd",
    "Bishan St 22", "Yishun Ring Rd", "Pasir Ris Dr 1", "Marine Parade Rd",
    "Geylang Rd", "Tiong Bahru Rd", "Holland Rd", "Balestier Rd",
]

SG_FIRST = [
    "Wei", "Jia", "Hui", "Xin", "Yi", "Zhi", "Ming", "Siti", "Nur",
    "Ahmad", "Priya", "Raj", "Kumar", "Mei", "Li", "Chen", "Aisha",
    "Hafiz", "Devi", "Ravi", "Ling", "Fang", "Hao", "Jun", "Yan",
]

SG_LAST = [
    "Tan", "Lim", "Lee", "Ng", "Wong", "Chan", "Koh", "Ong", "Goh",
    "Ibrahim", "Nair", "Singh", "Kumar", "Chen", "Lin", "Wu", "Zhang",
    "Patel", "Das", "Ali", "Yeo", "Teo", "Sim", "Chong", "Leong",
]

PLACE_LABELS = ["Home", "Office", "Gym", "School", "Parents", "MRT", "Mall",
                "Hospital", "Temple", "Church", "Mosque", "Park"]

VEHICLE_MAKES = [
    ("Toyota", "Prius"), ("Toyota", "Camry"), ("Toyota", "Corolla"),
    ("Honda", "Civic"), ("Honda", "Fit"),
    ("Hyundai", "Ioniq"), ("Hyundai", "Avante"),
    ("BYD", "e6"), ("BYD", "Atto 3"),
    ("Kia", "Cerato"), ("Kia", "Niro"),
]

BIKE_MODELS = ["Niu NQi GTS", "Honda PCX", "Yamaha NMAX", "Vespa Sprint",
               "Gogoro Viva", "NIU MQi+"]

FOOD_NAMES = {
    "mains":    ["Nasi Lemak", "Laksa", "Char Kway Teow", "Mee Goreng",
                 "Fish Soup", "Roti Prata", "Satay Set", "Bak Kut Teh",
                 "Hokkien Mee", "Chicken Chop", "Nasi Padang", "Duck Rice",
                 "Wanton Mee", "Claypot Rice", "Yong Tau Foo"],
    "sides":    ["Fried Wonton", "Spring Roll", "Curry Puff", "Otah",
                 "Popiah", "Ngoh Hiang", "Prawn Fritter"],
    "drinks":   ["Teh Tarik", "Kopi-O", "Milo Dinosaur", "Bandung",
                 "Lime Juice", "Barley Water", "Soya Bean"],
    "desserts": ["Ice Kachang", "Chendol", "Tau Huay", "Pulut Hitam",
                 "Bubur Cha Cha", "Mango Sago"],
    "snacks":   ["Egg Tart", "Kueh Lapis", "Ondeh Ondeh", "Goreng Pisang",
                 "Roti John", "Muah Chee"],
}
FOOD_CATS = list(FOOD_NAMES.keys())

CUISINES = ["Chinese", "Malay", "Indian", "Western", "Beverages",
            "Desserts", "Japanese", "Korean", "Thai", "Vietnamese"]

BIZ_SUFFIXES = ["Kitchen", "Cafe", "Bistro", "Food Stall", "Bakery",
                "Noodle House", "Kopitiam", "Eatery", "Corner", "Express"]

# ── Plans ────────────────────────────────────────────────────
# These are the editable-truth plans. Users embed only snapshots.

PLANS = [
    {"planId": "plan-premium",          "name": "GrabCar Premium",       "commissionRate": 0.20, "features": ["priority-matching", "lounge-access", "premium-support"],                "monthlyPrice": 29.99, "tier": "premium"},
    {"planId": "plan-standard",         "name": "GrabCar Standard",      "commissionRate": 0.25, "features": ["standard-matching"],                                                    "monthlyPrice":  0.00, "tier": "standard"},
    {"planId": "plan-driver-flexi",     "name": "Driver Flexi",          "commissionRate": 0.22, "features": ["flexible-hours", "standard-matching"],                                  "monthlyPrice":  9.99, "tier": "standard"},
    {"planId": "plan-premium-plus",     "name": "GrabCar Premium Plus",  "commissionRate": 0.18, "features": ["priority-matching", "lounge-access", "premium-support", "ev-priority"], "monthlyPrice": 49.99, "tier": "premium"},
    {"planId": "plan-basic",            "name": "GrabCar Basic",         "commissionRate": 0.28, "features": ["standard-matching"],                                                    "monthlyPrice":  0.00, "tier": "standard"},
    {"planId": "plan-grabfood-partner", "name": "GrabFood Partner",      "commissionRate": 0.30, "features": ["food-delivery", "merchant-dashboard"],                                  "monthlyPrice":  0.00, "tier": "partner"},
    {"planId": "plan-grabfood-standard","name": "GrabFood Standard",     "commissionRate": 0.35, "features": ["food-delivery"],                                                       "monthlyPrice":  0.00, "tier": "standard"},
    {"planId": "plan-grabfood-elite",   "name": "GrabFood Elite",        "commissionRate": 0.28, "features": ["food-delivery", "merchant-dashboard", "priority-listing"],              "monthlyPrice": 14.99, "tier": "partner"},
    {"planId": "plan-merchant-pro",     "name": "Merchant Pro",          "commissionRate": 0.25, "features": ["featured-placement", "analytics-access", "food-delivery"],              "monthlyPrice": 19.99, "tier": "premium"},
    {"planId": "plan-merchant-basic",   "name": "Merchant Basic",        "commissionRate": 0.32, "features": ["food-delivery", "basic-dashboard"],                                    "monthlyPrice":  0.00, "tier": "standard"},
]

PASSENGER_PLANS = [p for p in PLANS if "GrabCar" in p["name"]]
DRIVER_PLANS = [p for p in PLANS if any(f in str(p["features"]) for f in ["matching", "flexible"]) and "GrabCar" in p["name"]]
FOOD_DRIVER_PLANS = [p for p in PLANS if "GrabFood" in p["name"]]
MERCHANT_PLANS = [p for p in PLANS if p["name"].startswith(("Merchant", "GrabFood"))]


# ── Helpers ──────────────────────────────────────────────────

def sg_phone(prefix="9"):
    """Generate a Singapore phone number."""
    return f"+65{prefix}{random.randint(1000000, 9999999)}"


def sg_address():
    """Generate a random Singapore-style address."""
    return f"{random.randint(1, 300)} {random.choice(SG_STREETS)}"


def sg_coords():
    """Generate random lat/lng within Singapore bounds."""
    return (round(1.25 + random.random() * 0.15, 4),
            round(103.68 + random.random() * 0.22, 4))


def random_date(year_min=2023, year_max=2025):
    """Generate a random YYYY-MM-DD date string."""
    y = random.randint(year_min, year_max)
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    return f"{y}-{m:02d}-{d:02d}"


def recent_date():
    """Generate a recent date for lastUsed fields (late 2024 to Jan 2025)."""
    offset = random.randint(0, 90)
    if offset < 30:
        return f"2025-01-{max(1, 28 - offset):02d}"
    else:
        d = offset - 30
        return f"2024-{max(10, 12 - d // 30):02d}-{max(1, 28 - d % 30):02d}"


def js_val(v):
    """Convert a Python value to a JavaScript literal string."""
    if v is None:
        return "null"
    return json.dumps(v, ensure_ascii=False)


# ── Generate Data ────────────────────────────────────────────

print("RideLink Lab Dataset Generator")
print("=" * 50)

# All data for Design A
users_a = []

# All data for Design B (satellite collections)
users_b = []
saved_places_b = []
preferences_b = []
vehicles_b = []
earnings_b = []
payment_methods_b = []
menu_items_b = []

uid_counter = 2000  # Start after slide-ready data IDs


# ── Passengers ───────────────────────────────────────────────
print(f"\nGenerating {NUM_PASSENGERS} passengers...")

for i in range(NUM_PASSENGERS):
    uid_counter += 1
    user_id = f"passenger-{uid_counter}"
    fn = random.choice(SG_FIRST)
    ln = random.choice(SG_LAST)
    phone = sg_phone("9")
    email = f"{fn.lower()}{uid_counter}@example.com"
    tier = random.choice(["standard"] * 3 + ["premium"])

    # Saved places (0–5; some passengers have none yet)
    n_places = random.randint(0, 5)
    places = []
    used_labels = set()
    for _ in range(n_places):
        label = random.choice(PLACE_LABELS)
        while label in used_labels:
            label = random.choice(PLACE_LABELS)
        used_labels.add(label)
        lat, lng = sg_coords()
        freq = random.choice(["daily", "weekday", "weekly", "monthly"])
        places.append({
            "label": label,
            "address": sg_address(),
            "lat": lat,
            "lng": lng,
            "frequency": freq,
            "lastUsed": recent_date(),
        })

    # Payment methods (1–3)
    n_pms = random.randint(1, 3)
    pms = []
    for k in range(n_pms):
        pm_type = random.choice(["card", "grabpay"])
        pm = {"type": pm_type, "isDefault": k == 0}
        if pm_type == "card":
            pm["last4"] = f"{random.randint(1000, 9999)}"
        elif pm_type == "grabpay":
            pm["balance"] = round(random.uniform(0, 200), 2)
        pms.append(pm)

    # Ride preferences
    ride_prefs = {
        "vehicleType": random.choice(["JustGrab", "GrabCar", "GrabShare"]),
        "quietRide": random.choice([True, False]),
        "temperature": random.choice(["cold", "normal"]),
    }

    # Build Design A document
    user_doc = {
        "userId": user_id,
        "displayName": f"{fn} {ln}",
        "phone": phone,
        "email": email,
        "role": "passenger",
        "tier": tier,
        "savedPlaces": places,
        "paymentMethods": pms,
        "ridePreferences": ride_prefs,
        "rewardPoints": random.randint(0, 20000),
    }

    if tier == "premium":
        plan = random.choice(PASSENGER_PLANS)
        user_doc["loyaltyTier"] = random.choice(["gold", "platinum"])
        user_doc["loungeAccess"] = True
        user_doc["subscriptionSnapshot"] = {
            "planNameAtSignUp": plan["name"],
            "priceAtSignUp": plan["monthlyPrice"],
            "signUpDate": random_date(2023, 2024),
        }

    users_a.append(user_doc)

    # Design B: core identity
    core = {
        "userId": user_id,
        "displayName": f"{fn} {ln}",
        "phone": phone,
        "email": email,
        "role": "passenger",
        "tier": tier,
    }
    users_b.append(core)

    # Design B: satellite collections
    for p in places:
        saved_places_b.append(dict(p, userId=user_id))
    for pm in pms:
        payment_methods_b.append(dict(pm, userId=user_id))
    preferences_b.append({"userId": user_id, "ridePreferences": ride_prefs})

print(f"  → {NUM_PASSENGERS} passengers generated")
print(f"    ({sum(1 for u in users_a[-NUM_PASSENGERS:] if u.get('tier') == 'premium')} premium)")


# ── Drivers ──────────────────────────────────────────────────
print(f"\nGenerating {NUM_DRIVERS} drivers...")

for i in range(NUM_DRIVERS):
    uid_counter += 1
    user_id = f"driver-{uid_counter}"
    fn = random.choice(SG_FIRST)
    ln = random.choice(SG_LAST)
    phone = sg_phone("8")
    email = f"{fn.lower()}{uid_counter}@example.com"
    is_food = random.random() < 0.3

    plan = random.choice(FOOD_DRIVER_PLANS if is_food else DRIVER_PLANS)
    zones = random.sample(SG_ZONES, random.randint(1, 3))

    # Licence expiry: spread across 2025, 2026, 2027 (for dot notation queries)
    exp_y = random.choice([2025, 2026, 2027])
    exp_m = random.randint(1, 12)
    exp_d = random.randint(1, 28)

    prefs = {
        "maxDistance": random.choice([10, 15, 20, 25, 30]),
        "preferredZones": zones,
        "autoAccept": random.choice([True, False]),
    }

    earnings_doc = {
        "currentWeek": round(random.uniform(200, 2000), 2),
        "incentiveProgress": {
            "ridesCompleted": random.randint(10, 80),
            "target": random.choice([50, 75, 100]),
            "bonus": round(random.uniform(30, 150), 2),
        },
    }

    license_doc = {
        "licenseNumber": f"S{random.randint(1000000, 9999999)}{random.choice('ABCDEFG')}",
        "expiryDate": f"{exp_y}-{exp_m:02d}-{exp_d:02d}",
        "vocationalLicenseExpiry": f"{exp_y}-{exp_m:02d}-{exp_d:02d}",
    }

    user_doc = {
        "userId": user_id,
        "displayName": f"{fn} {ln}",
        "phone": phone,
        "email": email,
        "role": "driver",
        "driverType": "grabfood" if is_food else "grabcar",
        "license": license_doc,
        "preferences": prefs,
        "earnings": earnings_doc,
        "subscriptionSnapshot": {
            "planNameAtSignUp": plan["name"],
            "commissionRateAtSignUp": plan["commissionRate"],
            "signUpDate": random_date(2023, 2024),
        },
    }

    # Vehicle or bike depending on type
    if is_food:
        user_doc["bike"] = {
            "type": "electric_scooter",
            "model": random.choice(BIKE_MODELS),
            "plateNumber": f"FB{random.choice('ABCDE')}{random.randint(1000, 9999)}{random.choice('WXYZ')}",
        }
        user_doc["thermalBagCertified"] = random.choice([True, True, True, False])
        user_doc["deliveryZone"] = random.choice(SG_ZONES)
    else:
        make, model = random.choice(VEHICLE_MAKES)
        user_doc["vehicle"] = {
            "make": make,
            "model": model,
            "year": random.randint(2018, 2024),
            "plateNumber": f"S{random.choice('BCDEFG')}{random.choice('ABCDE')}{random.randint(1000, 9999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
            "vehicleType": random.choice(["standard", "premium"]),
        }

    pm = {"type": "bank_transfer", "last4": f"{random.randint(1000, 9999)}", "isDefault": True}
    user_doc["paymentMethods"] = [pm]

    users_a.append(user_doc)

    # Design B
    core = {
        "userId": user_id,
        "displayName": f"{fn} {ln}",
        "phone": phone,
        "email": email,
        "role": "driver",
        "driverType": user_doc["driverType"],
    }
    users_b.append(core)

    veh_doc = {"userId": user_id, "license": license_doc}
    if "vehicle" in user_doc:
        veh_doc["vehicle"] = user_doc["vehicle"]
    if "bike" in user_doc:
        veh_doc["bike"] = user_doc["bike"]
        veh_doc["thermalBagCertified"] = user_doc.get("thermalBagCertified", False)
        veh_doc["deliveryZone"] = user_doc.get("deliveryZone")
    vehicles_b.append(veh_doc)

    earnings_b.append({"userId": user_id, "earnings": earnings_doc})
    preferences_b.append({"userId": user_id, "preferences": prefs})
    payment_methods_b.append(dict(pm, userId=user_id))

food_count = sum(1 for u in users_a[-NUM_DRIVERS:] if u.get("driverType") == "grabfood")
print(f"  → {NUM_DRIVERS} drivers generated ({food_count} GrabFood, {NUM_DRIVERS - food_count} GrabCar)")


# ── Merchants ────────────────────────────────────────────────
print(f"\nGenerating {NUM_MERCHANTS} merchants...")

total_menu_items = 0

for i in range(NUM_MERCHANTS):
    uid_counter += 1
    user_id = f"merchant-{uid_counter}"
    fn = random.choice(SG_FIRST)
    ln = random.choice(SG_LAST)
    phone = sg_phone("6")
    email = f"{fn.lower()}{uid_counter}@example.com"
    plan = random.choice(MERCHANT_PLANS)
    biz_name = f"{fn}'s {random.choice(BIZ_SUFFIXES)}"
    cuisine = random.choice(CUISINES)

    # Menu items (4–20): sample without replacement for natural names
    n_items = random.randint(4, 20)
    all_food = [(name, cat) for cat, names in FOOD_NAMES.items() for name in names]
    pool = all_food.copy()
    random.shuffle(pool)
    selected = pool[:n_items]

    menu = []
    for item_name, cat in selected:
        price = round(random.uniform(1.50, 15.00), 2)

        # Customisations (0–3)
        custs = []
        if random.random() > 0.3:
            custs.append({"name": "Less spicy", "price": 0.00})
        if random.random() > 0.6:
            custs.append({"name": "Extra portion", "price": round(random.uniform(0.50, 2.00), 2)})
        if random.random() > 0.8:
            custs.append({"name": "Add topping", "price": round(random.uniform(0.50, 1.50), 2)})

        menu.append({
            "itemName": item_name,
            "price": price,
            "category": cat,
            "customisations": custs,
        })

    total_menu_items += len(menu)

    # Operating hours (closed on a random day)
    closed_day = random.choice(["monday", "tuesday", "wednesday", "thursday",
                                "friday", "saturday", "sunday"])
    hours = {}
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        if day == closed_day:
            hours[day] = None
        elif day in ("saturday", "sunday"):
            hours[day] = {"open": "09:00", "close": "22:00"}
        else:
            hours[day] = {"open": "10:00", "close": "21:00"}

    # Promotions (0–2)
    promos = []
    if random.random() > 0.6:
        promos.append({
            "code": f"{fn.upper()}{random.randint(10, 99)}",
            "discount": round(random.choice([0.05, 0.10, 0.15, 0.20]), 2),
            "validUntil": random_date(2025, 2025),
        })

    user_doc = {
        "userId": user_id,
        "displayName": fn,
        "phone": phone,
        "email": email,
        "role": "merchant",
        "businessName": biz_name,
        "cuisine": cuisine,
        "operatingHours": hours,
        "menu": menu,
        "promotions": promos,
        "subscriptionSnapshot": {
            "planNameAtSignUp": plan["name"],
            "commissionRateAtSignUp": plan["commissionRate"],
            "signUpDate": random_date(2023, 2024),
        },
    }

    users_a.append(user_doc)

    # Design B
    core = {
        "userId": user_id,
        "displayName": fn,
        "phone": phone,
        "email": email,
        "role": "merchant",
        "businessName": biz_name,
    }
    users_b.append(core)

    preferences_b.append({"userId": user_id, "operatingHours": hours})

    for item in menu:
        menu_items_b.append(dict(item, merchantId=user_id))

print(f"  → {NUM_MERCHANTS} merchants generated ({total_menu_items} total menu items)")


# ── Summary ──────────────────────────────────────────────────
total_users = NUM_PASSENGERS + NUM_DRIVERS + NUM_MERCHANTS

print(f"\n{'=' * 50}")
print(f"Design A totals:")
print(f"  users:           {total_users:>6}")
print(f"  plans:           {len(PLANS):>6}")
print(f"\nDesign B totals:")
print(f"  users_b:         {len(users_b):>6}")
print(f"  savedPlaces_b:   {len(saved_places_b):>6}")
print(f"  preferences_b:   {len(preferences_b):>6}")
print(f"  vehicles_b:      {len(vehicles_b):>6}")
print(f"  earnings_b:      {len(earnings_b):>6}")
print(f"  paymentMethods_b:{len(payment_methods_b):>6}")
print(f"  menuItems_b:     {len(menu_items_b):>6}")
print(f"  plans:           {len(PLANS):>6}")


# ── Write JavaScript ─────────────────────────────────────────

script_dir = os.path.dirname(os.path.abspath(__file__))
outpath = os.path.join(script_dir, "lab-data.js")

print(f"\nWriting JS to {outpath}...")


def write_insert_many(f, collection, docs, batch_size=500):
    """Write insertMany statements, batched for large arrays."""
    for start in range(0, len(docs), batch_size):
        batch = docs[start:start + batch_size]
        f.write(f"db.{collection}.insertMany(\n")
        f.write(json.dumps(batch, indent=2, ensure_ascii=False, default=str))
        f.write("\n);\n\n")


with open(outpath, "w") as f:
    f.write("// ============================================================\n")
    f.write("// RideLink Super-App — Lab Dataset\n")
    f.write("// ============================================================\n")
    f.write(f"// Auto-generated by generate-lab-data.py\n")
    f.write(f"// Seed: {SEED}  (deterministic — same output every run)\n")
    f.write("//\n")
    f.write(f"// Design A:\n")
    f.write(f"//   users:            {total_users:>6}\n")
    f.write(f"//   plans:            {len(PLANS):>6}\n")
    f.write("//\n")
    f.write(f"// Design B:\n")
    f.write(f"//   users_b:          {len(users_b):>6}\n")
    f.write(f"//   savedPlaces_b:    {len(saved_places_b):>6}\n")
    f.write(f"//   preferences_b:    {len(preferences_b):>6}\n")
    f.write(f"//   vehicles_b:       {len(vehicles_b):>6}\n")
    f.write(f"//   earnings_b:       {len(earnings_b):>6}\n")
    f.write(f"//   paymentMethods_b: {len(payment_methods_b):>6}\n")
    f.write(f"//   menuItems_b:      {len(menu_items_b):>6}\n")
    f.write(f"//   plans:            {len(PLANS):>6}\n")
    f.write("//\n")
    f.write(f"// Distribution: ~{NUM_PASSENGERS} passengers ({NUM_PASSENGERS/total_users*100:.0f}%),")
    f.write(f" ~{NUM_DRIVERS} drivers ({NUM_DRIVERS/total_users*100:.0f}%),")
    f.write(f" ~{NUM_MERCHANTS} merchants ({NUM_MERCHANTS/total_users*100:.0f}%)\n")
    f.write("//\n")
    f.write("// Prerequisites: run seed-data.js first (slide-ready data).\n")
    f.write("// ============================================================\n\n")

    # ── Plans ──
    f.write("// ── Plans (shared across both designs) ──\n")
    f.write("// Upsert to avoid duplicates if slide-ready data already loaded.\n")
    for plan in PLANS:
        f.write(f'db.plans.updateOne({{planId: {js_val(plan["planId"])}}}, {{$set: {json.dumps(plan, ensure_ascii=False)}}}, {{upsert: true}});\n')
    f.write("\n")

    # ── Design A ──
    f.write("// ── Design A: Aggregate-first (users collection) ──\n")
    write_insert_many(f, "users", users_a)

    # ── Design B ──
    f.write("// ── Design B: Reference-heavy (satellite collections) ──\n\n")

    f.write("// Core identity\n")
    write_insert_many(f, "users_b", users_b)

    f.write("// Saved places\n")
    write_insert_many(f, "savedPlaces_b", saved_places_b)

    f.write("// Preferences\n")
    write_insert_many(f, "preferences_b", preferences_b)

    f.write("// Vehicles and licences\n")
    write_insert_many(f, "vehicles_b", vehicles_b)

    f.write("// Earnings\n")
    write_insert_many(f, "earnings_b", earnings_b)

    f.write("// Payment methods\n")
    write_insert_many(f, "paymentMethods_b", payment_methods_b)

    f.write("// Menu items\n")
    write_insert_many(f, "menuItems_b", menu_items_b)

print(f"Done. {os.path.getsize(outpath):,} bytes written.")
