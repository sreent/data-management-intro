
---

### Question 1(a):

**The E/R diagram below is part of a model for a new system that will track zoo animals for breeding programs. If this Entity/Relationship model is going to be implemented as a relational model, what will need to change?**

**Correct Answer: ii. The relationship between Keeper and Animal is many-to-many and will need to be rewritten with a new entity between them.**

**Detailed Explanation:**

- **Choice i:** Some attributes have the same name (name and date of birth). They must be renamed to be unique.
  - **Explanation:** Renaming attributes for uniqueness is important, but this is a minor issue compared to addressing many-to-many relationships when converting to a relational model.

- **Choice ii:** The relationship between Keeper and Animal is many-to-many and will need to be rewritten with a new entity between them.
  - **Explanation:** This is correct. In a relational model, many-to-many relationships must be resolved using a join table (associative entity), creating two one-to-many relationships.

- **Choice iii:** The circular relationship between Zoo, Animal, and Keeper should be rewritten to remove the loop.
  - **Explanation:** Circular relationships can exist in complex systems and do not necessarily require changes when transitioning to a relational model.

- **Choice iv:** Spaces are not permitted in attributes in the relational model. Attributes such as date of birth and conservation status must be renamed.
  - **Explanation:** This is a naming convention concern that doesn’t address structural changes, making it a less critical issue.

**Real-World Example:**
In a student-course registration system, a student can register for multiple courses, and each course can have multiple students. This many-to-many relationship is resolved with an enrollment table that links students and courses.

**Common Pitfalls:**
- Overlooking the need for join tables when handling many-to-many relationships in a relational database.

**Key Takeaways:**
- Many-to-many relationships in E/R models require a join table in a relational model.
- Structural changes, like resolving many-to-many relationships, are more critical than simple naming conventions.

**Important Points to Remember:**
- Many-to-many relationships in a relational database require a separate join table.
- Renaming attributes for uniqueness is important but is a secondary concern.

---

### Question 1(b):

**Look carefully at the following table and assess its level of normalization.**

| Animal  | Species      | Feed      |
|---------|--------------|-----------|
| Simba   | Lion         | Meat      |
| Hiss    | Royal python | Meat      |
| Eeyore  | Donkey       | Silage    |
| Fozzy   | Brown bear   | Nuts      |
| Fozzy   | Brown bear   | Berries   |
| Baloo   | Brown bear   | Nuts      |
| Baloo   | Brown bear   | Berries   |

**Correct Answer: i. The table is in 1NF – all rows are a single data type.**

**Detailed Explanation:**

- **Choice i:** The table is in 1NF – all rows are a single data type.
  - **Explanation:** This is correct. The table is in 1NF because it has atomic values and no repeating groups.

- **Choice ii:** The table is in 2NF – no attribute is dependent on any non-key element or any subset of the primary key.
  - **Explanation:** Incorrect. The table is not in 2NF because it has partial dependencies (e.g., `Species` depends only on `Animal`).

- **Choice iii:** The table is in 3NF – it is in 2NF and any transitive dependencies depend on the primary key.
  - **Explanation:** Incorrect. Since the table is not in 2NF, it cannot be in 3NF.

- **Choice iv:** The table is in 4NF – there are no multivalued dependencies.
  - **Explanation:** Incorrect. A table cannot be in 4NF unless it first satisfies 3NF, which this table does not.

**Real-World Example:**
In a product catalog where multiple colors or sizes exist for each product, ensuring atomic values and eliminating partial dependencies is key to proper normalization.

**Common Pitfalls:**
- Assuming a table is in higher normal forms without verifying compliance with lower normal forms.
- Overlooking partial dependencies when assessing normalization levels.

**Key Takeaways:**
- A table must satisfy 1NF before it can move to higher normal forms.
- Partial dependencies must be eliminated for 2NF, and transitive dependencies must be removed for 3NF.

**Important Points to Remember:**
- 1NF requires atomic values and no repeating groups.
- Higher normal forms (2NF, 3NF, 4NF) require eliminating specific types of dependencies.

---

### Question 1(c):

**At the beginning of the school year, a temporary administrator is hired to add students to the school database. Which of these GRANT commands would be most appropriate to use for the new hire?**

**Correct Answer: iii. GRANT INSERT, UPDATE, SELECT, DELETE ON Students to 'temp'.**

**Detailed Explanation:**

- **Choice i:** GRANT ALL ON * TO 'temp' WITH GRANT OPTION.
  - **Explanation:** This is too permissive. It grants full access to all tables and allows the user to grant permissions to others, which is inappropriate for a temporary role.

- **Choice ii:** GRANT SELECT ON Students to 'temp'.
  - **Explanation:** This is insufficient for the tasks the temporary administrator needs to perform, such as adding or updating records.

- **Choice iii:** GRANT INSERT, UPDATE, SELECT, DELETE ON Students to 'temp'.
  - **Explanation:** This is correct. It provides the necessary permissions specific to the `Students` table while avoiding unnecessary privileges.

- **Choice iv:** GRANT ALL ON Students to 'temp'.
  - **Explanation:** This is too permissive, as it includes unnecessary permissions like dropping or altering the table.

**Real-World Example:**
In enterprise systems, role-based access control (RBAC) ensures that users have the minimum permissions necessary to perform their roles, reducing security risks.

**Common Pitfalls:**
- Granting more permissions than necessary, leading to potential misuse.
- Overlooking the specific permissions needed for the user’s role.

**Key Takeaways:**
- The principle of least privilege is key when granting permissions.
- Permissions should be tailored to the specific tasks users need to perform.

**Important Points to Remember:**
- Always apply the principle of least privilege when assigning permissions.
- Be specific in granting permissions based on the user’s role and tasks.

---

### Question 1(d):

**How many triples are there in the following RDF/Turtle?**

```turtle
chEvents:22498 a event:Event, ecrm:E7_Activity, schema:Event ;
dct:date "1952-11-30T17:30:00"^^xsd:dateTime ;
rdfs:label "Cordelle Walcott"@en .
```

**Correct Answer: iii. 5**

**Detailed Explanation:**

In RDF, each triple consists of a subject, predicate, and object. Let’s break down the given Turtle syntax:

1. **Triple 1:** `chEvents:22498 a event:Event`
2. **Triple 2:** `chEvents:22498 a ecrm:E7_Activity`
3. **Triple 3:** `chEvents:22498 a schema:Event`
4. **Triple 4:** `chEvents:22498 dct:date "1952-11-30T17:30:00"^^xsd:dateTime`
5. **Triple 5:** `chEvents:22498 rdfs:label "Cordelle Walcott"@en`

**Common Pitfalls:**
- Misinterpreting the structure of RDF triples and undercounting or overcounting based on assumptions about how Turtle syntax works.

**Key Takeaways:**
- RDF triples consist of subject, predicate, and object.
- When multiple objects are listed under the same predicate, each creates a separate triple.

**Important Points to Remember:**
- Each RDF triple is formed as subject-predicate-object.
- When multiple objects share a single predicate, each combination forms a distinct triple.

---

### Question 1(e):

**Look at the data and associated XML schema fragments below. The XML below is not well-formed. Why not?**

```xml
<movie>
  <title>Citizen Kane</title>
  <cast>
    <actor>Orson Welles</actor>
    <actor role="Jebediah Leland">Joseph Cotton</actor>
</movie>
```

**Associated XML Schema:**

```xml
<xs:element name="movie">
  <xs:complexType>
    <xs:all maxOccurs="unbounded">
      <xs:element ref="cast"/>
      <xs:element ref="releaseYear"/>
      <xs:element ref="title"/>
    </xs:all>
  </xs:complexType>
</xs:element>

<xs:element name="cast">
  <xs:complexType>
    <xs:sequence>
      <xs:element maxOccurs="unbounded" ref="actor"/>
    </xs:sequence>
  </xs:complexType>
</xs:element>

<xs:element name="actor">
  <xs:complexType mixed="true">
    <xs:attribute name="role"/>
  </xs:complexType>
</xs:element>

<xs:element name="releaseYear" type="xs:integer"/>

<xs:element name="title">
  <xs:complexType mixed="true">
    <xs:attribute name="lang" use="required"/>
  </xs:complexType>
</xs:element>
```

**Select ALL correct statements:**

i. cast should come before title  
ii. The cast element is not closed  
iii. title should have a lang attribute  
iv. actor element containing Orson Welles should have a role attribute  
v. releaseYear is missing  

---

### Solution:

**Correct Answer: ii**

**Explanation:**

- **ii. The cast element is not closed.**
  - The XML is **not well-formed** because the `<cast>` element is not properly closed. Properly closing tags is fundamental to creating well-formed XML.

**Why Other Options Are Incorrect:**

- **i. cast should come before title:**
  - The order of elements is flexible because the schema uses `<xs:all>`, which allows elements to appear in any order within the `<movie>` element.

- **iii. title should have a lang attribute:**
  - This relates to schema validation, not well-formedness. The question specifically asks about well-formedness.

- **iv. actor element containing Orson Welles should have a role attribute:**
  - The `role` attribute is optional according to the schema.

- **v. releaseYear is missing:**
  - This pertains to schema validation, not well-formedness.

**Key Takeaways:**
- Well-formed XML requires properly closed tags and correct nesting.
- Validity against the schema is a separate consideration from well-formedness.

**Important Points to Remember:**
- Always check for properly closed tags when determining if XML is well-formed.
- The order of elements can be flexible depending on the schema’s definition.

---

### Question 1(f):

**Look again at the code from the previous question. The XML is not valid. Why not? Exclude any aspects that mean the XML is not well-formed in your answer.**

**Select ALL correct statements:**

i. cast should come before title  
ii. The cast element is not closed  
iii. title should have a lang attribute  
iv. actor element containing Orson Welles should have a role attribute  
v. releaseYear is missing  

**Correct Answer: iii, v**

**Explanation:**

- **iii. title should have a lang attribute.**
  - The XML Schema defines the `title` element with a required `lang` attribute. Since this attribute is missing, the XML is invalid according to the schema.

- **v. releaseYear is missing.**
  - The XML Schema specifies a `releaseYear` element as part of the `<movie>` structure. The absence of this element makes the XML invalid according to the schema.

**Why Other Options Are Incorrect:**

- **i. cast should come before title:**
  - The order of elements does not matter here because the schema uses `<xs:all>`, allowing elements to appear in any order.

- **ii. The cast element is not closed:**
  - This relates to well-formedness, not schema validation. The question specifically asks about schema validation, excluding well-formedness issues.

- **iv. actor element containing Orson Welles should have a role attribute:**
  - The `role` attribute is optional according to the schema, so its absence does not make the XML invalid.

**Key Takeaways:**
- XML validation involves ensuring that required elements and attributes are present according to the schema.
- Well-formedness and validity are distinct concepts: well-formedness focuses on tag structure, while validity involves compliance with the schema.

**Important Points to Remember:**
- Well-formedness and schema validity are separate concepts.
- Ensure that required attributes and elements are present to validate against a schema.

---

### Question 1(g):

**Which of the following are true statements comparing MongoDB with SQL?**

**Select ALL correct statements:**

i. Unlike SQL, MongoDB has no explicit indexes.  
ii. Unlike MongoDB, a SQL DBMS can guarantee ACID compliance in all transactions.  
iii. A single MongoDB update would often map to more than one command in SQL.  
iv. A MongoDB document can have a more complex structure than an SQL table.

**Correct Answer: ii, iii, iv**

**Detailed Explanation:**

- **ii. Unlike MongoDB, a SQL DBMS can guarantee ACID compliance in all transactions.**
  - SQL databases are built to ensure ACID (Atomicity, Consistency, Isolation, Durability) properties for transactions, which guarantees data integrity even under complex and concurrent operations. MongoDB, while offering some ACID features (especially with multi-document transactions in newer versions), is not inherently ACID-compliant in the same way as traditional SQL databases.

- **iii. A single MongoDB update would often map to more than one command in SQL.**
  - In MongoDB, operations on complex documents may involve nested structures and arrays, which could require multiple commands in SQL to achieve the same outcome.

- **iv. A MongoDB document can have a more complex structure than an SQL table.**
  - MongoDB’s document model allows for nested documents, arrays, and varied structures, which can be more complex than the flat, row-based structure typical of an SQL table.

**Why Other Options Are Incorrect:**

- **i. Unlike SQL, MongoDB has no explicit indexes:**
  - This is incorrect because MongoDB does support indexes. Indexing is a crucial feature in MongoDB for optimizing query performance.

**Key Takeaways:**
- SQL databases guarantee ACID compliance, making them suitable for transactions requiring strict consistency.
- MongoDB’s flexible document model allows for more complex and varied structures compared to SQL tables.
- While both systems support indexing, MongoDB’s indexing capabilities are often underestimated.

**Important Points to Remember:**
- MongoDB supports indexing, similar to SQL.
- ACID compliance is a key difference between traditional SQL databases and NoSQL systems like MongoDB.

---

### Question 1(h):

**An international researcher will be arriving to visit an archive. They want a list of all documents that satisfy their research requirements, which they will then digitize during their visit. After they return, they will work through the results manually and discard documents that shouldn’t be there. Assume that digitization in this case is quick, easy, and cost-free, but has to be done by the researcher when they are present. How would you best evaluate the IR system they use?**

**Options:**

i. Evaluate the system’s precision (recall is less important here).  
ii. Evaluate the system’s recall (precision is less important here).  
iii. Evaluate the system’s F-measure (precision and recall need to be balanced).  
iv. Evaluate the system’s Shannon entropy (the information content is most important in this case).

**Correct Answer: i. Evaluate the system’s precision (recall is less important here).**

**Detailed Explanation:**

- **i. Evaluate the system’s precision (recall is less important here).**
  - In this scenario, the researcher needs to ensure that the documents returned are highly relevant, as they will later manually sift through the results to remove irrelevant items. Since digitization is quick and cost-free, it is more important that the retrieved documents are relevant (high precision) than ensuring all possible relevant documents are found (high recall).

**Why F-Measure Is Not Ideal in This Scenario:**

- **iii. Evaluate the system’s F-measure (precision and recall need to be balanced).**
  - The F-Measure balances precision and recall. However, in this case, recall is less critical because it is easy to manually filter out irrelevant results. The researcher is willing to trade off recall (missing some relevant documents) for higher precision, meaning that precision is the primary metric of interest.

**Key Takeaways:**
- Precision is crucial when the primary concern is retrieving highly relevant documents and the cost of false positives is low.
- F-Measure is useful when both precision and recall are equally important, but in this scenario, precision is prioritized.

**Important Points to Remember:**
- Precision is prioritized when irrelevant results can be easily discarded.
- F-Measure is only relevant when balancing both precision and recall is necessary.

---

### Question 1(i):

**What distinguishes a graph from a tree?**

**Select ALL correct statements:**

i. A graph does not need a root node; a tree does.  
ii. A tree can include text; a graph cannot.  
iii. A node in a tree has exactly one parent node; a graph has no such constraint.  
iv. A tree does not need a root node; a graph does.

**Correct Answer: i, iii**

**Detailed Explanation:**

- **i. A graph does not need a root node; a tree does.**
  - This is correct. A tree is a special type of graph that is hierarchical in structure, with a designated root node. General graphs do not require a root node, and their structure can be more flexible and interconnected.

- **ii. A tree can include text; a graph cannot.**
  - This is incorrect. Both trees and graphs can include text labels for their nodes. The inclusion of text is not a distinguishing factor between trees and graphs.

- **iii. A node in a tree has exactly one parent node; a graph has no such constraint.**
  - This is correct. In a tree structure, each child node has exactly one parent (except for the root), while in a general graph, nodes can have multiple incoming edges, allowing for more complex relationships without the single-parent constraint.

- **iv. A tree does not need a root node; a graph does.**
  - This is incorrect. Trees must have a root node to define their hierarchical structure, while general graphs do not require a root node.

**Real-World Example:**
- File systems are typically modeled as trees, with a root directory at the top and subdirectories forming branches. Social networks, on the other hand, are modeled as graphs, where connections between people are not necessarily hierarchical and can involve complex relationships.

**Common Pitfalls:**
- Confusing trees with general graphs. Trees are a subset of graphs with additional rules (like the need for a root and single parent per node).

**Key Takeaways:**
- Trees are hierarchical structures with a root node, whereas graphs can have any structure and do not require a root.
- In trees, each node (except the root) has exactly one parent, while graphs can have multiple connections per node.

**Important Points to Remember:**
- Trees are a specialized type of graph with hierarchical constraints.
- General graphs allow more flexible and interconnected structures without a designated root or single-parent rule.

---

### Question 1(j):

**Which of the following statements about types of joins in SQL are correct?**

**Select ALL correct statements:**

i. A LEFT JOIN will produce at least as many rows as an INNER JOIN.  
ii. An INNER JOIN will produce at least as many rows as a LEFT JOIN.  
iii. A CROSS JOIN will produce at least as many rows as a LEFT JOIN.  
iv. A LEFT JOIN will produce at least as many rows as a CROSS JOIN.  
v. No type of join can produce more rows than a CROSS JOIN.

**Correct Answer: i, iii, v**

**Detailed Explanation:**

- **i. A LEFT JOIN will produce at least as many rows as an INNER JOIN.**
  - This is correct. A LEFT JOIN returns all rows from the left table, even if there is no matching row in the right table. An INNER JOIN only returns rows with matching keys in both tables, so a LEFT JOIN will always produce at least as many rows as an INNER JOIN.

- **ii. An INNER JOIN will produce at least as many rows as a LEFT JOIN.**
  - This is incorrect. An INNER JOIN will produce fewer rows than a LEFT JOIN if there are rows in the left table that do not have matching rows in the right table.

- **iii. A CROSS JOIN will produce at least as many rows as a LEFT JOIN.**
  - This is correct. A CROSS JOIN returns the Cartesian product of the two tables, resulting in a large number of rows (multiplying the number of rows in both tables). This is usually much more than what a LEFT JOIN would produce.

- **iv. A LEFT JOIN will produce at least as many rows as a CROSS JOIN.**
  - This is incorrect. A CROSS JOIN generally produces many more rows because it returns every possible combination of rows from both tables.

- **v. No type of join can produce more rows than a CROSS JOIN.**
  - This is correct. A CROSS JOIN, which is the Cartesian product of two tables, produces the maximum possible number of rows from a join operation.

**Real-World Example:**
- In a database with employees and departments, a LEFT JOIN would return all employees, including those without a department, while an INNER JOIN would only return employees with a department. A CROSS JOIN, however, would create every possible combination of employees and departments, resulting in a very large result set.

**Common Pitfalls:**
- Misunderstanding the behavior of LEFT JOIN versus INNER JOIN. A LEFT JOIN includes unmatched rows from the left table, while an INNER JOIN only includes matches.
- Assuming that a CROSS JOIN behaves like other types of joins, when in fact it creates the Cartesian product, leading to potentially massive result sets.

**Key Takeaways:**
- LEFT JOIN includes unmatched rows from the left table, while INNER JOIN only includes matches.
- CROSS JOIN produces the Cartesian product, which usually results in the largest possible number of rows.

**Important Points to Remember:**
- A CROSS JOIN generates every possible combination of rows from both tables.
- LEFT JOIN typically returns more rows than INNER JOIN because it retains unmatched rows from the left table.

---
