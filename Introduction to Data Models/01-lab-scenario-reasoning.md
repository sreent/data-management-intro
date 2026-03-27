# Topic 1 Lab — Scenario-Based Reasoning: Matching Models to Workloads

This is a reasoning lab, not a coding lab. Part A checks your command of the chapter's vocabulary and decision framework. Parts B and C apply that framework to realistic scenarios, building the conceptual foundation that Topics 2–10 depend on.

Use the formal vocabulary (data model, workload, schema, constraint, query) and reference specific chapter tables (especially Tables 7–11 for the enforcement spectrum and decision framework, and Table 1 for vocabulary) throughout your reasoning.

**Time budget:** Part A ~8 min | Part B ~35 min | Part C ~10 min | **Total ~53 min**

---

## Part A — Concept Check

Answer each question by selecting **one** option. For each, write one sentence justifying your choice.

---

**Q1. Vocabulary.** A colleague says: "We should switch our data model from MySQL to MongoDB." What is wrong with this statement?

- (A) MySQL and MongoDB implement the same data model, so switching achieves nothing.
- (B) MySQL and MongoDB are databases, not data models; the decision should be framed as switching from the relational model to the document model.
- (C) MongoDB is not a data model because it does not enforce schemas.
- (D) Nothing is wrong — "data model" and "database" are interchangeable terms.

---

**Q2. Pattern classification.** A biomedical consortium needs to answer: "Which genes are associated with diseases treated by drugs targeting the ACE2 receptor?" The data exists in three independent sources with different schemas and different identifiers. Which row in the decision framework's Step 1 table (Table 9) matches this workload?

- (A) Aggregate read
- (B) Cross-entity aggregation
- (C) Bounded traversal
- (D) Cross-source integration

---

**Q3. Enforcement spectrum.** You insert a document into MongoDB (no validation rules configured) with `price` set to the string `"abc"` instead of a number. What happens?

- (A) MongoDB rejects the insert with a type error.
- (B) MongoDB accepts the document — the system is schema-on-read by default.
- (C) MongoDB silently converts `"abc"` to `0`.
- (D) MongoDB accepts the document but marks it as invalid for later cleanup.

---

**Q4. Mismatch diagnosis.** A system stores data in model X. The team reports: "Queries are correct but slow. Every read reconstructs nested output from flat, normalised rows using multiple JOINs. Adding a new data section requires a schema migration." Which type of mismatch is this?

- (A) Guarantee mismatch — the model lacks the consistency mechanism the workload demands.
- (B) Shape mismatch — the storage shape fights the delivery shape.
- (C) Schema mismatch — the schema is too permissive for the workload.
- (D) Query mismatch — the query language cannot express the required operation.

---

**Q5. Model–workload match.** A government tax authority receives 2 million annual tax returns from employers. Each return must conform to a legally mandated schema (published as an XSD). Returns that fail validation are rejected with error codes *before* entering any system. Which model does the decision framework select?

- (A) Relational — because CHECK constraints enforce data validity.
- (B) Document — because each tax return is a self-contained entity.
- (C) XML/XSD — because the workload is schema-validated exchange across an organisational boundary.
- (D) RDF — because data comes from multiple independent sources.

---

## Part B — Scenario Reasoning

Each scenario presents a real-world system. Apply the decision framework, compare models, and articulate trade-offs. Use the formal vocabulary and reference the chapter's tables by number.

---

### Scenario 1: RideLink vs NeoBank — Why the Same Model Cannot Serve Both

**RideLink** is a ride-hailing super-app. The product team's primary operation is "load the complete profile for the app home screen" — a single API call returning name, default address, preferred payment method, active promotions, and ride preferences. A passenger profile contains: name, phone, a list of saved addresses (each with label, street, lat/lng), a list of payment methods (each with type, last4, whether default), preferences (language, currency, notifications), and active promotions (code, expiry, used). Different user types (passenger, driver, merchant) have different profile structures. New profile sections are added every quarter.

**NeoBank** is a digital bank. Every fund transfer creates two ledger entries: a debit on the sender's account and a credit on the receiver's account. The compliance team needs: running balances per account, monthly aggregate reports (total inflows, total outflows), and guaranteed atomicity — both entries exist or neither does.

**Q6.** For each system:
- (a) Identify the primary query pattern (Table 9), the consistency requirement (Table 10), and the schema stability (Table 11). Present your answers in two side-by-side decision framework tables.
- (b) NeoBank also needs a "transaction receipt" page — a single self-contained view of one transfer (sender, receiver, amount, timestamp, status). For this specific sub-workload, which model would align better? What does this suggest about systems with multiple workloads?

**Q7.** The mobile app expects a single nested JSON response for RideLink profiles. Sketch the relational shape (list the tables and JOINs required) and the document shape (describe the JSON structure). Which shape aligns with the delivery format? What does the misaligned shape pay on every read?

**Q8.** Two transfers arrive simultaneously at NeoBank: one crediting $500, one debiting $300, both for account A-1001.
- (a) Describe what happens in the document model (default behaviour, no multi-document transactions configured).
- (b) Describe what happens in the relational model. Name the mechanism that prevents the lost-update problem.

---

### Scenario 2: TelX — Fraud Detection

TelX operates a telecommunications network. Every call generates a record: caller, callee, timestamp, duration, cell tower. The fraud team's primary operation is: "Starting from a phone number flagged for SIM-swap fraud, find all numbers called within 2 hops in the last 7 days, and for each, show the call frequency and total duration." The investigation often expands: "Now show 3 hops." "Now 5 hops." The depth is not known in advance.

**Q9.** Describe the access pattern using the terms: starting point, edges, hops, per-hop filter. Which row in Table 9 matches? Then compare the two shapes:
- (a) *Property graph:* What are the nodes? What are the edges? What properties do edges carry? Describe the traversal in one sentence: "Start at ___, follow ___ edges where ___, collect ___ at each hop."
- (b) *Relational:* You have a `Calls` table with columns `caller`, `callee`, `timestamp`, `duration`. How many self-joins for 2 hops? What happens at 5 hops? N hops? What structural difference makes variable-depth traversal natural in the graph model but awkward in the relational model?

**Q10.** The CFO asks: "What is the total call duration across all subscribers this month?" — a global aggregation. Which model handles this efficiently? TelX also needs subscriber billing (monthly invoices, payment history, ACID guarantees). Is a single model sufficient for both workloads? Justify your answer by referencing the trade-off table.

---

### Scenario 3: International Shipping — Two Workloads, Two Models

A logistics company ships packages across borders. Two things must happen for each shipment:

1. **Internal tracking:** The company tracks shipment status — picked up, in transit, customs hold, delivered — with timestamped state transitions, aggregate reporting (packages per route, average transit time), and ACID guarantees.
2. **Customs declaration:** For each border crossing, the company must produce a customs declaration conforming to the destination country's published schema. The customs authority validates the document and rejects non-conforming submissions.

**Q11.** Walk through the decision framework for each workload separately. Fill in both tables:

*Internal tracking:*

| Step | Your assessment | Justification |
|---|---|---|
| Primary query pattern | ___ | ___ |
| Consistency requirement | ___ | ___ |
| Schema stability | ___ | ___ |
| Model selection | ___ | ___ |
| Costs accepted | ___ | ___ |

*Customs declaration:*

| Step | Your assessment | Justification |
|---|---|---|
| Primary query pattern | ___ | ___ |
| Consistency requirement | ___ | ___ |
| Schema stability | ___ | ___ |
| Model selection | ___ | ___ |
| Costs accepted | ___ | ___ |

**Q12.** Why can a single model not serve both workloads? State specifically what each model would lose if forced to handle the other workload. Who controls the customs schema — the logistics company or the destination country — and how does this affect model selection?

---

## Part C — Synthesis

**Q13. Right choice / wrong choice.** Using what you have learned from the scenarios above and the chapter's trade-off table, complete the following for each model. Each cell should be a specific workload condition, not a generic statement.

| Model | Right choice when... | Wrong choice when... |
|---|---|---|
| Relational | ___ | ___ |
| Document | ___ | ___ |
| Property graph | ___ | ___ |
| XML/XSD | ___ | ___ |
| RDF | ___ | ___ |

**Q14. Close the loop.** Return to the two failures from the chapter opening (RideLink storing profiles relationally; NeoBank storing its ledger in a document database):
- (a) For each failure, name the mismatch type (shape mismatch or guarantee mismatch).
- (b) Referencing your Q6 framework tables (do not reproduce them), explain in two sentences per failure how the framework would have prevented the engineering mistake.
- (c) Across all three scenarios in this lab, a recurring pattern emerged: single-model assumptions break when a system has multiple workloads. State this principle in one sentence using the course vocabulary.

---

## Deliverable

- **Part A** (Q1–Q5): Five MCQ answers, each with a one-sentence justification
- **Part B** (Q6–Q12): Completed scenario analyses — decision framework tables, shape comparisons, and trade-off articulation
- **Part C** (Q13–Q14): Completed synthesis table and failure re-analysis

---

## Solutions

Complete your own answers before reviewing the solutions below. Each explanation references specific chapter tables so you can trace the reasoning back to the source material.

---

### Part A — Concept Check Solutions

<details>
<summary><strong>Q1 Solution — Click to reveal</strong></summary>

**Answer: (B)**

MySQL and MongoDB are *databases* (running systems), not *data models* (conceptual paradigms). The chapter distinguishes these explicitly: "A data model is a conceptual paradigm — a way of structuring and connecting data. A database is a running system (MySQL, MongoDB, Neo4j) that implements a model." The correct framing is: "We should switch from the relational model to the document model" — then evaluate which databases implement each.

- (A) is wrong because MySQL implements the relational model while MongoDB implements the document model — they are structurally different.
- (C) is wrong because schema enforcement is not what defines a data model; the document model is a data model despite its schema-on-read default.
- (D) is wrong because the distinction between model and database is central to the course vocabulary (Table 1).

</details>

---

<details>
<summary><strong>Q2 Solution — Click to reveal</strong></summary>

**Answer: (D) Cross-source integration**

The defining characteristic is that data already exists in three *independent* sources with *different schemas* and *different identifiers*. No single source can answer the query alone. Table 9 maps this pattern to cross-source integration, which points toward RDF.

- (A) Aggregate read describes loading one self-contained entity — not merging across independent sources.
- (B) Cross-entity aggregation (SUM, GROUP BY) assumes data lives in one system with a shared schema.
- (C) Bounded traversal describes following relationships N hops from a starting node — the access pattern here is integration across sources, not depth-first traversal within one.

</details>

---

<details>
<summary><strong>Q3 Solution — Click to reveal</strong></summary>

**Answer: (B)**

MongoDB without validation rules is schema-on-read by default — it sits at the "nothing rejects" end of the enforcement spectrum (Table 7). The document is accepted as-is. The type error surfaces only when the application *reads* and tries to treat `"abc"` as a number. Compare to PostgreSQL (engine rejects at insert time) where a `price NUMERIC NOT NULL` column would refuse the string immediately.

- (A) describes relational behaviour (engine rejects), not document behaviour.
- (C) and (D) are fabricated — MongoDB performs no implicit conversion and has no "invalid" marking mechanism by default.

</details>

---

<details>
<summary><strong>Q4 Solution — Click to reveal</strong></summary>

**Answer: (B) Shape mismatch**

The symptoms are diagnostic: "nested output from flat, normalised rows" means the storage shape (flat tables) fights the delivery shape (nested structure). "Multiple JOINs" is the reconstruction cost. "Schema migration for new sections" is the rigidity cost. This matches Failure 1 (RideLink) exactly — a shape mismatch, not a guarantee mismatch.

- (A) Guarantee mismatch would manifest as data integrity bugs (lost updates, inconsistent balances) — not slow reads and JOIN overhead.
- (C) and (D) are not terms from the chapter's vocabulary; the two mismatch types introduced are shape mismatch and guarantee mismatch.

</details>

---

<details>
<summary><strong>Q5 Solution — Click to reveal</strong></summary>

**Answer: (C)**

The workload is schema-validated exchange across an organisational boundary (Table 9). The critical detail is validation *before* entry — the tax authority rejects non-conforming submissions at the boundary. XML/XSD sits at "validator rejects" on the enforcement spectrum (Table 7).

- (A) is tempting but wrong: relational CHECK constraints operate at *insert time* — they cannot reject a document before it reaches the database. The tax authority needs boundary validation, not insert-time validation.
- (B) is wrong because although each return is self-contained, the workload is not aggregate read — it is schema-validated exchange with an external party that controls the schema.
- (D) is wrong because the data comes from many employers, but they all submit to *one* authority using *one* published schema — this is not cross-source integration with independent schemas.

</details>

---

### Part B — Scenario Reasoning Solutions

**Hint:** For each system, start with the dominant operation — what does the user or analyst do most often? Then match that operation to a row in Table 9. For sub-part (b), consider: is a transaction receipt more like a self-contained entity or a cross-entity aggregation?

<details>
<summary><strong>Q6 Solution — Click to reveal</strong></summary>

**(a) Decision framework tables:**

**RideLink:**

| Step | Assessment | Justification |
|---|---|---|
| Primary query pattern | Aggregate read (Table 9) | "Load the complete profile in one call" — one entity, self-contained, all related data |
| Consistency requirement | Eventual consistency (Table 10) | Profiles are authored individually; brief staleness (e.g., a promotion expiring seconds late) is acceptable |
| Schema stability | Evolving (Table 11) | Different user types have different structures; new profile sections added quarterly |
| Model selection | **Document** | All three steps align with the document model |
| Costs accepted | Cross-document queries are expensive (e.g., "how many users have 3+ saved addresses?"); no referential integrity across documents |

**NeoBank:**

| Step | Assessment | Justification |
|---|---|---|
| Primary query pattern | Cross-entity aggregation (Table 9) | Running balances, monthly totals — SUM and GROUP BY across many ledger entries |
| Consistency requirement | ACID transactions (Table 10) | Both debit and credit entries must exist or neither; concurrent transfers must not corrupt balances |
| Schema stability | Fixed (Table 11) | Ledger structure (account, entry type, amount, timestamp) is stable and well-defined |
| Model selection | **Relational** | All three steps align with the relational model |
| Costs accepted | Schema rigidity; write scalability under high transaction volumes; impedance mismatch if downstream systems expect nested formats |

The two systems both store data about entities, yet different models suit each because the *workloads* differ: aggregate read vs cross-entity aggregation, eventual consistency vs ACID.

**(b) Transaction receipt sub-workload:**

The transaction receipt is a single self-contained entity — all the data (sender, receiver, amount, currency, timestamp, status) in one view. This is an **aggregate read**, which aligns with the **document model**. One key lookup returns the full receipt with no JOINs.

This suggests that systems with **multiple workloads** may need **multiple models** — or at minimum, different access patterns within the same system may point to different models. NeoBank's primary workload (cross-entity aggregation, ACID) demands the relational model, but a secondary workload (displaying a single receipt) would benefit from a document shape. Chapter 11 addresses this directly: when no single model satisfies all workloads, the system may split — one model per workload, with explicit boundaries between them.

</details>

---

**Hint:** List the relational tables needed (at least five). Count the JOINs. Then describe the equivalent JSON structure — which shape matches the mobile app's expected response?

<details>
<summary><strong>Q7 Solution — Click to reveal</strong></summary>

**Relational shape:** At minimum, the tables `Users`, `Addresses`, `PaymentMethods`, `Preferences`, and `Promotions` — connected by `user_id` as a foreign key. Loading one passenger's profile requires a 5-table JOIN (`Users` JOIN `Addresses` JOIN `PaymentMethods` JOIN `Preferences` JOIN `Promotions`). The result is a flat row set that the application must re-nest into JSON.

**Document shape:** A single JSON document:

```json
{
  "user_id": "P-3921",
  "name": "Mei Lin",
  "phone": "+65-9123-4567",
  "addresses": [ { "label": "Home", "street": "12 Orchard Rd" }, ... ],
  "payment_methods": [ { "type": "visa", "last4": "4242", "default": true } ],
  "preferences": { "language": "en", "currency": "SGD" },
  "promotions": [ { "code": "RIDE50", "expiry": "2024-06-30" } ]
}
```

The **document shape** aligns with the delivery format — the mobile app expects nested JSON, and the document *is* nested JSON. One read, no reconstruction.

The **relational shape** pays the cost on every read: execute the multi-table JOIN, receive flat rows, and re-nest them in application code. This is shape misalignment — the storage shape (flat, normalised) fights the delivery shape (nested, self-contained).

</details>

---

**Hint:** Think about what happens when two processes read the same balance at the same time. What mechanism does the relational model have that the document model lacks by default?

<details>
<summary><strong>Q8 Solution — Click to reveal</strong></summary>

**(a) Document model (default behaviour):** Both transactions read the current balance of A-1001 (say, $1,000). Transaction 1 computes $1,000 + $500 = $1,500 and writes it. Transaction 2 computes $1,000 − $300 = $700 and writes it. Whichever writes last overwrites the other. The final balance is either $1,500 or $700 — both wrong (the correct answer is $1,200). This is the **lost-update problem**. Without multi-document ACID transactions configured, the document model's default behaviour offers no mechanism to prevent it.

**(b) Relational model:** The database wraps each transfer in a transaction with isolation guarantees. Under serialisable or snapshot isolation, one transaction acquires a lock (or detects a conflict) on the balance row. The second transaction must wait (or retry). Both updates are applied sequentially: $1,000 + $500 = $1,500, then $1,500 − $300 = $1,200. The mechanism is **ACID transactions** — specifically, the isolation property prevents concurrent access from producing an incorrect result. The relational model enforces this by default; the document model requires explicit opt-in (MongoDB 4.0+ multi-document transactions).

</details>

---

**Hint:** Identify the four components: starting point, edges, hops, and per-hop filter. For the graph shape, name the nodes, edges, and edge properties. For the relational version, count the self-joins at 2, 5, and N hops — what happens to the query each time the analyst increases depth?

<details>
<summary><strong>Q9 Solution — Click to reveal</strong></summary>

**Access pattern:** The pattern is a **bounded traversal**: the *starting point* is a flagged phone number; the *edges* are call records (CALLED relationships); the *hops* are variable (2, then 3, then 5 — depth not known in advance); the *per-hop filter* is "within the last 7 days." At each hop, the fraud team collects call frequency and total duration. This matches the **bounded traversal** row in Table 9, which points toward the **property graph** model.

**(a) Property graph shape:**
- **Nodes:** Phone numbers (or subscribers), each with properties (number, name, flagged status).
- **Edges:** CALLED relationships, each carrying properties: `timestamp`, `duration`, `cell_tower`.
- **Traversal:** "Start at the flagged phone number, follow CALLED edges where the timestamp is within the last 7 days, collect call frequency and total duration at each hop."

The traversal extends naturally: changing from 2 hops to 5 hops means adjusting a depth parameter, not rewriting the query.

**(b) Relational shape:**
- For 2 hops: the `Calls` table is referenced twice with 1 self-join. `Calls c1 JOIN Calls c2 ON c1.callee = c2.caller` (with timestamp filters on both).
- For 5 hops: 5 table references and 4 self-joins. For N hops: N table references and N−1 self-joins — and the query must be **rewritten** each time because SQL has no native "traverse to variable depth" operator. (Recursive CTEs can help but are syntactically complex and harder to optimise.)
- The result set can grow **exponentially**: each hop multiplies the number of candidate paths.

The **structural difference**: in the property graph, edges are first-class objects — traversal follows edges natively. In the relational model, relationships are implicit (matching values across rows via JOINs) — variable-depth traversal requires constructing a chain of joins, one per hop, at query-writing time.

</details>

---

**Hint:** Check Table 8 — which model's "costs" column mentions global aggregation? Now check which model's "optimises for" column includes cross-entity queries with ACID.

<details>
<summary><strong>Q10 Solution — Click to reveal</strong></summary>

"Total call duration across all subscribers this month" is a **global aggregation** — a scan-and-sum across the entire dataset. The **relational model** handles this efficiently with `SUM(duration) ... GROUP BY ... WHERE timestamp BETWEEN ...` on indexed columns. The property graph model *can* aggregate (Neo4j supports it), but scanning all nodes is slower than relational `GROUP BY` on indexed columns — this is precisely the cost listed in Table 8 for the property graph model.

A single model is **not sufficient** for both workloads:
- The fraud team needs **bounded traversal** → property graph (Table 8: optimises for relationship traversal with edge filtering).
- The billing team needs **cross-entity aggregation with ACID guarantees** → relational (Table 8: optimises for ACID consistency + complex cross-entity queries).

Forcing the property graph to handle billing means building transactional consistency in application code — exactly the guarantee mismatch pattern from the chapter opening. Forcing the relational model to handle variable-depth fraud traversal means recursive self-joins that must be rewritten for each depth — the structural awkwardness described in Section 4.3. This is a multi-workload system that points toward a multi-model design (Chapter 11). Chapter 10 develops the property graph model and Cypher query language in depth — you will write the traversal query that TelX's fraud team needs.

</details>

---

**Hint:** Walk through the four steps for each workload independently. Pay attention to *who controls the schema* for the customs workload — the logistics company or the destination country? Check where this sits on the enforcement spectrum (Table 7).

<details>
<summary><strong>Q11 Solution — Click to reveal</strong></summary>

**Internal tracking:**

| Step | Assessment | Justification |
|---|---|---|
| Primary query pattern | Cross-entity aggregation (Table 9) | Packages per route, average transit time — aggregate queries across many shipments |
| Consistency requirement | ACID transactions (Table 10) | State transitions must be atomic (a package cannot be simultaneously "in transit" and "delivered"); reporting must reflect consistent state |
| Schema stability | Fixed (Table 11) | Shipment structure (origin, destination, status, timestamps) is stable and well-defined |
| Model selection | **Relational** | All three steps align with the relational model |
| Costs accepted | Schema rigidity if new shipment types emerge; impedance mismatch if downstream APIs expect nested formats |

**Customs declaration:**

| Step | Assessment | Justification |
|---|---|---|
| Primary query pattern | Schema-validated exchange (Table 9) | Produce a structured document conforming to the destination country's published schema; the customs authority validates and rejects non-conforming submissions |
| Consistency requirement | Validator rejects before entry (Table 7) | The customs authority validates the document at the boundary — before it enters any system |
| Schema stability | Fixed, externally controlled (Table 11) | The schema is published by the destination country; the logistics company must conform, not design |
| Model selection | **XML/XSD** | The workload is cross-boundary exchange with schema validation |
| Costs accepted | Verbosity; processing overhead; not designed for querying at scale (the logistics company does not query customs documents — it produces them) |

</details>

---

**Hint:** For each model, state specifically what capability it loses when forced to handle the other workload. Then ask: who publishes the customs schema?

<details>
<summary><strong>Q12 Solution — Click to reveal</strong></summary>

A single model cannot serve both because the workloads occupy fundamentally different positions on the enforcement spectrum and serve different purposes:

- **If the relational model is forced to handle customs declarations:** Relational CHECK constraints operate at *insert time* — they cannot validate a document *before* it enters the system. The customs authority requires boundary validation against an externally published XSD. The relational model has no mechanism for this. Furthermore, the hierarchical structure of a customs declaration (nested elements, attributes) maps awkwardly to flat relational tables.

- **If XML/XSD is forced to handle internal tracking:** XML is an interchange format, not a database. It has no native aggregation (`GROUP BY`, `SUM`), no transaction isolation, and no indexing for efficient queries across millions of shipments. Building reporting and ACID guarantees on top of XML would require re-implementing what the relational model provides natively.

The customs schema is controlled by the **destination country**, not the logistics company. This is the defining characteristic of schema-validated exchange: the receiver defines the contract, and the sender must conform. This external schema control is precisely what XML/XSD is designed for — the schema is a contract between parties.

The **boundary** between the two models is the data flow from internal to external: the relational system stores shipment data; when a border crossing occurs, the application extracts the relevant fields and produces an XML document conforming to the destination country's XSD. Information flows from the relational model (internal storage) to the XML model (external exchange) — one direction, at a well-defined integration point. This two-model pattern — with a clear data flow between them — is an instance of multi-model design; Chapter 11 develops the architecture for managing such boundaries. Chapter 7 develops XSD and JSON Schema validation in full — you will write the XSD contract and validate documents against it.

</details>

---

### Part C — Synthesis Solutions

**Hint:** Use the "Optimises for" and "Costs" columns in Table 8 directly. The "right choice" is when the workload matches the model's strength; the "wrong choice" is when the workload demands what the model lists as a cost.

<details>
<summary><strong>Q13 Solution — Click to reveal</strong></summary>

| Model | Right choice when... | Wrong choice when... |
|---|---|---|
| **Relational** | The workload requires cross-entity aggregation (SUM, GROUP BY) with ACID transactions and a stable, well-defined schema — e.g., banking ledgers, order processing, inventory management. | The primary operation is loading a single self-contained entity with nested structure (shape mismatch) or the schema evolves frequently (rigidity cost). |
| **Document** | The primary operation is an aggregate read — one entity, all related data, delivered as a nested structure — and the schema evolves with business needs — e.g., user profiles, product catalogues. | The workload requires cross-document aggregation with guaranteed consistency, or data integrity depends on relationships across documents (guarantee mismatch). |
| **Property graph** | The primary operation is bounded traversal — following chains of relationships with per-hop filtering, where depth is variable — e.g., fraud detection, social network analysis, recommendation engines. | The workload is dominated by global aggregation (scanning all entities for totals) or requires ACID transactions across entities — the graph model's traversal strength becomes irrelevant. |
| **XML/XSD** | The workload is schema-validated exchange across an organisational boundary, where the receiver defines the schema and rejects non-conforming documents — e.g., regulatory submissions, payment messages, healthcare records. | The workload requires storing and querying data at scale — XML is an interchange format, not a database; it has no native aggregation, indexing, or transaction support. |
| **RDF** | The workload requires integrating data from independent sources with different schemas and different identifiers, using shared URIs — e.g., biomedical knowledge graphs, cross-institutional research data. | The workload involves simple lookups or transactional operations within a single system — RDF's triple verbosity and SPARQL complexity make simple queries unnecessarily costly. |

</details>

---

**Hint:** Name the mismatch type first, then reference your Q6 tables — the framework work is already done. For part (c), look for the pattern that recurred in every scenario.

<details>
<summary><strong>Q14 Solution — Click to reveal</strong></summary>

**(a) Identifying the mismatches:**

- **RideLink (Failure 1):** **Shape mismatch.** The workload is *personalisation* — an aggregate read delivering a nested profile. The relational model stores data as flat, normalised rows across multiple tables. The delivery shape (nested JSON) does not match the storage shape (flat rows), so every read pays the cost of multi-table JOINs and application-layer re-nesting.

- **NeoBank (Failure 2):** **Guarantee mismatch.** The workload is *transactional* — cross-entity aggregation (running balances) with ACID requirements (atomic debit/credit pairs). The document model optimises for self-contained reads; cross-document aggregation is possible (e.g., MongoDB's aggregation pipeline) but is not the model's architectural strength, and multi-document ACID transactions are available (MongoDB 4.0+) but not the default behaviour. The model lacks the consistency mechanism the workload demands.

**(b) How the framework would have prevented each failure (referencing Q6 tables):**

- **RideLink:** The Q6 framework identified aggregate read (Table 9), eventual consistency (Table 10), and evolving schema (Table 11) — all three pointing to the document model. Applying the framework before building would have avoided the 5-table JOIN reconstruction cost and the quarterly schema migration burden.

- **NeoBank:** The Q6 framework identified cross-entity aggregation (Table 9), ACID transactions (Table 10), and fixed schema (Table 11) — all three pointing to the relational model. The framework would have prevented the guarantee mismatch that left concurrent transfers unprotected.

**(c) The recurring principle:**

Model selection must follow workload, not domain: when a system's workloads require structurally incompatible access patterns or occupy different positions on the enforcement spectrum, no single model can serve all workloads without paying the cost of mismatch. This principle appeared in every scenario — RideLink vs NeoBank (aggregate read vs cross-entity aggregation), TelX (bounded traversal vs global aggregation), and International Shipping (internal tracking vs schema-validated exchange). Chapter 6 revisits RideLink's profile workload using MongoDB, and Chapters 2–5 develop the relational model that NeoBank's ledger demands.

</details>
