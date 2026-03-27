# Financial Transfers — Fraud Detection Network Seed Data

A fraud-detection graph for Chapter 10 (Property Graphs / Cypher). Two data scales in one file: a small hand-traceable core subgraph (8 accounts, 9 edges) for the narrative worked example, and a surrounding network (60 accounts, 150 edges total) for the lab. Designed to demonstrate: edge-centric modelling, bounded traversal with per-hop filtering, cycle detection, supernode handling, and cross-model comparison.

**60 accounts | 150 transfers | 1 supernode | 2 fraud rings | 1 flagged account**

---

## File Inventory

| File | Purpose | Used in |
|------|---------|---------|
| `seed-data.cypher` | Cypher CREATE statements — accounts and transfers | Lab setup Cell 5 (full dataset) |

The narrative chapter (§4.4) hand-traces the 8-account, 9-edge core subgraph extracted from Section 3 of the seed data. The lab loads the entire 60-account, 150-edge dataset.

---

## Domain Context

A simplified financial transfer network inspired by anti-money-laundering (AML) monitoring systems. Accounts send transfers to other accounts; each transfer carries an amount, date, and type. The domain demonstrates:

- **Edge-centric modelling:** Transfer data (amount, date, type) lives on the `:TRANSFERRED_TO` relationship, not on either account node — same semantics as Chapter 2's associative entity (OrderLine), but structural rather than tabular.
- **Bounded traversal:** "Follow the money from flagged account acct_2049, up to 3 hops, where each transfer exceeds $5,000 in the last 90 days."
- **Cycle detection:** Money-flow rings where funds leave an account and return through intermediaries — the query objective, not a design error.
- **Supernode handling:** processor_001 (a payment processor) has 42 edges; unbounded traversal through it produces path explosion.

---

## Graph Schema

```
(:Account {id, name, type, flagged})
    -[:TRANSFERRED_TO {amount, date, transfer_type}]->
(:Account)
```

### Node Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique account identifier (e.g., `acct_2049`) |
| `name` | string | Account holder name (e.g., `Alice Chen`) |
| `type` | string | Account type: Personal, Business, Merchant, or Processor |
| `flagged` | boolean | Whether the account is flagged for investigation |

### Relationship Properties

| Property | Type | Description |
|----------|------|-------------|
| `amount` | integer | Transfer amount in dollars |
| `date` | Neo4j date | Transfer date (range: 2024-01-05 through 2024-03-18) |
| `transfer_type` | string | Transfer method: wire, ACH, card, or crypto |

---

## Account Summary

| Type | Count | Examples |
|------|-------|---------|
| Personal | 31 | acct_2049 (Alice Chen, flagged), acct_4522 (Carla Diaz), acct_7801 (David Okonkwo) |
| Business | 19 | acct_3017 (Bob Rivera), acct_9900 (Elena Rossi), acct_5678 (Isabella Moreno) |
| Merchant | 9 | acct_8800 (Grace Lin), acct_1009 (Chen Wei), acct_1013 (Lucas Bergman) |
| Processor | 1 | processor_001 (QuickPay Hub) — supernode, 42 total edges |
| **Total** | **60** | |

---

## Data Sections (in seed-data.cypher)

### Section 1 — Core accounts (11 nodes)

The 8 accounts in the narrative's worked example subgraph, plus 3 additional accounts used in the fraud rings.

### Section 2 — Background accounts (49 nodes)

Additional accounts to bring the total to 60. Mix of Personal, Business, and Merchant types.

### Section 3 — Core transfers: worked example subgraph (9 edges)

The 8-account, 9-edge subgraph hand-traced in the chapter narrative (§4.4). These are the ground truth for the worked query trace:

| From | To | Amount | Date | Type |
|------|----|--------|------|------|
| acct_2049 | acct_3017 | $8,000 | 2024-03-01 | wire |
| acct_2049 | acct_4522 | $3,000 | 2024-02-15 | ACH |
| acct_3017 | acct_7801 | $12,000 | 2024-03-05 | wire |
| acct_3017 | acct_9900 | $2,000 | 2024-01-10 | ACH |
| acct_4522 | processor_001 | $6,000 | 2024-03-10 | card |
| processor_001 | acct_7801 | $15,000 | 2024-03-12 | wire |
| processor_001 | acct_5566 | $9,000 | 2024-03-14 | wire |
| processor_001 | acct_8800 | $1,000 | 2024-02-01 | ACH |
| acct_7801 | acct_2049 | $7,000 | 2024-03-08 | wire |

### Section 4 — Fraud ring 2 (4 edges)

A 4-node cycle: acct_5566 → acct_1234 → acct_5678 → acct_9012 → acct_5566.

| From | To | Amount | Date | Type |
|------|----|--------|------|------|
| acct_5566 | acct_1234 | $6,000 | 2024-02-20 | wire |
| acct_1234 | acct_5678 | $5,500 | 2024-02-25 | wire |
| acct_5678 | acct_9012 | $4,500 | 2024-03-01 | ACH |
| acct_9012 | acct_5566 | $4,000 | 2024-03-05 | wire |

### Section 5 — Supernode edges (38 edges)

processor_001's incoming and outgoing transfers: 18 incoming + 20 outgoing = 38 edges. Combined with Section 3's 1 incoming and 3 outgoing edges, processor_001 has **19 incoming + 23 outgoing = 42 total edges**.

### Section 6 — Background transfers (99 edges)

Random transfers between background accounts. Covers all four transfer types, date range, and amount distribution to make the graph realistic.

---

## Planted Features (Ground Truth)

### Flagged account

- **acct_2049 (Alice Chen)** — `flagged: true`. Starting point for Q3–Q6 traversals.

### Fraud rings

| Ring | Length | Path | Min edge (bottleneck) |
|------|--------|------|-----------------------|
| Ring 1 | 3 | acct_2049 → acct_3017 → acct_7801 → acct_2049 | $7,000 |
| Ring 2 | 4 | acct_5566 → acct_1234 → acct_5678 → acct_9012 → acct_5566 | $4,000 |

### Supernode

- **processor_001 (QuickPay Hub)** — type: Processor. 19 incoming + 23 outgoing = 42 total edges. Used in Q2, Q6(b), Q9, Q10.

### Key query ground truth

| Query | Expected result |
|-------|----------------|
| Q5: "follow the money" from acct_2049, 3 hops, >$5K, after 2024-01-02 | Includes acct_3017 (depth 1), acct_7801 (depth 2), acct_2049 cycle (depth 3), plus additional paths through the wider network |
| Q7: Cycles of length 3–6 with edges >$3K | Ring 1 (3 rows from 3 starting points) + Ring 2 (4 rows from 4 starting points) = 7 raw rows → 2 unique rings after deduplication |

---

## Teaching Scenarios Supported

| Scenario | Concept | Lab question |
|----------|---------|-------------|
| **Edge properties** | Data belongs on the edge, not on endpoints | Q1 (inspect transfer relationship) |
| **Supernode identification** | Degree distribution, supernode as traversal bottleneck | Q2 (find highest in-degree node) |
| **Effective degree** | Edge filtering reduces traversal cost | Q3(b) (filter >$5K, last 90 days) |
| **Bounded traversal** | `*1..k` with `ALL(... WHERE ...)` | Q4–Q5 (predict-first, then execute) |
| **Explosion demonstration** | Unbounded traversal from supernode | Q6(b) (remove all bounds from processor_001) |
| **Cycle detection** | Same-variable pattern `(a)-[*3..6]->(a)` | Q7 (find rings, deduplicate) |
| **Bottleneck estimation** | Minimum edge in cycle limits laundered volume | Q8 (reduce over ring edges) |
| **Supernode handling** | Edge filtering vs node skipping | Q9–Q10 (two strategies compared) |
| **Cross-model comparison** | SQL CTE vs SPARQL reified vs Cypher | Q11–Q13 (read, complete, compare) |
| **Four-model synthesis** | Relational, document, RDF, property graph | Q14 (preparation for Chapter 11) |
