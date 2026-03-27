# Resources — Data Files by Domain

Seed data, schemas, and generators organised by canonical domain. Each domain maps to specific chapters as defined in the syllabus.

## Directory Structure

```
resources/
├── orders-payments/     Chapters 2–5 (Relational)
│   ├── ddl.sql                  Schema definition (12 tables + triggers)
│   ├── seed-data.sql            Slide-ready data (5 customers, 7 orders, 13 lines)
│   ├── seed-data.md             Documentation with teaching scenarios
│   ├── schema.md                ERD, DBML, constraint annotations, BCNF analysis
│   ├── large-data.sql           Performance dataset (100K+ order lines)
│   └── generate-large.py        Generator for large dataset
│
├── ridelink/            Chapters 1, 6, 11 (Super-app)
│   ├── seed-data.js             Slide-ready MongoDB inserts (7 users, 4 plans)
│   ├── seed-data.md             Documentation with teaching scenarios + walkthroughs
│   ├── generate-lab-data.py     Generator for lab dataset (200 users, both designs)
│   └── lab-data.js              Generated lab data (auto-generated, do not edit)
│
├── e-invoicing/         Chapter 7 (XML / XSD / XPath)
│   ├── invoice_schema.xsd       XSD contract (named types, root element)
│   ├── invoice_valid.xml        Valid invoice (Kopi Tech → Marina Bay Trading, SGD)
│   ├── invoice_invalid.xml      Invalid invoice (4 planted errors for predict-then-verify)
│   ├── invoice.dtd              DTD equivalent (for DTD vs XSD comparison)
│   ├── invoice_namespaced.xml   Namespaced invoice (inv: prefix, namespace trap demo)
│   └── seed-data.md             Documentation with teaching scenarios + error matrix
│
├── movie-kg/            Chapters 8–9 (RDF / SPARQL)
│   ├── movie_ontology.ttl       Ontology contract (6 classes, 9 properties)
│   ├── source_a.ttl             Filmography source (3 directors, 9 films, 3 actors)
│   ├── source_b.ttl             Genres and awards source (6 genres, 3 awards)
│   └── seed-data.md             Documentation with teaching scenarios + integration points
│
├── financial-transfers/ Chapter 10 (Property Graph / Cypher)
│   ├── seed-data.cypher         Cypher CREATE statements (60 accounts, 150 transfers)
│   └── seed-data.md             Documentation with teaching scenarios + ground truth
│
└── README.md            This file
```

## Domain Register

| Domain | Directory | Chapters | Data Size (slide-ready) |
|--------|-----------|----------|------------------------|
| **Orders & Payments** | `orders-payments/` | 2, 3, 4, 5 | 5 customers, 6 products, 7 orders, 13 order lines |
| **RideLink Super-App** | `ridelink/` | 1, 6, 11 | 3 passengers, 2 drivers, 2 merchants, 4 plans |
| **E-invoicing (Peppol)** | `e-invoicing/` | 7 | 1 XSD, 1 valid invoice, 1 invalid invoice (4 errors), 1 DTD, 1 namespaced invoice |
| **Movie Knowledge Graph** | `movie-kg/` | 8, 9 | 1 ontology, 2 sources, 3 directors, 9 films, 3 actors, 6 genres, 3 awards (103 triples) |
| **Financial Transfers** | `financial-transfers/` | 10 | 60 accounts, 150 transfers, 1 supernode (42 edges), 2 fraud rings |

## Naming Convention

Files within each domain folder drop the domain prefix:

| Old name | New name |
|----------|----------|
| `orders-payments-ddl.sql` | `orders-payments/ddl.sql` |
| `orders-payments-seed-data.sql` | `orders-payments/seed-data.sql` |
| `ridelink-seed-data.js` | `ridelink/seed-data.js` |

## Usage

- **Slide-ready data** (`seed-data.*`): Small enough to trace by hand. Use in lecture slides and worked examples.
- **Large data** (`large-data.*`): For performance demos (indexes, explain, selectivity). Generated deterministically with seed 42.
- **Schema docs** (`schema.md`): ERDs, constraint annotations, BCNF analysis for reference.
