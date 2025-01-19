
---

# **Question 2: Bird Spotter’s Records in MySQL Database**

## **2(a)**

### **Question**
A sightings table in MySQL contains various bird sightings. **Write a query** to retrieve all distinct bird **Species** that have been seen **since January 1, 2021**.

### **Correct Answer**
```sql
SELECT DISTINCT Species
FROM Sightings
WHERE Date >= '2021-01-01';
```

---

### **Detailed Explanation**
- **Filtering by Date:** `WHERE Date >= '2021-01-01'` ensures only sightings from January 1, 2021 onward are returned.  
- **Eliminating Duplicates:** `SELECT DISTINCT` returns unique `Species`, preventing repeats.  
- **Standard Date Format:** In SQL, `YYYY-MM-DD` is the usual string format for dates, ensuring proper comparison logic.

### **Real-World Scenario Connection**
- **Conservation Tracking:** If a bird-watching society wants to see which **new** bird species have shown up this year, they can run a query like this to see distinct species after a certain date. This helps biologists track migrations or changes in habitat usage.

### **Edge Cases / “What If?”**
- **What if** the table columns are named differently (e.g. `BirdSpecies`)? Adjust the query accordingly.  
- **What if** you want *all columns* for sightings? You’d omit `DISTINCT` or use `SELECT *`.

### **DIY Exploration**
- **Try** removing `DISTINCT` to see how many total sightings there are (with duplicates).  
- **Try** a different date range (e.g. `WHERE Date BETWEEN '2021-01-01' AND '2021-06-30'`).

### **Key Terms**
- **`SELECT DISTINCT`:** Returns unique values from a column.  
- **Date Comparison:** Uses standard `'YYYY-MM-DD'` format in SQL.

### **Common Pitfalls**
- **Forgetting `DISTINCT`:** Results in repeated species.  
- **Incorrect Date Format:** `'2021-1-1'` (missing zero) can sometimes cause issues or different interpretations.

### **Key Takeaways**
- Date filtering + `DISTINCT` is a **fundamental** SQL pattern to isolate unique entries within a time window.

---

## **2(b)**

### **Question**
**Is the sightings table in 1NF (First Normal Form)?** Explain your reasoning.

### **Correct Answer**
Yes, it **is** in 1NF.

---

### **Detailed Explanation**
- **1NF Requirements:** All columns contain **atomic** values, and no column has repeated groups or arrays.  
- **Evaluating Table Structure:** Each row in the sightings table presumably has a single `Species`, a single `Date`, and a single integer or numeric `NumberSighted`. None of these are multi-valued; hence it meets 1NF.

### **Real-World Scenario Connection**
- **Basic Data Integrity:** 1NF ensures every column has one piece of data. In a spreadsheet of sightings, you don’t want columns containing “multiple species” or “mixed data formats.”

### **Edge Cases / “What If?”**
- **What if** the table had a field like `MultipleSpeciesSighted` with comma-separated species? That would violate 1NF.

### **DIY Exploration**
- **Check** your own database tables for multi-valued columns (like “tags” or “categories” in one field). Such designs break 1NF and complicate queries.

### **Key Terms**
- **1NF:** Each cell is atomic, no repeating groups, consistent data type in each column.

### **Common Pitfalls**
- **Storing Lists** in a single field (like `Species = "crow, robin"`). This breaks 1NF.

### **Key Takeaways**
- 1NF is the **foundation** for normalization. Ensuring columns have single (atomic) values simplifies queries and updates.

---

## **2(c)**

### **Question**
**Normalize** the sightings data. **List** the tables, their primary keys, and foreign keys after normalization.

### **Correct Answer (Example 3NF Design)**
1. **Species**  
   - **PK:** `SpeciesName`  
   - Attributes: `ConservationStatus`

2. **NatureReserves**  
   - **PK:** `NatureReserave`  
   - Attributes: `Location`

3. **Sightings**  
   - **PK:** (`SpeciesName`, `NatureReserve`, `Date`)  
   - Attributes: `NumberSighted`  
   - **Foreign Keys:**  
     - `SpeciesName` → **references** Species(`SpeciesName`)  
     - `NatureReserve` → **references** NatureReserves(`NatureReserve`)

---

### **Detailed Explanation**
- **Breaking Out Species:** Repeated fields about conservation status belong in a separate `Species` table.  
- **Handling Locations:** Repeated location data (nature reserve names, lat/long) belong in a `NatureReserves` table.  
- **Sightings Table:** Links `Species` and `NatureReserve` via FKs and stores date and number sighted.

### **Real-World Scenario Connection**
- **Database Efficiency:** By **removing redundancy**, updates become easier. If a species’ conservation status changes, you only update one table, not every sightings row.

### **Edge Cases / “What If?”**
- **What if** you also want to track bird watchers’ info? You might add a `User` or `Observer` table, linking them via an ID.

### **DIY Exploration**
- **Try** writing the actual `CREATE TABLE` statements for each table. Ensure you define PK/FK constraints properly.

### **Key Terms**
- **3NF:** Third Normal Form eliminates transitive dependencies—every non-key attribute depends only on the table’s primary key.  
- **Functional Dependencies:** The relationships that define which columns depend on which keys.

### **Common Pitfalls**
- **Leaving Redundant Data** in a single table, leading to data anomalies.  
- **Not Defining** foreign keys—losing referential integrity.

### **Key Takeaways**
- Proper normalization (to at least 3NF) **reduces data redundancy** and **improves consistency** in relational databases.

---

## **2(d)**

### **Question**
**What normal form** have we **reached**? **Explain** your conclusion.

### **Correct Answer**
3NF (Third Normal Form).

---

### **Detailed Explanation**
- **Why 3NF?:**  
  1. Already in 2NF (no partial dependencies on a composite key).  
  2. **No transitive dependencies** (attributes depending on other non-key attributes).  
  3. Each non-key attribute depends on the table’s primary key only.

### **Real-World Scenario Connection**
- **Business Databases:** Most enterprise systems aim for 3NF to avoid anomalies and keep queries performant.

### **Edge Cases / “What If?”**
- **If** there were extra columns that indirectly depended on something else (like an attribute that depends on `ConservationStatus`), that might break 3NF.

### **DIY Exploration**
- **Try** verifying each table’s dependencies with “Dependency Diagrams” to confirm no transitive dependencies remain.

### **Key Terms**
- **Transitive Dependency:** A non-key attribute depends on another non-key attribute, which depends on the key.

### **Common Pitfalls**
- **Confusing 2NF & 3NF:** 2NF addresses partial dependencies (only relevant if you have a composite primary key); 3NF addresses transitive dependencies.

### **Key Takeaways**
- Reaching 3NF typically **satisfies** most real-world use cases: data is well-structured, with minimal redundancy.

---

## **2(e)**

### **Question**
Given your **new tables**, write a **SQL query** to retrieve **bird types (SpeciesName) and their ConservationStatus** for sightings **since January 1, 2021**.

### **Correct Answer**
```sql
SELECT s.SpeciesName, sp.ConservationStatus
FROM Sightings s
JOIN Species sp ON s.SpeciesName = sp.SpeciesName
WHERE s.Date >= '2021-01-01';
```

---

### **Detailed Explanation**
- **Joining Tables:** `Sightings` → `Species` on the shared `SpeciesName`.  
- **Date Filter:** `s.Date >= '2021-01-01'` selects only sightings from 2021 onwards.  
- **Selecting Relevant Fields:** We want the species name and conservation status. The join ensures these fields come together.

### **Real-World Scenario Connection**
- **Conservation Monitoring:** Quickly see which species are being sighted in a certain period along with their conservation statuses, enabling targeted research or protection measures.

### **Edge Cases / “What If?”**
- **What if** some sightings have `SpeciesName` not in `Species` table? A standard `JOIN` would exclude them. A `LEFT JOIN` might be needed if you want to see sightings even if the species table is missing records.

### **DIY Exploration**
- **Try** adding `ORDER BY sp.ConservationStatus` to organize by status.  
- **Try** counting how many sightings each species has, e.g. `COUNT(*)`.

### **Key Terms**
- **Inner Join:** Only rows with matching keys in both tables appear.

### **Common Pitfalls**
- **Omitting a Join Condition:** Could produce a **CROSS JOIN** with unintentional results.

### **Key Takeaways**
- Knowing how to properly **JOIN** in SQL is crucial for retrieving information spread across multiple normalized tables.

---

## **2(f)**

### **Question**
The bird spotter wants to ensure their **next set of updates** is **consistent**. **Would a transaction help?** Illustrate with example SQL.

### **Correct Answer**
Yes. **Transactions** ensure data integrity for multiple statements. For example:

```sql
START TRANSACTION;

INSERT INTO Sightings (SpeciesName, Date, NumberSighted, NatureReserve)
VALUES ('Wood pigeon', '2021-09-07', 5, 'Epping Forest');

UPDATE Species
SET ConservationStatus = 'Endangered'
WHERE SpeciesName = 'Wood pigeon';

COMMIT;
```

---

### **Detailed Explanation**
- **Atomicity:** If any statement fails, you can `ROLLBACK`, preventing partial updates.  
- **Consistency:** The bird spotter’s data remains consistent—no record will show a bird without also updating its conservation status or vice versa.  
- **Commit & Rollback:** `COMMIT` finalizes changes; `ROLLBACK` undoes them.

### **Real-World Scenario Connection**
- **Financial Systems:** A transfer from Account A to B must **either** debit A and credit B **together** or do neither. Similarly, for multiple related bird updates, you don’t want partial changes.

### **Edge Cases / “What If?”**
- **What if** the second statement fails? If you **haven’t** committed, you can `ROLLBACK` to revert the first insert as well.

### **DIY Exploration**
- **Try** intentionally causing an error in the middle of a transaction to see how `ROLLBACK` works.

### **Key Terms**
- **Transaction:** A group of one or more SQL statements treated as a single unit.  
- **ACID properties:** Atomicity, Consistency, Isolation, Durability.

### **Common Pitfalls**
- **Forgetting `COMMIT`:** Leaves changes uncommitted, so they might roll back automatically or remain invisible to other sessions.

### **Key Takeaways**
- Transactions are **essential** when multiple data manipulations must succeed or fail together, protecting data consistency.

---

# **Question 3: Exploring Music Encoding with MEI and Linked Data Models**

## **3(a)**

### **Question**
Look at the MEI (Music Encoding Initiative) code. **List all the element types** visible in the snippet.

### **Correct Answer**
1. `<measure>`  
2. `<staff>`  
3. `<layer>`  
4. `<chord>`  
5. `<note>`

---

### **Detailed Explanation**
- **MEI Hierarchy:** Each `<measure>` can contain multiple `<staff>` elements. Each `<staff>` can have one or more `<layer>` elements, which in turn contain `<chord>` or `<note>`.  
- **Chord vs. Note:** A `<chord>` can hold multiple `<note>` elements simultaneously sounding, whereas a `<note>` is usually a single pitch event.

### **Real-World Scenario Connection**
- **Digital Sheet Music:** Programs like MuseScore or Verovio may use MEI-like structures to represent measures, staves, layers, and chords.

### **Edge Cases / “What If?”**
- **What if** some music passages only have single notes (no chords)? Then `<chord>` might be absent, and `<note>` stands alone.

### **DIY Exploration**
- **Try** finding or creating a small MEI file with multi-staff music. Observe how `<staff>` and `<layer>` nest.

### **Key Terms**
- **MEI:** Music Encoding Initiative, an XML schema for musical scores.  
- **Measure, Staff, Layer:** Reflect standard musical concepts.

### **Common Pitfalls**
- **Missing Opening/Closing Tags:** In MEI, each container must properly nest elements.

### **Key Takeaways**
- Understanding these elements is crucial for manipulating or querying digital music notation.

---

## **3(b)**

### **Question**
You want **all chords** in the staff `n="2"` (right hand) that **contain notes** with `pname="f"`. Your initial XPath was incorrect. **Give a correct XPath**.

### **Correct Answer**
```xpath
//staff[@n="2"]/layer/chord[note[@pname="f"]]
```

---

### **Detailed Explanation**
- **Selecting Staff with `@n="2"`:** `[ @n="2" ]` is an **attribute** filter, not a positional predicate.  
- **Filtering Chords with a Note** `@pname="f"`: Inside `chord`, you look for `note[@pname="f"]`.

### **Real-World Scenario Connection**
- **XML Queries in Music Apps:** In a complex score, you might want to isolate chords that contain specific pitches in specific staves (like right-hand piano staff).

### **Edge Cases / “What If?”**
- **What if** you wanted chords with *all* notes = f? You’d need a different expression or logic. This expression finds *any* chord that has at least one note with `pname="f"`.

### **DIY Exploration**
- **Try** modifying your XPath to find chords with `pname="c"` or to locate notes in staff `n="1"` (left hand).

### **Key Terms**
- **XPath:** A language to navigate XML trees.  
- **Attribute Selector:** `[@attrName="value"]`.

### **Common Pitfalls**
- **Confusing** `[n="2"]` (positional index) with `[ @n="2" ]` (attribute filter).  
- **Missing the `//staff`** slash patterns can lose scope or produce empty results.

### **Key Takeaways**
- Correctly filtering by **attributes** in XPath is crucial for precisely retrieving elements in structured XML documents.

---

## **3(c)**

### **Question**
A group is moving the MEI data into MongoDB.  

**(i) Translate** the **first chord** element into **JSON**.  
**(ii)** Given the **whole data** as an array of chords, write a **MongoDB find** that returns chords with an **“up” stem** containing **f** in at least one note.

---

### **(i) Correct Answer (JSON Translation)**
```json
{
  "chord": {
    "xml:id": "d13e1",
    "dur": 8,
    "dur.ppq": 12,
    "stem.dir": "up",
    "notes": [
      { "xml:id": "d1e101", "pname": "c", "oct": 5 },
      { "xml:id": "d1e118", "pname": "a", "oct": 4 },
      { "xml:id": "d1e136", "pname": "c", "oct": 4 }
    ]
  }
}
```

#### **Detailed Explanation (for JSON)**
- **Hierarchical to JSON:** The `<chord>` attributes become key-value pairs (e.g. `"dur": 8`).  
- **Notes as Array:** Each `<note>` is an object in the `notes` array, preserving multiple pitches.

#### **Real-World Scenario Connection**
- Many **NoSQL** or modern web applications store nested data in JSON format (e.g., music apps, e-commerce catalogs).

#### **Edge Cases**
- **What if** a chord has no notes? Then `"notes": []`.

#### **DIY Exploration**
- **Try** adding extra chord attributes or note attributes (like `stem.dir`, `accid` for accidentals).

#### **Key Terms**
- **JSON:** JavaScript Object Notation, flexible for nested data.

#### **Common Pitfalls**
- **Missing Quotes** around object keys or values can break JSON parsing.

#### **Key Takeaways**
- Properly preserving hierarchical structure in JSON ensures data is **intact** when transitioning from XML to NoSQL.

---

### **(ii) Correct Answer (MongoDB Find)**
```js
db.chords.find({
  "stem.dir": "up",
  "notes.pname": "f"
})
```
or
```js
db.chords.find({
  "stem.dir": "up",
  "notes": {
    "$elemMatch": { "pname": "f" }
  }
})
```

Here is an updated explanation to cover **both** approaches—matching array elements via **dot notation** (`"notes.pname": "f"`) or **`$elemMatch`**:

---

#### **Detailed Explanation (MongoDB Query)**

1. **Filtering on “stem.dir”:**  
   We include `{"stem.dir": "up"}` to return only chords whose field `stem.dir` is exactly `"up"`.

2. **Matching Notes Containing `"pname":"f"`**  
   MongoDB offers **two** common ways to match array sub-documents:

   - **Dot-Notation Match**  
     ```js
     db.chords.find({
       "stem.dir": "up",
       "notes.pname": "f"
     })
     ```
     Using `"notes.pname": "f"` tells Mongo to look in the `notes` array for at least one sub-document where `pname` equals `"f"`. This implicitly does an “array contains an object with that key-value pair” check.

   - **`$elemMatch`**  
     ```js
     db.chords.find({
       "stem.dir": "up",
       "notes": {
         "$elemMatch": { "pname": "f" }
       }
     })
     ```
     Here, `$elemMatch` explicitly says: “Return documents where **at least one** array element in `notes` meets the condition `pname` = `"f"`.”  

   **When to Use Which**  
   - For a **single** condition, either style works fine.  
   - If you have **multiple** conditions that must apply **to the same element** in the array, `$elemMatch` is necessary. For example, `"$elemMatch": { "pname": "f", "oct": "3" }` ensures both conditions refer to the same array entry.

These queries find **chords** with:

- `stem.dir` = `"up"`  
- **At least one** note whose `"pname"` is `"f"`.

Either **dot notation** or **`$elemMatch`** achieves the “notes contain a sub-document with `pname: 'f'`” logic.

#### **Real-World Scenario Connection**
- **Music Information Retrieval:** Searching for chords with upward stems that contain a particular pitch is straightforward in MongoDB’s document model.

#### **Edge Cases**
- **What if** you only want chords where *all* notes have `pname="f"`? You’d need a different query, e.g. `"$all"` approach or `$elemMatch` with more constraints.

#### **DIY Exploration**
- **Try** adding more filters, like `dur: 8`, or searching for chords with multiple pitch names.

#### **Key Terms**
- **$elemMatch**: MongoDB operator that finds array elements matching specific criteria.

#### **Common Pitfalls**
- **Forgetting** `$elemMatch` when you need to match array contents.

#### **Key Takeaways**
- MongoDB’s array operators enable **flexible** queries for data that’s naturally nested (like chords/notes).

---

## **3(d): Linked Data SPARQL Query**

### **Question**
We have a SPARQL query to find chords containing an `F`.  

**(i)** Why use `rdfs:member` instead of a custom property like `mei:hasNotes`?  
**(ii)** Provide some RDF for the first chord element (in any serialization).

---

### **(i) Correct Answer**
Using **`rdfs:member`** leverages **existing** W3C standards, **maximizing interoperability** with other linked data. We avoid defining a **new** property like `mei:hasNotes` that may duplicate a standard concept.

#### **Detailed Explanation**
- **Interoperability:** Reusing a property like `rdfs:member` means other linked-data tools and vocabularies can understand it right away.  
- **Less Redundancy:** If `rdfs:member` serves the same semantic function (“this chord has these notes”), no need for a custom property.

#### **Real-World Scenario Connection**
- **Semantic Web**: Reusing established vocabularies (like RDF Schema, OWL) helps data from different domains mesh more easily.

#### **Edge Cases**
- **What if** we need more specialized relationships? We might define a specialized property only if no standard property fits.

#### **DIY Exploration**
- **Try** exploring other RDF vocabularies (e.g. `schema.org`, `foaf`) to see how they can also reduce custom definitions.

#### **Key Terms**
- **`rdfs:member`:** A generic property for membership relationships in RDF.

#### **Common Pitfalls**
- **Overdefining** new properties leads to “ontology bloat” and hinders data reuse.

#### **Key Takeaways**
- Always check existing vocabularies before inventing new properties, to remain consistent and interoperable.

---

### **(ii) Correct Answer (Turtle Example)**

```turtle
@prefix mei: <http://example.org/mei#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://example.org/chord/d13e1> a mei:Chord ;
  mei:duration "8" ;
  mei:durationPpq "12" ;
  mei:stemDirection "up" ;
  rdfs:member <http://example.org/note/d1e101>,
              <http://example.org/note/d1e118>,
              <http://example.org/note/d1e136> .

<http://example.org/note/d1e101> a mei:Note ;
  mei:pitchName "c" ;
  mei:octave "5" .

<http://example.org/note/d1e118> a mei:Note ;
  mei:pitchName "a" ;
  mei:octave "4" .

<http://example.org/note/d1e136> a mei:Note ;
  mei:pitchName "c" ;
  mei:octave "4" .
```

#### **Detailed Explanation**
- **RDF Resources:** Each chord and note is given a unique URI.  
- **Using `rdfs:member`:** Indicates that the chord “contains” those notes.  
- **mei:* Terms:** Custom namespace for music concepts (e.g., `mei:Note`, `mei:duration`).

#### **Real-World Scenario Connection**
- **Linked Data**: By providing URIs, your data can link to other resources—like a universal pitch class or a DBpedia entry for “B♭ Clarinet.”

#### **Edge Cases**
- **What if** you want to add chord inversions or key signatures? You’d define more properties or link to existing vocabularies.

#### **DIY Exploration**
- **Try** adding or reusing `schema:MusicComposition` or `schema:MusicEvent` from `schema.org` to see how standard vocabularies can integrate.

#### **Key Terms**
- **Turtle:** A compact RDF serialization format.  
- **URIs:** Global unique identifiers for RDF resources.

#### **Common Pitfalls**
- **Malformed RDF** (missing semicolons or periods) leads to parse errors.

#### **Key Takeaways**
- **RDF** in Turtle syntax elegantly captures structured relationships. Reusing standard properties (`rdfs:member`) fosters data integration.

---

# **Question 4: Designing a Zoo Database System**

## **4(a)**

### **Question**
**List the tables and their fields** for an SQL zoo design. **Indicate primary keys**.

### **Correct Answer (Example)**
1. **Zoo**  
   - PK: `ZooName`  
   - Fields: `Country`, `Location`

2. **Enclosure**  
   - PK: `EnclosureName`  
   - Fields: `ZooName` (FK → `Zoo.ZooName`), `Location`

3. **Animal**  
   - PK: `AnimalID`  
   - Fields: `Species`, `ConservationStatus`, `DateOfBirth`, `EnclosureName` (FK → `Enclosure.EnclosureName`)

4. **Species**  
   - PK: `SpeciesName`  
   - Fields: `LatinName`, `ConservationStatus`

---

### **Detailed Explanation**
- **Zoo ↔ Enclosure:** 1 zoo can have multiple enclosures.  
- **Enclosure ↔ Animal:** 1 enclosure can house multiple animals.  
- **Species Table**: Avoid duplicating species details among many animals.

### **Real-World Scenario Connection**
- **Scalable Zoo Management:** Each enclosure references a zoo, ensuring no enclosure can exist without a corresponding zoo. This structure is typical in any hierarchical entity system (e.g., warehouses & sections).

### **Edge Cases**
- **What if** an enclosure has no animals currently? The table design still accommodates that (the enclosure record just has 0 animals referencing it).

### **DIY Exploration**
- **Try** adding a `Keeper` table for staff who manage certain animals or enclosures, introducing more foreign keys.

### **Key Terms**
- **Primary Key (PK):** Unique identifier for each row.  
- **Foreign Key (FK):** A reference to another table’s PK to maintain relationships.

### **Common Pitfalls**
- **Omitting** foreign keys, which can lead to orphan records or lost references.

### **Key Takeaways**
- Proper **entity-relationship** modeling ensures a logical, consistent, and scalable database.

---

## **4(b)**

### **Question**
Give **SQL `CREATE TABLE` commands** for **any TWO** of your tables, including foreign keys.

### **Correct Answer (Example)**
```sql
CREATE TABLE Zoo (
  ZooName VARCHAR(255) PRIMARY KEY,
  Country VARCHAR(255),
  Location VARCHAR(255)
);

CREATE TABLE Enclosure (
  EnclosureName VARCHAR(255) PRIMARY KEY,
  ZooName VARCHAR(255),
  Location VARCHAR(255),
  FOREIGN KEY (ZooName) REFERENCES Zoo(ZooName)
);
```

---

### **Detailed Explanation**
- **Defining PK:** `PRIMARY KEY` on `ZooName` or `EnclosureName`.  
- **Foreign Key Constraint:** `FOREIGN KEY (ZooName) REFERENCES Zoo(ZooName)` ensures each enclosure references a valid zoo.

### **Real-World Scenario Connection**
- **Data Integrity:** If an admin tries to insert an enclosure for a non-existent zoo, this statement would reject it, preserving referential integrity.

### **Edge Cases**
- **What if** you want cascading deletes (removing a zoo removes all enclosures)? Then add `ON DELETE CASCADE`.

### **DIY Exploration**
- **Try** creating the `Animal` or `Species` tables yourself with a similar structure.

### **Key Terms**
- **Referential Integrity:** Ensures linked data remains consistent.

### **Common Pitfalls**
- **Mismatch** in data types between foreign key and primary key columns (e.g., `VARCHAR(255)` vs. `INT`).

### **Key Takeaways**
- Correct usage of **PK** and **FK** in `CREATE TABLE` statements is crucial for relational databases.

---

## **4(c)**

### **Question**
Write a single SQL query to find **how many species** are housed in the **zoo named ‘Singapore Zoo’**.

### **Correct Answer**
```sql
SELECT COUNT(DISTINCT s.SpeciesName) AS SpeciesCount
FROM Animal a
JOIN Enclosure e ON a.EnclosureName = e.EnclosureName
JOIN Zoo z ON e.ZooName = z.ZooName
JOIN Species s ON a.Species = s.SpeciesName
WHERE z.ZooName = 'Singapore Zoo';
```

---

### **Detailed Explanation**
- **Table Joins:**  
  1. `Animal` → `Enclosure` on `EnclosureName`.  
  2. `Enclosure` → `Zoo` on `ZooName`.  
  3. `Animal` → `Species` on `SpeciesName`.  
- **Filtering by Zoo:** `WHERE z.ZooName = 'Singapore Zoo'`.  
- **Counting Distinct Species:** `COUNT(DISTINCT …)` ensures each species is only counted once.

### **Real-World Scenario Connection**
- **Inventory / Catalog Counting:** This pattern is common in **any** scenario where you count unique items in a specific location.

### **Edge Cases**
- **What if** the zoo has no animals? Then the query returns `0`.

### **DIY Exploration**
- **Try** grouping by `z.ZooName` to see how many species are in **each** zoo, if your DB has multiple zoos.

### **Key Terms**
- **Aggregate Functions (COUNT) + DISTINCT**: Summarize or count unique items.

### **Common Pitfalls**
- **Forgetting `DISTINCT`:** Could overcount species if multiple animals in the same species exist.

### **Key Takeaways**
- Combining **JOIN** + `COUNT(DISTINCT...)` is a staple pattern in relational SQL queries for unique item counts.

---

## **4(d)**

### **Question**
Write a single SQL query to find the **date of birth** of the **oldest animal** of the species called `'Buceros bicornis'` in **each zoo**.

### **Correct Answer**
```sql
SELECT z.ZooName, MIN(a.DateOfBirth) AS OldestDateOfBirth
FROM Animal a
JOIN Enclosure e ON a.EnclosureName = e.EnclosureName
JOIN Zoo z ON e.ZooName = z.ZooName
WHERE a.Species = 'Buceros bicornis'
GROUP BY z.ZooName;
```

---

### **Detailed Explanation**
- **Filtering by Species:** `'Buceros bicornis'`.  
- **Grouping by Zoo:** One row per zoo.  
- **Using `MIN(DateOfBirth)`:** Retrieves the **earliest** birth date (i.e., the oldest animal).

### **Real-World Scenario Connection**
- **Aggregation by Location:** In business or research, you often want the oldest, newest, or average among each group/branch.

### **Edge Cases**
- **What if** a zoo has no `'Buceros bicornis'` animals? That zoo might not appear in the result.

### **DIY Exploration**
- **Try** using `MAX` to find the **youngest** animal, or `COUNT` to see how many exist.

### **Key Terms**
- **GROUP BY:** Aggregates data by categories or groups (here, by zoo).

### **Common Pitfalls**
- **Forgetting `GROUP BY`:** SQL error or unintended results.

### **Key Takeaways**
- Aggregation functions (`MIN`, `MAX`, etc.) with `GROUP BY` allow analyzing data **within groups**.

---

## **4(e)**

### **Question**
Choose **ONE** of **XML** or **RDF** and:  
1. Assess the suitability of this zoo model for that technology.  
2. Give **instance data** covering most entities/attributes in that technology’s format.

---

### **(i) Correct Answer (Choosing RDF)**  
**Suitability:**  
- RDF is well-suited for describing **entities** (Zoo, Enclosure, Animal, Species) as **interlinked resources**.  
- Each resource can be assigned a **URI**, and relationships like “enclosure belongs to zoo” or “animal has species” can be expressed via **RDF properties**.  
- This approach **enhances interoperability**, allowing you to link out to other data sources (e.g., external conservation databases).

#### **Detailed Explanation**
- **Graph Nature:** The many-to-one or one-to-many relationships in the zoo scenario map nicely onto RDF’s subject–predicate–object triples.  
- **Integration:** If a zoo wants to link “Buceros bicornis” to an external ontology, RDF’s linked data approach is perfect.

#### **Real-World Scenario Connection**
- **Global Biodiversity Data:** Zoos might link their species to external conservation status resources (like the IUCN Red List) via URIs.

#### **Key Terms**
- **RDF:** Resource Description Framework, designed for the semantic web.  
- **URI:** Unique identifier for a resource.

#### **Common Pitfalls**
- **Reinventing properties** rather than using established ontologies (like `schema.org`, `FOAF`, etc.).

#### **Key Takeaways**
- RDF fosters an **open, interconnected** data ecosystem, ideal for knowledge sharing and integration.

---

### **(ii) Correct Answer (Turtle Example for Zoo Data)**
```turtle
@prefix zoo: <http://example.org/zoo#> .
@prefix schema: <http://schema.org/> .

zoo:SingaporeZoo a schema:Zoo ;
  schema:location "Singapore" ;
  schema:country "Singapore" .

zoo:Enclosure1 a schema:Enclosure ;
  schema:location "Tropical Rainforest" ;
  schema:zoo zoo:SingaporeZoo .

zoo:Animal1 a schema:Animal ;
  schema:species "Buceros bicornis" ;
  schema:dateOfBirth "2005-03-21" ;
  schema:enclosure zoo:Enclosure1 .

zoo:BucerosBicornis a schema:Species ;
  schema:latinName "Buceros bicornis" ;
  schema:conservationStatus "Vulnerable" .
```

#### **Detailed Explanation**
- **Assigning URIs:** `zoo:SingaporeZoo` references the zoo resource.  
- **Linking**: `schema:zoo zoo:SingaporeZoo` ties the enclosure to the Singapore Zoo.  
- **Reusing `schema:`** Instead of making new terms for “Animal” or “Species,” we leverage `schema.org` to keep it standard.

#### **Real-World Scenario Connection**
- **Semantic Web**: Allows for easy linking to other data sets or expansions (like adding caretaker info, global species references).

#### **Edge Cases**
- **What if** some animals are unknown species? You can still create an RDF resource with minimal info.

#### **DIY Exploration**
- **Try** referencing `dbpedia.org` or `wikidata.org` URIs for more official connections (like `foaf:Person` for zookeepers).

#### **Key Terms**
- **Turtle:** A concise, human-readable RDF serialization format.

#### **Common Pitfalls**
- **Forgetting** to maintain consistent URIs (leading to data fragmentation).

#### **Key Takeaways**
- By encoding zoo data in RDF, you create a flexible graph that can easily plug into broader **linked data** contexts.

---
