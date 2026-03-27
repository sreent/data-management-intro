# Topic 2 Lab — ERD Construction and Schema Translation

This is a design lab, not a coding lab. Part 1 builds an Entity-Relationship Diagram incrementally using ERDPlus. Part 2 translates that ERD to a relational schema using dbdiagram.io and verifies the round-trip. Two standalone exercises (weak entity and self-reference) extend the core patterns.

Use the formal vocabulary (entity, relationship, (min, max) cardinality, associative entity, weak entity, composite key, foreign key) and reference specific chapter tables (Tables 2.2–2.6) throughout your work.

**Time budget:** Part 1 ~60 min | Part 2 ~45 min | **Total ~105 min**

**Tools required:**
- [ERDPlus](https://erdplus.com/) — free, browser-based, Chen notation
- [dbdiagram.io](https://dbdiagram.io/) — free, browser-based, DDL export

---

## Part 1 — ERD Construction (ERDPlus)

### Discussion Opener (~5 min, no building)

Before building anything, consider a naive ERD with only three elements:

```
  ┌──────────┐   (0,N)     (0,N)   ┌──────────┐
  │ customer │───── Purchases ──────│ product  │
  └──────────┘                      └──────────┘
```

**Q1.** What is missing from this design? List at least three limitations. Think about: dates, quantities, grouping items into a single transaction, and tracking payments.

<details>
<summary><strong>Q1 Hint — Click to reveal</strong></summary>

Ask: "How would I record that a customer bought 3 units of Product A and 2 units of Product B in a single transaction on 15 January?" The naive ERD cannot represent this — there is no entity to group items into an order, no place to record quantity, and no way to attach a date to a specific purchase.

</details>

---

Now build the Orders & Payments ERD incrementally. After each question, add the specified entities and relationships to your ERDPlus diagram.

---

### Q2. Core: `customer`, `order`, and `order_line`

Add the following to your ERDPlus diagram:

- **`customer`** entity with attributes: `customer_id` (PK), `name`, `email`, `city`
- **`order`** entity with attributes: `order_id` (PK), `order_date`, `status`
- **`product`** entity with attributes: `product_id` (PK), `name`, `price`
- **places** relationship between `customer` and `order`
- **includes** relationship between `order` and `product` (this will become an associative entity)

**(a)** Assign (min, max) pairs to the places relationship. Consider: Can a customer exist without placing any orders? Can an order exist without a customer?

**(b)** Assign (min, max) pairs to the includes relationship. Consider: Can an order exist with no products? Can a product exist that has never been ordered?

**(c)** The includes relationship carries attributes: `quantity` and `unit_price`. Why do these attributes belong to the *relationship* and not to either `order` or `product`?

**(d)** Promote the includes relationship to an associative entity called `order_line`. What is its composite key?

---

### Q3. `payment` and `shipment`

Add the following to your ERDPlus diagram:

- **`payment`** entity with attributes: `payment_id` (PK), `amount`, `payment_date`, `method`
- **`shipment`** entity with attributes: `shipment_id` (PK), `address`, `shipped_date`, `status`
- **is paid by** relationship between `order` and `payment`
- **is shipped by** relationship between `order` and `shipment`

**(a)** ShopEasy does not support instalments — each order has exactly one payment, and each payment applies to exactly one order. Assign (min, max) pairs. What type of relationship is this?

**(b)** An order may or may not have been shipped yet (a pending order has no shipment record). Once shipped, each order has exactly one shipment record. Assign (min, max) pairs. How does the optionality on the `order` side differ from the is paid by relationship?

**(c)** Using Table 2.3 from the chapter, predict: will `order_id` in the `payments` table be UNIQUE? Will `order_id` in the `shipments` table be UNIQUE? Justify each answer.

---

### Q4. `review`, `supplier`, and `category`

Add the following to your ERDPlus diagram:

- **`review`** entity with attributes: `review_id` (PK), `rating`, `comment`, `review_date`
- **`supplier`** entity with attributes: `supplier_id` (PK), `name`, `contact_email`
- **`category`** entity with attributes: `category_id` (PK), `name`, `description`
- **writes** relationship between `customer` and `review`
- **reviews** relationship between `review` and `product`
- **supplied by** relationship between `supplier` and `product`
- **categorised as** relationship between `product` and `category`

**(a)** Assign (min, max) pairs to all four relationships. For each, state whether a junction table is needed and why.

**(b)** A business stakeholder asks: "Can a customer write multiple reviews for the same product?" Your ERD currently has `review` as a separate entity with its own PK (`review_id`). Does this allow multiple reviews? If you wanted to prevent it, what would you change?

**(c)** Identify which of these four relationships produce junction tables. Name the junction tables and their composite primary keys.

---

### Q5. Weak Entity — University Buildings and Rooms (standalone domain)

This exercise uses a separate domain to test the weak entity pattern.

A university tracks buildings and rooms. Each building has a `building_id` and a `name`. Each room has a `room_number` and a `capacity`. Room 101 in Building A is a different room from Room 101 in Building B — a room cannot be identified without knowing its building.

**(a)** Draw an ERD with `building` and `room`, where `room` is a weak entity of `building`. What is `room`'s partial key? What is its full composite key?

**(b)** Assign (min, max) pairs to the contains relationship. Consider: can a building have zero rooms? Can a room exist without a building?

**(c)** What should happen when a building is demolished (deleted from the database)? What schema mechanism enforces this?

**(d)** *Predict before checking:* Write the `CREATE TABLE` statement for `rooms`. Include the composite PK and the cascade delete. Then compare your answer with Pattern 3 in Section 2.4 of the chapter.

---

### Q6. Self-Reference — Employee Management Hierarchy (standalone domain)

This exercise uses a separate domain to test the self-referencing pattern.

A company tracks employees. Each employee has an `employee_id`, a `name`, and a `hire_date`. An employee may be managed by another employee. The CEO has no manager.

**(a)** Draw an ERD with a single `employee` entity and a self-referencing "manages" relationship. Assign (min, max) pairs. Consider: must every employee have a manager? Can a manager manage multiple employees?

**(b)** Using the derivation rules, determine: Where does the FK go? Is it NOT NULL? Is it UNIQUE?

**(c)** Write the `CREATE TABLE` statement for `employees` with the self-referencing FK. How does the CEO row differ from all other employee rows?

**(d)** *Checkpoint:* A new business rule says "every employee, including the CEO, must have a designated successor." This is a *second* self-referencing relationship (Succeeds). What are the (min, max) pairs? How does this FK differ from `manager_id` in terms of NOT NULL?

---

## Part 2 — Schema Translation and Verification (dbdiagram.io)

### Setup

Open [dbdiagram.io](https://dbdiagram.io/) and start a new diagram. You will translate your ERDPlus ERD into a schema here and export the MySQL DDL.

---

### Q7. Translate the ERD

Translate the complete Orders & Payments ERD (from Q2–Q4) into dbdiagram.io. For each relationship:

**(a)** Apply Rule 1: Where does the FK go? (N-side for 1:N; junction table for M:N)

**(b)** Apply Rule 2: Is the FK NOT NULL? (Yes if min = 1)

**(c)** Apply Rule 3: Is the FK UNIQUE? (Yes if max = 1 from the other side)

**(d)** Apply Rule 4: Does a junction table or composite PK exist? (For M:N and weak entities)

Record your decisions in a table like Table 2.5 from the chapter before entering them in dbdiagram.io.

---

### Q8. Export and inspect DDL

Export the MySQL DDL from dbdiagram.io.

**(a)** Open the exported DDL. Does it include all the tables you expected?

**(b)** *Predict before checking:* How many tables does the schema have? Count them from your ERD first, then compare to the export.

**(c)** Inspect the `payments` table's DDL. Does `order_id` have both NOT NULL and UNIQUE? If not, add the constraint manually and note the gap.

**(d)** Inspect the `order_lines` table's DDL. Does it have a composite PK on `(order_id, product_id)`? Are `quantity` and `unit_price` present as columns?

**(e)** *Reading crow's foot back to (min, max).* Look at the dbdiagram.io visual for the `customers`–`orders` relationship. The line has a fork (<) at the `orders` end and a single bar (|) at the `customers` end. Using the crow's foot symbols from Table 2.3, map these back to (min, max) pairs: what is the (min, max) on the `customer` side? On the `order` side? Do the same for the `orders`–`payments` line (which should show a single bar on both ends with UNIQUE). How does the visual differ from the `customers`–`orders` line, and what does that difference encode?

---

### Q9. Round-trip verification

Complete the following verification table. For each (min, max) pair in your ERD, confirm the corresponding constraint exists in the exported DDL. Mark any mismatches.

| ERD Rule | (min, max) | Expected Constraint | Present in DDL? | Notes |
|---|---|---|---|---|
| `order` → `customer` | (1, 1) | `customer_id` NOT NULL on `orders` | ___ | ___ |
| `customer` → `order` | (0, N) | No constraint on `customers` side | ___ | ___ |
| `order` ↔ `product` (via `order_lines`) | M:N | Junction table with composite PK | ___ | ___ |
| `order` → `payment` | (1, 1) | `order_id` NOT NULL UNIQUE on `payments` | ___ | ___ |
| `payment` → `order` | (1, 1) | `order_id` NOT NULL UNIQUE on `payments` | ___ | ___ |
| `order` → `shipment` | (0, 1) | `order_id` NOT NULL UNIQUE on `shipments` | ___ | ___ |
| `customer` → `review` | (0, N) | No constraint on `customers` side | ___ | ___ |
| `review` → `customer` | (1, 1) | `customer_id` NOT NULL on `reviews` | ___ | ___ |
| `review` → `product` | (1, 1) | `product_id` NOT NULL on `reviews` | ___ | ___ |
| `supplier` ↔ `product` | M:N | Junction table `supplier_products` | ___ | ___ |
| `product` ↔ `category` | M:N | Junction table `product_categories` | ___ | ___ |

**(a)** Are there any mismatches? If so, identify the gap and explain how you would fix it.

**(b)** Are there any constraints in the DDL that do *not* have a corresponding ERD rule? If so, is this drift or a legitimate addition?

---

### Q10. Reflection — the value of two levels

**(a)** During the lab, did you discover any business rule ambiguity that the ERD forced you to resolve? Describe the ambiguity and how you resolved it.

**(b)** Imagine ShopEasy later decides to support instalment payments (multiple payments per order). Which (min, max) pair changes? Trace the impact: does the schema structure change, or only a constraint? Compare the effort of this change in the ERD vs in a production database with 1.4 million payment records.

**(c)** Chapter 1 introduced shape alignment: storage shape vs delivery shape. The schema you built stores data in flat, normalised tables. If the mobile app expects a nested JSON response (order → array of line items → each with product name, quantity, price), what must the application do on every read? Name the Chapter 1 concept this illustrates.

---

## Deliverable

- **Part 1** (Q1–Q6): Complete ERDPlus diagram for Orders & Payments, plus standalone ERDs for `buildings` & `rooms` (weak entity) and `employee` hierarchy (self-reference)
- **Part 2** (Q7–Q9): dbdiagram.io schema with exported MySQL DDL and completed round-trip verification table
- **Reflection** (Q10): Written answers connecting the lab to Chapter 1 concepts

---

## Solutions

Complete your own work before reviewing the solutions below. Each explanation references specific chapter tables and derivation rules.

---

### Part 1 Solutions

<details>
<summary><strong>Q1 Solution — Click to reveal</strong></summary>

The naive "`customer` Purchases `product`" ERD has at least four limitations:

1. **No grouping into transactions.** There is no entity to represent an order — you cannot record that three items were purchased together as a single transaction.
2. **No quantity.** The M:N relationship between `customer` and `product` records *that* a purchase occurred, but not *how many* units.
3. **No date per transaction.** You can add a date attribute to the relationship, but without an `order` entity, every `customer`–`product` pair gets one date — you cannot record multiple purchases of the same product on different dates.
4. **No payment or shipment tracking.** `payment` and `shipment` would need to connect to something — but there is no `order` entity for them to reference.

The fix is to introduce the `order` entity as an intermediary: `customer` → `order` → `order_line` → `product`. This gives you a natural grouping, per-line quantities, per-order dates, and an entity for `payment` and `shipment` to reference.

</details>

---

<details>
<summary><strong>Q2 Solution — Click to reveal</strong></summary>

**(a) places relationship:**
- `customer` side: **(0, N)** — a customer may place zero or more orders.
- `order` side: **(1, 1)** — every order is placed by exactly one customer.

This is a 1:N relationship. The FK (`customer_id`) goes on the `orders` table (Rule 1: FK on the N-side). NOT NULL because min = 1 on the `order` side (Rule 2).

**(b) includes relationship:**
- `order` side: **(1, N)** — every order includes at least one product (an empty order makes no business sense).
- `product` side: **(0, N)** — a product may appear in zero or more orders (a newly listed product has no orders yet).

This is an M:N relationship.

**(c)** `quantity` and `unit_price` belong to the relationship because they describe the specific pairing of *this order* and *this product*. The same product may have different quantities in different orders, and the unit price may change over time — the price at the time of purchase belongs to the order-line, not to the `product` entity.

**(d)** The associative entity `order_line` has composite key **(order_id, product_id)**. It also carries the relationship attributes `quantity` and `unit_price` as columns.

</details>

---

<details>
<summary><strong>Q3 Solution — Click to reveal</strong></summary>

**(a) is paid by relationship:**
- `order` side: **(1, 1)** — every order has exactly one payment.
- `payment` side: **(1, 1)** — every payment is for exactly one order.

This is a **1:1 mandatory** relationship. Both sides have min = 1 (mandatory) and max = 1 (at most one).

**(b) is shipped by relationship:**
- `order` side: **(0, 1)** — an order may or may not have a shipment record (pending orders have not shipped). At most one shipment record per order.
- `shipment` side: **(1, 1)** — every shipment record belongs to exactly one order.

The difference: is paid by has min = 1 on the `order` side (every order *must* have a payment), while is shipped by has min = 0 (an order *may* not yet have a shipment record). The optionality is on the `order` side — a `shipments` row may not exist for every `orders` row.

**(c)** Both `order_id` columns are **UNIQUE**:
- **`payments`:** From the `order` side, max = 1 — each order has at most one payment. So `order_id` on `payments` must be UNIQUE (Rule 3: max = 1 → UNIQUE). This prevents two payments referencing the same order.
- **`shipments`:** Same logic — max = 1 from the `order` side means UNIQUE on `order_id` in `shipments`.

The UNIQUE constraint is what distinguishes a 1:1 relationship from a 1:N relationship at the schema level. Without UNIQUE, nothing would prevent multiple payments per order — exactly the ShopEasy ambiguity from the chapter's Failure 1.

</details>

---

<details>
<summary><strong>Q4 Solution — Click to reveal</strong></summary>

**(a)** (min, max) assignments and junction table decisions:

| Relationship | Side A | (min, max) | Side B | (min, max) | Junction table? |
|---|---|---|---|---|---|
| writes | `customer` (0, N) | → | `review` (1, 1) | | No — 1:N. FK `customer_id` on `reviews`. |
| reviews | `product` (0, N) | → | `review` (1, 1) | | No — 1:N. FK `product_id` on `reviews`. |
| supplied by | `supplier` (0, N) | ↔ | `product` (1, N) | | **Yes** — M:N. Junction: `supplier_products(supplier_id, product_id)`. |
| categorised as | `category` (0, N) | ↔ | `product` (1, N) | | **Yes** — M:N. Junction: `product_categories(product_id, category_id)`. |

**(b)** Yes, a customer can write multiple reviews for the same product because `review` has its own PK (`review_id`). Each review is a distinct entity — two reviews by the same customer for the same product are different rows with different `review_id` values. To prevent multiple reviews, you could add a UNIQUE constraint on `(customer_id, product_id)` in the `reviews` table — this is an enforcement constraint developed in Chapter 5.

**(c)** Two junction tables:
- **`supplier_products`**: composite PK `(supplier_id, product_id)`.
- **`product_categories`**: composite PK `(product_id, category_id)`.

</details>

---

<details>
<summary><strong>Q5 Solution — Click to reveal</strong></summary>

**(a)** `room` is a **weak entity** of `building`.
- Partial key: `room_number` (unique only within a building).
- Full composite key: `(building_id, room_number)`.

**(b)** contains relationship:
- `building` side: **(1, N)** — every building contains at least one room (a building with no rooms is unusual; adjust to (0, N) if the business allows empty buildings).
- `room` side: **(1, 1)** — every room belongs to exactly one building.

**(c)** When a building is demolished, all its rooms should be deleted. The schema mechanism is **ON DELETE CASCADE** on the foreign key from `rooms` to `buildings`. Without CASCADE, deleting a building would either fail (if RESTRICT) or leave orphan room records (if no action is specified).

**(d)** CREATE TABLE statement:

```sql
CREATE TABLE rooms (
    building_id INT NOT NULL REFERENCES buildings(building_id) ON DELETE CASCADE,
    room_number VARCHAR(10) NOT NULL,
    capacity    INT,
    PRIMARY KEY (building_id, room_number)
);
```

Key features: composite PK (Rule 4), FK NOT NULL (Rule 2: min = 1, mandatory participation), ON DELETE CASCADE (weak entity lifecycle dependency).

</details>

---

<details>
<summary><strong>Q6 Solution — Click to reveal</strong></summary>

**(a)** Self-referencing "manages" relationship on `employee`:
- Manager side: **(0, N)** — an employee may manage zero or more subordinates.
- Subordinate side: **(0, 1)** — an employee may have at most one manager (the CEO has none).

**(b)** Derivation rules:
- **Rule 1 (FK placement):** FK `manager_id` on the `employees` table, referencing `employees(employee_id)`. The FK goes on the N-side (the subordinate side — many subordinates per manager).
- **Rule 2 (NOT NULL):** No — min = 0 on the subordinate side means participation is optional. The CEO has no manager, so `manager_id` must be **nullable**.
- **Rule 3 (UNIQUE):** No — max = N on the manager side means one manager can have many subordinates. UNIQUE would limit each manager to one subordinate.

**(c)** CREATE TABLE statement:

```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    hire_date   DATE NOT NULL,
    manager_id  INT REFERENCES employees(employee_id)
    -- nullable: CEO has no manager (min = 0)
);
```

The CEO row has `manager_id = NULL`. All other employees have a non-NULL `manager_id` pointing to their manager's `employee_id`. The self-referencing FK creates a tree structure rooted at the CEO.

**(d)** "Succeeds" relationship:
- Every employee must have a designated successor: min = 1 on the subordinate side → **NOT NULL**.
- Each employee has at most one successor: max = 1 on the subordinate side.

So `successor_id` is **NOT NULL** (unlike `manager_id`, which is nullable). This means every employee row, *including the CEO*, must have a `successor_id` value. The FK would be: `successor_id INT NOT NULL REFERENCES employees(employee_id)`.

</details>

---

### Part 2 Solutions

<details>
<summary><strong>Q7 Solution — Click to reveal</strong></summary>

The complete derivation table:

| Relationship | Type | Rule 1 (FK placement) | Rule 2 (NOT NULL) | Rule 3 (UNIQUE) | Rule 4 (Composite PK) |
|---|---|---|---|---|---|
| places | 1:N | FK `customer_id` on `orders` | NOT NULL (min=1) | No (max=N) | — |
| includes | M:N | Junction table `order_lines` | Both FKs NOT NULL (PK) | No (composite PK) | PK (order_id, product_id) |
| is paid by | 1:1 | FK `order_id` on `payments` | NOT NULL (min=1) | UNIQUE (max=1) | — |
| is shipped by | 1:1 | FK `order_id` on `shipments` | NOT NULL (min=1) | UNIQUE (max=1) | — |
| writes | 1:N | FK `customer_id` on `reviews` | NOT NULL (min=1) | No (max=N) | — |
| reviews | 1:N | FK `product_id` on `reviews` | NOT NULL (min=1) | No (max=N) | — |
| supplied by | M:N | Junction table `supplier_products` | Both FKs NOT NULL (PK) | No (composite PK) | PK (supplier_id, product_id) |
| categorised as | M:N | Junction table `product_categories` | Both FKs NOT NULL (PK) | No (composite PK) | PK (product_id, category_id) |

</details>

---

<details>
<summary><strong>Q8 Solution — Click to reveal</strong></summary>

**(a)** The export should include all tables. Check for: `customers`, `orders` (note that `ORDER` is a reserved word in SQL, so dbdiagram.io may escape it), `products`, `order_lines`, `payments`, `shipments`, `reviews`, `suppliers`, `supplier_products`, `categories`, `product_categories`.

**(b)** **11 tables** total: 8 entity tables (`customers`, `orders`, `products`, `payments`, `shipments`, `reviews`, `suppliers`, `categories`) + 3 junction tables (`order_lines`, `supplier_products`, `product_categories`).

Note: `Inventory` from the chapter's worked example is modelled as an attribute of `product` (`quantity_in_stock`) or as a separate table depending on design choices. If modelled as a separate table, the count is 12.

**(c)** `payments`' `order_id` should have both NOT NULL (Rule 2: min = 1) and UNIQUE (Rule 3: max = 1 from `order` side). Some tools may not export UNIQUE constraints on FK columns automatically — this is a common gap to check in the round-trip.

**(d)** `order_lines` should have: composite PK on `(order_id, product_id)`, plus `quantity` and `unit_price` columns. Both FK columns are NOT NULL by virtue of being part of the PK.

**(e)** Reading the crow's foot symbols back to (min, max):

**`customers`–`orders` line:** Fork (<) at `orders` = "many" → max = N from the `customer` side. Circle (○) at `customers` = "optional" → min = 0 from the `order` side (a customer may have zero orders). Double bar (║) at `orders` = "mandatory" → min = 1 from the `customer` side (every order must have a customer). Result: `customer` side **(0, N)**, `order` side **(1, 1)** — matching the Chen ERD.

**`orders`–`payments` line:** Single bar (|) at both ends = "one" → max = 1 on both sides. Double bar (║) at both ends = "mandatory" → min = 1 on both sides. The UNIQUE constraint on `order_id` in `payments` is what enforces the single-bar at the `payments` end — without UNIQUE, the FK alone would permit many payments per order (a fork, not a bar). Result: both sides **(1, 1)** — a 1:1 mandatory relationship.

The visual difference: the `customers`–`orders` line has a fork (many) at one end; the `orders`–`payments` line has bars (one) at both ends. The fork vs bar distinction is how crow's foot encodes the max value — and UNIQUE on the FK is how the schema enforces it.

</details>

---

<details>
<summary><strong>Q9 Solution — Click to reveal</strong></summary>

The completed verification table should show all constraints present. Common mismatches to watch for:

1. **UNIQUE on 1:1 FKs** — dbdiagram.io may not automatically add UNIQUE to `order_id` in `payments` and `shipments`. This is the most common gap.
2. **NOT NULL on FK columns** — some tools default to nullable FKs. Check that `customer_id` on `orders`, `customer_id` and `product_id` on `reviews`, and similar mandatory FKs are NOT NULL.
3. **Composite PK on junction tables** — verify that `order_lines`, `supplier_products`, and `product_categories` have composite PKs, not auto-increment single-column PKs.

**(a)** If mismatches exist, they typically fall into the UNIQUE and NOT NULL categories above. Fix by adding the constraint manually to the DDL.

**(b)** dbdiagram.io may add auto-increment IDs or index definitions not present in the ERD. These are implementation details (not business rules) and are acceptable additions — they do not constitute drift. However, if a FK constraint appears without an ERD relationship, that is drift.

</details>

---

<details>
<summary><strong>Q10 Solution — Click to reveal</strong></summary>

**(a)** Common ambiguities discovered during the lab:
- "Can a customer place zero orders?" (yes — a newly registered customer)
- "Can a product exist in zero categories?" (depends on business rule — we chose min = 1)
- "Can a customer review the same product twice?" (yes, with separate review_ids — but is this the business intent?)

The ERD forces you to assign (min, max) pairs, which forces you to resolve these ambiguities *before* writing DDL.

**(b)** To support instalments, the is paid by relationship changes from 1:1 to **1:N**: `order` (1, N) ← is paid by → (1, 1) `payment`. The change:
- The `UNIQUE` constraint on `order_id` in the `payments` table is **removed** (Rule 3: max changes from 1 to N).
- The table structure does not change — no new tables, no dropped columns.
- In the ERD: change one number. In a production database: write a migration to drop the UNIQUE constraint, test with existing data, schedule a maintenance window. The asymmetry in effort is exactly why the ERD exists.

**(c)** The application must JOIN `orders`, `order_lines`, and `products`, then re-nest the flat rows into a JSON structure in application code. This is **shape mismatch** from Chapter 1 — the storage shape (flat, normalised tables) does not match the delivery shape (nested JSON). Every read pays the cost of JOINs and re-nesting. If this aggregate-read workload dominated, Chapter 1's decision framework would point toward the document model.

</details>
