
# **Question 2**

## **Question 2(a)**
**Context**: The genealogical XML snippet includes `<royal>`, `<title>`, attributes like `rank="king"`, etc. We want two examples of element names and two examples of attribute names.

### **Answer**  
- **Element Names:**  
  1. `<royal>`  
  2. `<title>`  

- **Attribute Names:**  
  1. `rank`  
  2. `territory`  

### **Detailed Explanation & Real-World Scenario**  
- **Elements** are the fundamental containers in XML, defined by opening and closing tags. For example, `<royal>` might represent a person in the lineage.  
- **Attributes** appear in the start tag of an element (e.g., `<title rank="king" territory="England">`). They provide metadata, such as the `rank` or `territory` associated with a title.

**Common Pitfalls**  
- Mixing up elements and attributes. Elements are tags that can contain data or child elements, while attributes are key-value pairs inside an element’s start tag.

### **Exam Tip (Key Points Summary)**  
- **Elements**: `<royal>`, `<title>`  
- **Attributes**: `rank="..."`, `territory="..."`  
- Always distinguish **data** in elements vs. **metadata** in attributes.

---

## **Question 2(b)**
**Context**: An XPath query:
```xpath
//title[@rank="king" and @regnal="VIII"]/../royal[@name="Henry"]
```
We need to identify **which node** it selects in the genealogical XML.

### **Answer**  
It selects `<royal name="Henry" ...>` (often `<royal name="Henry" xml:id="HenryVIII">`) that is **sibling** to a `<title>` with `rank="king"` and `regnal="VIII"` (same parent).

### **Detailed Explanation & Real-World Scenario**  
- `//title[@rank="king" and @regnal="VIII"]` picks `<title>` elements that match both attributes.  
- `/..` moves up to the parent node (likely a `<royal>`).  
- Then `/royal[@name="Henry"]` selects a sibling `<royal>` with `name="Henry"`.  

**Practical Use**: In a family tree or genealogical data, you might look for a particular “Henry” associated with a specific title.

**Common Pitfalls**  
- Forgetting `..` in XPath can lead to selecting child or descendant nodes instead of siblings.

### **Exam Tip (Key Points Summary)**  
- **Logic**: Find `<title>` with `rank="king"` & `regnal="VIII"`, then go to parent, then to sibling `<royal name="Henry">`.  
- It effectively filters for Henry VIII in the same context as that specific title.

---

## **Question 2(c)**
**Context**: Another XPath:
```xpath
//title[@rank="king" or @rank="queen"]/../relationship/children/royal/relationship/children/royal/
```
We want to describe **which nodes** are returned.

### **Answer**  
It returns **descendant `<royal>` elements** that are accessed two levels down (`relationship -> children -> royal -> relationship -> children -> royal`) from any `<title>` with `rank="king"` or `rank="queen"`.

### **Detailed Explanation & Real-World Scenario**  
- `[ @rank="king" or @rank="queen" ]` means the title can be *either* king or queen.  
- `/../relationship/children/royal` steps from `<title>` up to the `<royal>` parent, then down through `<relationship>` and `<children>`.  
- You eventually reach `<royal>` nodes that might represent **descendants or further relationships** of those royals who are kings or queens.

**Common Pitfalls**  
- Using `or` in the XPath condition can broaden your selection unexpectedly if not intended.  
- The nested path is quite deep—any mismatch in the hierarchy (e.g., `<relationship>` spelled differently) leads to no matches.

### **Exam Tip (Key Points Summary)**  
- Returns **deeply nested** `<royal>` nodes for those with an ancestor `<title>` whose rank is `king` or `queen`.  
- Good for multi-generation or extended family queries.

---

## **Question 2(d)**
**Context**: We add Mary I’s Spanish consort info. Where to place it?

### **Answer**  
Under `<royal name="Mary">`, add:

```xml
<relationship type="marriage" spouse="#PhilipOfSpain" from="1556-01-16">
  <title rank="queen" territory="Spain" regnal="consort"
         from="1556-01-16" to="1558-11-17"/>
</relationship>
```

### **Detailed Explanation & Real-World Scenario**  
- This snippet shows Mary’s marriage relationship to Philip of Spain, with a nested `<title>` for her role as queen consort, including relevant dates.  
- **spouse="#PhilipOfSpain"** might reference another `<royal xml:id="PhilipOfSpain">` node, thus linking them.

**Common Pitfalls**  
- Placing it under the wrong `<royal>` would incorrectly associate that relationship.  
- Failing to close tags or set correct attributes (e.g., from date, to date).

### **Exam Tip (Key Points Summary)**  
- **Location**: Inside `<royal name="Mary">`.  
- **Structure**: `<relationship>` element plus nested `<title>` describing the consort rank & timeline.

---

## **Question 2(e)**
**Context**: Strengths/weaknesses of using **XML** for genealogical/historical data.

### **Answer**  
**Strengths**  
1. **Natural Hierarchy** – Genealogies have parent-child structures that align well with XML nesting.  
2. **Flexible & Self‐Descriptive** – Easy to insert new attributes, elements; `<relationship>`, `<children>` are intuitive.  
3. **Readable** – XML is relatively human‐readable.

**Weaknesses**  
1. **Verbosity** – Repeated tags can cause large file sizes.  
2. **Complex Queries** – Deeply nested data can be slow or cumbersome to query with XPath.  
3. **Scalability** – Maintaining huge genealogical data can get unwieldy.

### **Detailed Explanation & Real-World Scenario**  
- For smaller genealogical datasets, XML’s hierarchy is a good fit. But if the dataset is large or has many cross‐branch relationships, the file size and nested queries become a burden.  
- Historians might appreciate the self-describing tags but could struggle with performance on massive lineages.

**Common Pitfalls**  
- Over-nesting or duplicating data (like repeating `<title>` blocks all over).  
- Assuming XML can easily handle many-to-many relationships (it’s more complicated than in relational or graph models).

### **Exam Tip (Key Points Summary)**  
- **Strengths**: Great for hierarchical structure, self-explanatory.  
- **Weaknesses**: Verbose, potentially slow for large genealogical data, not ideal for many-to-many relations.

---

## **Question 2(f)**
**Context**: One colleague suggests **RDF**; another suggests **relational**. Who is right?

### **Answer**  
Both have valid points. 

- **RDF**: More flexible for graph-like data (multiple marriages, cross links).  
- **Relational**: Good if you can structure genealogical data in tables, with well-defined foreign keys.  

### **Detailed Explanation & Real-World Scenario**  
- **RDF** is ideal when the data is a web/graph of relationships: e.g., multiple spouses, alliances, lineage branches.  
- **Relational** is simpler if each person, title, or relationship can be turned into a table row and you want fast, tabular SQL queries.

**Common Pitfalls**  
- Choosing relational for extremely graph-like data can lead to complicated join tables. Conversely, forcing RDF where tabular data is enough might be overkill.

### **Exam Tip (Key Points Summary)**  
- Both approaches are “correct,” depending on complexity:  
  - **Graph-like** genealogies → RDF.  
  - **Tabular** genealogies → RDB.

---

## **Question 2(g)**
**Context**: Choose one approach (RDF or relational) and show how it addresses (e)’s strengths/weaknesses.

### **Answer** (Example: **Relational** Approach)

1. **Addresses Verbosity** by normalizing data in tables—no repeated tags.  
2. **Handles Complexity** with standard SQL relationships/joins.  
3. **Scalability** is improved due to RDB indexes & query optimizers.

### **Detailed Explanation & Real-World Scenario**  
- In a relational system, you might have tables like `Person`, `Marriage`, `Title`. This **reduces duplication** and allows strong performance for queries (like “Who are the children of Henry VIII?”).  
- Large genealogical data sets often run faster in a relational DB than in a huge nested XML.

**Common Pitfalls**  
- If relationships are extremely multi-branch or dynamic, some might prefer a graph database (like RDF triple store). But many genealogical use cases still do fine in relational.

### **Exam Tip (Key Points Summary)**  
- A relational DB can solve the **weaknesses** of XML by reducing **redundancy** & **improving** performance on large genealogical sets.

---

# **Question 3**

## **Question 3(a)**
**Context**: A SPARQL query for Wikidata:

```sparql
SELECT DISTINCT ?person
WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P19 wd:Q60.
}
```
Meaning?

### **Answer**  
It returns **distinct** individuals (`?person`) who are **instance of** (`wdt:P31`) a **human** (`wd:Q5`) and have **place of birth** (`wdt:P19`) in **New York City** (`wd:Q60`).

### **Detailed Explanation & Real-World Scenario**  
- `wd:Q5` = “human” in Wikidata; `wd:Q60` = “New York City.”  
- For instance, it might list persons like “Robert Downey Jr.” or “Jennifer Lopez” if their Wikidata entries have placeOfBirth = Q60.

**Common Pitfalls**  
- If the data is incomplete (someone lacks a P19 statement), they’re missed.

### **Exam Tip (Key Points Summary)**  
- The query yields IRIs of humans born in NYC.  
- Must have `wdt:P31 wd:Q5` and `wdt:P19 wd:Q60` set in Wikidata.

---

## **Question 3(b)**
**Context**: The question: “What assumptions does it make? What data must be present?”

### **Answer**  
1. **Assumption**: Each matching person’s data must have `wdt:P31 wd:Q5` (human) and `wdt:P19 wd:Q60` (placeOfBirth = NYC).  
2. **Needed**: The correct properties (P31, P19) and standard entity IDs (Q5, Q60) in the dataset.

### **Detailed Explanation & Key Points**  
- If someone is “human” but placeOfBirth uses a different code for “New York City,” the query misses them.  
- RDF queries require consistent property usage.

### **Exam Tip (Key Points Summary)**  
- **Completeness**: The query depends on P31, P19 being correctly assigned.  
- **ID consistency**: Must be `wd:Q60` for NYC.

---

## **Question 3(c)**
**Context**: The next query uses a location path:
```sparql
SELECT DISTINCT ?person
WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P19/wdt:P131* wd:Q60.
}
```
Does it fix assumptions from (b)?

### **Answer**  
**Yes**, it broadens the place-of-birth check to nested territories. Now “Queens” or “Brooklyn” (with `wdt:P131*` linking them to NYC) are included.

### **Detailed Explanation & Key Points**  
- `wdt:P19/wdt:P131*` means “placeOfBirth” then zero or more `locatedIn` steps until eventually `Q60` (NYC).  
- This resolves the direct match assumption, capturing sub-entities of NYC.

### **Exam Tip (Key Points Summary)**  
- **Path expression** lets you match “X is inside Y which is inside New York City.”  
- More flexible than a direct `wdt:P19 wd:Q60`.

---

## **Question 3(d)**
**Context**: The results aren’t human‐readable. Why not?

### **Answer**  
Because SPARQL returns entity IRIs (e.g., `http://www.wikidata.org/entity/Q...`) by default, not plain English labels.

### **Detailed Explanation & Key Points**  
- Linked data typically references everything by URIs.  
- You must fetch `rdfs:label` or use `wikibase:label` to get user-friendly names.

### **Exam Tip (Key Points Summary)**  
- If you want “John Smith” instead of `wd:Q98765`, query the label property or use the label service.

---

## **Question 3(e)**
**Context**: Rewriting the query in (c) to get more readable labels.

### **Answer**  
**Generic RDF**:
```sparql
SELECT DISTINCT ?person ?personLabel
WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P19/wdt:P131* wd:Q60.
  ?person rdfs:label ?personLabel .
  FILTER (lang(?personLabel) = "en")
}
```

**Wikidata** approach:
```sparql
SELECT DISTINCT ?person ?personLabel
WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P19/wdt:P131* wd:Q60.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```

### **Detailed Explanation & Key Points**  
- `rdfs:label` is standard in RDF.  
- In Wikidata, `SERVICE wikibase:label` automatically retrieves labels in the requested language.

### **Exam Tip (Key Points Summary)**  
- By retrieving labels, results become user-friendly (“Jennifer Lopez” vs. QID).  
- The `SERVICE` block is unique to Wikidata.

---

## **Question 3(f)**
**Context**: Compare how IMDB does place-of-birth vs. Wikidata approach.

### **Answer**  
- **IMDB**: specialized in movies, typically offers a web interface but not a robust public SPARQL-like endpoint.  
- **Wikidata**: broad linked data, open SPARQL endpoint, easy to query place-of-birth for any entity.

### **Detailed Explanation & Key Points**  
- IMDB is proprietary; you can look up “Born in New York City” but not as flexible if you want a large, custom query.  
- Wikidata is open, flexible, but may be less detailed on certain film/TV data.

### **Exam Tip (Key Points Summary)**  
- IMDB → domain-specific, partial or no open API for advanced queries.  
- Wikidata → open, general knowledge with full SPARQL.

---

## **Question 3(g)**
**Context**: IMDB specialized data + Wikidata approach. How to combine?

### **Answer**  
Use **cross‐references**: IMDB IDs in Wikidata link the same entity (actor/film). Possibly do a **federated** approach: gather general facts from Wikidata, then fetch specialized movie info from IMDB.

### **Detailed Explanation & Key Points**  
- Many Wikidata entries store `P345` (IMDB ID).  
- This bridging yields deeper info than either source alone.  
- E.g., for an actor, get birth info from Wikidata, filmography from IMDB.

### **Exam Tip (Key Points Summary)**  
- Link across both platforms using shared IDs.  
- Gains breadth (Wikidata) + depth (IMDB).

---

## **Question 3(h)**
**Context**: The query in (b) but using a **relational** model.

### **Answer**  
Use a **triple table** (Subject, Predicate, Object) and do:

```sql
SELECT DISTINCT t1.Subject
FROM TripleTable t1
JOIN TripleTable t2 ON t1.Subject = t2.Subject
WHERE t1.Predicate = 'instanceOf'
  AND t1.Object = 'Human'
  AND t2.Predicate = 'placeOfBirth'
  AND t2.Object = 'New York City';
```

### **Detailed Explanation & Key Points**  
- **Subject** is like `?person`, `Predicate` is `wdt:P31`, and `Object` is `wd:Q5` if storing string equivalents.  
- The join ensures the same Subject satisfies both conditions.

### **Exam Tip (Key Points Summary)**  
- “Triple table” method replicates RDF in an RDB.  
- Self‐join to find entries that satisfy two conditions.

---

## **Question 3(i)**
**Context**: The version in (c) used a property path. In SQL, we might replicate that with more joins or recursion.

### **Answer**  
You’d store each location step in the triple table, then do multiple self-joins or a recursive CTE to track the path from sub-location up to NYC.

```sql
SELECT DISTINCT t1.Subject
FROM TripleTable t1
JOIN TripleTable t2 ON t1.Subject = t2.Subject
JOIN TripleTable t3 ON t2.Object = t3.Subject
...
```
(etc.)

### **Explanation & Key Points**  
- The `P131*` path means indefinite administrative territory steps. In SQL, you’d do repeated or recursive queries to handle multiple “locatedIn” relationships.  
- More complex than a direct match.

### **Exam Tip (Key Points Summary)**  
- It’s doable in SQL but more complex than SPARQL’s built-in `*` operator.  
- Potentially a “recursive CTE” approach for indefinite depth.

---

# **Question 4**

## **Question 4(a)**
**Context**: We have a hospital/hospitality E/R diagram. Which of the six subquestions can we answer?

### **Answer**  
Likely these three:

1. **Which building did Neha Ahuja stay in?**  
2. **Which hospital was responsible for Neha’s stay?**  
3. **In which wards are Orthopedics patients housed?**

### **Detailed Explanation & Key Points**  
- Because the model shows Patient–Ward–Building–Hospital relationships, we can trace a patient to a building/hospital.  
- If Orthopedics is a department linked to wards, we can see which wards they occupy.

### **Exam Tip (Key Points Summary)**  
- The other subquestions might need extra links (like “Which doctor treated Neha?”) if not present in the model.

---

## **Question 4(b)**
**Context**: Part of the model that can’t be done directly in relational form. Typically the many-to-many.

### **Answer**  
- The many-to-many **Doctor ↔ Department** must be resolved via a **junction table** (e.g., `Doctor_Department`).  
- The **StayIn** relationship with arrival/departure dates might be simplified to a single table or bridging table.

### **Detailed Explanation & Key Points**  
- Relational DBs require an **associative entity** for M:N. E.g., `Doctor_Department(DoctorID, DeptID)`.  
- If “StayIn” had extra attributes (arrivalDate, departureDate), place them in a bridging table like `PatientWardStay`.

### **Exam Tip (Key Points Summary)**  
- M:N = bridging table.  
- Relationship attributes → store them in that bridging table.

---

## **Question 4(c)**
**Context**: Adapt the model so everything is resolved, plus cardinalities.

### **Answer**  
A typical revised design:

1. **Hospital**(HospitalID PK)  
2. **Building**(BuildingID PK, HospitalID FK)  
3. **Ward**(WardID PK, BuildingID FK)  
4. **Department**(DeptID PK)  
5. **Doctor**(DoctorID PK)  
6. **Doctor_Department**(DoctorID, DeptID) for M:N  
7. **Patient**(PatientID PK, …)  
8. **PatientWardStay**(PatientID, WardID, ArrivalDate, DepartureDate)

**Cardinality**:  
- Hospital 1–M Building, Building 1–M Ward, Ward 1–M PatientWardStay, etc.  
- Doctor M–N Department.

### **Exam Tip (Key Points Summary)**  
- Clear PK/FK links, bridging tables for M:N, plus a stay table for arrival/departure.

---

## **Question 4(d)**
**Context**: List the tables + keys in the SQL. No need for full fields.

### **Answer**  
1. **Hospital**(HospitalID PK)  
2. **Building**(BuildingID PK, HospitalID FK)  
3. **Ward**(WardID PK, BuildingID FK)  
4. **Department**(DeptID PK)  
5. **Doctor**(DoctorID PK)  
6. **Doctor_Department**(DoctorID, DeptID) composite PK  
7. **Patient**(PatientID PK)  
8. **PatientWardStay**(PatientID, WardID) + Arrival/Departure (composite PK or separate PK)

### **Explanation & Key Points**  
- Each table has a numeric or string PK.  
- Associative table `Doctor_Department` handles many-to-many.  
- `PatientWardStay` handles the “Patient stayed in which ward, from date X to date Y.”

### **Exam Tip (Key Points Summary)**  
- Outline each table’s name and key. That’s all that’s needed here.

---

## **Question 4(e)**
**Context**: Provide MySQL queries for the subquestions in (a).

### **Answer** (Samples)

1. **Which building did Neha Ahuja stay in?**
   ```sql
   SELECT b.Name
   FROM Patient p
   JOIN PatientWardStay pws ON p.PatientID = pws.PatientID
   JOIN Ward w ON pws.WardID = w.WardID
   JOIN Building b ON w.BuildingID = b.BuildingID
   WHERE p.Name = 'Neha Ahuja';
   ```

2. **Which hospital was responsible for Neha’s stay?**
   ```sql
   SELECT h.Name
   FROM Patient p
   JOIN PatientWardStay pws ON p.PatientID = pws.PatientID
   JOIN Ward w ON pws.WardID = w.WardID
   JOIN Building b ON w.BuildingID = b.BuildingID
   JOIN Hospital h ON b.HospitalID = h.HospitalID
   WHERE p.Name = 'Neha Ahuja';
   ```

3. **In which wards are Orthopedics patients housed?**
   ```sql
   SELECT DISTINCT w.Name AS WardName
   FROM Department d
   JOIN Doctor_Department dd ON d.DeptID = dd.DeptID
   JOIN Doctor doc ON dd.DoctorID = doc.DoctorID
   -- Possibly a link to which wards the doc visits or the doc's patients
   ...
   WHERE d.Name = 'Orthopedics';
   ```

*(Exact logic depends on how doctors/departments tie to wards or patients in your schema.)*

### **Explanation & Key Points**  
- We rely on **multi-table** joins. Each relationship (Patient → Ward, Ward → Building, Building → Hospital) is a foreign key chain.  
- For Orthopedics wards, you may need additional relationships that connect doctors or departments to wards.

### **Exam Tip (Key Points Summary)**  
- The key technique is **JOIN** on foreign keys.  
- Filter by patient name or department name as needed.

---

## **Question 4(f)**
**Context**: Could a tree-based (XML) model be better than the relational approach?

### **Answer**  
Generally, **no**. Healthcare data often has many cross-links (doctor to many departments, wards to buildings, etc.). An XML tree is less suitable for these many-to-many relationships.

### **Detailed Explanation & Key Points**  
- XML is good for hierarchical data but struggles with repeating or cross-linked relationships.  
- A relational or graph-based model handles such complexity more gracefully.

### **Exam Tip (Key Points Summary)**  
- For multi-relationship hospital data, relational is often more efficient and simpler than a purely hierarchical XML approach.

