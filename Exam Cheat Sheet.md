
---

# Exam Cheat Sheet

---

| **Topic**                      | **Key Concepts**                                                                                          | **Must-Know Examples/Notes**                                                                                       |
|--------------------------------|------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| **Relational Databases**       | **E/R Diagrams:** Entities, Attributes, Relationships (1:1, 1:M, M:N)                                      | **Schema Conversion:** Mapping entities to tables, relationships to foreign keys.                                   |
|                                | **Normalization:** 1NF, 2NF, 3NF, BCNF                                                                     | **1NF:** Eliminate repeating groups, atomicity.<br>**2NF:** Remove partial dependencies.<br>**3NF:** Remove transitive dependencies.<br>**BCNF:** Candidate keys only. |
|                                | **Common Pitfalls:** Avoid over-normalization.                                                             | **Denormalization:** When to avoid it for performance optimization.                                                 |
|                                | **Strengths/Weaknesses:**                                                                                  | **Strengths:** Consistency, integrity, structured query language (SQL).<br>**Weaknesses:** Rigid schema, complex joins, difficult horizontal scaling. |
| **SQL Joins**                  | **Types of Joins:** INNER, LEFT, RIGHT                                                                      | **INNER JOIN:** Matching rows.<br>**LEFT JOIN:** Left table rows + matching right.<br>**RIGHT JOIN:** Right table rows + matching left. |
| **XML**                        | **Structure:** Elements, Attributes, Hierarchies                                                           | `<book><title>XML Fundamentals</title><author>Jane Doe</author></book>`.                                            |
|                                | **XML Schema (XSD):** Defines element structure, data types                                                | **Strengths/Weaknesses:**<br>**Strengths:** Validation, enforce structure.<br>**Weaknesses:** Verbose, complex for large datasets.              |
| **XPath**                      | **Selecting Nodes:** `//book/title`, `@attribute`                                                         | **Common Functions:** `count()`, `contains()`.                                                                      |

---

| **Topic**                      | **Key Concepts**                                                                                          | **Must-Know Examples/Notes**                                                                                       |
|--------------------------------|------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| **RDF & Linked Data**          | **RDF Triples:** Subject-Predicate-Object                                                                   | **Example:** `<ex:Person1 ex:hasName "John Doe">`.                                                                  |
|                                | **Linked Data:** URIs to link data across datasets                                                         | **Ontologies:** FOAF, Dublin Core.                                                                                  |
|                                | **Strengths/Weaknesses:**                                                                                  | **Strengths:** Interoperability, data integration, semantic web.<br>**Weaknesses:** Complexity, performance overhead, steep learning curve. |
| **SPARQL**                     | **Basic Queries:** SELECT, WHERE                                                                           | **Example:** `SELECT ?name WHERE { ?person ex:hasName ?name }`.                                                     |
| **JSON**                       | **Structure:** Key-Value Pairs, Nested Objects/Arrays                                                      | **Example:** `{"name": "Alice", "skills": ["JavaScript", "MongoDB"]}`.                                              |
| **MongoDB**                    | **Queries:** Flexible Schema, CRUD Operations                                                              | **Example:** `db.users.find({ "age": { "$gt": 25 } })`.                                                             |
| **Precision, Recall, F1-Measure** | **Precision:** \( \frac{TP}{TP + FP} \)<br>**Recall:** \( \frac{TP}{TP + FN} \)                                  | **F1-Measure:** \( 2 \times \frac{Precision \times Recall}{Precision + Recall} \)<br>**Common Use:** Precision (Spam detection), Recall (Disease screening). |

---

### **Key Formulas and Concepts:**
| **Concept**                      | **Formula/Description**                                                                                     |
|----------------------------------|-------------------------------------------------------------------------------------------------------------|
| **Normalization**                | **1NF:** Remove repeating groups.<br>**2NF:** Eliminate partial dependencies.<br>**3NF:** Eliminate transitive dependencies.<br>**BCNF:** All determinants are candidate keys. |
| **SQL Joins**                    | **INNER JOIN:** Match common rows.<br>**LEFT JOIN:** Include all left rows, match right rows.<br>**RIGHT JOIN:** Include all right rows, match left rows. |
| **XPath**                        | **Selecting Nodes:** `//book/title`, `@attribute`.<br>**Functions:** `count()`, `contains()`.               |
| **RDF Triples**                  | **Structure:** Subject-Predicate-Object.<br>**Example:** `<ex:Person1 ex:hasName "John Doe">`.              |
| **SPARQL**                       | **Basic Query:** `SELECT ?name WHERE { ?person ex:hasName ?name }`.                                          |
| **Precision, Recall, F1-Measure** | **Precision:** \( \frac{TP}{TP + FP} \)<br>**Recall:** \( \frac{TP}{TP + FN} \)<br>**F1-Measure:** \( 2 \times \frac{Precision \times Recall}{Precision + Recall} \) |

---

### **Important Points to Remember:**
1. **Normalization** is key to efficient database design, preventing redundancy.
2. **Joins** in SQL are essential for combining data across multiple tables.
3. **XPath** is critical for querying XML data.
4. **Linked Data & RDF** facilitate semantic web and data integration.
5. **JSON/MongoDB** are flexible for handling semi-structured data.
6. **Precision, Recall, F1-Measure** are vital metrics for evaluating machine learning models.

---

### **Commonly Tested Concepts:**
- **Normalization:** Frequently tested in scenarios requiring conversion of data into different normal forms.
- **SQL Joins:** Commonly tested in complex query formulation.
- **XPath Queries:** Often appear in questions related to extracting data from XML.
- **RDF & SPARQL:** Typically tested in data integration and querying linked data.
- **Precision & Recall:** Important in evaluating classifier performance, especially with imbalanced datasets.

---
