# Lab 11 — Multi-Model Capstone: Designing a Super-App Data Architecture

This is a **design lab**, not a coding lab. You design the data architecture for the ride-hailing super-app from Chapters 1, 6, and 10. The lab provides a system description with concrete services, data entities, access patterns, and constraints. You decompose the system into workloads, assign data models, design data-flow boundaries, draw an architecture diagram, and test your assignments by substitution.

Use the formal vocabulary (data model, workload, schema, constraint, query) and reference specific chapter mechanisms throughout your justifications. Vague justifications ("it is better") receive no credit — cite the chapter, the mechanism, and the specific operation that is made cheap or expensive.

**Materials required:** This document, plus your Chapter 6 and Chapter 10 Colab notebooks for reference. No new tools or installations needed.

**Time budget:** Part 1 ~20 min | Part 2 ~40 min | Part 3 ~25 min | Part 4 ~30 min | Part 5 ~20 min | Part 6 ~30 min | Part 7 ~15 min | **Total ~180 min**

---

## Reference: The Super-App's Services

The table below describes the super-app's eight services. Use it as input for all questions in this lab.

**Table 1:** Super-app service descriptions

| Service | Data owned | Top reads | Top writes | Consistency need |
|---|---|---|---|---|
| Ride booking | Rides, driver assignments | "Available drivers near location X"; "Ride status for ride R" | "Create ride, assign driver, record fare" | ACID (fare + payment must be atomic) |
| Payment processing | Payments, settlements, promo usage | "Payment status for ride R"; "Driver earnings this month" | "Process payment, apply promo, settle to driver" | ACID (payment + promo decrement must be atomic) |
| Passenger profiles | Preferences, saved places, payment methods, recent activity | "Load full profile on app open"; "Recent rides for passenger P" | "Update preferences"; "Add saved place" | Eventual (2s delay acceptable) |
| Driver profiles | Vehicle details, licence info, earnings summary, incentive progress, preferred zones | "Load full profile on driver login"; "Incentive progress for driver D" | "Update preferred zones"; "Record incentive milestone" | Eventual (2s delay acceptable) |
| Merchant management | Menus, operating hours, promotions, order analytics | "Load merchant dashboard"; "Menu for merchant M" | "Update menu item"; "Create promotion" | Eventual (5s delay acceptable) |
| Regulatory reporting | E-invoices, tax summaries, compliance filings | "Generate monthly invoice batch for Peppol submission" | "Record submission result (accepted/rejected)" | Schema-validated before submission |
| Partner integration | Transit authority data, mapping provider data, government transport registry | "Which drivers operate in high-accident zones?"; "Match internal driver ID to licence registry" | "Ingest nightly partner data feed" | Tolerant of incomplete/conflicting data across sources |
| Fraud monitoring | Account transfer network, flagged accounts, suspicious patterns | "Trace transfers from account A within k hops, filtered by amount and date"; "Find transfer cycles involving flagged accounts" | "Add transfer edge when payment exceeds threshold" | Eventual (hourly query cycle) |

---

## Worked Example: Analysing a Ninth Service

Before tackling the eight services above, study this worked example. It demonstrates the complete analytical arc — workload classification, model assignment, and boundary design — on a hypothetical ninth service.

**Service: Push notifications.** The notification service sends real-time alerts to users: ride confirmations, payment receipts, promo announcements, and driver arrival notices. It owns a `NotificationLog` (user ID, message content, delivery status, timestamp). Its top read is "recent notifications for user U" (aggregate read of the user's notification history). Its top write is "create notification and mark as delivered" (single-entity write). Consistency: eventual (a 1–3 second delay before the notification appears in the user's history is acceptable).

**Step 1 — Workload classification.** The dominant access pattern is an aggregate read (load all recent notifications for one user) with single-entity writes. The consistency requirement is eventual. The data shape is a per-user list of notification objects with variable structure (ride notifications have different fields from promo notifications).

**Step 2 — Model assignment.** The workload's dominant operations match the document model's cheap path: aggregate-shaped reads (one document per user, loaded as a unit) and structural variation (different notification types have different fields, handled without schema migration). The two-part justification:
- **Cheap operation (document model, Chapter 6):** A single `db.notifications.find({userId: "U"})` returns all recent notifications as a nested document — no joins, no re-nesting.
- **Why not relational?** A relational `Notifications` table handles this workload adequately at low volume (simple SELECT with WHERE clause). At high volume with structural variation (each notification type has different payload fields), the relational approach requires either nullable columns per type or an EAV pattern — Chapter 6's Failure 1 at smaller scale.

**Step 3 — Boundary design.** The notification service *receives* triggers from the transactional core (ride completion → "Your ride is complete" notification). Boundary: Relational → Document, triggered by ride-completion events, eventual consistency, retry queue if MongoDB is unavailable. The notification content includes a **snapshot** of the ride (fare, driver name) — Chapter 6's snapshot discipline.

**Step 4 — Consolidation check.** Could this service share the personalisation workload's document store? Yes — notifications are per-user, aggregate-shaped, and eventually consistent, just like profiles. Adding a `notifications` collection to the same MongoDB instance eliminates one boundary (the notification service reads profile data directly, no cross-store query needed). **Verdict:** Consolidate with the personalisation layer rather than creating a sixth data store. This demonstrates Mechanism 3 — fewer models when the boundary cost exceeds the benefit.

---

## Part 1 — System Decomposition (Q1–Q2)

**Q1.** Group these eight services into workloads based on shared access patterns and consistency requirements. You should arrive at approximately five workloads. For each workload:
- (a) Name it.
- (b) List the services it contains.
- (c) Justify each grouping in one sentence — explain *why* these services share a workload, referencing the access pattern and consistency requirement they have in common.

*(Note: Parts 2–3 will ask you to justify each model assignment in detail. For now, focus on why these services group together, not which model each gets.)*

<details><summary>Solution — Q1</summary>

Five workloads:

| Workload | Services | Justification |
|---|---|---|
| **Transactional core** | Ride booking, Payment processing | Both require ACID transactions on normalised data with constraint enforcement (FK, CHECK) — the dominant access pattern is atomic multi-step writes with cross-entity consistency. |
| **Personalisation layer** | Passenger profiles, Driver profiles, Merchant management | All three read and write self-contained, structurally variable profile documents on every session — the dominant access pattern is aggregate-shaped reads with eventual consistency. |
| **Regulatory exchange** | Regulatory reporting | The workload is schema-validated document generation against an externally mandated standard (UBL XSD) — distinct from any internal data operation. |
| **Partner integration** | Partner integration | The workload is cross-source data merging from independent organisations with different identifiers and schemas — requires open-world tolerance for incomplete and conflicting data. |
| **Fraud monitoring** | Fraud monitoring | The workload is bounded multi-hop traversal with per-edge filtering and cycle detection — a fundamentally different access pattern from row lookups or aggregate reads. |

</details>

---

**Q2.** For each workload, fill in the workload card from the chapter's Algorithm section (Step 3). Use Table 1 above as input — the dominant reads and writes come directly from the "Top reads" and "Top writes" columns.

**Before filling in the cards**, predict: which workload will have the most complex growth pattern? Which will have the simplest?

| Field | Value |
|---|---|
| Workload name | ___ |
| Dominant reads (top 2–3) | ___ |
| Dominant writes (top 1–2) | ___ |
| Data shape as accessed | ___ |
| Consistency requirement | ___ |
| Growth pattern | ___ |

<details><summary>Solution — Q2</summary>

**Transactional core:**

| Field | Value |
|---|---|
| Workload name | Transactional core |
| Dominant reads | "Available drivers near location X"; "Payment status for ride R"; "Driver earnings this month" |
| Dominant writes | "Create ride + assign driver + record fare" (atomic); "Process payment + apply promo + settle to driver" (atomic) |
| Data shape | Normalised rows with FK relationships across tables (Rides, Payments, Drivers, Promos) |
| Consistency | ACID — fare, payment, promo decrement, and settlement must be atomic |
| Growth pattern | Rows grow linearly with ride volume; tables are fixed-schema |

**Personalisation layer:**

| Field | Value |
|---|---|
| Workload name | Personalisation layer |
| Dominant reads | "Load full profile on app open / driver login / merchant dashboard" (aggregate read) |
| Dominant writes | "Update preferences"; "Add saved place"; "Update menu item" (single-document writes) |
| Data shape | Nested JSON documents; different structure per user type (passenger, driver, merchant) |
| Consistency | Eventual — 2–5 second delay acceptable |
| Growth pattern | Document count grows with users; nesting depth grows with features; bounded by embed-or-reference rules (Chapter 6) |

**Regulatory exchange:**

| Field | Value |
|---|---|
| Workload name | Regulatory exchange |
| Dominant reads | "Generate monthly invoice batch for Peppol submission" (batch extraction) |
| Dominant writes | "Record submission result (accepted/rejected)" |
| Data shape | Ordered XML tree conforming to UBL XSD |
| Consistency | Schema-validated before submission — local validation against XSD required |
| Growth pattern | Document count grows with monthly transaction volume; structure is fixed by the external XSD |

**Partner integration:**

| Field | Value |
|---|---|
| Workload name | Partner integration |
| Dominant reads | "Which drivers operate in high-accident zones?"; "Match internal driver ID to licence registry" (cross-source graph pattern) |
| Dominant writes | "Ingest nightly partner data feed" (bulk merge) |
| Data shape | Triples with URI-based identity; heterogeneous schemas across sources |
| Consistency | Open-world — tolerant of incomplete and conflicting data across sources |
| Growth pattern | Triple count grows with number of partners and data feeds; schema evolves independently per source |

**Fraud monitoring:**

| Field | Value |
|---|---|
| Workload name | Fraud monitoring |
| Dominant reads | "Trace transfers within k hops, filtered by amount and date"; "Find transfer cycles involving flagged accounts" (bounded traversal) |
| Dominant writes | "Add transfer edge when payment exceeds threshold" (edge creation) |
| Data shape | Labelled property graph — nodes (accounts) and edges (transfers) with property maps |
| Consistency | Eventual — hourly query cycle |
| Growth pattern | Edge count grows with payment volume; node count grows with account base; supernode degree grows with processor transaction volume |

**Prediction check:** The fraud monitoring workload has the most complex growth pattern (edge growth + supernode degree growth, affecting traversal cost via d^k). The regulatory exchange workload has the simplest (fixed-schema documents, linear growth with transaction volume).

</details>

---

## Part 2 — Model Assignment (Q3–Q6)

For each workload below, write the justification as specified. After completing all five assignments (Q3–Q6 in this part and Q7 in Part 3), compile them into a single summary table:

| Workload | Model | Cheap operation (mechanism, chapter reference) | Why not [alternative]? |
|---|---|---|---|
| ___ | ___ | ___ | ___ |

---

**Q3 (Transactional core).** The ride-booking and payment-processing workload is assigned to the **relational model**. Write the justification in 3–4 sentences, referencing at least two specific mechanisms from Chapters 2–5 (e.g., FK constraints, ACID isolation, normalisation, CHECK constraints). Then state what the document model would sacrifice if used instead — reference Chapter 6's discussion of multi-document transactions and referential integrity.

<details><summary>Solution — Q3</summary>

The relational model's cheap path is atomic, multi-step writes with declarative constraint enforcement. A ride completion requires inserting a ride record, processing the payment, decrementing promo usage, and updating the driver settlement — all atomically. Chapters 2 and 5 provide the mechanisms: FK constraints ensure the passenger and driver exist before the ride is recorded (Chapter 2's derivation rules), and ACID transaction isolation (Chapter 5) guarantees that either all four operations succeed or none do. CHECK-like constraints enforce business rules such as promo usage limits within the transaction. Normalisation (Chapter 3) ensures each fact lives in one place, eliminating update anomalies when settlement amounts are reconciled.

**Why not the document model?** The document model from Chapter 6 provides single-document atomic writes but not multi-document transactions by default. A ride completion touches multiple entities (ride, payment, promo, settlement) — in MongoDB, these would be separate documents or collections. Multi-document transactions are available (MongoDB 4.0+) but are not the default behaviour and carry performance overhead (Chapter 6's trade-off ledger). More critically, the document model has no FK constraint equivalent — referential integrity between rides, payments, and driver settlements must be enforced entirely in application code, eliminating the schema-level safety net that Chapters 2 and 5 established.

</details>

---

**Q4 (Personalisation layer).** The profile workload is assigned to the **document model**. Write the justification in 3–4 sentences, referencing at least two specific mechanisms from Chapter 6 (e.g., aggregate-shaped reads, structural variation, single-document atomic writes, embed vs reference). Then state what the relational model would sacrifice — reference the multi-table JOIN and EAV workaround from the chapter's Failure 1.

**Before writing**, predict: how many relational tables would a passenger profile require if stored relationally? How many JOINs would the profile-load query need?

<details><summary>Solution — Q4</summary>

The document model's cheap path is aggregate-shaped reads — loading a complete, deeply nested profile in a single read without joins or re-nesting. Chapter 6's aggregate design principle aligns storage with the application's delivery shape: one document per user, read and written as a unit. Structural variation across user types (passenger, driver, merchant) is handled without schema migration — a new user type or a new preference field is a data change, not a DDL change (Chapter 6, Failure 1). The embed-or-reference test (Chapter 6, Section 3.2) governs boundary decisions: saved places (bounded, owned by the user) are embedded; shared data like promo definitions are referenced.

**Why not the relational model?** A passenger profile stored relationally spans at least 4 tables: `UserProfile`, `SavedPlaces`, `PaymentMethods`, `Preferences` (plus `RecentRides` for activity data). The profile-load query requires a 4–5 table JOIN, and the flat result set must be re-nested into JSON for the mobile API — the exact re-nesting overhead described in Chapter 6's Failure 2. Adding a new profile section (e.g., accessibility preferences) requires a new table, a new JOIN, and a schema migration. Over six months, the Chapter 6 failure case documented 14 schema migrations for profile changes alone, each requiring DBA review and coordinated deployment.

**Prediction check:** A passenger profile requires at least 4 relational tables (UserProfile, SavedPlaces, PaymentMethods, Preferences/RecentRides), and the profile-load query needs 3–4 JOINs depending on how many tables are touched.

</details>

---

**Q5 (Regulatory exchange).** The regulatory reporting workload is assigned to **XML/XSD**. Write the justification in 3–4 sentences, referencing at least two specific mechanisms from Chapter 7 (e.g., schema-on-write at the boundary, XSD contract reading, well-formed vs valid distinction, element contract cards). Then state why JSON (Chapter 6) would not suffice — reference the fact that the Peppol portal mandates XML with UBL schema validation, not JSON.

<details><summary>Solution — Q5</summary>

The XML/XSD model's cheap path is schema-validated exchange across organisational boundaries. The Peppol portal validates every submission against a UBL XSD — the schema is imposed externally, not chosen by the development team. Chapter 7's two key mechanisms apply: first, the well-formed vs valid distinction means the team must produce not just syntactically correct XML but structurally valid documents that satisfy `xs:sequence` ordering, `minOccurs`/`maxOccurs` cardinality, and `xs:simpleType` restrictions. Second, Chapter 7's "validate before submission" principle requires local `xmllint --schema` validation before sending, avoiding the 24–48 hour feedback loop of portal rejection.

**Why not JSON (Chapter 6)?** The Peppol portal does not accept JSON. This is not a technical limitation of JSON — JSON Schema can validate structure — but a regulatory constraint: the UBL standard is published as an XSD, and the portal's validation pipeline expects XML. The element ordering requirements (`xs:sequence` mandates a specific order of child elements) have no equivalent in JSON, where object key order is not guaranteed. Chapter 7's Failure documented 38 invoices rejected because the element ordering violated the XSD's `xs:sequence` constraints — a failure mode that does not exist in JSON because JSON has no ordering contract to violate (and therefore no way to satisfy the ordering requirement either).

</details>

---

**Q6 (Partner integration).** The partner integration workload is assigned to **RDF**. Write the justification in 3–4 sentences, referencing at least two specific mechanisms from Chapters 8–9 (e.g., URI-based global identity, open-world assumption, SPARQL federation, multi-source graph merging). Then state what the relational model would sacrifice — reference the brittle ETL scripts from the chapter's Failure 1 and the identifier mismatch problem.

<details><summary>Solution — Q6</summary>

The RDF model's cheap path is cross-source integration with heterogeneous schemas and identifiers. Chapter 8's URI-based global identity means the same driver can be identified by a single URI (`ex:driver_drv4072`) regardless of which source mentions them — the transit authority's licence number and the mapping provider's contributor ID both resolve to the same graph node through URI alignment. The open-world assumption (Chapter 8, Section 3) tolerates incomplete and conflicting data across sources: if the transit authority publishes accident zones but not driver ratings, the RDF graph accommodates the partial information without schema modification. SPARQL (Chapter 9) provides pattern-based querying across the merged graph, enabling "which drivers operate in high-accident zones?" as a single graph pattern query.

**Why not the relational model?** The relational model requires a fixed schema — every source's data must be mapped to predetermined tables and columns before ingestion. The chapter's Failure 1 described ad-hoc ETL scripts that broke every time a partner changed their export format. Each partner uses different identifiers (internal `driver_id`, licence number, contributor ID), and the relational model has no native mechanism for URI-based identity alignment — the mapping must be maintained manually in lookup tables. When the transit authority renames a field or changes a licence number format, the ETL pipeline breaks and requires developer intervention. RDF's schema-optional, URI-based approach absorbs these changes structurally.

</details>

---

## Part 3 — The Fraud-Detection Component (Q7–Q9)

**Q7 (Property graph assignment).** The fraud-monitoring workload is assigned to the **property graph model**. Write the justification in 3–4 sentences, referencing at least two specific mechanisms from Chapter 10 (e.g., edge properties, bounded traversal with per-hop filtering, cycle detection, Cypher's declarative path patterns). Then state what the relational model would sacrifice — reference the recursive CTE from Chapter 10's Q11 (line count, duplicated filtering, string-hack cycle prevention).

**Before writing**, predict: how many lines of Cypher does the "follow the money" query require? How many lines of SQL for the equivalent recursive CTE? (Reference your Chapter 10 comparison table from Q13.)

<details><summary>Solution — Q7</summary>

The property graph model's cheap path is bounded traversal with per-hop filtering and cycle detection. Chapter 10's edge properties make transfer amount, date, and type first-class data on the `:TRANSFERRED_TO` relationship — the same associative entity semantics as Chapter 2's OrderLine, but structural rather than tabular. Cypher's variable-length path patterns (`*1..3`) express bounded traversal in a single clause, and `ALL(r IN relationships(p) WHERE ...)` applies per-hop edge filtering declaratively — Chapter 10's core syntax. Cycle detection is a pattern constraint (`(a)-[*3..6]->(a)`, same variable on both ends), not a separate algorithm.

**Why not the relational model?** Chapter 10's Q11 and Q13 showed the cost: the SQL recursive CTE for the same "follow the money" query requires ~20 lines versus ~6 lines of Cypher. The filtering predicates (amount > $5K, date within 90 days) must be duplicated in both the base case and recursive step of the CTE. Cycle prevention requires a string-concatenation hack (`CAST`, `CONCAT`, `FIND_IN_SET`) — three lines of string manipulation that break on edge cases. Changing the hop limit from 3 to 5 requires restructuring the CTE, while Cypher requires changing one integer: `*1..5`. The recursive CTE is functionally capable but operationally brittle for ad-hoc compliance queries.

**Prediction check:** Cypher: ~6 lines. SQL recursive CTE: ~20 lines. (From Chapter 10, Table 7.)

</details>

---

**Q8.** The fraud-detection graph needs transfer data that originates in the relational payment system. Design this boundary:

- (a) What event triggers the data flow? (e.g., every payment above $X, every flagged-account payment, nightly batch of all payments)
- (b) What transformation is needed? (relational row → graph node/edge: which fields map to node properties, which to edge properties?)
- (c) What consistency is guaranteed? (synchronous? async event? batch?)
- (d) What happens if Neo4j is unavailable when the trigger fires? (data loss? queue? retry?)

<details><summary>Solution — Q8</summary>

**(a)** Every payment above a configurable threshold (e.g., $1,000) triggers an asynchronous event. Flagged-account payments trigger regardless of amount. This balances graph completeness (capturing significant transfers) against edge volume (not flooding the graph with $5 coffee purchases). An alternative design — nightly batch of all payments — would work but introduces up to 24 hours of staleness, which may be unacceptable if the compliance team queries during the day.

**(b)** The relational `Payments` row maps to:
- **Source node:** `(:Account {id: from_account_id})` — MERGE (create if not exists)
- **Target node:** `(:Account {id: to_account_id})` — MERGE (create if not exists)
- **Edge:** `[:TRANSFERRED_TO {amount: payment_amount, date: payment_date, transfer_type: payment_method}]` — CREATE (each payment is a distinct edge)

Node properties come from the `Accounts` table (id, name, type, flagged status). Edge properties come from the `Payments` table (amount, date, method). The `flagged` property on account nodes is updated separately when the compliance team flags an account.

**(c)** Asynchronous with eventual consistency. The relational ACID transaction commits the payment first; the Neo4j edge creation is triggered by an event (message queue or CDC stream) after the commit. The compliance team queries the graph hourly, so a delay of seconds to minutes is acceptable.

**(d)** If Neo4j is unavailable, the event is placed in a retry queue (e.g., a message queue with persistence). The payment is NOT rolled back — the relational transaction has already committed, and the payment is the source of truth. The retry mechanism must be idempotent: if the same event is replayed (e.g., after a network timeout), the MERGE on nodes prevents duplicate nodes, and the edge creation should include a unique transaction ID to prevent duplicate edges.

</details>

---

**Q9.** A compliance officer asks: "If we already have all the payment data in the relational database, why do we need a separate graph database? Can't we just use SQL?"

Write a 3–4 sentence response that:
- Acknowledges the legitimate concern (data duplication, operational complexity)
- Explains what the property graph provides that SQL resists (bounded traversal with per-hop filtering, cycle detection, query expressiveness for path-based questions)
- References Chapter 10's line-count comparison (Q13) as evidence

<details><summary>Solution — Q9</summary>

The concern is legitimate: maintaining a separate graph database introduces data duplication between the relational payment store and the Neo4j transfer graph, plus the operational cost of the data-flow boundary (event triggers, retry logic, identifier mapping). However, the compliance team's core queries — "trace transfers within k hops where each hop exceeds $5,000" and "find transfer cycles involving flagged accounts" — are fundamentally path-based operations that the relational model handles awkwardly. Chapter 10's comparison (Q13) showed the evidence: the same 3-hop filtered traversal requires ~6 lines of Cypher versus ~20 lines of SQL (with duplicated filtering and string-hack cycle prevention). More importantly, changing the hop limit from 3 to 5 requires a single integer change in Cypher but a structural rewrite of the recursive CTE. For a compliance team that adjusts traversal parameters daily based on emerging fraud patterns, the query expressiveness difference is operational, not just aesthetic — it determines whether the analyst can answer a regulator's question in minutes or hours.

</details>

---

## Part 4 — Data-Flow Boundaries (Q10–Q12)

**Q10.** Identify at least four data-flow boundaries in your architecture. For each, fill in the boundary table:

| # | Trigger | Source store (model) | Target store (model) | Transformation | Consistency | Failure mode |
|---|---|---|---|---|---|---|
| 1 | ___ | ___ | ___ | ___ | ___ | ___ |
| 2 | ___ | ___ | ___ | ___ | ___ | ___ |
| 3 | ___ | ___ | ___ | ___ | ___ | ___ |
| 4 | ___ | ___ | ___ | ___ | ___ | ___ |

<details><summary>Solution — Q10</summary>

| # | Trigger | Source store (model) | Target store (model) | Transformation | Consistency | Failure mode |
|---|---|---|---|---|---|---|
| 1 | Ride completion | Relational (MySQL) | Document (MongoDB) | Ride row → `recentRides` array entry + reward point increment; driver name as snapshot | Eventual (async event, 2s acceptable) | Retry queue; ride is committed regardless |
| 2 | Payment > $1,000 | Relational (MySQL) | Property graph (Neo4j) | Payment row → MERGE account nodes + CREATE transfer edge with amount/date/type | Eventual (async event, minutes acceptable) | Retry queue with idempotent replay |
| 3 | Month-end batch | Relational (MySQL) | XML/XSD (Peppol) | Ride + payment rows → UBL XML elements; validate against XSD before submission | Batch (monthly, schema-validated) | Local validation catches errors before submission; rejected invoices are corrected and resubmitted |
| 4 | Nightly ETL | Relational (MySQL) + external feeds | RDF (triple store) | Driver rows → triples with URIs; partner CSV/JSON → triples; identifier alignment via URI mapping | Batch (nightly, tolerant of partial data) | Partial ingestion accepted (open-world); failed sources retried next cycle |

</details>

---

**Q11.** For the ride-completion → profile-update boundary (boundary #1 from Q10), trace the full data flow:

- (a) The relational database commits the ride record and payment in an ACID transaction. An event (message, CDC event, or application callback) is emitted after COMMIT.
- (b) The passenger profile in MongoDB is updated: `recentRides` array gets a new entry, reward points are incremented.
- (c) **Question:** If the MongoDB update fails (network timeout), what happens? The ride is committed in the relational store but the profile is stale. Is this acceptable? What mechanism would you use to recover? *(Options: retry queue, periodic reconciliation batch, idempotent update design.)*
- (d) Now consider the relational → monthly e-invoice batch boundary (boundary #3). At what point does Chapter 7's "validate before submission" principle apply? What is the cost of skipping local XSD validation and letting the Peppol portal reject the batch instead? *(Reference: Chapter 7's 24–48 hour feedback loop.)*

<details><summary>Solution — Q11</summary>

**(c)** The ride is committed and valid — the relational store is the source of truth for ride data. The MongoDB profile being temporarily stale is acceptable under the eventual consistency contract (2-second delay is normal; a network timeout may cause a longer delay). Recovery options:

- **Retry queue (recommended):** The failed event is placed in a persistent message queue and retried with exponential backoff. The update operation should be **idempotent** — using the ride ID as a deduplication key so that replayed events do not create duplicate `recentRides` entries. This handles transient failures automatically.
- **Periodic reconciliation batch:** A nightly job compares the relational ride table against MongoDB profiles and patches any missing entries. This is a safety net for the retry mechanism, not a replacement.
- **Idempotent update design:** The MongoDB update uses `$addToSet` or a conditional update with the ride ID to ensure that the same ride is never added twice, even if the event is replayed multiple times.

**(d)** Chapter 7's "validate before submission" principle applies *before* the batch is sent to the Peppol portal — specifically, after XML generation and before network transmission. The development team should run `xmllint --schema` (or equivalent programmatic validation) against the UBL XSD on every generated invoice document. If validation fails, the error is caught immediately and can be corrected within the same batch cycle.

The cost of skipping local validation: the Peppol portal rejects invalid invoices with error codes, but the feedback loop is 24–48 hours (Chapter 7, Failure). This means a single invalid element (e.g., wrong ordering within `<cac:InvoiceLine>`) blocks the entire monthly batch for 1–2 days. Local validation catches this in seconds. The principle is the same as Chapter 7's: validate at the boundary you control, not at the boundary you do not.

</details>

---

**Q12.** The partner integration workload (RDF) needs driver data that originates in the relational system and the document profiles. Design the identifier alignment strategy:

- (a) The relational system uses `driver_id = 4072` (integer). The MongoDB profile uses `userId: "driver-4072"` (string). The transit authority uses `licence_SG12345`. The RDF graph needs a single URI for each driver. What URI scheme would you use?
- (b) How would you maintain the mapping across all three source identifiers?
- (c) What updates are needed when the transit authority changes a driver's licence number?

<details><summary>Solution — Q12</summary>

**(a)** A URI scheme based on the canonical internal identifier: `ex:driver_drv4072` (or `https://ridelink.example.org/driver/DRV-4072`). The internal ID (`DRV-4072`) is the canonical identifier because it is controlled by the super-app team and stable across system migrations. The integer `driver_id = 4072` and the string `userId: "driver-4072"` are both derivable from the canonical form.

**(b)** The mapping is maintained as triples in the RDF graph itself:

```turtle
ex:driver_drv4072
    ex:internalId     "DRV-4072" ;
    ex:relationalId   4072 ;
    ex:transitLicence  "SG12345" ;
    rdfs:label         "Priya Nair" .
```

Each source identifier is a property of the driver's URI node. When ingesting data from the transit authority, the ETL process looks up the transit licence number to find the corresponding URI. When ingesting from the relational store, it uses the `relationalId` mapping. This is Chapter 8's URI alignment principle made concrete: same URI = same node = edges from different sources connect automatically.

**(c)** When the transit authority changes a driver's licence number (e.g., from `SG12345` to `SG12345-R`):
- Update the mapping triple: remove `ex:transitLicence "SG12345"`, add `ex:transitLicence "SG12345-R"`.
- The driver's URI (`ex:driver_drv4072`) does not change — it is based on the internal ID, not the external one.
- All existing edges connected to `ex:driver_drv4072` (from the transit authority's data, the mapping provider's data, and the internal data) remain valid because they reference the URI, not the licence number.
- If the mapping were maintained in ad-hoc ETL scripts (the relational alternative from the chapter's Failure 1), the licence-number change would break the join condition in the ETL, requiring developer intervention to update the script.

</details>

---

## Part 5 — Architecture Diagram (Q13–Q14)

**Q13.** Draw the system architecture diagram. It should include:
- Five data stores (labelled with model type and the workload served)
- The services that read from / write to each store
- Data-flow arrows between stores, each annotated with: trigger, consistency contract, and direction
- A legend explaining the symbols

You may draw this by hand, in a drawing tool, or describe it in structured text. The key requirement is that every data-flow boundary from Q10 appears as an annotated arrow.

<details><summary>Solution — Q13</summary>

```
                    Super-App Multi-Model Architecture

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  ┌─────────────────────┐                                        │
  │  │  RELATIONAL (MySQL)  │                                        │
  │  │  Transactional Core  │                                        │
  │  │  ─────────────────── │                                        │
  │  │  Services:           │                                        │
  │  │  • Ride booking      │                                        │
  │  │  • Payment processing│                                        │
  │  └──┬──────┬──────┬─────┘                                        │
  │     │      │      │                                              │
  │     │ (1)  │ (2)  │ (3)                                          │
  │     │      │      │                                              │
  │     ▼      │      ▼                                              │
  │  ┌──────────┐  │  ┌───────────────┐                              │
  │  │ DOCUMENT  │  │  │   XML/XSD     │                              │
  │  │ (MongoDB) │  │  │   (Peppol)    │                              │
  │  │ Personal- │  │  │   Regulatory  │                              │
  │  │ isation   │  │  │   reporting   │                              │
  │  │ ───────── │  │  │   ──────────  │                              │
  │  │ Passenger │  │  │   E-invoices  │                              │
  │  │ Driver    │  │  │   Tax filings │                              │
  │  │ Merchant  │  │  └───────────────┘                              │
  │  │ profiles  │  │                                                │
  │  └──────────┘  │                                                 │
  │                │                                                 │
  │                ▼            (4)                                   │
  │  ┌──────────────────┐     ┌───────────────────┐                  │
  │  │  PROPERTY GRAPH   │     │   RDF              │                  │
  │  │  (Neo4j)          │     │   (Triple Store)    │                  │
  │  │  Fraud monitoring │     │   Partner           │                  │
  │  │  ──────────────── │     │   integration       │                  │
  │  │  Transfer network │     │   ─────────────     │                  │
  │  │  Cycle detection  │     │   Transit auth.     │                  │
  │  │  Flagged accounts │     │   Mapping provider  │                  │
  │  └──────────────────┘     │   ID alignment      │                  │
  │                           └───────────────────┘                  │
  └──────────────────────────────────────────────────────────────────┘

  Data-flow arrows:
  (1) Relational → Document:  Trigger: ride completion
                               Consistency: eventual (async, 2s)
  (2) Relational → Prop Graph: Trigger: payment > $1,000
                               Consistency: eventual (async)
  (3) Relational → XML/XSD:   Trigger: month-end batch
                               Consistency: batch (monthly, validated)
  (4) Relational + external → RDF: Trigger: nightly ETL + partner feeds
                               Consistency: batch (nightly, open-world)

  Legend:
  ┌──────┐ = Data store (model type and workload labelled)
  ──►      = Data-flow arrow (trigger + consistency annotated)
```

</details>

---

**Q14.** Review your diagram against Sanity Checks 1–7 from the chapter narrative. For each check, note whether your diagram passes or requires a change. Then answer one additional question:

- Is there any store that only *receives* data from other stores but is never queried directly by a service? If so, what justifies its existence as a separate store?

<details><summary>Solution — Q14</summary>

**Sanity check review:**

| Check | Pass/Fail | Notes |
|---|---|---|
| 1 — Workload decomposition | Pass | Five distinct workloads identified, not "one workload: the super-app." |
| 2 — Forced assignment | Pass | Each model is assigned to a workload whose access pattern matches its cheap path. No model is assigned based on incidental capabilities (e.g., XML for internal validation). |
| 3 — Missing boundaries | Pass | Four data-flow arrows present; all cross-store data flows are annotated. |
| 4 — Consistency confusion | Pass | Only the relational store's internal operations are labelled ACID. Cross-store flows are labelled eventual or batch. |
| 5 — Model-strength inversion | Pass | No model is assigned to a workload that contradicts its native strengths. |
| 6 — Consolidation | Pass (for this system) | All five models have workload justification. If regulatory reporting or partner integration were removed from the system requirements, the corresponding models should be removed. |
| 7 — Identifier drift | Acknowledged | The diagram's data-flow arrows imply identifier mappings at each boundary. If the relational `driver_id` scheme changes, three of four boundaries break (document, graph, RDF). The XML boundary is insulated (uses national registry ID). The architecture should document the canonical identifier (`DRV-5582`) and the mapping strategy. |

**Additional question:** The XML/XSD store arguably only *produces* documents (generated from relational data, submitted to Peppol) and records submission results. It does not serve a query workload in the traditional sense. Its existence is justified by the *external mandate*: the Peppol portal requires XML conforming to UBL XSD. The "store" here is less a persistent database and more a generation-validation-submission pipeline — but it is architecturally distinct because the transformation (relational rows → ordered XML tree) and validation (against externally mandated XSD) are non-trivial. The RDF store receives data from external feeds and from the relational store, but it IS queried directly by the partner integration service ("which drivers operate in high-accident zones?"), so it is not receive-only.

</details>

---

## Part 6 — Substitution Testing (Q15–Q17)

**Q15.** Choose the personalisation workload (currently assigned to the document model). Hypothetically substitute the relational model. Trace what happens:

- (a) How would you store passenger, driver, and merchant profiles in a relational schema? (Subtype tables? EAV? Wide table with NULLs?)
- (b) What is the profile-load query's JOIN count?
- (c) What happens when the product team adds a new preference field? (DDL change? Another nullable column?)
- (d) **Verdict:** Is the substitution viable? At what scale or feature velocity does it break?

<details><summary>Solution — Q15</summary>

**(a)** Three options, each with costs:
- **Wide table with NULLs:** A single `UserProfile` table with 40+ columns (passenger fields, driver fields, merchant fields). Any given row uses fewer than half. The schema no longer communicates what a "passenger" or "driver" looks like. This is Chapter 6's Failure 1, option (a).
- **Subtype tables:** `PassengerProfile`, `DriverProfile`, `MerchantProfile` with shared columns in a base `UserProfile` table. Correct but rigid — a fourth role requires a new table, new JOINs, new application logic.
- **EAV:** `UserAttribute(user_id, attr_name, attr_value)`. Flexible but type-unsafe — `licenceExpiry` (date) and `maxDistance` (integer) are both stored as strings. Chapter 6's Failure 1, option (b).

The subtype-table approach is the most defensible relational design.

**(b)** With subtype tables, a driver profile-load query joins: `UserProfile` + `DriverProfile` + `PreferredZones` (multi-valued) + `RecentTrips` = 4 tables, 3 JOINs minimum. The result set is flat and must be re-nested into JSON for the mobile API.

**(c)** A new preference field (e.g., `accessibilityNeeds`) requires: ALTER TABLE to add the column, application code update to handle the new field, schema migration coordinated across environments. In the document model, the same change is: insert a new field in the JSON document. No schema migration, no DDL, no deployment coordination.

**(d)** The substitution is viable at small scale (few user types, low feature velocity). It breaks when: (1) the number of user types exceeds 3–4 (each new type requires a new subtype table and new JOIN chains), or (2) the product team ships profile changes more than once per sprint (each change requires a schema migration, and Chapter 6 documented the cost: 14 migrations in 6 months, 3–4 engineering-days per sprint on migration logistics). The document model's advantage is not performance — it is development velocity for structurally variable data.

</details>

---

**Q16.** Choose the fraud-monitoring workload (currently assigned to the property graph). Hypothetically substitute the relational model with recursive CTEs. Reference Chapter 10's Q11 and Q13 comparison:

- (a) How many lines of SQL are needed for the 3-hop filtered traversal?
- (b) How does cycle prevention work in the CTE? (String concatenation + FIND_IN_SET.)
- (c) What happens when the compliance team changes the hop limit from 3 to 5?
- (d) **Verdict:** Is the substitution viable for ad-hoc compliance queries?

<details><summary>Solution — Q16</summary>

**(a)** Chapter 10's comparison (Table 7) showed ~20 lines of SQL versus ~6 lines of Cypher. The SQL includes: base case (5 lines), recursive step (7 lines with duplicated filtering), cycle-prevention hack (3 lines of string manipulation), and the outer SELECT.

**(b)** The CTE tracks visited nodes by concatenating account IDs into a comma-separated string (`CAST(t.from_id AS CHAR(500))`, `CONCAT(mt.path, ',', t.from_id)`). Cycle prevention checks `FIND_IN_SET(t.to_id, mt.path) = 0`. This breaks when: (1) account IDs contain commas, (2) the path string exceeds 500 characters (silently truncated), or (3) the concatenation produces ambiguous substring matches. Cypher handles this natively through relationship uniqueness — no string manipulation required.

**(c)** Changing from 3 to 5 hops requires modifying `WHERE mt.depth < 3` to `WHERE mt.depth < 5` — a simple change. However, the query's complexity and execution time grow substantially: more recursive iterations, more string concatenation, and the cycle-prevention hack becomes increasingly unreliable as paths grow longer. In Cypher: change `*1..3` to `*1..5` — one integer.

**(d)** The substitution is technically viable for fixed, simple traversals. It becomes operationally unviable for ad-hoc compliance queries where: (1) the hop limit changes frequently (compliance officers adjust parameters based on emerging patterns), (2) cycle detection is required (the string-hack cycle prevention is fragile and hard to trust), and (3) the compliance team needs to read and audit the query logic (the CTE's control flow is opaque compared to Cypher's declarative pattern). The property graph's advantage for this workload is expressiveness and auditability, not just performance.

</details>

---

**Q17.** Choose one workload where substitution *does* work — where the assigned model could be replaced by another without significant degradation. Explain why.

*(Hint: think about which workload has the lowest volume and simplest access pattern. At what scale does a specialised model justify its boundary cost?)*

<details><summary>Solution — Q17</summary>

The **regulatory exchange** workload could be served by the relational model without a separate XML/XSD component. The relational database already contains the ride and payment data needed for invoices. The XML generation could be handled by application code: a monthly batch job queries the relational store, constructs XML strings programmatically, validates against the XSD using a library (e.g., Python's `lxml`), and submits to Peppol. No separate "XML store" is needed — the XML documents are transient artefacts, not persistent data.

This works because: (1) the volume is low (monthly batch, not per-transaction), (2) the access pattern is simple (batch extraction + transformation, not ad-hoc querying of XML data), and (3) the XML documents are generated from relational data and then submitted — they are not queried or stored long-term.

The specialised XML/XSD component is justified when: (1) the team needs to maintain and evolve XSD-aware tooling (contract card reading, local validation pipelines), (2) multiple external schemas are involved (not just Peppol but also tax authority, insurance, banking regulators), or (3) the XML documents need to be queried and archived as first-class data. At low volume with a single schema, the boundary cost of a separate component may exceed the benefit.

This is the consolidation principle from the chapter's Mechanism 3: every additional model adds boundary complexity. If the workload can be adequately served by the existing model with a reasonable workaround, the simpler architecture is often the better one.

</details>

---

## Part 7 — Reflection (Q18–Q19)

**Q18.** What surprised you most in this exercise? Consider:
- Was there a model assignment that felt forced (the workload did not clearly need a separate model)?
- Was there a boundary that was harder to design than you expected?
- Did the substitution testing (Q15–Q17) change your view on any assignment?

Write 3–4 sentences.

<details><summary>Solution — Q18</summary>

*(This is a reflection question — answers will vary. A strong answer might note:)*

The boundary design (Q10–Q11) was harder than the model assignment. Assigning models to workloads felt systematic — the decision framework from Chapter 1 and the cost analysis from Table 3 made the choices defensible. But designing the data-flow boundaries required thinking about failure modes, retry logic, and consistency contracts — topics that no single prior chapter fully prepared for. The identifier alignment problem (Q12) was unexpectedly central: it appeared in every boundary, not just the RDF one. The substitution testing (Q17) revealed that the XML/XSD assignment is the weakest — at low volume, the relational model with application-level XML generation is a simpler architecture. This honesty about when a model is unnecessary feels like the most important lesson.

</details>

---

**Q19.** A hiring manager asks you: "We're building a new ride-hailing app. Should we use a relational database, MongoDB, or a graph database?"

In 3–4 sentences, explain why the question is malformed and what the right question is. Your answer should connect to the principle from Chapter 3 — that even a single database can have two schema designs (BCNF + star schema) for different workloads — and show how this chapter generalises that lesson to multiple models across multiple workloads.

<details><summary>Solution — Q19</summary>

The question is malformed because it assumes the app has a single workload that a single model should serve. A ride-hailing app has at least three distinct workloads: transactional (ride booking + payments requiring ACID), personalisation (user profiles requiring aggregate-shaped reads), and potentially fraud monitoring (transfer traversal requiring per-hop filtering). Each workload has a different dominant access pattern, and no single model makes all of them cheap.

The right question is: "What are the workloads in our ride-hailing app, and which data model fits each?" This generalises Chapter 3's insight: even within a single relational database, the course showed that OLTP and OLAP workloads needed different schema designs (BCNF for transactional integrity, star schema for reporting performance). This chapter extends that same principle beyond a single model: different workloads may need not just different schemas but different data models entirely — and the design challenge is not choosing one model but decomposing the system, assigning models to workloads, and designing the boundaries between them.

</details>

---

## Deliverable

Submit completed responses for Q1–Q19:

- **Q1–Q2:** Workload decomposition table and workload cards
- **Q3–Q7:** Model assignments with two-part justifications (cheap operation + why not alternative), compiled into a summary table
- **Q8–Q9:** Fraud-detection boundary design and compliance officer response
- **Q10–Q12:** Boundary specifications (table), ride-completion trace, identifier alignment strategy
- **Q13–Q14:** Architecture diagram (legible, with annotated data-flow arrows) and sanity-check review
- **Q15–Q17:** Substitution analyses (two substitutions that break + one that works)
- **Q18–Q19:** Reflection (3–4 sentences each)

Written responses should reference specific chapters and mechanisms — vague justifications receive no credit.
