-- ============================================================
-- Orders & Payments — Database & Table Creation (DDL)
-- MySQL 8.0+
-- ============================================================
-- 14 tables | Chapters 2–5
-- Ch2: base structure from ERD
-- Ch3: BCNF normalisation (postcodes decomposition,
--       order_total derived attribute)
-- Ch4: sales organisation extension (offices, employees,
--       customers.sales_rep_id)
-- Ch5: enforcement (CHECK, UNIQUE, CASCADE, triggers)
-- ============================================================

CREATE DATABASE IF NOT EXISTS orders_payments
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE orders_payments;

-- ------------------------------------------------------------
-- 1. postcodes (Ch3 BCNF decomposition)
-- ------------------------------------------------------------
CREATE TABLE postcodes (
  postcode  VARCHAR(10)  NOT NULL,
  city      VARCHAR(50)  NOT NULL,
  PRIMARY KEY (postcode)
);

-- ------------------------------------------------------------
-- 2. customers
-- ------------------------------------------------------------
CREATE TABLE customers (
  customer_id  INT          NOT NULL,
  name         VARCHAR(100) NOT NULL,
  email        VARCHAR(100) NOT NULL,
  postcode     VARCHAR(10),
  PRIMARY KEY (customer_id),
  UNIQUE (email),
  FOREIGN KEY (postcode) REFERENCES postcodes(postcode)
);

-- ------------------------------------------------------------
-- 3. orders
-- ------------------------------------------------------------
CREATE TABLE orders (
  order_id        INT           NOT NULL,
  customer_id     INT           NOT NULL,
  invoice_number  VARCHAR(20),
  order_date      DATE,
  status          VARCHAR(20),
  order_total     DECIMAL(10,2),
  PRIMARY KEY (order_id),
  UNIQUE (customer_id, invoice_number),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ------------------------------------------------------------
-- 4. products
-- ------------------------------------------------------------
CREATE TABLE products (
  product_id        INT           NOT NULL,
  name              VARCHAR(100),
  price             DECIMAL(10,2),
  quantity_in_stock INT           DEFAULT 0,
  PRIMARY KEY (product_id)
);

-- ------------------------------------------------------------
-- 5. order_lines (weak entity — CASCADE on delete)
-- ------------------------------------------------------------
CREATE TABLE order_lines (
  order_id    INT           NOT NULL,
  product_id  INT           NOT NULL,
  quantity    INT,
  unit_price  DECIMAL(10,2),
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (order_id)   REFERENCES orders(order_id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  CHECK (quantity > 0)
);

-- ------------------------------------------------------------
-- 6. payments (one payment per order)
-- ------------------------------------------------------------
CREATE TABLE payments (
  payment_id    INT           NOT NULL,
  order_id      INT           NOT NULL,
  amount        DECIMAL(10,2),
  payment_date  DATE,
  method        VARCHAR(30),
  PRIMARY KEY (payment_id),
  UNIQUE (order_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  CHECK (amount > 0)
);

-- ------------------------------------------------------------
-- 7. shipments (snapshot addresses — Ch3 justified downshift)
-- ------------------------------------------------------------
CREATE TABLE shipments (
  shipping_id       INT          NOT NULL,
  order_id          INT          NOT NULL,
  shipping_address  VARCHAR(200),
  shipping_city     VARCHAR(50),
  shipping_postcode VARCHAR(10),
  shipped_date      DATE,
  status            VARCHAR(20),
  PRIMARY KEY (shipping_id),
  UNIQUE (order_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- ------------------------------------------------------------
-- 8. reviews
-- ------------------------------------------------------------
CREATE TABLE reviews (
  review_id    INT  NOT NULL,
  customer_id  INT  NOT NULL,
  product_id   INT  NOT NULL,
  rating       INT,
  comment      TEXT,
  review_date  DATE,
  PRIMARY KEY (review_id),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (product_id)  REFERENCES products(product_id),
  CHECK (rating BETWEEN 1 AND 5)
);

-- ------------------------------------------------------------
-- 9. suppliers
-- ------------------------------------------------------------
CREATE TABLE suppliers (
  supplier_id    INT          NOT NULL,
  name           VARCHAR(100),
  contact_email  VARCHAR(100),
  PRIMARY KEY (supplier_id)
);

-- ------------------------------------------------------------
-- 10. supplier_products (M:N junction)
-- ------------------------------------------------------------
CREATE TABLE supplier_products (
  supplier_id  INT  NOT NULL,
  product_id   INT  NOT NULL,
  PRIMARY KEY (supplier_id, product_id),
  FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
  FOREIGN KEY (product_id)  REFERENCES products(product_id)
);

-- ------------------------------------------------------------
-- 11. categories
-- ------------------------------------------------------------
CREATE TABLE categories (
  category_id  INT         NOT NULL,
  name         VARCHAR(50),
  description  TEXT,
  PRIMARY KEY (category_id)
);

-- ------------------------------------------------------------
-- 12. product_categories (M:N junction)
-- ------------------------------------------------------------
CREATE TABLE product_categories (
  product_id   INT  NOT NULL,
  category_id  INT  NOT NULL,
  PRIMARY KEY (product_id, category_id),
  FOREIGN KEY (product_id)  REFERENCES products(product_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- ------------------------------------------------------------
-- 13. offices (Ch4 — sales organisation)
-- ------------------------------------------------------------
CREATE TABLE offices (
  office_id  INT          NOT NULL,
  city       VARCHAR(50)  NOT NULL,
  country    VARCHAR(50)  NOT NULL,
  phone      VARCHAR(20),
  territory  VARCHAR(50),
  PRIMARY KEY (office_id)
);

-- ------------------------------------------------------------
-- 14. employees (Ch4 — self-referencing manager hierarchy)
-- ------------------------------------------------------------
CREATE TABLE employees (
  employee_id    INT           NOT NULL,
  first_name     VARCHAR(50)   NOT NULL,
  last_name      VARCHAR(50)   NOT NULL,
  email          VARCHAR(100)  NOT NULL,
  office_id      INT           NOT NULL,
  manager_id     INT,
  job_title      VARCHAR(50)   NOT NULL,
  salary         DECIMAL(10,2),
  commission_pct DECIMAL(4,2),
  PRIMARY KEY (employee_id),
  UNIQUE (email),
  FOREIGN KEY (office_id)  REFERENCES offices(office_id),
  FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

-- customers ← sales rep assignment (Ch4 extension)
ALTER TABLE customers
  ADD COLUMN sales_rep_id INT,
  ADD FOREIGN KEY (sales_rep_id) REFERENCES employees(employee_id);

-- ============================================================
-- Trigger: maintain orders.order_total (Ch3 derived attribute,
-- Ch5 enforcement). Fires after INSERT on order_lines.
-- ============================================================
DELIMITER //

CREATE TRIGGER trg_orderline_after_insert
AFTER INSERT ON order_lines
FOR EACH ROW
BEGIN
  UPDATE orders
  SET    order_total = (
           SELECT SUM(ol.quantity * ol.unit_price)
           FROM   order_lines ol
           WHERE  ol.order_id = NEW.order_id
         )
  WHERE  order_id = NEW.order_id;
END//

CREATE TRIGGER trg_orderline_after_update
AFTER UPDATE ON order_lines
FOR EACH ROW
BEGIN
  UPDATE orders
  SET    order_total = (
           SELECT SUM(ol.quantity * ol.unit_price)
           FROM   order_lines ol
           WHERE  ol.order_id = NEW.order_id
         )
  WHERE  order_id = NEW.order_id;
END//

CREATE TRIGGER trg_orderline_after_delete
AFTER DELETE ON order_lines
FOR EACH ROW
BEGIN
  UPDATE orders
  SET    order_total = (
           SELECT COALESCE(SUM(ol.quantity * ol.unit_price), 0)
           FROM   order_lines ol
           WHERE  ol.order_id = OLD.order_id
         )
  WHERE  order_id = OLD.order_id;
END//

DELIMITER ;
