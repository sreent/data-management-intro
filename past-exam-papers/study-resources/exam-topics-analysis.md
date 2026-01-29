# Exam Topics & Concepts Analysis

## Overview

This document provides a comprehensive analysis of exam questions and solution sheets from **Mock March 2021 through Mock October 2025**, identifying topics, key concepts, and trends to help students prepare for future exams.

---

## Summary Table: Topics by Exam Period

| Topic | Key Concepts | Mar 2021 | Sep 2021 | Mar 2022 | Sep 2022 | Mar 2023 | Sep 2023 | Mar 2024 | Sep 2024 | Mar 2025 | Oct 2025 |
|-------|--------------|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| **SQL/Relational** | Normal forms, E/R, CREATE TABLE, JOINs, GROUP BY | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **SQL Transactions** | COMMIT, ROLLBACK, ACID | ✓ | ✓ | | ✓ | | | | | | |
| **SQL Permissions** | GRANT, least privilege | | ✓ | | ✓ | | | | ✓ | | ✓ |
| **XML/XPath** | Navigation, predicates, attributes | ✓ | ✓ | ✓ | ✓ | ✓ | | | ✓ | ✓ | ✓ |
| **XML Validation** | Well-formed vs valid, DTD, XSD, RelaxNG | | ✓ | | ✓ | ✓ | | | | ✓ | |
| **TEI** | Text encoding, lg/l elements | | | | ✓ | | ✓ | | ✓ | | |
| **XSLT** | Transformations, namespaces | | | | ✓ | | | | | | |
| **RDF/Turtle** | Triple counting, serialization | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | |
| **SPARQL** | Basic queries, property paths, SERVICE | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| **Linked Data Principles** | URIs, dereferencing, 4 principles, BIBFRAME | ✓ | | | | | ✓ | ✓ | ✓ | | ✓ |
| **Ontologies** | schema.org, FOAF, Dublin Core, OWL | ✓ | | | ✓ | ✓ | ✓ | ✓ | | ✓ | |
| **Wikidata** | Property paths, P-codes, federated queries | | | ✓ | | | | ✓ | ✓ | | |
| **MongoDB** | find(), regex, $elemMatch, operators | ✓ | ✓ | | ✓ | | ✓ | ✓ | ✓ | | |
| **JSON/JSON-LD** | Structure, conversion from XML | | ✓ | | | | | | | ✓ | |
| **Precision/Recall** | IR metrics, F1-measure | ✓ | ✓ | | ✓ | | ✓ | | | ✓ | |
| **Data Model Comparison** | Tree vs graph vs relational | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **MapReduce** | Distributed processing | ✓ | | | | | | | | | |
| **Licensing** | Copyleft, GPL, MIT | ✓ | | | | | | | | | |
| **Star Schema** | Dimensional modeling, fact/dimension tables | | | | | | | | | ✓ | |
| **Open/Closed World** | Assumption differences | | | | | | | | | ✓ | |
| **Cross-validation** | k-fold, model evaluation | | | | | | | | | ✓ | |
| **Denormalization** | Performance vs integrity trade-offs | | | | | | | | | | ✓ |

---

## Topic Frequency Analysis

| Topic | Exam Appearances | Frequency |
|-------|------------------|-----------|
| SQL/Relational (E/R, Normal forms, JOINs) | 10/10 | **100%** |
| Data Model Comparison | 9/10 | **90%** |
| XML/XPath | 8/10 | **80%** |
| RDF/Turtle | 8/10 | **80%** |
| SPARQL | 7/10 | **70%** |
| MongoDB | 7/10 | **70%** |
| Ontologies | 6/10 | **60%** |
| Precision/Recall | 5/10 | **50%** |
| Linked Data Principles | 5/10 | **50%** |
| XML Validation (DTD, XSD, RelaxNG) | 4/10 | **40%** |
| SQL Permissions (GRANT) | 4/10 | **40%** |
| TEI | 3/10 | **30%** |
| Wikidata SPARQL | 3/10 | **30%** |
| SQL Transactions | 3/10 | **30%** |

---

## General Testing Patterns and Trends

### Core Topics (Tested Every Exam)

#### 1. SQL/Relational Databases

This is the foundation of every exam. Students are consistently expected to:

- Design E/R diagrams from text descriptions
- Normalize data to at least 3NF and justify the normal form
- Write CREATE TABLE statements with proper keys and constraints
- Compose queries using JOINs, GROUP BY, and aggregation functions

The complexity has increased over time - earlier exams asked for simpler queries, while recent exams (2024-2025) include CTEs (Common Table Expressions) and more complex multi-table joins.

#### 2. Data Model Comparison

Almost every exam includes a question asking students to evaluate when to use relational vs document vs graph/RDF models. The expected answer always includes trade-offs around:

- Query patterns (analytical vs document retrieval vs relationship traversal)
- Schema flexibility
- Data integrity requirements
- Scalability needs

---

### Secondary Core Topics (Tested in 70-90% of Exams)

#### 3. RDF/Turtle and SPARQL

Linked Data has become increasingly important:

- Triple counting in Turtle (understanding `;` and `,` syntax)
- Writing SPARQL queries (especially property paths since 2022)
- Understanding ontologies and vocabulary reuse
- Wikidata queries appear regularly from March 2022 onwards

#### 4. XML/XPath

Remains consistent throughout:

- XPath navigation with `//`, `/`, `@`, and predicates
- Understanding namespace handling
- Distinguishing well-formed from valid XML
- TEI appears periodically when questions involve humanities/text data

#### 5. MongoDB/Document Databases

Tested as a practical alternative to relational:

- Basic find() queries with operators ($gte, $lt, $regex)
- Array queries with $elemMatch
- Converting between document and relational models
- Evaluating when document DBs are appropriate

---

### Periodic Topics

#### Information Retrieval Metrics

Precision, recall, and F1-measure appear in about half the exams. Questions typically ask students to:

- Calculate metrics from given numbers
- Explain precision vs recall trade-offs
- Evaluate classifier performance against baselines

#### SQL Transactions and Permissions

These appear sporadically (about 1/3 of exams):

- COMMIT/ROLLBACK and ACID properties
- GRANT statements and principle of least privilege
- Practical security scenarios (e.g., double-blind peer review systems in Oct 2025)

---

### Observable Trends Over Time

#### 1. Increasing SPARQL Complexity (2021→2025)

| Year | SPARQL Complexity |
|------|-------------------|
| 2021 | Basic triple patterns |
| 2022 | Property paths introduced (`wdt:P131*`) |
| 2024-2025 | Federated queries with SERVICE, complex FILTER patterns |

#### 2. Real-World Data Sources

- **Earlier exams**: Hypothetical scenarios (Doctor Who, Zoos, Recipe databases)
- **Later exams**: Real datasets (Wikidata, Carnegie Hall, MusicBrainz, UK Government data)
- **Oct 2025**: Domain-specific standards (MARC library cataloguing from Bodleian Library)

#### 3. Growing Emphasis on Data Quality

Recent exams (2024-2025) include questions about:

- Historical data anomalies (1752 calendar skip)
- Data validation and parity checks
- Handling missing/null values
- Data cleaning and normalization challenges

#### 4. Star Schema/Dimensional Modeling

Introduced in March 2025, suggesting potential future emphasis on data warehousing concepts.

#### 5. JSON-LD and RDF Interoperability

Increasing focus on understanding different serialization formats as equivalent representations of the same underlying RDF graph.

#### 6. Domain-Specific Linked Data Standards

October 2025 introduced BIBFRAME (Bibliographic Framework), the Library of Congress's Linked Data standard designed to replace MARC:

- Benefits: Web integration, deduplication via shared URIs, richer relationships
- Risks: Migration costs, training requirements, ecosystem changes
- This signals growing interest in how Linked Data principles apply to real-world domain migrations

#### 7. Database Performance vs Integrity Trade-offs

October 2025 explicitly tested denormalization concepts:

- When denormalization is appropriate (read-heavy workloads, proven bottlenecks)
- Why premature optimization is problematic (update anomalies, complexity)
- Alternative solutions (indexing, caching, read replicas)
- Understanding that 1,000 records is trivial for modern databases

---

### Question Structure Patterns

#### Section B Structure

Section B typically follows this pattern:

- **Question 2**: Usually focuses on relational design with some alternative (XML, RDF, or document)
- **Question 3**: Often XML-based or involves text encoding, with comparisons to other models
- **Question 4**: Frequently involves RDF/SPARQL/Linked Data, or MongoDB

#### MCQs (Section A)

MCQs consistently test:

- Normal forms and normalization
- JOIN types and behavior
- Triple counting in Turtle
- XPath expression results
- Precision/Recall calculations
- Data model characteristics

---

## Key Exam Preparation Recommendations

Based on this analysis, students should prioritize:

### Must Know (Tested Every Exam)

1. **SQL fundamentals** - JOINs (LEFT, INNER, CROSS), GROUP BY, aggregation functions
2. **Normal forms** - Be able to identify and justify 1NF, 2NF, 3NF, BCNF
3. **E/R diagrams** - Design from text, identify cardinality, map to relational schema
4. **CREATE TABLE** - Proper syntax with PRIMARY KEY, FOREIGN KEY, constraints

### High Priority (70%+ of Exams)

5. **SPARQL property paths** - `*`, `+`, `/` combinations, FILTER, OPTIONAL
6. **XML/XPath** - Navigation with `//`, `/`, `@`, predicates, namespace handling
7. **MongoDB** - find() queries with operators, when to use document DBs
8. **Triple counting** - Turtle syntax with `;` and `,` (nearly always in MCQs)
9. **Data model comparison** - Pros/cons of relational vs document vs graph

### Medium Priority (40-60% of Exams)

10. **Precision/Recall** - Know formulas, interpretation, and trade-offs
11. **Well-formed vs valid XML** - Understand the distinction
12. **Ontologies** - Know schema.org, FOAF, Dublin Core basics
13. **Linked Data principles** - Tim Berners-Lee's 4 principles

### Be Familiar With (Periodic)

14. **SQL Transactions** - START TRANSACTION, COMMIT, ROLLBACK, ACID
15. **SQL GRANT** - Principle of least privilege
16. **TEI** - Basic structure for text encoding
17. **JSON-LD** - As RDF serialization format

---

## Quick Reference: Common Exam Patterns

### Triple Counting in Turtle

```turtle
:Bob a :Person ;       # Triple 1
     :name "Bob" ;     # Triple 2
     :knows :A, :B .   # Triples 3 and 4
# Total: 4 triples
```

| Syntax | Meaning |
|--------|---------|
| `.` | End statement |
| `;` | Same subject, new predicate |
| `,` | Same subject+predicate, new object |

### JOIN Behavior

| JOIN Type | Rows Returned |
|-----------|---------------|
| INNER JOIN | Only matching rows |
| LEFT JOIN | All left + matching right (NULL for no match) |
| CROSS JOIN | Cartesian product (all combinations) |

### XPath Quick Reference

| Expression | Meaning |
|------------|---------|
| `//element` | Find anywhere |
| `/element` | Direct child |
| `[@attr='value']` | Attribute filter |
| `[1]` | First occurrence |
| `/..` | Parent |

### MongoDB Operators

| Operator | Meaning |
|----------|---------|
| `$gt`, `$gte` | Greater than (or equal) |
| `$lt`, `$lte` | Less than (or equal) |
| `$regex` | Pattern matching |
| `$elemMatch` | Match array element with multiple conditions |

### Precision/Recall Formulas

| Metric | Formula |
|--------|---------|
| Precision | TP / (TP + FP) |
| Recall | TP / (TP + FN) |
| F1 | 2 × (P × R) / (P + R) |

---

## Exam Coverage by Real-World Datasets

| Exam | Dataset/Context |
|------|-----------------|
| Mar 2021 | Doctor Who (fictional), Recipe Database |
| Sep 2021 | Zoo Database, MEI Music Encoding |
| Mar 2022 | English Monarchy Family Tree, Wikidata, Hospital Database |
| Sep 2022 | Film Database, Shakespeare Cast Lists, TEI |
| Mar 2023 | ODF/XML, MusicBrainz, 16th-Century Music Database |
| Sep 2023 | BabelNet, Estate Agency, Document Database |
| Mar 2024 | Carnegie Hall RDF, UK Government Education Data, MongoDB People |
| Sep 2024 | Lute Music Database, Poetry Contest, Wikidata Belgian Artists |
| Mar 2025 | London Mortality Bills, BeerXML, MusicBrainz JSON-LD |
| Oct 2025 | MARC Library Catalogue (Bodleian), Conference Management System |

---

*Analysis generated from solution sheets: Mock March 2021 through Mock October 2025*
