# Orders & Payments — Slide-Ready Seed Data

A minimal dataset for the Orders & Payments schema, small enough to trace by hand on teaching slides. Designed to demonstrate key concepts from Chapters 2–5.

**5 offices | 8 employees | 5 customers | 6 products | 7 orders | 13 order lines**

---

## Data Tables

### postcodes

| postcode | city |
|----------|------|
| 018956 | Singapore |
| 50088 | Kuala Lumpur |
| 10110 | Bangkok |

### customers

| customer_id | name | email | postcode | sales_rep_id |
|-------------|------|-------|----------|-------------|
| 1 | Alice Tan | alice@example.com | 018956 | 5 (Mei Ling) |
| 2 | Bob Patel | bob@example.com | 50088 | 4 (Ahmad) |
| 3 | Carol Lim | carol@example.com | 10110 | 6 (Somchai) |
| 4 | Dave Wong | dave@example.com | 018956 | 7 (Rizal) |
| 5 | Eve Santos | eve@example.com | *NULL* | *NULL* |

> Eve has no postcode (optional FK), no orders (LEFT JOIN / anti-join demo), and no sales rep (NULL trap for NOT IN).

### products

| product_id | name | price | quantity_in_stock |
|------------|------|-------|-------------------|
| 1 | Widget A | 9.99 | 500 |
| 2 | Widget B | 14.99 | 300 |
| 3 | Gadget X | 49.99 | 100 |
| 4 | Gadget Y | 79.99 | 80 |
| 5 | Cable USB-C | 4.99 | 1000 |
| 6 | Screen 24" | 199.99 | 60 |

> product 6 has no order lines (anti-join demo — "unsold product").

### orders

| order_id | customer_id | invoice_number | order_date | status | order_total |
|----------|-------------|----------------|------------|--------|-------------|
| 101 | 1 (Alice) | INV-2024-00101 | 2024-03-15 | completed | 34.97 |
| 102 | 1 (Alice) | INV-2024-00102 | 2024-06-20 | completed | 49.99 |
| 103 | 2 (Bob) | INV-2024-00103 | 2024-04-10 | shipped | 29.97 |
| 104 | 2 (Bob) | INV-2024-00104 | 2024-09-01 | paid | 129.98 |
| 105 | 3 (Carol) | INV-2024-00105 | 2024-07-22 | completed | 79.99 |
| 106 | 3 (Carol) | INV-2024-00106 | 2024-11-05 | pending | 39.95 |
| 107 | 4 (Dave) | INV-2024-00107 | 2024-08-18 | completed | 29.96 |

> Alice has 2 orders (count inflation demo). Eve has 0 orders (LEFT JOIN demo). Order 106 is pending (transaction demo).

### order_lines

| order_id | product_id | quantity | unit_price | line_total |
|----------|------------|----------|------------|------------|
| 101 | 1 (Widget A) | 2 | 9.99 | 19.98 |
| 101 | 2 (Widget B) | 1 | 14.99 | 14.99 |
| 102 | 3 (Gadget X) | 1 | 49.99 | 49.99 |
| 103 | 1 (Widget A) | 1 | 9.99 | 9.99 |
| 103 | 2 (Widget B) | 1 | 14.99 | 14.99 |
| 103 | 5 (Cable) | 1 | 4.99 | 4.99 |
| 104 | 3 (Gadget X) | 1 | 49.99 | 49.99 |
| 104 | 4 (Gadget Y) | 1 | 79.99 | 79.99 |
| 105 | 4 (Gadget Y) | 1 | 79.99 | 79.99 |
| 106 | 1 (Widget A) | 3 | 9.99 | 29.97 |
| 106 | 5 (Cable) | 2 | 4.99 | 9.98 |
| 107 | 2 (Widget B) | 1 | 14.99 | 14.99 |
| 107 | 5 (Cable) | 3 | 4.99 | 14.97 |

> `line_total` is not a stored column — shown here for traceability. `order_total` on orders = SUM of line totals per order.

**Count inflation check:** Alice has 2 orders but 3 order lines. Joining customers → orders → order_lines produces 3 rows for Alice. `COUNT(*)` = 3 (wrong). `COUNT(DISTINCT order_id)` = 2 (correct).

### payments

| payment_id | order_id | amount | payment_date | method |
|------------|----------|--------|-------------|--------|
| 201 | 101 | 34.97 | 2024-03-15 | card |
| 202 | 102 | 49.99 | 2024-06-20 | paypal |
| 203 | 103 | 29.97 | 2024-04-10 | card |
| 204 | 104 | 129.98 | 2024-09-01 | bank_transfer |
| 205 | 105 | 79.99 | 2024-07-22 | card |
| 206 | 107 | 29.96 | 2024-08-18 | paypal |

> Order 106 (pending) has no payment — transaction demo target.

### shipments

| shipping_id | order_id | shipping_address | shipping_city | shipping_postcode | shipped_date | status |
|-------------|----------|------------------|---------------|-------------------|-------------|--------|
| 301 | 101 | 10 Raffles Quay | Singapore | 018956 | 2024-03-17 | delivered |
| 302 | 102 | 10 Raffles Quay | Singapore | 018956 | 2024-06-23 | delivered |
| 303 | 103 | 25 Jalan Bukit Bintang | Kuala Lumpur | 50088 | 2024-04-13 | shipped |
| 304 | 105 | 8 Sukhumvit Soi 11 | Bangkok | 10110 | 2024-07-25 | delivered |
| 305 | 107 | 42 Marina Boulevard | Singapore | 018956 | 2024-08-20 | delivered |

> Shipping address is a snapshot. Orders 104 and 106 have no shipping record.

### reviews

| review_id | customer_id | product_id | rating | comment | review_date |
|-----------|-------------|------------|--------|---------|-------------|
| 1 | 1 (Alice) | 1 (Widget A) | 5 | Excellent quality | 2024-04-01 |
| 2 | 1 (Alice) | 3 (Gadget X) | 4 | Good value | 2024-07-15 |
| 3 | 2 (Bob) | 2 (Widget B) | 3 | Decent | 2024-05-20 |
| 4 | 3 (Carol) | 4 (Gadget Y) | 5 | Perfect | 2024-08-30 |

### categories

| category_id | name | description |
|-------------|------|-------------|
| 1 | Peripherals | Input and output devices |
| 2 | Cables | Connectivity accessories |
| 3 | Displays | Monitors and screens |

### product_categories

| product_id | category_id |
|------------|-------------|
| 1 (Widget A) | 1 (Peripherals) |
| 2 (Widget B) | 1 (Peripherals) |
| 3 (Gadget X) | 1 (Peripherals) |
| 4 (Gadget Y) | 1 (Peripherals) |
| 5 (Cable) | 2 (Cables) |
| 6 (Screen) | 3 (Displays) |

### suppliers

| supplier_id | name | contact_email |
|-------------|------|---------------|
| 1 | TechParts Pte Ltd | sales@techparts.sg |
| 2 | CableCo Sdn Bhd | info@cableco.my |

### supplier_products

| supplier_id | product_id |
|-------------|------------|
| 1 (TechParts) | 1 (Widget A) |
| 1 (TechParts) | 2 (Widget B) |
| 1 (TechParts) | 3 (Gadget X) |
| 2 (CableCo) | 5 (Cable) |

> Products 4 (Gadget Y) and 6 (Screen) have no supplier — demonstrates M:N sparsity.

### offices

| office_id | city | country | phone | territory |
|-----------|------|---------|-------|-----------|
| 1 | Singapore | SG | +65 6234 5678 | Singapore |
| 2 | Kuala Lumpur | MY | +60 3-2345 6789 | Malaysia |
| 3 | Bangkok | TH | +66 2-345-6789 | Thailand |
| 4 | Jakarta | ID | +62 21-5678-9012 | Indonesia |
| 5 | Ho Chi Minh City | VN | +84 28-3456-7890 | Vietnam |

> Ho Chi Minh City (office 5) has no employees — anti-join demo.

### employees

| employee_id | first_name | last_name | email | office_id | manager_id | job_title | salary | commission_pct |
|-------------|------------|-----------|-------|-----------|------------|-----------|--------|---------------|
| 1 | Sarah | Tan | stan@company.com | 1 (Singapore) | *NULL* | Managing Director | 85000 | *NULL* |
| 2 | Wei Jie | Lim | wjlim@company.com | 1 (Singapore) | 1 (Sarah) | Sales Manager SG | 52000 | *NULL* |
| 3 | Budi | Santoso | bsantoso@company.com | 4 (Jakarta) | 1 (Sarah) | Sales Manager ID | 55000 | *NULL* |
| 4 | Ahmad | Ismail | aismail@company.com | 2 (Kuala Lumpur) | 2 (Wei Jie) | Sales Rep | 34000 | 0.15 |
| 5 | Mei Ling | Wong | mlwong@company.com | 1 (Singapore) | 2 (Wei Jie) | Sales Rep | 38000 | 0.12 |
| 6 | Somchai | Prasert | sprasert@company.com | 3 (Bangkok) | 2 (Wei Jie) | Sales Rep | 31000 | 0.18 |
| 7 | Rizal | Pratama | rpratama@company.com | 4 (Jakarta) | 3 (Budi) | Sales Rep ID | 56000 | 0.10 |
| 8 | Nurul | Huda | nhuda@company.com | 1 (Singapore) | 2 (Wei Jie) | Sales Rep | 33000 | 0.15 |

> Sarah (employee 1) has NULL `manager_id` — the managing director has no manager (self-join demo). Rizal Pratama (employee 7, salary $56k) earns more than his manager Budi Santoso (employee 3, salary $55k) — salary comparison demo. Managers have NULL `commission_pct`; sales reps have non-NULL values — NULL handling demos.

**Reporting hierarchy:**

```
Sarah Tan (MD, Singapore)
├── Wei Jie Lim (Sales Manager SG, Singapore)
│   ├── Ahmad Ismail (Sales Rep, Kuala Lumpur)
│   ├── Mei Ling Wong (Sales Rep, Singapore)
│   ├── Somchai Prasert (Sales Rep, Bangkok)
│   └── Nurul Huda (Sales Rep, Singapore)
└── Budi Santoso (Sales Manager ID, Jakarta)
    └── Rizal Pratama (Sales Rep ID, Jakarta)
```

---

## Teaching Scenarios Supported

| Scenario | Chapter | What to show on slide |
|----------|---------|----------------------|
| **Count inflation** | Ch4 | Alice: 2 orders, 3 line items. `COUNT(*)` after 3-table join = 3 (wrong). `COUNT(DISTINCT order_id)` = 2 (correct). |
| **Silent data loss** | Ch4 | INNER JOIN customers → Order drops Eve (0 orders). LEFT JOIN keeps her with NULLs. |
| **Anti-join** | Ch4 | product 6 (Screen) has no order_lines rows. Ho Chi Minh City office has no employees. `LEFT JOIN ... WHERE IS NULL` finds them. |
| **FWGHOS trace** | Ch4 | Trace any query step by step: F (7 orders × avg 1.9 lines = 13 rows), W (filter), G (group), H (filter groups), O (sort), S (output). |
| **Self-join** | Ch4 | employees with their manager: `employees e JOIN employees m ON e.manager_id = m.employee_id`. Sarah (MD) has NULL manager — LEFT JOIN preserves her. |
| **NULL trap (NOT IN)** | Ch4 | `WHERE employee_id NOT IN (SELECT sales_rep_id FROM customers)` returns 0 rows because Eve's NULL `sales_rep_id` poisons `NOT IN`. Anti-join version works correctly. |
| **NULL in aggregates** | Ch4 | `COUNT(*)` = 8 employees. `COUNT(commission_pct)` = 5 (managers have NULL commission). `commission_pct != NULL` returns 0 rows. |
| **Salary comparison** | Ch4 | Rizal Pratama ($56k) earns more than his manager Budi Santoso ($55k). Self-join with WHERE filter. |
| **BCNF decomposition** | Ch3 | postcodes → City extracted from customers into postcodes lookup. Both Alice and Dave share 018956 → Singapore (update once, correct everywhere). |
| **Snapshot justification** | Ch3 | Shipping address frozen at ship time. If "Raffles Quay" is renamed, shipping records still show original address. |
| **Derived attribute** | Ch3/Ch5 | `order_total` = SUM of line totals. Verify: Order 101 = 19.98 + 14.99 = 34.97 ✓ |
| **Star schema derivation** | Ch3 | Fact: order_lines + order_date. Dimensions: products (with category), customers (with postcode/city), Time. |
| **CHECK constraint** | Ch5 | `INSERT INTO order_lines VALUES (101, 6, -3, 199.99)` — rejected by `CHECK (quantity > 0)`. |
| **UNIQUE constraint** | Ch5 | `INSERT INTO orders VALUES (108, 1, 'INV-2024-00101', ...)` — rejected (Alice already has INV-2024-00101). |
| **CASCADE delete** | Ch5 | DELETE Order 101 → order_lines rows (101,1) and (101,2) also deleted. |
| **Transaction demo** | Ch5 | Order 106 (pending): BEGIN → INSERT payments → UPDATE status → COMMIT. Or: simulate failure → ROLLBACK. |
| **View + GRANT** | Ch5 | `revenue_by_product` view: Widget A total = (2×9.99) + (1×9.99) + (3×9.99) = 59.94. No customer emails visible. |
| **Index selectivity** | Ch5 | `WHERE status = 'completed'` matches 4/7 (57% — low selectivity). `WHERE customer_id = 4` matches 1/7 (14% — higher selectivity). |

---

## SQL INSERT Statements

```sql
-- ============================================================
-- Orders & Payments — Slide-Ready Seed Data
-- Small enough to trace by hand
-- (5 offices, 8 employees, 5 customers, 7 orders, 13 lines)
-- ============================================================

USE orders_payments;

-- Postcodes
INSERT INTO postcodes (postcode, city) VALUES
  ('018956', 'Singapore'),
  ('50088',  'Kuala Lumpur'),
  ('10110',  'Bangkok');

-- Customers (Eve has no postcode and no orders)
INSERT INTO customers (customer_id, name, email, postcode) VALUES
  (1, 'Alice Tan',   'alice@example.com', '018956'),
  (2, 'Bob Patel',   'bob@example.com',   '50088'),
  (3, 'Carol Lim',   'carol@example.com', '10110'),
  (4, 'Dave Wong',   'dave@example.com',  '018956'),
  (5, 'Eve Santos',  'eve@example.com',    NULL);

-- Products (product 6 has no order lines — anti-join demo)
INSERT INTO products (product_id, name, price, quantity_in_stock) VALUES
  (1, 'Widget A',    9.99,  500),
  (2, 'Widget B',   14.99,  300),
  (3, 'Gadget X',   49.99,  100),
  (4, 'Gadget Y',   79.99,   80),
  (5, 'Cable USB-C', 4.99, 1000),
  (6, 'Screen 24"',199.99,   60);

-- Orders (Alice: 2 orders, Eve: 0 orders, Order 106: pending)
INSERT INTO orders (order_id, customer_id, invoice_number, order_date, status, order_total) VALUES
  (101, 1, 'INV-2024-00101', '2024-03-15', 'completed',  34.97),
  (102, 1, 'INV-2024-00102', '2024-06-20', 'completed',  49.99),
  (103, 2, 'INV-2024-00103', '2024-04-10', 'shipped',    29.97),
  (104, 2, 'INV-2024-00104', '2024-09-01', 'paid',      129.98),
  (105, 3, 'INV-2024-00105', '2024-07-22', 'completed',  79.99),
  (106, 3, 'INV-2024-00106', '2024-11-05', 'pending',    39.95),
  (107, 4, 'INV-2024-00107', '2024-08-18', 'completed',  29.96);

-- order_lines (13 rows — Alice has 3 lines across 2 orders = count inflation)
INSERT INTO order_lines (order_id, product_id, quantity, unit_price) VALUES
  (101, 1, 2,  9.99),   -- Alice order 1: Widget A ×2 = 19.98
  (101, 2, 1, 14.99),   -- Alice order 1: Widget B ×1 = 14.99
  (102, 3, 1, 49.99),   -- Alice order 2: Gadget X ×1 = 49.99
  (103, 1, 1,  9.99),   -- Bob order 1: Widget A ×1
  (103, 2, 1, 14.99),   -- Bob order 1: Widget B ×1
  (103, 5, 1,  4.99),   -- Bob order 1: Cable ×1
  (104, 3, 1, 49.99),   -- Bob order 2: Gadget X ×1
  (104, 4, 1, 79.99),   -- Bob order 2: Gadget Y ×1
  (105, 4, 1, 79.99),   -- Carol order 1: Gadget Y ×1
  (106, 1, 3,  9.99),   -- Carol order 2: Widget A ×3
  (106, 5, 2,  4.99),   -- Carol order 2: Cable ×2
  (107, 2, 1, 14.99),   -- Dave: Widget B ×1
  (107, 5, 3,  4.99);   -- Dave: Cable ×3

-- Payments (no payment for pending Order 106)
INSERT INTO payments (payment_id, order_id, amount, payment_date, method) VALUES
  (201, 101,  34.97, '2024-03-15', 'card'),
  (202, 102,  49.99, '2024-06-20', 'paypal'),
  (203, 103,  29.97, '2024-04-10', 'card'),
  (204, 104, 129.98, '2024-09-01', 'bank_transfer'),
  (205, 105,  79.99, '2024-07-22', 'card'),
  (206, 107,  29.96, '2024-08-18', 'paypal');

-- shipments (snapshot addresses — no shipping for Orders 104 and 106)
INSERT INTO shipments (shipping_id, order_id, shipping_address, shipping_city, shipping_postcode, shipped_date, status) VALUES
  (301, 101, '10 Raffles Quay',          'Singapore',     '018956', '2024-03-17', 'delivered'),
  (302, 102, '10 Raffles Quay',          'Singapore',     '018956', '2024-06-23', 'delivered'),
  (303, 103, '25 Jalan Bukit Bintang',   'Kuala Lumpur',  '50088',  '2024-04-13', 'shipped'),
  (304, 105, '8 Sukhumvit Soi 11',       'Bangkok',       '10110',  '2024-07-25', 'delivered'),
  (305, 107, '42 Marina Boulevard',       'Singapore',     '018956', '2024-08-20', 'delivered');

-- Reviews
INSERT INTO reviews (review_id, customer_id, product_id, rating, comment, review_date) VALUES
  (1, 1, 1, 5, 'Excellent quality', '2024-04-01'),
  (2, 1, 3, 4, 'Good value',        '2024-07-15'),
  (3, 2, 2, 3, 'Decent',            '2024-05-20'),
  (4, 3, 4, 5, 'Perfect',           '2024-08-30');

-- Categories
INSERT INTO categories (category_id, name, description) VALUES
  (1, 'Peripherals', 'Input and output devices'),
  (2, 'Cables',      'Connectivity accessories'),
  (3, 'Displays',    'Monitors and screens');

-- product_categories
INSERT INTO product_categories (product_id, category_id) VALUES
  (1, 1), (2, 1), (3, 1), (4, 1),  -- Peripherals
  (5, 2),                            -- Cables
  (6, 3);                            -- Displays

-- Suppliers
INSERT INTO suppliers (supplier_id, name, contact_email) VALUES
  (1, 'TechParts Pte Ltd', 'sales@techparts.sg'),
  (2, 'CableCo Sdn Bhd',   'info@cableco.my');

-- supplier_products (Products 4 and 6 have no supplier)
INSERT INTO supplier_products (supplier_id, product_id) VALUES
  (1, 1), (1, 2), (1, 3),  -- TechParts supplies Widgets + Gadget X
  (2, 5);                    -- CableCo supplies Cable

-- Offices (Ho Chi Minh City has no employees — anti-join demo)
INSERT INTO offices (office_id, city, country, phone, territory) VALUES
  (1, 'Singapore',       'SG', '+65 6234 5678',    'Singapore'),
  (2, 'Kuala Lumpur',    'MY', '+60 3-2345 6789',  'Malaysia'),
  (3, 'Bangkok',         'TH', '+66 2-345-6789',   'Thailand'),
  (4, 'Jakarta',         'ID', '+62 21-5678-9012', 'Indonesia'),
  (5, 'Ho Chi Minh City','VN', '+84 28-3456-7890', 'Vietnam');

-- Employees (Sarah has no manager — self-join demo)
INSERT INTO employees (employee_id, first_name, last_name, email, office_id, manager_id, job_title, salary, commission_pct) VALUES
  (1, 'Sarah',   'Tan',     'stan@company.com',     1, NULL, 'Managing Director', 85000, NULL),
  (2, 'Wei Jie', 'Lim',     'wjlim@company.com',    1, 1,    'Sales Manager SG',  52000, NULL),
  (3, 'Budi',    'Santoso', 'bsantoso@company.com', 4, 1,    'Sales Manager ID',  55000, NULL),
  (4, 'Ahmad',   'Ismail',  'aismail@company.com',  2, 2,    'Sales Rep',         34000, 0.15),
  (5, 'Mei Ling','Wong',    'mlwong@company.com',   1, 2,    'Sales Rep',         38000, 0.12),
  (6, 'Somchai', 'Prasert', 'sprasert@company.com', 3, 2,    'Sales Rep',         31000, 0.18),
  (7, 'Rizal',   'Pratama', 'rpratama@company.com', 4, 3,    'Sales Rep ID',      56000, 0.10),
  (8, 'Nurul',   'Huda',    'nhuda@company.com',    1, 2,    'Sales Rep',         33000, 0.15);

-- Assign sales reps to customers (Eve has no rep — NULL trap)
UPDATE customers SET sales_rep_id = 5 WHERE customer_id = 1;  -- Alice ← Mei Ling
UPDATE customers SET sales_rep_id = 4 WHERE customer_id = 2;  -- Bob ← Ahmad
UPDATE customers SET sales_rep_id = 6 WHERE customer_id = 3;  -- Carol ← Somchai
UPDATE customers SET sales_rep_id = 7 WHERE customer_id = 4;  -- Dave ← Rizal
-- Eve (customer_id = 5): no sales rep (NULL)
```
