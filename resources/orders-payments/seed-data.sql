-- ============================================================
-- Orders & Payments — Slide-Ready Seed Data
-- MySQL 8.0+
-- ============================================================
-- Small enough to trace by hand on teaching slides.
-- 5 offices | 8 employees | 5 customers | 6 products
-- 7 orders | 13 order lines
--
-- Prerequisites: run ddl.sql first.
-- ============================================================

USE orders_payments;

-- ------------------------------------------------------------
-- Postcodes
-- ------------------------------------------------------------
INSERT INTO postcodes (postcode, city) VALUES
  ('018956', 'Singapore'),
  ('50088',  'Kuala Lumpur'),
  ('10110',  'Bangkok');

-- ------------------------------------------------------------
-- Customers (Eve has no postcode and no orders)
-- ------------------------------------------------------------
INSERT INTO customers (customer_id, name, email, postcode) VALUES
  (1, 'Alice Tan',   'alice@example.com', '018956'),
  (2, 'Bob Patel',   'bob@example.com',   '50088'),
  (3, 'Carol Lim',   'carol@example.com', '10110'),
  (4, 'Dave Wong',   'dave@example.com',  '018956'),
  (5, 'Eve Santos',  'eve@example.com',    NULL);

-- ------------------------------------------------------------
-- Products (products 6 has no order lines — anti-join demo)
-- ------------------------------------------------------------
INSERT INTO products (product_id, name, price, quantity_in_stock) VALUES
  (1, 'Widget A',    9.99,  500),
  (2, 'Widget B',   14.99,  300),
  (3, 'Gadget X',   49.99,  100),
  (4, 'Gadget Y',   79.99,   80),
  (5, 'Cable USB-C', 4.99, 1000),
  (6, 'Screen 24"',199.99,   60);

-- ------------------------------------------------------------
-- Orders (Alice: 2 orders, Eve: 0 orders, Order 106: pending)
-- Note: order_total is initially NULL — triggers will
-- populate it when order_lines rows are inserted below.
-- ------------------------------------------------------------
INSERT INTO orders (order_id, customer_id, invoice_number, order_date, status, order_total) VALUES
  (101, 1, 'INV-2024-00101', '2024-03-15', 'completed', NULL),
  (102, 1, 'INV-2024-00102', '2024-06-20', 'completed', NULL),
  (103, 2, 'INV-2024-00103', '2024-04-10', 'shipped',   NULL),
  (104, 2, 'INV-2024-00104', '2024-09-01', 'paid',      NULL),
  (105, 3, 'INV-2024-00105', '2024-07-22', 'completed', NULL),
  (106, 3, 'INV-2024-00106', '2024-11-05', 'pending',   NULL),
  (107, 4, 'INV-2024-00107', '2024-08-18', 'completed', NULL);

-- ------------------------------------------------------------
-- order_lines (13 rows)
-- The after-insert trigger sets order_total automatically.
-- Alice has 3 lines across 2 orders = count inflation demo.
-- ------------------------------------------------------------
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

-- ------------------------------------------------------------
-- Payments (no payment for pending Order 106)
-- ------------------------------------------------------------
INSERT INTO payments (payment_id, order_id, amount, payment_date, method) VALUES
  (201, 101,  34.97, '2024-03-15', 'card'),
  (202, 102,  49.99, '2024-06-20', 'paypal'),
  (203, 103,  29.97, '2024-04-10', 'card'),
  (204, 104, 129.98, '2024-09-01', 'bank_transfer'),
  (205, 105,  79.99, '2024-07-22', 'card'),
  (206, 107,  29.96, '2024-08-18', 'paypal');

-- ------------------------------------------------------------
-- shipments (snapshot addresses — no shipping for 104 and 106)
-- ------------------------------------------------------------
INSERT INTO shipments (shipping_id, order_id, shipping_address, shipping_city, shipping_postcode, shipped_date, status) VALUES
  (301, 101, '10 Raffles Quay',          'Singapore',     '018956', '2024-03-17', 'delivered'),
  (302, 102, '10 Raffles Quay',          'Singapore',     '018956', '2024-06-23', 'delivered'),
  (303, 103, '25 Jalan Bukit Bintang',   'Kuala Lumpur',  '50088',  '2024-04-13', 'shipped'),
  (304, 105, '8 Sukhumvit Soi 11',       'Bangkok',       '10110',  '2024-07-25', 'delivered'),
  (305, 107, '42 Marina Boulevard',       'Singapore',     '018956', '2024-08-20', 'delivered');

-- ------------------------------------------------------------
-- Reviews
-- ------------------------------------------------------------
INSERT INTO reviews (review_id, customer_id, product_id, rating, comment, review_date) VALUES
  (1, 1, 1, 5, 'Excellent quality', '2024-04-01'),
  (2, 1, 3, 4, 'Good value',        '2024-07-15'),
  (3, 2, 2, 3, 'Decent',            '2024-05-20'),
  (4, 3, 4, 5, 'Perfect',           '2024-08-30');

-- ------------------------------------------------------------
-- Categories
-- ------------------------------------------------------------
INSERT INTO categories (category_id, name, description) VALUES
  (1, 'Peripherals', 'Input and output devices'),
  (2, 'Cables',      'Connectivity accessories'),
  (3, 'Displays',    'Monitors and screens');

-- ------------------------------------------------------------
-- product_categories
-- ------------------------------------------------------------
INSERT INTO product_categories (product_id, category_id) VALUES
  (1, 1), (2, 1), (3, 1), (4, 1),  -- Peripherals
  (5, 2),                            -- Cables
  (6, 3);                            -- Displays

-- ------------------------------------------------------------
-- Suppliers
-- ------------------------------------------------------------
INSERT INTO suppliers (supplier_id, name, contact_email) VALUES
  (1, 'TechParts Pte Ltd', 'sales@techparts.sg'),
  (2, 'CableCo Sdn Bhd',   'info@cableco.my');

-- ------------------------------------------------------------
-- supplier_products (Products 4 and 6 have no supplier)
-- ------------------------------------------------------------
INSERT INTO supplier_products (supplier_id, product_id) VALUES
  (1, 1), (1, 2), (1, 3),  -- TechParts supplies Widgets + Gadget X
  (2, 5);                    -- CableCo supplies Cable

-- ------------------------------------------------------------
-- Offices (Ho Chi Minh City has no employees — anti-join demo)
-- ------------------------------------------------------------
INSERT INTO offices (office_id, city, country, phone, territory) VALUES
  (1, 'Singapore',       'SG', '+65 6234 5678',    'Singapore'),
  (2, 'Kuala Lumpur',    'MY', '+60 3-2345 6789',  'Malaysia'),
  (3, 'Bangkok',         'TH', '+66 2-345-6789',   'Thailand'),
  (4, 'Jakarta',         'ID', '+62 21-5678-9012', 'Indonesia'),
  (5, 'Ho Chi Minh City','VN', '+84 28-3456-7890', 'Vietnam');

-- ------------------------------------------------------------
-- Employees (Sarah has no manager — self-join demo)
-- 3 managers (NULL commission_pct), 5 reps (with commission)
-- Rizal Pratama earns more than his manager Budi Santoso
-- ------------------------------------------------------------
INSERT INTO employees (employee_id, first_name, last_name, email, office_id, manager_id, job_title, salary, commission_pct) VALUES
  (1, 'Sarah',   'Tan',     'stan@company.com',     1, NULL, 'Managing Director', 85000, NULL),
  (2, 'Wei Jie', 'Lim',     'wjlim@company.com',    1, 1,    'Sales Manager SG',  52000, NULL),
  (3, 'Budi',    'Santoso', 'bsantoso@company.com', 4, 1,    'Sales Manager ID',  55000, NULL),
  (4, 'Ahmad',   'Ismail',  'aismail@company.com',  2, 2,    'Sales Rep',         34000, 0.15),
  (5, 'Mei Ling','Wong',    'mlwong@company.com',   1, 2,    'Sales Rep',         38000, 0.12),
  (6, 'Somchai', 'Prasert', 'sprasert@company.com', 3, 2,    'Sales Rep',         31000, 0.18),
  (7, 'Rizal',   'Pratama', 'rpratama@company.com', 4, 3,    'Sales Rep ID',      56000, 0.10),
  (8, 'Nurul',   'Huda',    'nhuda@company.com',    1, 2,    'Sales Rep',         33000, 0.15);

-- ------------------------------------------------------------
-- Assign sales reps to customers (Eve has no rep — NULL trap)
-- ------------------------------------------------------------
UPDATE customers SET sales_rep_id = 5 WHERE customer_id = 1;  -- Alice ← Mei Ling
UPDATE customers SET sales_rep_id = 4 WHERE customer_id = 2;  -- Bob ← Ahmad
UPDATE customers SET sales_rep_id = 6 WHERE customer_id = 3;  -- Carol ← Somchai
UPDATE customers SET sales_rep_id = 7 WHERE customer_id = 4;  -- Dave ← Rizal
-- Eve (customer_id = 5): no sales rep (NULL)
