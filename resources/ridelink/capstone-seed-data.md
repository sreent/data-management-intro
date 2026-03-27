# RideLink Super-App — Capstone Seed Data (Chapter 11)

One entity, five representations. This file shows how the same real-world entities — a driver, a passenger, a ride — appear across all five data models used in the super-app's multi-model architecture.

**Use case:** Chapter 11's worked example traces a single ride-completion event through four data-flow boundaries. This seed data provides the concrete values for that trace.

**Source data:** All values are consistent with the existing seed data files:
- `resources/ridelink/seed-data.js` (Chapter 6 — Document)
- `resources/orders-payments/seed-data.sql` (Chapters 2–5 — Relational patterns)
- `resources/financial-transfers/seed-data.cypher` (Chapter 10 — Property graph)
- `resources/e-invoicing/invoice_valid.xml` (Chapter 7 — XML/XSD)
- `resources/movie-kg/source_a.ttl` (Chapters 8–9 — RDF patterns)

---

## Identifier Mapping

The same entities appear with different identifiers in each model. This table is the integration contract — every data-flow boundary must resolve between these identifiers.

| Entity | Relational | Document (MongoDB) | Property Graph (Neo4j) | RDF (Triple Store) | XML/XSD (Peppol) |
|--------|-----------|-------------------|----------------------|-------------------|-----------------|
| Ahmad Ibrahim (driver) | `driver_id = 5582` | `userId: "driver-5582"` | `{id: 'DRV-5582'}` | `ex:driver_drv5582` | `<CompanyID>SG-S1234567A</CompanyID>` |
| Sarah Tan (passenger) | `passenger_id = 1001` | `userId: "passenger-1001"` | `{id: 'PAX-1001'}` | N/A | N/A |
| Ride R-2001 | `ride_id = 2001` | `recentRides[].rideId: "R-2001"` | edge `:TRANSFERRED_TO` | N/A | `<InvoiceLine>` |
| Payment P-3001 | `payment_id = 3001` | N/A | edge property `amount: 68.50` | N/A | `<LineAmount>68.50</LineAmount>` |

---

## 1. Relational — Transactional Core

The ride-booking and payment-processing workload. ACID transactions, FK constraints, normalised storage (Chapters 2–5).

### Schema (DDL)

```sql
CREATE TABLE Drivers (
    driver_id    INT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    licence_no   VARCHAR(20)  NOT NULL UNIQUE,
    commission   DECIMAL(3,2) NOT NULL DEFAULT 0.20,
    CHECK (commission BETWEEN 0.00 AND 1.00)
);

CREATE TABLE Passengers (
    passenger_id INT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    phone        VARCHAR(20)  NOT NULL UNIQUE
);

CREATE TABLE Rides (
    ride_id      INT PRIMARY KEY,
    passenger_id INT NOT NULL REFERENCES Passengers(passenger_id),
    driver_id    INT NOT NULL REFERENCES Drivers(driver_id),
    fare         DECIMAL(10,2) NOT NULL,
    ride_date    DATE NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'completed',
    CHECK (fare > 0)
);

CREATE TABLE Payments (
    payment_id   INT PRIMARY KEY,
    ride_id      INT NOT NULL REFERENCES Rides(ride_id),
    amount       DECIMAL(10,2) NOT NULL,
    method       VARCHAR(30) NOT NULL,
    payment_date DATE NOT NULL,
    CHECK (amount > 0)
);

CREATE TABLE DriverSettlements (
    driver_id    INT PRIMARY KEY REFERENCES Drivers(driver_id),
    balance      DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    last_settled DATE
);

CREATE TABLE PromoUsage (
    promo_id     INT PRIMARY KEY,
    code         VARCHAR(20) NOT NULL UNIQUE,
    times_used   INT NOT NULL DEFAULT 0,
    max_uses     INT NOT NULL,
    CHECK (times_used >= 0),
    CHECK (max_uses > 0)
);
```

### Seed Data

```sql
INSERT INTO Drivers (driver_id, name, licence_no, commission) VALUES
  (5582, 'Ahmad Ibrahim',  'S1234567A', 0.20),
  (5583, 'Priya Nair',     'S7654321B', 0.30);

INSERT INTO Passengers (passenger_id, name, phone) VALUES
  (1001, 'Sarah Tan',     '+6591234567'),
  (1002, 'Wei Ming Lim',  '+6598761234'),
  (1003, 'Rani Devi',     '+6587001234');

INSERT INTO Rides (ride_id, passenger_id, driver_id, fare, ride_date, status) VALUES
  (2001, 1001, 5582, 68.50, '2024-03-15', 'completed'),
  (2002, 1002, 5583,   18.50, '2024-03-14', 'completed');

INSERT INTO Payments (payment_id, ride_id, amount, method, payment_date) VALUES
  (3001, 2001, 68.50, 'card',    '2024-03-15'),
  (3002, 2002,   18.50, 'grabpay', '2024-03-14');

INSERT INTO DriverSettlements (driver_id, balance, last_settled) VALUES
  (5582, 54.80, '2024-03-15'),
  (5583,  544.00, '2024-03-14');

INSERT INTO PromoUsage (promo_id, code, times_used, max_uses) VALUES
  (1, 'RIDE50', 4, 5);  -- 4 after ride R-2001 (was 3 before the transaction)
```

### ACID Transaction — Ride Completion

```sql
BEGIN;
INSERT INTO Rides (ride_id, passenger_id, driver_id, fare, ride_date, status)
  VALUES (2001, 1001, 5582, 68.50, '2024-03-15', 'completed');
INSERT INTO Payments (payment_id, ride_id, amount, method, payment_date)
  VALUES (3001, 2001, 68.50, 'card', '2024-03-15');
UPDATE PromoUsage SET times_used = times_used + 1
  WHERE promo_id = 1 AND times_used < max_uses;
UPDATE DriverSettlements SET balance = balance + (68.50 * 0.80)
  WHERE driver_id = 5582;
COMMIT;
```

---

## 2. Document — Personalisation Layer

Ahmad's profile and Sarah's profile in MongoDB (Chapter 6). Values match `resources/ridelink/seed-data.js`.

### Sarah's Profile (before ride R-2001)

```javascript
db.users.findOne({ "userId": "passenger-1001" })
// Returns:
{
  "userId": "passenger-1001",
  "displayName": "Sarah Tan",
  "phone": "+6591234567",
  "role": "passenger",
  "tier": "standard",
  "savedPlaces": [
    {"label": "Home",   "address": "123 Clementi Ave 3"},
    {"label": "Office", "address": "1 Raffles Place"}
  ],
  "rewardPoints": 2840,
  "recentRides": []
}
```

### Profile Update (after ride R-2001 completes)

```javascript
db.users.updateOne(
  { userId: "passenger-1001" },
  { $push: { recentRides: {
      rideId: "R-2001", fare: 68.50, date: "2024-03-15",
      driver: "Ahmad Ibrahim"   // snapshot — Chapter 6 discipline
    }},
    $inc: { rewardPoints: 125 }
  }
)
```

After the update, Sarah's `rewardPoints` = 2846 and `recentRides` has one entry with a **snapshot** of Ahmad's display name.

---

## 3. Property Graph — Fraud Monitoring

The transfer edge created when payment exceeds the $1,000 threshold (Chapter 10).

```cypher
MERGE (from:Account {id: 'PAX-1001'})
  ON CREATE SET from.name = 'Sarah Tan', from.type = 'Personal', from.flagged = false
MERGE (to:Account {id: 'DRV-5582'})
  ON CREATE SET to.name = 'Ahmad Ibrahim', to.type = 'Personal', to.flagged = false
CREATE (from)-[:TRANSFERRED_TO {
  amount: 68.50, date: date('2024-03-15'), transfer_type: 'ride_payment'
}]->(to)
```

The edge carries the transfer data (amount, date, type) — Chapter 10's edge-centric modelling. The compliance team can now include this transfer in bounded traversals:

```cypher
MATCH p = (start:Account {id: 'DRV-5582'})-[:TRANSFERRED_TO*1..3]->(end)
WHERE ALL(r IN relationships(p) WHERE r.amount > 500 AND r.date > date('2024-01-01'))
RETURN [n IN nodes(p) | n.id] AS path, [r IN relationships(p) | r.amount] AS amounts
```

---

## 4. RDF — Partner Integration

Ahmad's identity in the partner integration triple store, linked to external data from the transit authority (Chapter 8's URI-based identity).

```turtle
@prefix ex:   <http://example.org/ridelink#> .
@prefix ta:   <http://transitauthority.gov.sg/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

ex:driver_drv5582
    rdf:type           ex:Driver ;
    rdfs:label         "Ahmad Ibrahim" ;
    ex:internalId      "DRV-5582" ;
    ex:relationalId    5582 ;
    ex:transitLicence  "SG-S1234567A" ;
    ex:operatesIn      ex:zone_central , ex:zone_east .

ta:licence_SG_S1234567A
    rdf:type           ta:DrivingLicence ;
    ta:holderName      "Ahmad Ibrahim" ;
    ta:expiryDate      "2026-08-15"^^xsd:date ;
    ta:vehicleClass    "Standard" ;
    ta:accidentHistory 0 .

ex:zone_east
    rdf:type           ex:ServiceZone ;
    rdfs:label         "East Zone" ;
    ta:accidentRate    "high" .
```

SPARQL query: "Which drivers operate in high-accident zones?"

```sparql
PREFIX ex: <http://example.org/ridelink#>
PREFIX ta: <http://transitauthority.gov.sg/>

SELECT ?driverName ?zoneName ?accidentRate
WHERE {
  ?driver rdf:type ex:Driver ;
          rdfs:label ?driverName ;
          ex:operatesIn ?zone .
  ?zone   rdfs:label ?zoneName ;
          ta:accidentRate ?accidentRate .
  FILTER (?accidentRate = "high")
}
```

Result: Ahmad Ibrahim operates in East Zone (high accident rate). The query spans data from two sources (internal driver zones + transit authority accident data) — merged via URI alignment.

---

## 5. XML/XSD — Regulatory Reporting

At month-end, Ahmad's accumulated ride settlements generate a UBL-compliant e-invoice for Peppol submission (Chapter 7). The XML uses the national registry ID, not the internal driver ID.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Invoice>
  <InvoiceNumber>INV-2024-03-DRV5582</InvoiceNumber>
  <IssueDate>2024-04-01</IssueDate>
  <Supplier>
    <Name>RideLink Pte Ltd</Name>
    <Address>1 Raffles Place, Singapore 048616</Address>
  </Supplier>
  <Customer>
    <Name>Ahmad Ibrahim</Name>
    <CompanyID>SG-S1234567A</CompanyID>
  </Customer>
  <InvoiceLines>
    <InvoiceLine>
      <ItemName>Driver Settlement — March 2024</ItemName>
      <Quantity>1</Quantity>
      <LineAmount currencyID="SGD">4960.00</LineAmount>
    </InvoiceLine>
  </InvoiceLines>
  <MonetaryTotal>
    <LineExtensionAmount currencyID="SGD">4960.00</LineExtensionAmount>
    <TaxAmount currencyID="SGD">0.00</TaxAmount>
    <PayableAmount currencyID="SGD">4960.00</PayableAmount>
  </MonetaryTotal>
  <PaymentMeans>
    <PaymentMethodCode>30</PaymentMethodCode>
    <PaymentDueDate>2024-04-15</PaymentDueDate>
  </PaymentMeans>
</Invoice>
```

This XML is validated against the UBL XSD before submission. Element ordering (`InvoiceLines` before `MonetaryTotal`) satisfies `xs:sequence`; `PaymentMethodCode` value `30` satisfies the enumeration constraint. Chapter 7's four-check model applies at this boundary.

---

## Teaching Scenarios

| Scenario | Section | What this data demonstrates |
|----------|---------|----------------------------|
| One entity, five IDs | Dataset Reference, §4.4 | Ahmad's identifier differs across every model — the integration tax |
| Ride-completion trace | §4.5 worked example | One business event crosses 4 boundaries, producing data in 4 stores |
| Snapshot discipline | Document update | `driver: "Ahmad Ibrahim"` is a snapshot, not a live reference |
| Boundary consistency | §4.2, Lab Q10–Q11 | ACID for relational; eventual for document/graph; batch for XML |
| Enforcement spectrum | §3.4, §4.6 | Each model enforces Ahmad's data differently (or not at all) |
| Cross-model query | §4.7 | "Find Ahmad's rides over $500" answered in 5 languages |
| Identifier alignment | §4.4, Lab Q12 | Transit authority changes licence number — which stores break? |
