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
