# Solution Sheet - Mock March 2021

## Exam Overview

| Section | Questions | Marks |
|---------|-----------|-------|
| Section A | 10 MCQs (Q1a-j) | 40 |
| Section B | Answer 2 of 3 | 60 |
| **Total** | | **100** |

---

# Section A: Multiple Choice Questions [40 marks]

---

## Question 1(a) [4 marks]

**Question:** Normalisation can be thought of as an attempt to reduce information duplication in a database. What is the ONE primary reason why this is desirable?

---

### Answer

**ii. Duplicate information can get out of sync, leading to logical inconsistencies in the data**

---

### Revision Notes

**Core Concept:** Normalisation prevents update anomalies.

**Why Option ii is Correct:**

| Anomaly Type | Problem | Example |
|--------------|---------|---------|
| **Update Anomaly** | Changing one copy but not others | Customer address updated in one row but not another |
| **Insertion Anomaly** | Can't add data without unrelated data | Can't add a new department without an employee |
| **Deletion Anomaly** | Deleting data loses unrelated data | Deleting last employee loses department info |

**Why Other Options Are Wrong:**

| Option | Problem |
|--------|---------|
| i. Storage cost | While true historically, this is a secondary concern |
| iii. Data entry speed | Normalisation can actually slow data entry (more tables) |
| iv. Security threat | Redundancy isn't primarily a security issue |

**Key Point:** The "ONE primary reason" is data integrity, not storage or performance.

---

## Question 1(b) [4 marks]

**Question:** I want to query a database table of books and join it to a table of authors. Where the book is anonymous, I want the author field to have the value NULL. What type of join do I need?

---

### Answer

**i. LEFT JOIN**

---

### Revision Notes

**Core Concept:** JOIN types determine how unmatched rows are handled.

**JOIN Type Comparison:**

| JOIN Type | Behaviour | Use Case |
|-----------|-----------|----------|
| **LEFT JOIN** | Keeps ALL rows from left table, NULL for unmatched right | Books without authors → NULL |
| **INNER JOIN** | Only rows that match in BOTH tables | Only books WITH authors |
| **CROSS JOIN** | Cartesian product (all combinations) | Every book × every author |
| **RIGHT JOIN** | Keeps ALL rows from right table | All authors, even without books |

**Visual Example:**

```
Books Table              Authors Table
+----+------------+      +----+----------+
| Id | Title      |      | Id | Name     |
+----+------------+      +----+----------+
| 1  | Beowulf    |      | 1  | Tolkien  |
| 2  | The Hobbit |      +----+----------+
+----+------------+

LEFT JOIN Result:
+------------+----------+
| Title      | Author   |
+------------+----------+
| Beowulf    | NULL     |  ← Anonymous book kept!
| The Hobbit | Tolkien  |
+------------+----------+
```

**Common Mistakes:**
- Thinking INNER JOIN with `WHERE Author IS NULL` would work (it won't — INNER JOIN excludes non-matches before WHERE)
- Confusing LEFT/RIGHT — the "left" table is the one mentioned first (before JOIN)

---

## Question 1(c) [4 marks]

**Question:** Look at the following sequence of commands and choose the statement that should replace XXXXXXX:
```sql
START TRANSACTION;
SELECT stockLevel FROM Stock WHERE ID=23948267;
UPDATE Stock SET stockLevel=stockLevel-2 WHERE ID=23948267;
INSERT INTO Orders (productID, quantity) VALUES (23948267, 2) WHERE ID=2924847
XXXXXXX
```

---

### Answer

**iv. COMMIT;**

---

### Revision Notes

**Core Concept:** Transactions must be explicitly committed to make changes permanent.

**Transaction Commands:**

| Command | Purpose |
|---------|---------|
| `START TRANSACTION` | Begin a transaction block |
| `COMMIT` | Save all changes permanently |
| `ROLLBACK` | Undo all changes since START |
| `SAVEPOINT name` | Create a restore point |

**Why Other Options Are Wrong:**

| Option | Problem |
|--------|---------|
| i. `GRANT...` | Permission command, not transaction control |
| ii. `UPDATE SET stockLevel=2` | Would overwrite to 2, not complete transaction |
| iii. `END TRANSACTION` | Not valid SQL syntax |
| v. `UPDATE +2` | Would add stock back (rollback logic, but not proper) |

**Transaction Flow:**
```
START TRANSACTION
    ↓
Operations (SELECT, UPDATE, INSERT...)
    ↓
COMMIT ← Makes changes permanent
   or
ROLLBACK ← Undoes all changes
```

**ACID Properties:**
- **A**tomicity: All or nothing
- **C**onsistency: Valid state to valid state
- **I**solation: Transactions don't interfere
- **D**urability: Committed = permanent

---

## Question 1(d) [4 marks]

**Question:** What does the following MongoDB call do?
```javascript
db.books.find({
  title: /*man/,
  author: /*man/,
  year: 1934
});
```

---

### Answer

**v. Finds all books with title and author ending in man with a year of 1934**

---

### Revision Notes

**Core Concept:** MongoDB uses regex patterns for string matching.

**Regex Pattern Analysis:**

| Pattern | Meaning |
|---------|---------|
| `/*man/` | Matches strings ending with "man" |
| `/man/` | Matches strings containing "man" anywhere |
| `/^man/` | Matches strings starting with "man" |
| `/^man$/` | Matches exactly "man" |

**Query Breakdown:**

```javascript
{
  title: /*man/,    // Title ends with "man" (e.g., "Batman", "Superman")
  author: /*man/,   // Author ends with "man" (e.g., "Gaiman")
  year: 1934        // Exact year match
}
```

All three conditions must be TRUE (implicit AND).

**Why Other Options Are Wrong:**

| Option | Problem |
|--------|---------|
| i. Sets year to 1934 | `find()` reads data, doesn't modify |
| ii. Called man | `*man` means "ends with", not exact match |
| iii. Ending in man (no year) | Year condition is also required |
| iv. Called man with year | Same issue — it's "ends with", not "equals" |
| vi. Adds a new record | `find()` queries, `insert()` adds records |

**MongoDB vs SQL Comparison:**
```javascript
// MongoDB
db.books.find({ title: /man$/, year: 1934 })

// Equivalent SQL
SELECT * FROM Books
WHERE Title LIKE '%man' AND Year = 1934;
```

---

## Question 1(e) [4 marks]

**Question:** Why are URLs important in Linked Data and other Semantic Web technologies? Select ALL correct statements.

---

### Answer

**i, ii, and iv are correct.**

---

### Revision Notes

**Core Concept:** URLs serve as global identifiers in Linked Data.

**Analysis of Each Statement:**

| Statement | Correct? | Explanation |
|-----------|----------|-------------|
| **i. Unique like Primary Key** | ✓ Yes | URLs are globally unique identifiers |
| **ii. Shareable reference** | ✓ Yes | Anyone can use the same URL to mean the same thing |
| **iii. Path encodes meaning** | △ Partial | URLs should be opaque; meaning comes from dereferencing |
| **iv. Dereferencing** | ✓ Yes | HTTP GET returns information about the resource |
| **v. Permanent and reliable** | ✗ No | URLs can break (404), move, or change |

**The Four Principles of Linked Data (Tim Berners-Lee):**
1. Use URIs as names for things
2. Use HTTP URIs so people can look up those names
3. When someone looks up a URI, provide useful information (RDF)
4. Include links to other URIs to discover more things

**URL vs URN vs URI:**

| Term | Example | Key Feature |
|------|---------|-------------|
| URL | `http://example.org/thing` | Locator — tells you WHERE |
| URN | `urn:isbn:0451450523` | Name — just identifies |
| URI | Either of above | Umbrella term for both |

**Why "Permanent" is FALSE:**
- Link rot: URLs stop working over time
- Cool URIs don't change, but many do
- No technical guarantee of permanence

---

## Question 1(f) [4 marks]

**Question:** Given the XML fragment, what does the XPath expression `//note/title` refer to?

---

### Answer

**i. The four title elements that appear as direct child nodes of note elements**

---

### Revision Notes

**Core Concept:** XPath navigation with `//` (descendant) and `/` (child).

**XPath Breakdown:**

| Part | Meaning |
|------|---------|
| `//` | Descendant axis — find anywhere in document |
| `note` | Element named "note" |
| `/` | Child axis — direct children only |
| `title` | Element named "title" |

**Full Expression:** Find all `<title>` elements that are **direct children** of `<note>` elements, anywhere in the document.

**Counting the Matches:**

In the XML fragment, there are two `<note>` elements:
1. First `<note>` contains: `<title>Annals of the Reformation</title>` and `<title>Annals</title>` (2 titles)
2. Second `<note>` contains: `<title>A Supplication made...</title>` and `<title>Annals</title>` (2 titles)

**Total: 4 title elements**

**Why Other Options Are Wrong:**

| Option | Problem |
|--------|---------|
| ii. Nothing (no note as root child) | `//` searches anywhere, not just root children |
| iii. First title only | XPath returns ALL matches, not just first |
| iv. No titles exist | There ARE title elements inside note elements |
| v. The note elements | Query selects title, not note |

**Common Mistakes:**
- Confusing `//note/title` (titles inside notes) with `//title` (all titles anywhere)
- Forgetting `//` searches descendants, not just children of root

---

## Question 1(g) [4 marks]

**Question:** Which of the following are true statements about MapReduce? Select ALL correct statements.

---

### Answer

**i, iii, v, vi, and viii are correct.**

---

### Revision Notes

**Core Concept:** MapReduce is a parallel processing framework for distributed data.

**Statement Analysis:**

| Statement | Correct? | Explanation |
|-----------|----------|-------------|
| **i. Map on local data** | ✓ Yes | Mappers process their local partition |
| **ii. Reduce on local data** | ✗ No | Reduce receives shuffled data from multiple mappers |
| **iii. Map produces key-distributable data** | ✓ Yes | Map outputs (key, value) pairs for distribution |
| **iv. Reduce produces key-distributable data** | ✗ No | Reduce produces final output |
| **v. Input can be distributed** | ✓ Yes | Data is partitioned across nodes |
| **vi. Reducers can be distributed** | ✓ Yes | Different reducers handle different keys |
| **vii. Reduces processing needed** | ✗ No | Same total work, just parallelised |
| **viii. Easier parallel processing** | ✓ Yes | Framework handles distribution complexity |

**MapReduce Flow:**

```
Input Data (distributed)
         ↓
    ┌────┴────┐
    ↓         ↓
  Map 1     Map 2      ← Local processing
    ↓         ↓
  (k,v)     (k,v)      ← Key-value output
    ↓         ↓
    └────┬────┘
         ↓
     Shuffle/Sort       ← Group by key
         ↓
    ┌────┴────┐
    ↓         ↓
 Reduce 1  Reduce 2    ← Distributed by key
    ↓         ↓
  Output   Output
```

**Key Points:**
- Map = "embarrassingly parallel" (no communication needed)
- Shuffle = the expensive communication phase
- Reduce = parallel across different keys

---

## Question 1(h) [4 marks]

**Question:** Given the music ontology and published data, which of the following MUST be true? Select ALL correct statements.

---

### Answer

**iii and v are correct.**

---

### Revision Notes

**Core Concept:** RDF inference from domain, range, and inverseOf.

**Given Information:**

```turtle
# Ontology
mo:listened a owl:ObjectProperty ;
    rdfs:domain foaf:Agent ;
    rdfs:range mo:Performance ;
    owl:inverseOf mo:listener .

# Data
orcid:0000-0003-4151-0499 a foaf:Agent ;
    mo:listened <http://data.carnegiehall.org/events/46018> .
```

**Inference Analysis:**

| Statement | True? | Reasoning |
|-----------|-------|-----------|
| i. orcid:... a mo:Performance | ✗ No | It's in the DOMAIN (Agent), not range |
| ii. event a foaf:Agent | ✗ No | Event is in the RANGE (Performance), not domain |
| **iii. event a mo:Performance** | ✓ Yes | From rdfs:range — object of mo:listened must be Performance |
| iv. orcid:... dct:date ... | ✗ No | The date is on the EVENT, not the person |
| **v. event mo:listener orcid:...** | ✓ Yes | From owl:inverseOf — if A listened B, then B listener A |

**Domain and Range Inference:**

```
Subject  ──predicate──>  Object
   ↓                       ↓
 domain                  range
   ↓                       ↓
foaf:Agent           mo:Performance
```

**InverseOf Inference:**

```
orcid:... mo:listened event    (given)
          ↓ inverseOf
event mo:listener orcid:...    (inferred)
```

**Common Mistakes:**
- Confusing domain with range
- Thinking properties apply transitively to subjects (the date is on the event, not the listener)
- Forgetting that inverseOf swaps subject and object

---

## Question 1(i) [4 marks]

**Question:** A retrieval algorithm has a fairly constant 20% precision across all result sets. If my corpus contains 15,030,482 documents of which 225,030 are relevant, which statements are likely to be true? Select ALL correct statements.

---

### Answer

**ii and iv are correct.**

---

### Revision Notes

**Core Concept:** Precision measures the proportion of retrieved documents that are relevant.

**Definitions:**

| Metric | Formula | Meaning |
|--------|---------|---------|
| **Precision** | Relevant Retrieved / Total Retrieved | "How accurate are my results?" |
| **Recall** | Relevant Retrieved / Total Relevant | "What fraction did I find?" |

**Calculations:**

**Statement Analysis:**

| Statement | Calculation | Result |
|-----------|-------------|--------|
| i. 80 docs → 32 matches | 80 × 20% = 16 | ✗ False |
| **ii. 80 docs → 16 matches** | 80 × 20% = 16 | ✓ True |
| iii. At most 45,000 matches | Max = 225,030 (all relevant) | ✗ False |
| **iv. Over 10× better than random** | See below | ✓ True |
| v. Over 100× better than random | See below | ✗ False |

**Random Baseline Calculation:**

```
Random precision = Relevant / Total
                 = 225,030 / 15,030,482
                 = 0.015 (1.5%)

Algorithm precision = 20%

Improvement = 20% / 1.5% = 13.3× better
```

- 13.3× > 10× ✓ (statement iv is TRUE)
- 13.3× < 100× ✗ (statement v is FALSE)

**Why Statement iii is False:**
- The maximum correct matches = total relevant documents = 225,030
- 45,000 is not a meaningful upper limit

---

## Question 1(j) [4 marks]

**Question:** Which of the following statements is true of Copyleft? Select ALL correct statements.

---

### Answer

**ii, iv, and v are correct.**

---

### Revision Notes

**Core Concept:** Copyleft requires derivative works to use the same licence.

**Statement Analysis:**

| Statement | Correct? | Explanation |
|-----------|----------|-------------|
| i. Copyleft = permissive | ✗ No | Copyleft is restrictive, not permissive |
| **ii. Copyleft ≠ permissive** | ✓ Yes | Correct — copyleft imposes conditions |
| iii. Derivatives choose own licence | ✗ No | This describes PERMISSIVE licences |
| **iv. Derivatives must be copyleft** | ✓ Yes | This IS the definition of copyleft |
| **v. GPL is copyleft** | ✓ Yes | GPL is the canonical copyleft licence |
| vi. MIT is copyleft | ✗ No | MIT is permissive, not copyleft |

**Licence Comparison:**

| Licence | Type | Derivative Works |
|---------|------|------------------|
| **GPL** | Copyleft | Must be GPL |
| **LGPL** | Weak Copyleft | Libraries can link to proprietary |
| **MIT** | Permissive | Any licence allowed |
| **BSD** | Permissive | Any licence allowed |
| **CC BY-SA** | Copyleft | Must be same licence |
| **CC BY** | Permissive | Any licence allowed |

**Key Terminology:**
- **Permissive:** "Do what you want, just credit me"
- **Copyleft:** "Share alike — keep it free"
- **Viral:** Slang for copyleft (spreads to derivatives)

---

# Section B

---

# Question 2: Doctor Who Database [30 marks]

## Sample Data Context

The question describes Doctor Who with:
- Multiple incarnations of the Doctor (First Doctor, Second Doctor, etc.)
- Actors playing each incarnation
- Companions (may appear with multiple Doctors)
- Broadcast dates

---

## Question 2(a) [6 marks]

**Question:** List the tables needed, indicating all keys.

---

### Answer

| Table | Primary Key | Foreign Keys |
|-------|-------------|--------------|
| **Doctors** | Incarnation | - |
| **Actors** | Name | - |
| **Companions** | Name | - |
| **PlaysDoctor** | (Actor, Doctor) | Actor → Actors(Name), Doctor → Doctors(Incarnation) |
| **PlaysCompanion** | (Actor, Companion) | Actor → Actors(Name), Companion → Companions(Name) |
| **DoctorCompanion** | (Doctor, Companion) | Doctor → Doctors(Incarnation), Companion → Companions(Name) |

**Alternative Schema (Simpler):**

| Table | Primary Key | Foreign Keys |
|-------|-------------|--------------|
| **Doctors** | Incarnation | PlayedBy → Actors(Name) |
| **Actors** | Name | - |
| **Companions** | Name | PlayedBy → Actors(Name) |
| **DoctorCompanion** | (Doctor, Companion) | Doctor → Doctors, Companion → Companions |

---

### Revision Notes

**Core Concept:** Identifying entities and relationships from text.

**Entities Identified:**
1. **Doctor incarnations** (First Doctor, Second Doctor, etc.)
2. **Actors** (William Hartnell, Patrick Troughton, etc.)
3. **Companions** (Susan Foreman, Amy Pond, etc.)

**Relationships:**
- Doctor **played by** Actor (potentially multiple actors for one incarnation)
- Companion **played by** Actor
- Companion **appears with** Doctor (M:N — companions can appear with multiple Doctors)

**Design Decisions:**

| Choice | Reasoning |
|--------|-----------|
| Separate Actors table | Same actor might play Doctor AND companion |
| DoctorCompanion junction | M:N relationship (companions overlap Doctors) |
| Incarnation as PK | "First Doctor", "Second Doctor" are distinct |

---

## Question 2(b) [3 marks]

**Question:** Give a MySQL command for creating ONE of these tables.

---

### Answer

```sql
CREATE TABLE Doctors (
    Incarnation VARCHAR(50) PRIMARY KEY,
    PlayedBy VARCHAR(100),
    PeriodStart DATE,
    PeriodEnd DATE,
    FOREIGN KEY (PlayedBy) REFERENCES Actors(Name)
);
```

**Alternative (Companions table):**

```sql
CREATE TABLE Companions (
    Name VARCHAR(100) PRIMARY KEY,
    PlayedBy VARCHAR(100),
    FOREIGN KEY (PlayedBy) REFERENCES Actors(Name)
);
```

**Alternative (Junction table):**

```sql
CREATE TABLE DoctorCompanion (
    Doctor VARCHAR(50),
    Companion VARCHAR(100),
    PRIMARY KEY (Doctor, Companion),
    FOREIGN KEY (Doctor) REFERENCES Doctors(Incarnation),
    FOREIGN KEY (Companion) REFERENCES Companions(Name)
);
```

---

### Revision Notes

**Core Concept:** CREATE TABLE syntax with constraints.

**Essential Components:**

```sql
CREATE TABLE TableName (
    Column1 DataType CONSTRAINT,
    Column2 DataType,
    PRIMARY KEY (Column1),
    FOREIGN KEY (Column2) REFERENCES OtherTable(Column)
);
```

**Common Data Types:**

| Type | Use Case |
|------|----------|
| `VARCHAR(n)` | Variable-length text |
| `INT` | Whole numbers |
| `DATE` | Dates (YYYY-MM-DD) |
| `DATETIME` | Date and time |

---

## Question 2(c) [3 marks]

**Question:** Are your tables in 2NF? How can you tell?

---

### Answer

**Yes**, the tables are in 2NF.

**How to verify:**
1. **1NF requirement met:** All columns contain atomic values (no repeating groups)
2. **2NF requirement met:** No partial dependencies — every non-key attribute depends on the WHOLE primary key

**For Doctors table:**
- PK: Incarnation (single column)
- All attributes (PlayedBy, PeriodStart, PeriodEnd) depend on the whole key
- Single-column PKs automatically satisfy 2NF

**For DoctorCompanion junction table:**
- PK: (Doctor, Companion) — composite
- No non-key attributes, so no partial dependencies possible

---

### Revision Notes

**Core Concept:** Normal forms and their requirements.

**Normal Form Hierarchy:**

| Form | Requirement |
|------|-------------|
| **1NF** | Atomic values, no repeating groups |
| **2NF** | 1NF + no partial dependencies |
| **3NF** | 2NF + no transitive dependencies |

**2NF Violation Example:**

```
OrderItems (OrderId, ProductId, ProductName, Quantity)
           \_______PK_______/

ProductName depends on ProductId alone, not the full PK
→ Partial dependency → NOT in 2NF
```

**Key Insight:** Tables with single-column primary keys are automatically in 2NF (partial dependencies are impossible).

---

## Question 2(d) [9 marks]

**Question:** Give MySQL commands to answer the following queries:

### (i) Who played the Doctor whose companion was Amy Pond? [2 marks]

```sql
SELECT D.PlayedBy
FROM Doctors D
INNER JOIN DoctorCompanion DC ON D.Incarnation = DC.Doctor
INNER JOIN Companions C ON DC.Companion = C.Name
WHERE C.Name = 'Amy Pond';
```

---

### (ii) Was companion Peri featured before Leela? [4 marks]

```sql
SELECT
    CASE
        WHEN MIN(D1.PeriodStart) < MIN(D2.PeriodStart) THEN 'Peri was before Leela'
        ELSE 'Leela was before Peri'
    END AS Result
FROM DoctorCompanion DC1
INNER JOIN Doctors D1 ON DC1.Doctor = D1.Incarnation
INNER JOIN Companions C1 ON DC1.Companion = C1.Name
CROSS JOIN DoctorCompanion DC2
INNER JOIN Doctors D2 ON DC2.Doctor = D2.Incarnation
INNER JOIN Companions C2 ON DC2.Companion = C2.Name
WHERE C1.Name = 'Peri' AND C2.Name = 'Leela';
```

**Simpler approach (returns data for comparison):**

```sql
SELECT C.Name, MIN(D.PeriodStart) AS FirstAppearance
FROM Companions C
INNER JOIN DoctorCompanion DC ON C.Name = DC.Companion
INNER JOIN Doctors D ON DC.Doctor = D.Incarnation
WHERE C.Name IN ('Peri', 'Leela')
GROUP BY C.Name
ORDER BY FirstAppearance;
```

---

### (iii) Which incarnation of the Doctor had the most companions? [3 marks]

```sql
SELECT D.Incarnation, COUNT(*) AS CompanionCount
FROM Doctors D
INNER JOIN DoctorCompanion DC ON D.Incarnation = DC.Doctor
GROUP BY D.Incarnation
ORDER BY CompanionCount DESC
LIMIT 1;
```

---

### Revision Notes

**Core Concept:** JOINs with GROUP BY and aggregation.

**Query Patterns:**

| Task | SQL Pattern |
|------|-------------|
| Find related data | JOIN tables on FK relationships |
| Filter results | WHERE clause |
| Aggregate | GROUP BY + COUNT/SUM/AVG |
| Find maximum | ORDER BY DESC LIMIT 1 |
| Compare values | CASE WHEN or subqueries |

---

## Question 2(e) [9 marks]

**Question:** Consider the DBpedia extract for the First Doctor.

### (i) What serialization language is this? [1 mark]

**Turtle** (Terse RDF Triple Language)

---

### (ii) How many triples are encoded here? [1 mark]

**14 triples**

Counting:
- `rdfs:label` → 1 triple
- `dbp:periodEnd` → 1 triple
- `dbp:periodStart` → 1 triple
- `dbp:companions` → 10 triples (one per companion)
- `dct:subject` → 1 triple
- `dbp:next` → 1 triple

**Total: 14**

---

### (iii) What can your database schema do that this approach can't? [2 marks]

1. **Track who played each companion** — The RDF only lists companion names as strings, not linked entities with their own properties
2. **Query which actor played the Doctor** — No actor information in this RDF extract
3. **Distinguish multiple actors for same companion** — Companions are just literal strings

---

### (iv) How would you fix that problem? [2 marks]

**Replace literal strings with URIs:**

```turtle
dbr:First_Doctor dbp:companions dbr:Susan_Foreman ,
                                dbr:Ian_Chesterton ,
                                dbr:Barbara_Wright .

dbr:Susan_Foreman a dbr:Companion ;
    rdfs:label "Susan Foreman"@en ;
    dbr:playedBy dbr:Carole_Ann_Ford .
```

**Key changes:**
1. Use resource URIs instead of string literals for companions
2. Create separate resources for each companion with their own properties
3. Link companions to actors via `playedBy` property

---

### (v) Fix the SPARQL query [3 marks]

**Original (broken):**
```sparql
SELECT dbr:doctor
WHERE {
  dbr:First_Doctor dbp:next+ ?doctor .
  dbr:doctor dbp:companion "Leela" .
}
```

**Fixed:**
```sparql
SELECT ?doctor
WHERE {
  dbr:First_Doctor dbp:next* ?doctor .
  ?doctor dbp:companions "Leela"@en .
}
```

**Issues Fixed:**

| Problem | Fix |
|---------|-----|
| `SELECT dbr:doctor` | Should be `SELECT ?doctor` (variable) |
| `dbr:doctor` in WHERE | Should be `?doctor` (same variable) |
| `dbp:companion` | Should be `dbp:companions` (as shown in data) |
| `"Leela"` | Should be `"Leela"@en` (language tag) |
| `dbp:next+` | Could use `dbp:next*` to include First Doctor |

**Note:** The question says "Amy Pond" but the query uses "Leela" — fix based on actual query shown.

---

# Question 3: XML Cast List [30 marks]

## Question 3(a) [4 marks]

### (i) This fragment is unbalanced. What is missing? [1 mark]

**Answer:** The closing `</castList>` tag is missing.

The fragment starts with `<castList>` but never closes it.

---

### (ii) What format is this? [1 mark]

**Answer:** **XML** (Extensible Markup Language), specifically using the **TEI** (Text Encoding Initiative) namespace.

The namespace `xmlns="http://www.tei-c.org/ns/1.0"` indicates TEI format.

---

### (iii) What attributes are used in this fragment? [2 marks]

**Answer:**
1. `xmlns` — Namespace declaration
2. `xml:id` — Unique identifier (e.g., `xml:id="Hermia_MND"`)

---

### Revision Notes

**Core Concept:** XML well-formedness requires balanced tags.

**XML Rules:**
- Every opening tag must have a closing tag
- Tags must be properly nested (no overlapping)
- Attribute values must be quoted
- There must be exactly one root element

**TEI (Text Encoding Initiative):**
- Standard for encoding texts in humanities
- Used for manuscripts, plays, poetry, etc.
- `castList`, `castItem`, `role` are TEI elements

---

## Question 3(b) [8 marks]

### (i) What is this file and what does it do? [2 marks]

**Answer:** This is an **XSD (XML Schema Definition)** file.

**Purpose:**
- Defines the structure and constraints for valid XML documents
- Specifies which elements can contain which children
- Defines attribute types and requirements
- Enables validation of XML against the schema

---

### (ii) Does the missing model.global/model.headLike make the document invalid? [3 marks]

**Answer:** **No**, the document is NOT invalid.

**Explanation:** The XSD defines:
```xml
<xs:choice minOccurs="0" maxOccurs="unbounded">
```

The `minOccurs="0"` means these elements are **optional** — zero occurrences are valid.

The first `<castGroup>` contains another `<castGroup>` as its first child, which is allowed by the second `<xs:sequence>` that permits `castItem`, `castGroup`, or `roleDesc`.

---

### (iii) Do the castGroup elements follow this definition correctly? [3 marks]

**Answer:** **Yes**, the castGroup elements follow the definition correctly.

**Verification:**
1. First castGroup contains: another castGroup (valid as per `<xs:element ref="ns1:castGroup"/>`)
2. Inner castGroup contains:
   - `<head>four lovers</head>` — matches `model.headLike` (optional, `minOccurs="0"`)
   - Multiple `<castItem>` elements — matches `<xs:element ref="ns1:castItem"/>`
3. Second top-level castGroup contains:
   - `<castItem>` with nested `<roleDesc>` — valid structure

---

### Revision Notes

**Core Concept:** XSD validation rules.

**XSD Occurrence Indicators:**

| Attribute | Meaning |
|-----------|---------|
| `minOccurs="0"` | Optional (can be absent) |
| `minOccurs="1"` | Required (default) |
| `maxOccurs="unbounded"` | Any number of occurrences |
| `maxOccurs="1"` | At most one (default) |

**XSD Compositors:**

| Element | Meaning |
|---------|---------|
| `<xs:sequence>` | Elements must appear in order |
| `<xs:choice>` | One of the options must appear |
| `<xs:all>` | All must appear, any order |

---

## Question 3(c) [7 marks]

### (i) What is this file and what is it for? [2 marks]

**Answer:** This is an **XSLT (Extensible Stylesheet Language Transformations)** file.

**Purpose:**
- Transforms XML documents into other formats (HTML, text, different XML)
- Uses template matching to process XML nodes
- Here, it transforms TEI cast list into HTML (`<div>`, `<dt>`, `<dd>`)

---

### (ii) This fragment won't work. What is missing from the match attributes? [2 marks]

**Answer:** The **namespace prefix** is missing.

The XML uses namespace `xmlns="http://www.tei-c.org/ns/1.0"`, so XSLT must either:
1. Declare and use the namespace prefix:
   ```xml
   <xsl:template match="tei:castItem">
   <xsl:template match="tei:role/tei:name">
   <xsl:template match="tei:roleDesc">
   ```
2. Or use wildcard namespace:
   ```xml
   <xsl:template match="*:castItem">
   ```

---

### (iii) What will be the format and content of the output? [3 marks]

**Answer:**

**Format:** HTML

**Content:** A definition list structure:
```html
<div>
    <dt>Hermia</dt>
</div>
<div>
    <dt>Lysander</dt>
</div>
<div>
    <dt>Helena</dt>
</div>
<div>
    <dt>Demetrius</dt>
</div>
<div>
    <dt>Theseus</dt>
    <dd>duke of Athens</dd>
</div>
```

**Explanation:**
- `castItem` → wrapped in `<div>`
- `role/name` → wrapped in `<dt>` (definition term)
- `roleDesc` → wrapped in `<dd>` (definition description)

---

## Question 3(d) [11 marks]

### (i) What tables would you use to represent this cast information? [6 marks]

**Answer:**

| Table | Primary Key | Other Columns | Foreign Keys |
|-------|-------------|---------------|--------------|
| **Plays** | PlayId | Title | - |
| **CastGroups** | GroupId | GroupName, PlayId, ParentGroupId | PlayId → Plays, ParentGroupId → CastGroups |
| **Roles** | RoleId | Name, GroupId, Description | GroupId → CastGroups |

**CREATE TABLE statements:**

```sql
CREATE TABLE Plays (
    PlayId VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(200)
);

CREATE TABLE CastGroups (
    GroupId VARCHAR(50) PRIMARY KEY,
    GroupName VARCHAR(100),
    PlayId VARCHAR(50),
    ParentGroupId VARCHAR(50),
    FOREIGN KEY (PlayId) REFERENCES Plays(PlayId),
    FOREIGN KEY (ParentGroupId) REFERENCES CastGroups(GroupId)
);

CREATE TABLE Roles (
    RoleId VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(100),
    Description VARCHAR(500),
    GroupId VARCHAR(50),
    FOREIGN KEY (GroupId) REFERENCES CastGroups(GroupId)
);
```

---

### (ii) Which works better here, relational or XML? [5 marks]

**Answer:** **XML works better** for this specific use case.

**Reasons XML is Better:**

| Aspect | XML Advantage |
|--------|---------------|
| **Hierarchical nature** | Cast lists are naturally nested (groups within groups) |
| **Mixed content** | Roles can have both name AND description text |
| **Document-centric** | This is essentially a document, not transactional data |
| **Existing standards** | TEI is an established standard for theatrical texts |
| **Transformation** | XSLT easily converts to HTML for display |

**Where Relational Would Be Better:**
- Large-scale querying ("How many roles across all Shakespeare plays?")
- Transactional updates
- Joining with other data (actor information, performance dates)

**Conclusion:** For display and document management, XML is ideal. For analytical queries across many plays, relational would be better.

---

# Question 4: Recipe Database [30 marks]

## E/R Diagram from Exam

```
RecipeBook ──Contains──> Recipe ──uses──> Ingredient
    │                      │
  Author                preparedBy
  Title                    │
                           ▼
                    PreparationStep
                         │
                       Action
```

---

## Question 4(a) [4 marks]

**Question:** Is there anything missing from this model?

---

### Answer

**Missing elements:**

| Missing | Why Needed |
|---------|------------|
| **Quantity for ingredients** | "Uses" needs amount (e.g., "2 cups flour") |
| **Step ordering** | PreparationSteps need a sequence number |
| **Recipe name** | The Recipe entity needs a Name attribute |
| **Unique identifiers** | Need PKs beyond just names (RecipeId, etc.) |

**Improved attributes:**

- **Recipe:** RecipeId (PK), Name
- **Uses relationship:** Quantity, Unit
- **PreparationStep:** StepNumber
- **Ingredient:** IngredientId (PK), Name

---

### Revision Notes

**Core Concept:** E/R diagrams should capture all necessary data.

**Questions to Ask:**
1. Can we identify each entity uniquely?
2. Do relationships need attributes?
3. Is ordering required for any collections?
4. What questions does the website need to answer?

---

## Question 4(b) [3 marks]

**Question:** What is the cardinality of the three relationships?

---

### Answer

| Relationship | Cardinality | Explanation |
|--------------|-------------|-------------|
| **Contains** (RecipeBook-Recipe) | M:N | A book has many recipes; a recipe can appear in multiple books |
| **Uses** (Recipe-Ingredient) | M:N | A recipe uses many ingredients; an ingredient is used in many recipes |
| **PreparedBy** (Recipe-PreparationStep) | 1:M | A recipe has many steps; a step belongs to one recipe |

---

### Revision Notes

**Core Concept:** Cardinality describes how many entities can be related.

**Notation:**

| Symbol | Meaning |
|--------|---------|
| 1:1 | One to one |
| 1:M | One to many |
| M:N | Many to many |

**M:N Requires Junction Table:**
```
Recipe ──M:N── Ingredient
    ↓
RecipeIngredient (junction table)
```

---

## Question 4(c) [10 marks]

**Question:** Give MySQL CREATE TABLE commands for TWO tables.

---

### Answer

**Table 1: Recipes**

```sql
CREATE TABLE Recipes (
    RecipeId INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(200) NOT NULL
);
```

**Table 2: RecipeIngredients (junction table with quantity)**

```sql
CREATE TABLE RecipeIngredients (
    RecipeId INT,
    IngredientId INT,
    Quantity DECIMAL(10,2),
    Unit VARCHAR(50),
    PRIMARY KEY (RecipeId, IngredientId),
    FOREIGN KEY (RecipeId) REFERENCES Recipes(RecipeId),
    FOREIGN KEY (IngredientId) REFERENCES Ingredients(IngredientId)
);
```

**Alternative: PreparationSteps**

```sql
CREATE TABLE PreparationSteps (
    StepId INT AUTO_INCREMENT PRIMARY KEY,
    RecipeId INT NOT NULL,
    StepNumber INT NOT NULL,
    Action TEXT NOT NULL,
    FOREIGN KEY (RecipeId) REFERENCES Recipes(RecipeId),
    UNIQUE (RecipeId, StepNumber)
);
```

**Alternative: RecipeBooks**

```sql
CREATE TABLE RecipeBooks (
    BookId INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    Author VARCHAR(100)
);
```

---

## Question 4(d) [4 marks]

**Question:** Find all recipe books which never use butter.

---

### Answer

```sql
SELECT RB.Title
FROM RecipeBooks RB
WHERE RB.BookId NOT IN (
    SELECT DISTINCT BC.BookId
    FROM BookContains BC
    INNER JOIN RecipeIngredients RI ON BC.RecipeId = RI.RecipeId
    INNER JOIN Ingredients I ON RI.IngredientId = I.IngredientId
    WHERE I.Name = 'butter'
);
```

**Alternative using LEFT JOIN:**

```sql
SELECT DISTINCT RB.Title
FROM RecipeBooks RB
LEFT JOIN (
    SELECT BC.BookId
    FROM BookContains BC
    INNER JOIN RecipeIngredients RI ON BC.RecipeId = RI.RecipeId
    INNER JOIN Ingredients I ON RI.IngredientId = I.IngredientId
    WHERE I.Name = 'butter'
) ButterBooks ON RB.BookId = ButterBooks.BookId
WHERE ButterBooks.BookId IS NULL;
```

---

### Revision Notes

**Core Concept:** Finding records that DON'T match a condition.

**Patterns for "NOT EXISTS":**

| Approach | SQL Pattern |
|----------|-------------|
| `NOT IN` | `WHERE Id NOT IN (SELECT ...)` |
| `LEFT JOIN ... IS NULL` | Join then filter for NULL |
| `NOT EXISTS` | `WHERE NOT EXISTS (SELECT ...)` |

---

## Question 4(e) [4 marks]

**Question:** Find the average number of steps in the recipe book called "Mushrooms" by "John Cage".

---

### Answer

```sql
SELECT AVG(StepCount) AS AvgSteps
FROM (
    SELECT R.RecipeId, COUNT(PS.StepId) AS StepCount
    FROM RecipeBooks RB
    INNER JOIN BookContains BC ON RB.BookId = BC.BookId
    INNER JOIN Recipes R ON BC.RecipeId = R.RecipeId
    INNER JOIN PreparationSteps PS ON R.RecipeId = PS.RecipeId
    WHERE RB.Title = 'Mushrooms' AND RB.Author = 'John Cage'
    GROUP BY R.RecipeId
) AS RecipeStepCounts;
```

**Alternative (if counting directly):**

```sql
SELECT COUNT(PS.StepId) / COUNT(DISTINCT R.RecipeId) AS AvgSteps
FROM RecipeBooks RB
INNER JOIN BookContains BC ON RB.BookId = BC.BookId
INNER JOIN Recipes R ON BC.RecipeId = R.RecipeId
INNER JOIN PreparationSteps PS ON R.RecipeId = PS.RecipeId
WHERE RB.Title = 'Mushrooms' AND RB.Author = 'John Cage';
```

---

## Question 4(f) [5 marks]

**Question:** Consider ONE technology and indicate whether it would be more suitable. Choose from: MongoDB, XML, or Linked Data.

---

### Answer (MongoDB)

**Would MongoDB be more suitable?** Partially yes, for certain aspects.

**Advantages of MongoDB for Recipes:**

| Aspect | Benefit |
|--------|---------|
| **Document structure** | Recipe as single document with embedded steps and ingredients |
| **Flexible schema** | Different recipes can have different fields |
| **Nested arrays** | Ingredients and steps naturally fit as arrays |
| **Read performance** | Single document retrieval (no JOINs) |

**Example MongoDB Document:**
```json
{
  "_id": "carbonara",
  "name": "Spaghetti Carbonara",
  "ingredients": [
    {"name": "spaghetti", "quantity": 400, "unit": "g"},
    {"name": "guanciale", "quantity": 200, "unit": "g"}
  ],
  "steps": [
    {"order": 1, "action": "Boil pasta"},
    {"order": 2, "action": "Fry guanciale"}
  ],
  "books": ["Italian Classics", "Quick Dinners"]
}
```

**Disadvantages:**

| Aspect | Problem |
|--------|---------|
| **Cross-collection queries** | "All books with butter" requires scanning |
| **Data duplication** | Ingredient info repeated across recipes |
| **Referential integrity** | No enforced foreign keys |

**Conclusion:** MongoDB works well if recipes are primarily read as whole documents. Relational is better for complex cross-recipe analytics (e.g., "most common ingredient across all books").

---

### Alternative Answer (Linked Data)

**Would Linked Data be more suitable?** For a public web resource, yes.

**Advantages:**

| Aspect | Benefit |
|--------|---------|
| **Standard vocabularies** | schema.org/Recipe already exists |
| **Linking** | Connect to Wikidata for ingredient nutrition |
| **Interoperability** | Other sites can query your data |
| **SEO** | Search engines understand structured recipes |

**Example in schema.org:**
```turtle
<#carbonara> a schema:Recipe ;
    schema:name "Spaghetti Carbonara" ;
    schema:recipeIngredient "400g spaghetti" ;
    schema:recipeInstructions "Boil pasta..." .
```

**Disadvantage:** More complex to implement than relational for a simple website.

---

# Quick Reference Summary

## SQL JOIN Types

```sql
-- LEFT JOIN: Keep all left rows, NULL for unmatched right
SELECT * FROM Books LEFT JOIN Authors ON Books.AuthorId = Authors.Id;

-- INNER JOIN: Only matched rows
SELECT * FROM Books INNER JOIN Authors ON Books.AuthorId = Authors.Id;
```

## Transaction Control

```sql
START TRANSACTION;
-- operations...
COMMIT;    -- or ROLLBACK;
```

## MongoDB Regex

```javascript
db.collection.find({ field: /pattern/ })
// /*text/ = ends with "text"
// /^text/ = starts with "text"
// /text/ = contains "text"
```

## XPath Essentials

```xpath
//element           -- Find anywhere
//parent/child      -- Direct child of parent
//element[@attr]    -- Element with attribute
//element[@attr="val"] -- Attribute equals value
```

## SPARQL Variables

```sparql
SELECT ?variable    -- Variable in SELECT
WHERE {
  ?variable pred obj .  -- Same variable in WHERE
}
```

---

*End of Solution Sheet - Mock March 2021*
