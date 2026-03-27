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
