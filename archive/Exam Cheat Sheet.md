
---

# Exam Cheat Sheet

---

| **Topic**                      | **Key Concepts**                                                                                          | **Must-Know Examples/Notes**                                                                                       |
|--------------------------------|------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| **Relational Databases**       | **E/R Diagrams:** Entities, Attributes, Relationships (1:1, 1:M, M:M)                                      | **Schema Conversion:** Map entities to tables; use foreign keys for 1:1, associative tables for M:M relationships.  |
|                                | **Normalization:** 1NF, 2NF, 3NF, BCNF                                                                     | **Essentials:** 1NF removes repeating groups; 2NF removes partial dependencies; 3NF removes transitive dependencies; BCNF ensures determinants are candidate keys. |
|                                | **Strengths/Weaknesses:**                                                                                  | **Strengths:** Data consistency, integrity, powerful querying with SQL.<br>**Weaknesses:** Rigid schema, complex joins, difficult horizontal scaling. |
| **SQL Joins**                  | **Types of Joins:** INNER, LEFT, RIGHT, CROSS, FULL OUTER                                                   | Key use cases: INNER JOIN for common rows, LEFT JOIN for left table focus, CROSS JOIN for Cartesian product, FULL OUTER JOIN for full table combinations. |
| **XML**                        | **Structure:** Elements, Attributes, Hierarchies                                                           | `<book><title>XML Fundamentals</title><author>Jane Doe</author></book>`.<br>**XML Schema (XSD):** Defines element structure, data types. |
|                                | **Strengths/Weaknesses:**                                                                                  | **Strengths:** Hierarchical structure, validation through XSD.<br>**Weaknesses:** Verbose syntax, complex for large datasets. |
| **XPath**                      | **Selecting Nodes:** `//book/title`, `@attribute`                                                         | **Common Functions:** `count()`, `contains()`.                                                                      |
| **RDF & Linked Data**          | **RDF Triples:** Subject-Predicate-Object                                                                   | **Example:** `<ex:Person1 ex:hasName "John Doe">`.                                                                  |
|                                | **Linked Data:** URIs to link data across datasets                                                         | **Ontologies:** FOAF, Dublin Core.<br>**Strengths/Weaknesses:**<br>**Strengths:** Interoperability, data integration, semantic web.<br>**Weaknesses:** Complexity, performance overhead, steep learning curve. |
| **SPARQL**                     | **Basic Queries:** SELECT, WHERE                                                                           | **Example:** `SELECT ?name WHERE { ?person ex:hasName ?name }`.                                                     |
| **JSON**                       | **Structure:** Key-Value Pairs, Nested Objects/Arrays                                                      | **Example:** `{"name": "Alice", "skills": ["JavaScript", "MongoDB"}`.                                               |
| **MongoDB**                    | **Queries:** Flexible Schema, CRUD Operations                                                              | **Example:** `db.users.find({ "age": { "$gt": 25 } })`.                                                             |
| **Precision, Recall, F1-Measure** | **Precision:** \( \frac{TP}{TP + FP} \)<br>**Recall:** \( \frac{TP}{TP + FN} \)                                  | **F1-Measure:** \( 2 \times \frac{Precision \times Recall}{Precision + Recall} \)<br>**Common Use:** Precision (Spam detection), Recall (Disease screening). |

---

### **Key Formulas and Concepts:**

| **Concept**                      | **Description**                                                                                           |
|----------------------------------|------------------------------------------------------------------------------------------------------------|
| **Normalization**                | 1NF: Remove repeating groups.<br>2NF: Eliminate partial dependencies.<br>3NF: Remove transitive dependencies.<br>BCNF: Determinants must be candidate keys. |
| **SQL Joins**                    | INNER JOIN: Match common rows.<br>LEFT JOIN: Include all left rows, match right rows.<br>RIGHT JOIN: Include all right rows, match left rows.<br>CROSS JOIN: Cartesian product.<br>FULL OUTER JOIN: All rows from both tables. |
| **XPath**                        | Selecting Nodes: `//book/title`, `@attribute`.<br>Functions: `count()`, `contains()`.                       |
| **RDF Triples**                  | Structure: Subject-Predicate-Object.<br>Example: `<ex:Person1 ex:hasName "John Doe">`.                      |
| **SPARQL**                       | Basic Query: `SELECT ?name WHERE { ?person ex:hasName ?name }`.                                             |
| **Precision, Recall, F1-Measure** | Precision: \( \frac{TP}{TP + FP} \)<br>Recall: \( \frac{TP}{TP + FN} \)<br>F1-Measure: \( 2 \times \frac{Precision \times Recall}{Precision + Recall} \) |

---

### **Important Points to Remember:**

1. **Normalization** is key to efficient database design, preventing redundancy.
2. **Joins** in SQL are essential for combining data across multiple tables.
3. **XPath** is critical for querying XML data structures.
4. **Linked Data & RDF** enable semantic web data integration.
5. **JSON/MongoDB** are flexible for managing semi-structured data.
6. **Precision, Recall, F1-Measure** are key metrics for evaluating models, especially with imbalanced datasets.

---

### **Commonly Tested Concepts:**

- **Normalization:** Tested for converting data to different normal forms.
- **SQL Joins:** Commonly appear in complex query formulation.
- **XPath Queries:** Frequently tested for extracting data from XML.
- **RDF & SPARQL:** Tested in data integration and querying linked data.
- **Precision & Recall:** Important for classifier evaluation.

---
