# Topic 2 Lab — ERD Construction and Schema Translation

This is a design lab, not a coding lab. Part 1 builds an Entity-Relationship Diagram incrementally using ERDPlus in Chen notation. Part 2 re-expresses the same design as a relational schema diagram in dbdiagram.io and verifies the round-trip to DDL. Two standalone exercises (weak entity and self-reference) extend the core patterns.

**A note on the two-part structure.** Chen notation (Part 1) is a *teaching scaffold* — it makes each cardinality commitment explicit as a (min, max) pair you must write down *before* touching any table. You are unlikely to encounter Chen diagrams outside a classroom. The relational schema diagram (Part 2) is what you will actually meet in industry: dbdiagram.io, MySQL Workbench, DataGrip, and most modern schema tools render schema diagrams with cardinality marks at line endpoints and generate DDL directly. The visual vocabulary these tools use resembles classical crow's foot (IE) notation, though rarely the full four-symbol set. The lab walks Chen → relational schema diagram so you can see exactly how each (min, max) decision turns into a schema constraint; in day-to-day practice, engineers draw the schema diagram directly. Treat Part 1 as training wheels and Part 2 as the bicycle.

**Reading convention: Look Across.** This lab and the chapter use the **Look Across** convention for (min, max) labels: the label written near entity B answers the question "for one instance of A, how many Bs?" — you stand at one entity and read the label near the *other* entity. This is the same convention used in the chapter's Chen ERDs and Table 2.3. If you see labels in a different position in other textbooks (for example the Same Side convention, where each label describes the entity it sits beside), translate those labels into Look Across positions before applying this lab's answers.

Use the formal vocabulary (entity, relationship, (min, max) cardinality, associative entity, weak entity, composite key, foreign key) and reference specific chapter tables (Tables 2.2–2.6) throughout your work.

**Time budget:** Part 1 ~60 min | Part 2 ~45 min | **Total ~105 min**

**Tools required:**
- [ERDPlus](https://erdplus.com/) — free, browser-based, Chen notation (used here as a learning aid)
- [dbdiagram.io](https://dbdiagram.io/) — free, browser-based relational schema diagram tool with DDL export (closer to real-practice tooling). Displays cardinality at line endpoints using symbols that resemble classical crow's foot, though not the full classical vocabulary.

---

## Part 1 — Chen ERD as a Learning Exercise (ERDPlus)

The goal of Part 1 is *commitment*: for every relationship you add, you must state the (min, max) pair on each side before you think about tables, columns, or keys. Chen notation is used here because it forces that commitment to be visible on the page — each relationship is a labelled diamond with explicit (min, max) annotations on both sides. This is a pedagogical discipline, not an industry artifact; you are rehearsing the thinking, not producing a deliverable that anyone downstream will read.

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

Now build the Orders & Payments ERD incrementally in ERDPlus. After each question, add the specified entities and relationships, and write the (min, max) pairs on each relationship *before* you think about how any of this will become tables. Resist the urge to jump to schema — the whole point of Part 1 is to separate the cardinality decision from the translation step.

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

**(b)** An order may or may not have been shipped yet (a pending order has no shipment record). Once shipped, each order has exactly one shipment record. Assign (min, max) pairs in Look Across positions. How does the optionality in the label near `shipment` differ from the equivalent label in the is paid by relationship?

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

## Part 2 — Relational Schema Diagram and DDL Translation (dbdiagram.io)

Part 2 is closer to what you would actually do on the job: draw the relational schema diagram in a tool that also generates DDL, and reason directly about foreign keys, NOT NULL, and UNIQUE. The (min, max) commitments from Part 1 are the discipline that makes this translation mechanical; once you have internalised that discipline, you can skip Part 1 and start here.

### Setup

Open [dbdiagram.io](https://dbdiagram.io/) and start a new diagram. You will re-express the ERD you built in Part 1 as a relational schema diagram here and export the MySQL DDL. In practice you would start from a blank dbdiagram.io canvas (or an equivalent tool such as MySQL Workbench or DataGrip); the Chen diagram from Part 1 is scaffolding you are temporarily leaning on while you learn the mapping rules.

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

**(e)** *Reading crow's foot back to (min, max).* Look at the dbdiagram.io visual for the `customers`–`orders` relationship. dbdiagram.io uses a visual vocabulary that resembles classical crow's foot (IE) notation but does not render the full four-symbol set — treat the symbols you see as a subset of the classical vocabulary from Table 2.3. The line has a fork (<) at the `orders` end and a single bar (|) at the `customers` end. Using the crow's foot symbols from Table 2.3, map these back to (min, max) pairs in Look Across positions: what is the (min, max) in the label near `customer`? In the label near `order`? Do the same for the `orders`–`payments` line (which should show a single bar on both ends with UNIQUE). How does the visual differ from the `customers`–`orders` line, and what does that difference encode?

*Teacher's note:* No crow's foot variant — including whatever dbdiagram.io renders — can display arbitrary numeric bounds like (0, 5) or (2, 7). The notation only distinguishes the four standard cases: (0, 1), (1, 1), (0, N), (1, N). If your design requires a specific numeric bound, it must be enforced as a CHECK constraint or in application code, not on the diagram.

---

### Q9. Round-trip verification

Complete the following verification table. For each (min, max) pair in your ERD, confirm the corresponding constraint exists in the exported DDL. Mark any mismatches.

| ERD Rule (Look Across label position) | (min, max) | Expected Constraint | Present in DDL? | Notes |
|---|---|---|---|---|
| places: label near `customer` | (1, 1) | `customer_id` NOT NULL on `orders` | ___ | ___ |
| places: label near `order` | (0, N) | No constraint on `customers` side | ___ | ___ |
| includes: `order` ↔ `product` (via `order_lines`) | M:N | Junction table with composite PK | ___ | ___ |
| is paid by: label near `order` | (1, 1) | `order_id` NOT NULL on `payments` | ___ | ___ |
| is paid by: label near `payment` | (1, 1) | `order_id` UNIQUE on `payments` | ___ | ___ |
| is shipped by: label near `order` | (1, 1) | `order_id` NOT NULL on `shipments` | ___ | ___ |
| is shipped by: label near `shipment` | (0, 1) | `order_id` UNIQUE on `shipments` | ___ | ___ |
| writes: label near `customer` | (1, 1) | `customer_id` NOT NULL on `reviews` | ___ | ___ |
| writes: label near `review` | (0, N) | No constraint on `customers` side | ___ | ___ |
| reviews: label near `product` | (1, 1) | `product_id` NOT NULL on `reviews` | ___ | ___ |
| reviews: label near `review` | (0, N) | No constraint on `products` side | ___ | ___ |
| supplied by: `supplier` ↔ `product` | M:N | Junction table `supplier_products` | ___ | ___ |
| categorised as: `product` ↔ `category` | M:N | Junction table `product_categories` | ___ | ___ |

**(a)** Are there any mismatches? If so, identify the gap and explain how you would fix it.

**(b)** Are there any constraints in the DDL that do *not* have a corresponding ERD rule? If so, is this drift or a legitimate addition?

---

### Q10. Reflection — from scaffold to practice

**(a)** During the lab, did you discover any business rule ambiguity that the (min, max) commitments forced you to resolve? Describe the ambiguity and how you resolved it.

**(b)** Imagine ShopEasy later decides to support instalment payments (multiple payments per order). Which (min, max) pair changes? Trace the impact: does the schema structure change, or only a constraint? Compare the effort of this change at the design stage versus in a production database with 1.4 million payment records.

**(c)** Chapter 1 introduced shape alignment: storage shape vs delivery shape. The schema you built stores data in flat, normalised tables. If the mobile app expects a nested JSON response (order → array of line items → each with product name, quantity, price), what must the application do on every read? Name the Chapter 1 concept this illustrates.

**(d)** The lab asked you to build the same design twice — once in Chen notation in Part 1 and once as a relational schema diagram in Part 2. Chen is a classroom scaffold; in industry, schema tools render a relational schema diagram (with cardinality symbols that resemble classical crow's foot at line endpoints) and you would draw that diagram directly. Which (min, max) commitments do you feel confident you could make straight onto a relational schema diagram without first detouring through Chen? Which ones (if any) still benefit from the explicit (min, max) annotation Chen forces on you? When you think you have fully internalised the Part 1 discipline, you can drop Part 1 entirely and work directly in Part 2 tooling.

**(e)** *Tooling limits.* dbdiagram.io displays cardinality using symbols that resemble classical crow's foot, but it does not render the full classical vocabulary you saw in Table 2.3, and no crow's foot variant can express arbitrary numeric bounds like (0, 5) — only the four standard cases (0, 1), (1, 1), (0, N), (1, N). If a design requires a specific numeric bound, where in the stack would you enforce it, and why can the diagram not carry that commitment on its own?

---

## Deliverable

- **Part 1** (Q1–Q6): Complete ERDPlus diagram for Orders & Payments, plus standalone ERDs for `buildings` & `rooms` (weak entity) and `employee` hierarchy (self-reference)
- **Part 2** (Q7–Q9): dbdiagram.io relational schema diagram with exported MySQL DDL and completed round-trip verification table
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
- Label near `customer`: **(1, 1)** — looking across from one order, there is exactly one customer who placed it.
- Label near `order`: **(0, N)** — looking across from one customer, there are zero or more orders they have placed.

This is a 1:N relationship. The FK (`customer_id`) goes on the `orders` table (Rule 1: FK on the N-side). NOT NULL because the label near `customer` has min = 1 — every order must reference a customer (Rule 2).

**(b) includes relationship:**
- Label near `order`: **(0, N)** — looking across from one product, there are zero or more orders containing it (a newly listed product has no orders yet).
- Label near `product`: **(1, N)** — looking across from one order, there is at least one product on it (an empty order makes no business sense).

This is an M:N relationship.

**(c)** `quantity` and `unit_price` belong to the relationship because they describe the specific pairing of *this order* and *this product*. The same product may have different quantities in different orders, and the unit price may change over time — the price at the time of purchase belongs to the order-line, not to the `product` entity.

**(d)** The associative entity `order_line` has composite key **(order_id, product_id)**. It also carries the relationship attributes `quantity` and `unit_price` as columns.

</details>

---

<details>
<summary><strong>Q3 Solution — Click to reveal</strong></summary>

**(a) is paid by relationship:**
- Label near `order`: **(1, 1)** — looking across from one payment, there is exactly one order it settles.
- Label near `payment`: **(1, 1)** — looking across from one order, there is exactly one payment for it.

This is a **1:1 mandatory** relationship. Both labels show min = 1 (mandatory) and max = 1 (at most one).

**(b) is shipped by relationship:**
- Label near `order`: **(1, 1)** — looking across from one shipment, there is exactly one order it ships.
- Label near `shipment`: **(0, 1)** — looking across from one order, there is at most one shipment record, and it may not yet exist (a pending order has none).

The difference: is paid by has min = 1 in the label near `payment` (every order *must* have a payment), while is shipped by has min = 0 in the label near `shipment` (an order *may* not yet have a shipment record). The optionality sits on the shipment side of the look-across reading — a `shipments` row may not exist for every `orders` row.

**(c)** Both `order_id` columns are **UNIQUE**:
- **`payments`:** The label near `payment` has max = 1 — looking across from one order, there is at most one payment. So `order_id` on `payments` must be UNIQUE (Rule 3: max = 1 on the look-across label near the FK table → UNIQUE). This prevents two payments referencing the same order.
- **`shipments`:** Same logic — max = 1 in the label near `shipment` means UNIQUE on `order_id` in `shipments`.

The UNIQUE constraint is what distinguishes a 1:1 relationship from a 1:N relationship at the schema level. Without UNIQUE, nothing would prevent multiple payments per order — exactly the ShopEasy ambiguity from the chapter's Failure 1.

</details>

---

<details>
<summary><strong>Q4 Solution — Click to reveal</strong></summary>

**(a)** (min, max) assignments and junction table decisions. Remember the Look Across reading: the label *near* an entity answers "for one instance of the other entity, how many of *this* entity?".

| Relationship | Label near A | Label near B | Junction table? |
|---|---|---|---|
| writes | `customer` **(1, 1)** | `review` **(0, N)** | No — 1:N. FK `customer_id` on `reviews`. |
| reviews | `product` **(1, 1)** | `review` **(0, N)** | No — 1:N. FK `product_id` on `reviews`. |
| supplied by | `supplier` **(1, N)** | `product` **(0, N)** | **Yes** — M:N. Junction: `supplier_products(supplier_id, product_id)`. |
| categorised as | `category` **(1, N)** | `product` **(0, N)** | **Yes** — M:N. Junction: `product_categories(product_id, category_id)`. |

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
- Label near `building`: **(1, 1)** — looking across from one room, there is exactly one building it sits in.
- Label near `room`: **(1, N)** — looking across from one building, there is at least one room inside (a building with no rooms is unusual; adjust the label near `room` to (0, N) if the business allows empty buildings).

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
- Label on the manager role: **(0, 1)** — looking across from one subordinate, there are zero or one managers (the CEO has none).
- Label on the subordinate role: **(0, N)** — looking across from one manager, there are zero or more subordinates they manage.

**(b)** Derivation rules:
- **Rule 1 (FK placement):** FK `manager_id` on the `employees` table, referencing `employees(employee_id)`. The FK goes on the N-side (the subordinate role — many subordinates per manager).
- **Rule 2 (NOT NULL):** No — the label near the manager role has min = 0, meaning a subordinate may have no manager at all. The CEO has no manager, so `manager_id` must be **nullable**.
- **Rule 3 (UNIQUE):** No — the label near the subordinate role has max = N, meaning one manager may have many subordinates. UNIQUE would limit each manager to one subordinate.

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

**(d)** "Succeeds" relationship. Reading the labels across the line:
- Label near the successor role: **(1, 1)** — looking across from any employee, there is exactly one designated successor (min = 1 → **NOT NULL**; max = 1 → at most one).
- Label near the predecessor role: **(1, 1)** — looking across from a successor, there is exactly one employee they succeed.

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

**(c)** `payments`' `order_id` should have both NOT NULL (Rule 2: min = 1 in the label near `payment`) and UNIQUE (Rule 3: max = 1 in the label near `payment` — looking across from one order, there is at most one payment). Some tools may not export UNIQUE constraints on FK columns automatically — this is a common gap to check in the round-trip.

**(d)** `order_lines` should have: composite PK on `(order_id, product_id)`, plus `quantity` and `unit_price` columns. Both FK columns are NOT NULL by virtue of being part of the PK.

**(e)** Reading the crow's foot symbols back to (min, max). Note that dbdiagram.io renders cardinality using a subset of the classical crow's foot (IE) vocabulary from Table 2.3 — the exact glyphs shown for circles, bars, and double-bars may vary between tools, so read the symbols as a resemblance to the classical set rather than a pixel-perfect match. Because crow's foot symbols sit at the line *endpoints*, they already read "look across" by construction: the symbol at the `orders` end describes what one customer sees when they look across at orders, and vice versa.

**`customers`–`orders` line:** Fork (<) at `orders` = "many" → max = N in the label near `orders` (looking across from one customer, there are many orders). Circle (○) at `orders` = "optional" → min = 0 in the label near `orders` (a customer may have zero orders). Double bar (║) at `customers` = "mandatory one" → (1, 1) in the label near `customers` (looking across from one order, there is exactly one customer, and it is mandatory). Result: label near `customer` **(1, 1)**, label near `order` **(0, N)** — matching the Chen ERD in Look Across form.

**`orders`–`payments` line:** Single bar (|) at both ends = "one" → max = 1 in both labels. Double bar (║) at both ends = "mandatory" → min = 1 in both labels. The UNIQUE constraint on `order_id` in `payments` is what enforces the single-bar at the `payments` end — without UNIQUE, the FK alone would permit many payments per order (a fork, not a bar). Result: both labels **(1, 1)** — a 1:1 mandatory relationship.

The visual difference: the `customers`–`orders` line has a fork (many) at the `orders` end; the `orders`–`payments` line has bars (one) at both ends. The fork vs bar distinction is how crow's foot encodes the max value in the look-across label — and UNIQUE on the FK is how the schema enforces it.

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

Committing to (min, max) pairs before writing DDL is what forces these ambiguities into the open — whichever notation you draw in.

**(b)** To support instalments, the is paid by relationship changes from 1:1 to **1:N**. In Look Across labels, the label near `payment` changes from **(1, 1)** to **(1, N)** — looking across from one order, there are now one-or-more payments instead of exactly one. The label near `order` stays at **(1, 1)**. The change:
- The `UNIQUE` constraint on `order_id` in the `payments` table is **removed** (Rule 3: max in the label near `payment` changes from 1 to N).
- The table structure does not change — no new tables, no dropped columns.
- At the design stage: change one number on a diagram. In a production database: write a migration to drop the UNIQUE constraint, test with existing data, schedule a maintenance window. That asymmetry is exactly why you commit to cardinalities deliberately at design time — whether on a relational schema diagram in dbdiagram.io, a whiteboard sketch, or (in this lab, as scaffolding) a Chen diagram.

**(c)** The application must JOIN `orders`, `order_lines`, and `products`, then re-nest the flat rows into a JSON structure in application code. This is **shape mismatch** from Chapter 1 — the storage shape (flat, normalised tables) does not match the delivery shape (nested JSON). Every read pays the cost of JOINs and re-nesting. If this aggregate-read workload dominated, Chapter 1's decision framework would point toward the document model.

**(d)** Expected self-assessment: most students find the simple 1:N cases (`customer` → `order`, `customer` → `review`) easy to commit to directly on a relational schema diagram after one or two passes. The cases that tend to benefit longest from the explicit Chen (min, max) discipline are 1:1 mandatory relationships (where forgetting UNIQUE on the FK silently collapses to 1:N — the ShopEasy Failure 1 pattern from the chapter) and weak entities (where the partial key and cascade behaviour are easy to miss). Once those patterns are second nature, Chen has done its job and you can work entirely in relational schema diagram tooling — which is what you will do outside the classroom.

**(e)** dbdiagram.io draws cardinality at line endpoints using a subset of the classical crow's foot (IE) vocabulary from Table 2.3 — the fork and bar convey max = N versus max = 1, but not every tool renders optional-circles or double-bars consistently, and none can draw a bound such as (0, 5). The four standard cases ((0, 1), (1, 1), (0, N), (1, N)) are the only cardinalities a relational schema diagram can visually commit to. A specific numeric bound belongs either in a `CHECK` constraint at the schema layer (e.g. `CHECK (quantity BETWEEN 1 AND 5)`) or in application-layer validation; the diagram itself cannot carry it. This is a limit of the notation, not a flaw in any particular tool.

</details>
