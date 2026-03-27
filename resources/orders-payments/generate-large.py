#!/usr/bin/env python3
"""
Orders & Payments — Large Dataset Generator
=============================================
Generates ~100K+ order_lines rows with realistic skewed distributions
for lab exercises and star schema demonstrations.

Usage:
    python3 orders-payments-generate-large.py

Output:
    orders-payments-large-data.sql  (in the same directory)

Deterministic: random.seed(42) ensures identical output every run.
"""

import random
import os
from datetime import date, timedelta
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

# ── Configuration ────────────────────────────────────────────
SEED = 42
random.seed(SEED)

NUM_POSTCODES    = 500
NUM_CUSTOMERS    = 2_000
NUM_PRODUCTS     = 200
NUM_ORDERS       = 20_000
NUM_CATEGORIES   = 15
NUM_SUPPLIERS    = 30
TARGET_LINES     = 100_000   # approximate; actual depends on per-order sampling
DATE_START       = date(2022, 1, 1)
DATE_END         = date(2024, 12, 31)
REVIEW_RATE      = 0.08      # probability a (customer, product) purchase generates a review
PAYMENT_RATE     = 0.95      # fraction of orders that have been paid
SHIPPING_RATE    = 0.85      # fraction of orders that have been shipped

BATCH_SIZE       = 1_000     # rows per INSERT for MySQL performance

# ── Helpers ──────────────────────────────────────────────────

_zipf_cache = {}

def zipf_choice(n, a=1.5):
    """Return an index 0..n-1 with Zipf-like skew (weights cached)."""
    key = (n, a)
    if key not in _zipf_cache:
        _zipf_cache[key] = [1.0 / (i + 1) ** a for i in range(n)]
    return random.choices(range(n), weights=_zipf_cache[key], k=1)[0]


def random_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def sql_str(s):
    """Escape single quotes for SQL string literals."""
    return s.replace("'", "''")


def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


# ── UK-style postcode + city data ────────────────────────────

UK_CITIES = [
    "London", "Manchester", "Birmingham", "Leeds", "Glasgow",
    "Liverpool", "Edinburgh", "Bristol", "Sheffield", "Newcastle",
    "Nottingham", "Cardiff", "Belfast", "Leicester", "Brighton",
    "Southampton", "Plymouth", "Reading", "Derby", "Coventry",
    "Oxford", "Cambridge", "York", "Bath", "Exeter",
    "Norwich", "Aberdeen", "Dundee", "Swansea", "Wolverhampton",
]

POSTCODE_AREAS = [
    "SW1A", "EC1A", "W1", "N1", "E1", "SE1", "NW1",
    "M1", "M2", "M3", "B1", "B2", "LS1", "LS2",
    "G1", "G2", "L1", "L2", "EH1", "EH2",
    "BS1", "BS2", "S1", "S2", "NE1", "NE2",
    "NG1", "CF1", "BT1", "LE1", "BN1",
    "SO1", "PL1", "RG1", "DE1", "CV1",
    "OX1", "CB1", "YO1", "BA1", "EX1",
    "NR1", "AB1", "DD1", "SA1", "WV1",
]

FIRST_NAMES = [
    "Alice", "Bob", "Carol", "Dave", "Eve", "Fiona", "George",
    "Hannah", "Ian", "Julia", "Kevin", "Laura", "Martin", "Nina",
    "Oscar", "Priya", "Quentin", "Rachel", "Sam", "Tara",
    "Uma", "Victor", "Wendy", "Xavier", "Yuki", "Zara",
    "Aiden", "Bella", "Caleb", "Diana", "Ethan", "Freya",
    "Gavin", "Holly", "Isaac", "Jade", "Kyle", "Lily",
    "Mason", "Nora", "Owen", "Piper", "Quinn", "Ruby",
    "Sean", "Thea", "Ulric", "Vera", "Will", "Xena",
]

LAST_NAMES = [
    "Chen", "Patel", "Liu", "Kim", "Brown", "Smith", "Jones",
    "Williams", "Taylor", "Wilson", "Davies", "Evans", "Thomas",
    "Roberts", "Walker", "Wright", "Hall", "Clarke", "Green",
    "Hill", "Scott", "Adams", "Baker", "Carter", "Cox",
    "Diaz", "Ellis", "Fisher", "Gray", "Hunt", "Iqbal",
    "Jackson", "Khan", "Lewis", "Morris", "Nash", "Owens",
    "Price", "Quinn", "Reed", "Shaw", "Turner", "Upton",
    "Vance", "Walsh", "Young", "Zhang", "Ali", "Bell",
    "Cook", "Day", "Ford", "Grant", "Hart", "Irwin",
    "James", "King", "Lane", "Moore", "Nolan", "Park",
]

PRODUCT_ADJECTIVES = [
    "Pro", "Lite", "Ultra", "Mini", "Max", "Plus", "Eco",
    "Smart", "Turbo", "Flex", "Core", "Edge", "Prime", "Air",
]

PRODUCT_NOUNS = [
    "Widget", "Gadget", "Cable", "Adapter", "Screen", "Keyboard",
    "Mouse", "Hub", "Charger", "Speaker", "Webcam", "Stand",
    "Dock", "Light", "Headset", "Stylus", "Sensor", "Module",
    "Board", "Case",
]

CATEGORIES = [
    ("Peripherals", "Input and output devices"),
    ("Cables", "Connectivity accessories"),
    ("Displays", "Monitors and screens"),
    ("Audio", "Speakers and headsets"),
    ("Power", "Chargers and power supplies"),
    ("Storage", "External drives and memory"),
    ("Networking", "Routers and adapters"),
    ("Input Devices", "Keyboards and mice"),
    ("Lighting", "Desk and monitor lights"),
    ("Stands & Mounts", "Ergonomic accessories"),
    ("Docking", "Docking stations and hubs"),
    ("Sensors", "Environmental and motion sensors"),
    ("Boards", "Development and prototyping boards"),
    ("Cases", "Device protection"),
    ("Accessories", "General accessories"),
]

SUPPLIER_NAMES = [
    "TechParts Ltd", "CableCo", "ScreenVision", "AudioWave",
    "PowerCell", "StoragePlus", "NetLink", "InputPro",
    "BrightLight", "DeskMount", "DockHub", "SensorTech",
    "BoardWorks", "CaseCraft", "GadgetSource", "MicroSupply",
    "ChipDirect", "WireWorld", "PlugPoint", "DeviceDepot",
    "CircuitCity", "TechWholesale", "ComponentCo", "PartsPrime",
    "ElectraTrade", "GizmoGlobal", "HardwareHub", "ModuleMart",
    "PeripheralPro", "SupplyStack",
]

PAYMENT_METHODS = ["card", "paypal", "bank_transfer"]
ORDER_STATUSES  = ["pending", "paid", "shipped", "delivered", "completed"]
SHIP_STATUSES   = ["shipped", "in_transit", "delivered"]

STREET_NAMES = [
    "High St", "Park Ave", "Rose Ln", "Main Rd", "Church St",
    "Queen St", "King St", "Station Rd", "Mill Ln", "Bridge St",
    "Green Ln", "Victoria Rd", "Albert St", "Market St", "York Rd",
    "Castle St", "George St", "New Rd", "West St", "North Ln",
]

# ── Generate data ────────────────────────────────────────────

print("Generating postcodes...")
postcodes = []
for i in range(NUM_POSTCODES):
    area = POSTCODE_AREAS[i % len(POSTCODE_AREAS)]
    num = (i // len(POSTCODE_AREAS)) + 1
    suffix = f"{random.randint(1,9)}{chr(65 + random.randint(0,25))}{chr(65 + random.randint(0,25))}"
    pc = f"{area} {num}{suffix}"
    city = UK_CITIES[i % len(UK_CITIES)]
    postcodes.append((pc, city))

print("Generating customers...")
customers = []
used_emails = set()
for i in range(1, NUM_CUSTOMERS + 1):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    # Ensure unique email
    base_email = f"{first.lower()}.{last.lower()}{i}@example.com"
    email = base_email
    while email in used_emails:
        email = f"{first.lower()}.{last.lower()}{i}{random.randint(10,99)}@example.com"
    used_emails.add(email)
    # 3% have NULL postcode (LEFT JOIN demo at scale)
    if random.random() < 0.03:
        pc = None
    else:
        pc = postcodes[zipf_choice(NUM_POSTCODES, a=1.2)][0]
    customers.append((i, name, email, pc))

print("Generating products...")
products = []
used_product_names = set()
for i in range(1, NUM_PRODUCTS + 1):
    while True:
        adj = random.choice(PRODUCT_ADJECTIVES)
        noun = random.choice(PRODUCT_NOUNS)
        variant = random.randint(100, 999)
        pname = f"{adj} {noun} {variant}"
        if pname not in used_product_names:
            used_product_names.add(pname)
            break
    # Price: skewed — most cheap, some expensive
    price_tier = random.random()
    if price_tier < 0.4:
        price = round(random.uniform(2.99, 14.99), 2)
    elif price_tier < 0.7:
        price = round(random.uniform(15.00, 49.99), 2)
    elif price_tier < 0.9:
        price = round(random.uniform(50.00, 149.99), 2)
    else:
        price = round(random.uniform(150.00, 499.99), 2)
    stock = random.randint(10, 2000)
    products.append((i, pname, price, stock))

# ── Lookup dicts for O(1) access ─────────────────────────────
product_price = {p[0]: p[2] for p in products}
customer_postcode = {c[0]: c[3] for c in customers}
postcode_city = {p[0]: p[1] for p in postcodes}

print("Generating categories...")
categories = [(i + 1, CATEGORIES[i][0], CATEGORIES[i][1]) for i in range(NUM_CATEGORIES)]

print("Generating product-category mappings...")
product_categories = []
for pid in range(1, NUM_PRODUCTS + 1):
    # Each product in 1–3 categories
    n_cats = random.choices([1, 2, 3], weights=[0.5, 0.35, 0.15], k=1)[0]
    cats = random.sample(range(1, NUM_CATEGORIES + 1), min(n_cats, NUM_CATEGORIES))
    for cid in cats:
        product_categories.append((pid, cid))

print("Generating suppliers...")
suppliers = [(i + 1, SUPPLIER_NAMES[i], f"sales{i+1}@{SUPPLIER_NAMES[i].lower().replace(' ', '').replace('&', '')}.co.uk")
             for i in range(NUM_SUPPLIERS)]

print("Generating supplier-product mappings...")
supplier_products = []
for pid in range(1, NUM_PRODUCTS + 1):
    # 90% of products have 1–2 suppliers; 10% have none (sparsity demo)
    if random.random() < 0.10:
        continue
    n_sup = random.choices([1, 2], weights=[0.7, 0.3], k=1)[0]
    sups = random.sample(range(1, NUM_SUPPLIERS + 1), min(n_sup, NUM_SUPPLIERS))
    for sid in sups:
        supplier_products.append((sid, pid))

print("Generating orders...")
orders = []
order_customer_map = {}
for oid in range(1, NUM_ORDERS + 1):
    # Zipf: some customers order much more often
    cid = customers[zipf_choice(NUM_CUSTOMERS, a=1.3)][0]
    inv = f"INV-{random.randint(2022, 2024)}-{oid:06d}"
    odate = random_date(DATE_START, DATE_END)
    # Status distribution: mostly completed
    status = random.choices(
        ORDER_STATUSES,
        weights=[0.05, 0.08, 0.07, 0.10, 0.70],
        k=1
    )[0]
    orders.append((oid, cid, inv, odate, status, None))  # order_total = NULL (trigger)
    order_customer_map[oid] = cid

print("Generating order lines...")
order_lines = []

# Distribute ~TARGET_LINES across orders
# Most orders: 3–7 lines; some: 1–2; a few: 8–15
lines_remaining = TARGET_LINES
order_ids = list(range(1, NUM_ORDERS + 1))
random.shuffle(order_ids)

for oid in order_ids:
    if lines_remaining <= 0:
        n_lines = random.randint(1, 3)  # minimum for remaining orders
    else:
        r = random.random()
        if r < 0.10:
            n_lines = random.randint(1, 2)
        elif r < 0.75:
            n_lines = random.randint(3, 7)
        else:
            n_lines = random.randint(8, 15)

    chosen_products = set()
    attempts = 0
    while len(chosen_products) < n_lines and attempts < n_lines * 3:
        # Zipf: some products sell much more (bestsellers)
        pid = products[zipf_choice(NUM_PRODUCTS, a=1.4)][0]
        if pid not in chosen_products:
            chosen_products.add(pid)
        attempts += 1

    for pid in chosen_products:
        qty = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            weights=[0.35, 0.25, 0.15, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.01],
            k=1
        )[0]
        unit_price = product_price[pid]
        order_lines.append((oid, pid, qty, unit_price))

    lines_remaining -= len(chosen_products)

total_lines = len(order_lines)
print(f"  → {total_lines:,} order lines generated")

# Pre-compute order totals for payment amounts (exact decimal arithmetic)
order_totals = defaultdict(lambda: Decimal("0.00"))
for oid, pid, qty, uprice in order_lines:
    order_totals[oid] += Decimal(qty) * Decimal(str(uprice))

print("Generating payments...")
payments = []
payment_id = 1
for oid, cid, inv, odate, status, _ in orders:
    if status == "pending":
        continue  # no payment for pending orders
    if random.random() > PAYMENT_RATE:
        continue
    amount = order_totals.get(oid, Decimal("0.00")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if amount <= 0:
        continue
    pdate = odate + timedelta(days=random.randint(0, 2))
    method = random.choice(PAYMENT_METHODS)
    payments.append((payment_id, oid, amount, pdate, method))
    payment_id += 1

print(f"  → {len(payments):,} payments generated")

print("Generating shipping...")
shippings = []
shipping_id = 1
for oid, cid, inv, odate, status, _ in orders:
    if status in ("pending", "paid"):
        continue
    if random.random() > SHIPPING_RATE:
        continue
    # Snapshot address
    cust_pc = customer_postcode.get(cid)
    if cust_pc:
        city = postcode_city.get(cust_pc, "London")
        pc = cust_pc
    else:
        pc_row = random.choice(postcodes)
        city = pc_row[1]
        pc = pc_row[0]
    addr = f"{random.randint(1, 200)} {random.choice(STREET_NAMES)}"
    sdate = odate + timedelta(days=random.randint(1, 5))
    sstatus = random.choice(SHIP_STATUSES)
    shippings.append((shipping_id, oid, addr, city, pc, sdate, sstatus))
    shipping_id += 1

print(f"  → {len(shippings):,} shipping records generated")

print("Generating reviews...")
reviews = []
review_id = 1
# Track earliest order date per (customer, product) pair
order_date_lookup = {o[0]: o[3] for o in orders}  # oid → order_date
customer_product_earliest = {}  # (cid, pid) → earliest order_date
for oid, pid, qty, uprice in order_lines:
    cid = order_customer_map[oid]
    odate = order_date_lookup[oid]
    key = (cid, pid)
    if key not in customer_product_earliest or odate < customer_product_earliest[key]:
        customer_product_earliest[key] = odate

comments = [
    "Excellent quality", "Good value", "Decent", "Works well",
    "As expected", "Great product", "Would buy again", "Solid build",
    "Fast delivery", "Perfect", "Not bad", "Highly recommend",
    "Average", "Does the job", "Very pleased",
    "Better than expected", "Good for the price", "Reliable",
]

for (cid, pid), earliest_date in customer_product_earliest.items():
    if random.random() < REVIEW_RATE:
        rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.10, 0.20, 0.35, 0.30], k=1)[0]
        comment = random.choice(comments)
        # reviews date: 1–90 days after purchase, capped at DATE_END
        review_offset = timedelta(days=random.randint(1, 90))
        rdate = min(earliest_date + review_offset, DATE_END)
        reviews.append((review_id, cid, pid, rating, comment, rdate))
        review_id += 1

print(f"  → {len(reviews):,} reviews generated")

# ── Write SQL ────────────────────────────────────────────────

script_dir = os.path.dirname(os.path.abspath(__file__))
outpath = os.path.join(script_dir, "large-data.sql")

print(f"\nWriting SQL to {outpath}...")

with open(outpath, "w") as f:
    f.write("-- ============================================================\n")
    f.write("-- Orders & Payments — Large Dataset (~100K+ order_lines rows)\n")
    f.write("-- ============================================================\n")
    f.write("-- Auto-generated by orders-payments-generate-large.py\n")
    f.write(f"-- Seed: {SEED}  (deterministic — same output every run)\n")
    f.write(f"--\n")
    f.write(f"-- Row counts:\n")
    f.write(f"--   postcodes:        {NUM_POSTCODES:>7,}\n")
    f.write(f"--   customers:        {NUM_CUSTOMERS:>7,}\n")
    f.write(f"--   products:         {NUM_PRODUCTS:>7,}\n")
    f.write(f"--   orders:          {NUM_ORDERS:>7,}\n")
    f.write(f"--   order_lines:       {total_lines:>7,}\n")
    f.write(f"--   payments:         {len(payments):>7,}\n")
    f.write(f"--   shipments:        {len(shippings):>7,}\n")
    f.write(f"--   reviews:          {len(reviews):>7,}\n")
    f.write(f"--   categories:        {NUM_CATEGORIES:>7}\n")
    f.write(f"--   product_categories: {len(product_categories):>7,}\n")
    f.write(f"--   suppliers:        {NUM_SUPPLIERS:>7}\n")
    f.write(f"--   supplier_products: {len(supplier_products):>7,}\n")
    f.write("--\n")
    f.write("-- Prerequisites: run orders-payments-ddl.sql first.\n")
    f.write("-- ============================================================\n\n")
    f.write("USE orders_payments;\n\n")

    # Disable FK checks and autocommit for bulk loading
    f.write("-- Bulk-load optimisations\n")
    f.write("SET FOREIGN_KEY_CHECKS = 0;\n")
    f.write("SET autocommit = 0;\n")
    f.write("SET unique_checks = 0;\n\n")

    # ── Postcodes ──
    f.write("-- Postcodes\n")
    for batch in chunked(postcodes, BATCH_SIZE):
        f.write("INSERT INTO postcodes (postcode, city) VALUES\n")
        lines = []
        for pc, city in batch:
            lines.append(f"  ('{sql_str(pc)}', '{sql_str(city)}')")
        f.write(",\n".join(lines) + ";\n\n")

    # ── Customers ──
    f.write("-- Customers\n")
    for batch in chunked(customers, BATCH_SIZE):
        f.write("INSERT INTO customers (customer_id, name, email, postcode) VALUES\n")
        lines = []
        for cid, name, email, pc in batch:
            pc_val = f"'{sql_str(pc)}'" if pc else "NULL"
            lines.append(f"  ({cid}, '{sql_str(name)}', '{sql_str(email)}', {pc_val})")
        f.write(",\n".join(lines) + ";\n\n")

    # ── Products ──
    f.write("-- Products\n")
    for batch in chunked(products, BATCH_SIZE):
        f.write("INSERT INTO products (product_id, name, price, quantity_in_stock) VALUES\n")
        lines = []
        for pid, pname, price, stock in batch:
            lines.append(f"  ({pid}, '{sql_str(pname)}', {price:.2f}, {stock})")
        f.write(",\n".join(lines) + ";\n\n")

    # ── Orders ──
    f.write("-- Orders (order_total = NULL; triggers populate it from order_lines inserts)\n")
    for batch in chunked(orders, BATCH_SIZE):
        f.write("INSERT INTO orders (order_id, customer_id, invoice_number, order_date, status, order_total) VALUES\n")
        lines = []
        for oid, cid, inv, odate, status, _ in batch:
            lines.append(f"  ({oid}, {cid}, '{sql_str(inv)}', '{odate}', '{sql_str(status)}', NULL)")
        f.write(",\n".join(lines) + ";\n\n")

    f.write("COMMIT;\n\n")

    # ── Temporarily disable triggers for bulk order_lines insert ──
    f.write("-- Disable order_total triggers for bulk loading performance.\n")
    f.write("-- We recalculate order_total in one pass after all lines are loaded.\n")
    f.write("DROP TRIGGER IF EXISTS trg_orderline_after_insert;\n")
    f.write("DROP TRIGGER IF EXISTS trg_orderline_after_update;\n")
    f.write("DROP TRIGGER IF EXISTS trg_orderline_after_delete;\n\n")

    # ── order_lines ──
    f.write("-- order_lines\n")
    for batch in chunked(order_lines, BATCH_SIZE):
        f.write("INSERT INTO order_lines (order_id, product_id, quantity, unit_price) VALUES\n")
        lines = []
        for oid, pid, qty, uprice in batch:
            lines.append(f"  ({oid}, {pid}, {qty}, {uprice:.2f})")
        f.write(",\n".join(lines) + ";\n\n")

    f.write("COMMIT;\n\n")

    # ── Bulk-update order_total ──
    f.write("-- Bulk-recalculate order_total from order_lines data\n")
    f.write("UPDATE orders o\n")
    f.write("SET    o.order_total = (\n")
    f.write("         SELECT COALESCE(SUM(ol.quantity * ol.unit_price), 0)\n")
    f.write("         FROM   order_lines ol\n")
    f.write("         WHERE  ol.order_id = o.order_id\n")
    f.write("       );\n\n")
    f.write("COMMIT;\n\n")

    # ── Recreate triggers ──
    f.write("-- Recreate order_total triggers\n")
    f.write("DELIMITER //\n\n")
    f.write("CREATE TRIGGER trg_orderline_after_insert\n")
    f.write("AFTER INSERT ON order_lines\n")
    f.write("FOR EACH ROW\n")
    f.write("BEGIN\n")
    f.write("  UPDATE orders\n")
    f.write("  SET    order_total = (\n")
    f.write("           SELECT SUM(ol.quantity * ol.unit_price)\n")
    f.write("           FROM   order_lines ol\n")
    f.write("           WHERE  ol.order_id = NEW.order_id\n")
    f.write("         )\n")
    f.write("  WHERE  order_id = NEW.order_id;\n")
    f.write("END//\n\n")
    f.write("CREATE TRIGGER trg_orderline_after_update\n")
    f.write("AFTER UPDATE ON order_lines\n")
    f.write("FOR EACH ROW\n")
    f.write("BEGIN\n")
    f.write("  UPDATE orders\n")
    f.write("  SET    order_total = (\n")
    f.write("           SELECT SUM(ol.quantity * ol.unit_price)\n")
    f.write("           FROM   order_lines ol\n")
    f.write("           WHERE  ol.order_id = NEW.order_id\n")
    f.write("         )\n")
    f.write("  WHERE  order_id = NEW.order_id;\n")
    f.write("END//\n\n")
    f.write("CREATE TRIGGER trg_orderline_after_delete\n")
    f.write("AFTER DELETE ON order_lines\n")
    f.write("FOR EACH ROW\n")
    f.write("BEGIN\n")
    f.write("  UPDATE orders\n")
    f.write("  SET    order_total = (\n")
    f.write("           SELECT COALESCE(SUM(ol.quantity * ol.unit_price), 0)\n")
    f.write("           FROM   order_lines ol\n")
    f.write("           WHERE  ol.order_id = OLD.order_id\n")
    f.write("         )\n")
    f.write("  WHERE  order_id = OLD.order_id;\n")
    f.write("END//\n\n")
    f.write("DELIMITER ;\n\n")

    # ── Payments ──
    f.write("-- Payments\n")
    for batch in chunked(payments, BATCH_SIZE):
        f.write("INSERT INTO payments (payment_id, order_id, amount, payment_date, method) VALUES\n")
        lines = []
        for payid, oid, amount, pdate, method in batch:
            lines.append(f"  ({payid}, {oid}, {amount}, '{pdate}', '{sql_str(method)}')")
        f.write(",\n".join(lines) + ";\n\n")

    f.write("COMMIT;\n\n")

    # ── shipments ──
    f.write("-- shipments\n")
    for batch in chunked(shippings, BATCH_SIZE):
        f.write("INSERT INTO shipments (shipping_id, order_id, shipping_address, shipping_city, shipping_postcode, shipped_date, status) VALUES\n")
        lines = []
        for sid, oid, addr, city, pc, sdate, sstatus in batch:
            lines.append(f"  ({sid}, {oid}, '{sql_str(addr)}', '{sql_str(city)}', '{sql_str(pc)}', '{sdate}', '{sql_str(sstatus)}')")
        f.write(",\n".join(lines) + ";\n\n")

    f.write("COMMIT;\n\n")

    # ── Reviews ──
    f.write("-- Reviews\n")
    for batch in chunked(reviews, BATCH_SIZE):
        f.write("INSERT INTO reviews (review_id, customer_id, product_id, rating, comment, review_date) VALUES\n")
        lines = []
        for rid, cid, pid, rating, comment, rdate in batch:
            lines.append(f"  ({rid}, {cid}, {pid}, {rating}, '{sql_str(comment)}', '{rdate}')")
        f.write(",\n".join(lines) + ";\n\n")

    f.write("COMMIT;\n\n")

    # ── Categories ──
    f.write("-- Categories\n")
    f.write("INSERT INTO categories (category_id, name, description) VALUES\n")
    lines = []
    for cid, cname, cdesc in categories:
        lines.append(f"  ({cid}, '{sql_str(cname)}', '{sql_str(cdesc)}')")
    f.write(",\n".join(lines) + ";\n\n")

    # ── product_categories ──
    f.write("-- product_categories\n")
    for batch in chunked(product_categories, BATCH_SIZE):
        f.write("INSERT INTO product_categories (product_id, category_id) VALUES\n")
        lines = []
        for pid, cid in batch:
            lines.append(f"  ({pid}, {cid})")
        f.write(",\n".join(lines) + ";\n\n")

    # ── Suppliers ──
    f.write("-- Suppliers\n")
    f.write("INSERT INTO suppliers (supplier_id, name, contact_email) VALUES\n")
    lines = []
    for sid, sname, semail in suppliers:
        lines.append(f"  ({sid}, '{sql_str(sname)}', '{sql_str(semail)}')")
    f.write(",\n".join(lines) + ";\n\n")

    # ── supplier_products ──
    f.write("-- supplier_products\n")
    for batch in chunked(supplier_products, BATCH_SIZE):
        f.write("INSERT INTO supplier_products (supplier_id, product_id) VALUES\n")
        lines = []
        for sid, pid in batch:
            lines.append(f"  ({sid}, {pid})")
        f.write(",\n".join(lines) + ";\n\n")

    f.write("COMMIT;\n\n")

    # Re-enable checks
    f.write("-- Re-enable checks\n")
    f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
    f.write("SET unique_checks = 1;\n")
    f.write("SET autocommit = 1;\n\n")

    f.write("-- ============================================================\n")
    f.write("-- Verification queries\n")
    f.write("-- ============================================================\n")
    f.write("SELECT 'postcodes'        AS table_name, COUNT(*) AS row_count FROM postcodes\n")
    f.write("UNION ALL SELECT 'customers',        COUNT(*) FROM customers\n")
    f.write("UNION ALL SELECT 'products',         COUNT(*) FROM products\n")
    f.write("UNION ALL SELECT 'orders',          COUNT(*) FROM orders\n")
    f.write("UNION ALL SELECT 'order_lines',       COUNT(*) FROM order_lines\n")
    f.write("UNION ALL SELECT 'payments',         COUNT(*) FROM payments\n")
    f.write("UNION ALL SELECT 'shipments',        COUNT(*) FROM shipments\n")
    f.write("UNION ALL SELECT 'reviews',          COUNT(*) FROM reviews\n")
    f.write("UNION ALL SELECT 'categories',        COUNT(*) FROM categories\n")
    f.write("UNION ALL SELECT 'product_categories', COUNT(*) FROM product_categories\n")
    f.write("UNION ALL SELECT 'suppliers',        COUNT(*) FROM suppliers\n")
    f.write("UNION ALL SELECT 'supplier_products', COUNT(*) FROM supplier_products;\n")

print("Done.")
