# Solution Sheet - September 2022

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

**Question:** What is missing from the following set of commands?

```sql
START TRANSACTION;
UPDATE Account SET Balance = Balance-100 WHERE AccNo=21430885;
UPDATE Account SET Balance = Balance+100 WHERE AccNo=29584776;
SELECT SUM(Balance) FROM Account;
```

---

### Answer: **iv. COMMIT;**

---

### Revision Notes

**Core Concept:** SQL transactions require explicit completion with COMMIT or ROLLBACK.

| Command | Purpose |
|---------|---------|
| `START TRANSACTION` | Begin a transaction block |
| `COMMIT` | Make all changes permanent |
| `ROLLBACK` | Undo all changes since START TRANSACTION |

**Why COMMIT?**
- Without COMMIT, the updates remain uncommitted and could be rolled back or lost
- `ROLLBACK` (choice i) reverses changes, not the intent here
- `END TRANSACTION` (choice iii) is not standard SQL syntax

**ACID Properties:**
- **A**tomicity: All operations complete or none do
- **C**onsistency: Database remains in valid state
- **I**solation: Concurrent transactions don't interfere
- **D**urability: Committed changes survive system failure

---

## Question 1(b) [4 marks]

**Question:** The following SPARQL query should return Cristiano Ronaldo's birth city. Why doesn't it?

```sparql
SELECT DISTINCT *
WHERE {
  "Cristiano Ronaldo"@en dbo:birthPlace
    [
      a dbo:City ;
      rdfs:label ?cityName
    ] .
  FILTER ( LANG(?cityName) = 'en' )
}
```

---

### Answer: **ii. "Cristiano Ronaldo"@en is a string, not a URL. It can't be the subject of a triple.**

---

### Revision Notes

**Core Concept:** In RDF/SPARQL, subjects must be URIs, not literal strings.

**The Problem:**
- `"Cristiano Ronaldo"@en` is a literal string with language tag
- Literals cannot be subjects in RDF triples
- The query should use the URI: `<http://dbpedia.org/resource/Cristiano_Ronaldo>`

**Correct Approach:**
```sparql
SELECT DISTINCT ?cityName
WHERE {
  [] rdfs:label "Cristiano Ronaldo"@en ;
     dbo:birthPlace [
       a dbo:City ;
       rdfs:label ?cityName
     ] .
  FILTER ( LANG(?cityName) = 'en' )
}
```

Or using the resource URI directly:
```sparql
SELECT DISTINCT ?cityName
WHERE {
  dbr:Cristiano_Ronaldo dbo:birthPlace [
    a dbo:City ;
    rdfs:label ?cityName
  ] .
  FILTER ( LANG(?cityName) = 'en' )
}
```

---

## Question 1(c) [4 marks]

**Question:** How many predicates does this RDF/Turtle extract contain?

```turtle
card:I a :Male;
       foaf:family_name "Berners-Lee";
       foaf:givenname "Timothy";
       foaf:title "Sir".
```

---

### Answer: **i. 4**

---

### Revision Notes

**Core Concept:** Count the distinct predicates (properties) in Turtle statements.

**The Four Predicates:**
1. `a` (shorthand for `rdf:type`)
2. `foaf:family_name`
3. `foaf:givenname`
4. `foaf:title`

**Turtle Syntax Refresher:**
- `;` continues with same subject, different predicate
- `,` continues with same subject AND predicate, different object
- `.` ends the statement

**Common Mistakes:**
- Counting objects or subjects as predicates
- Overlooking `a` as a predicate (it's shorthand for `rdf:type`)

---

## Question 1(d) [4 marks]

**Question:** How many results does this XPath query select?

```xpath
//disk[@xml:id="1847336"]/track[@duration>150]/*
```

Given XML:
```xml
<collection>
  <disk xml:id="1847336">
    <title>The Greatest Hits Ever: Volume 123</title>
    <tracks>
      <track no="1" duration="193">
        <title>What is wrong with parsley?</title>
        <artist>Herbal Reasoning</artist>
      </track>
      <track no="2" duration="167">
        <title>Love threw me a googly</title>
        <artist>Botham and the Fielders</artist>
      </track>
      <track no="3" duration="121">
        <title>Comedy farm</title>
        <artist>Just weird</artist>
      </track>
    </tracks>
  </disk>
</collection>
```

---

### Answer: **vi. None**

---

### Revision Notes

**Core Concept:** XPath navigation with attribute predicates and wildcards.

**Query Breakdown:**

| Part | Meaning |
|------|---------|
| `//disk[@xml:id="1847336"]` | Find disk with specific xml:id |
| `/track[@duration>150]` | Direct child tracks with duration > 150 |
| `/*` | All direct children of matching tracks |

**Why it returns NOTHING:**

The XPath uses `/track` which looks for **direct children** of `<disk>`, but in the XML structure:
```
<disk>
  <title>...</title>
  <tracks>           ← direct child of disk
    <track>...</track>   ← child of tracks, NOT direct child of disk!
  </tracks>
</disk>
```

The `<track>` elements are children of `<tracks>` (plural), not direct children of `<disk>`. Therefore, `/track` finds nothing.

**If the XPath were correct** (`//disk[@xml:id="1847336"]/tracks/track[@duration>150]/*`):
1. Find tracks with `duration > 150`: Track 1 (193) and Track 2 (167)
2. Each track has 2 children: `<title>` and `<artist>`
3. Total would be: 2 tracks × 2 children = 4 elements

**Common Mistake:** Confusing `/` (direct child) with `//` (descendant). Using `//track` instead of `/track` would find tracks at any depth.

---

## Question 1(e) [4 marks]

**Question:** An archive search tool shows precision/recall behavior. Which parameter setting minimizes time spent on the task?

- Archive: 50,000 items, 30 relevant
- Time to find missed item manually: 15 minutes
- Time wasted on false positive: 30 seconds

---

### Answer: **ii. To the right of the graph, before it drops – with 68% precision and 90% recall**

---

### Revision Notes

**Core Concept:** Precision/Recall trade-offs and time optimization.

**Definitions:**
- **Precision** = True Positives / (True Positives + False Positives)
- **Recall** = True Positives / (True Positives + False Negatives)

**Time Calculation for Option ii (68% precision, 90% recall):**
- 90% recall on 30 items = 27 found, 3 missed
- Missed items: 3 × 15 min = 45 minutes
- With 68% precision and 27 true positives: ~12 false positives
- False positives: 12 × 0.5 min = 6 minutes
- Total: ~51 minutes

**Why not 100% precision (17% recall)?**
- Would miss 83% of 30 items = ~25 items
- Manual search: 25 × 15 min = 375 minutes = 6+ hours

---

## Question 1(f) [4 marks]

**Question:** Which normal forms does the Music Singles table satisfy?

| Chart | Date | Position | Title | Artist | Date of Birth |
|-------|------|----------|-------|--------|---------------|
| RIAS | 2022-04-14 | 1 | As It Was | Harry Styles | 1994-02-01 |
| ... | ... | ... | ... | ... | ... |

---

### Answer: **iv. 1NF – all rows are a single data type**

---

### Revision Notes

**Core Concept:** Identifying normal forms from table structure.

**Why only 1NF:**
- ✓ **1NF**: All values are atomic (no repeating groups, no arrays)
- ✗ **2NF**: Has partial dependencies (Date of Birth depends only on Artist, not full key)
- ✗ **3NF**: Has transitive dependencies (Artist → Date of Birth)

**Problems with this table:**
- Date of Birth depends on Artist, not on the composite key (Chart, Date, Position)
- If Harry Styles appears multiple times, Date of Birth is duplicated

**Normalized Design:**
```
Artists(ArtistName PK, DateOfBirth)
ChartEntries(Chart, Date, Position, Title, ArtistName FK)
```

---

## Question 1(g) [4 marks]

**Question:** Why is this E/R diagram not good? (Plant identification database)

---

### Answer: **i, ii, iii, iv, vi, viii**

---

### Revision Notes

**Core Concept:** E/R diagram conventions and best practices.

**Issues identified:**

| Issue | Problem | Convention |
|-------|---------|------------|
| (i) | Cardinality between entity and attribute | Should only be between entities |
| (ii) | Entities connected without relationships | Must use relationship diamonds |
| (iii) | Arrow is meaningless | Use proper E/R notation |
| (iv) | Spaces in attribute names | Avoid spaces (use camelCase or underscores) |
| (vi) | Cardinality "21" invalid | Use 1, n, m, *, etc. |
| (viii) | β and x are unusual | Standard: 1, n, m |

**Valid statement:**
- (v) Attributes CAN be shared in some notations
- (vii) There may or may not be a ternary relationship

---

## Question 1(h) [4 marks]

**Question:** Find staff who had interactions with client "Shug Avery". Which query continuations work?

```sql
SELECT Employee.givenName, Employee.familyName
```

---

### Answer: **iii and iv**

---

### Revision Notes

**Core Concept:** SQL JOINs to connect related tables.

**Why iii works:**
```sql
FROM Client
INNER JOIN Meeting ON (Meeting.ClientID = Client.ID)
INNER JOIN Employee ON (Employee.ID = Meeting.EmployeeID)
WHERE Client.givenName = "Shug"
AND Client.familyName = "Avery";
```
- Properly joins Client → Meeting → Employee
- Filters by client name correctly

**Why iv works:**
```sql
FROM Employee, Client, Meeting
WHERE Employee.ID = Meeting.EmployeeID
AND Client.ID = Meeting.ClientID
AND Client.givenName = "Shug"
AND Client.familyName = "Avery";
```
- Implicit join syntax (older style but valid)
- Same logic as explicit INNER JOINs

**Why others fail:**
- (i) Missing Meeting table
- (ii) Wrong join conditions (Meeting.ID = Client.ID is incorrect)
- (v) NATURAL JOIN without Meeting doesn't work

---

## Question 1(i) [4 marks]

**Question:** Which MongoDB query finds actors born before 1957?

---

### Answer: **vii**

```javascript
db.actors.find({
  "dateOfBirth": {$lt: ISODate("1957-01-01")}
});
```

---

### Revision Notes

**Core Concept:** MongoDB query operators and date handling.

**Why option vii is correct:**
- `find()` returns all matching documents (not just one)
- `$lt` is the correct "less than" operator
- `ISODate()` properly parses the date string

**Why others fail:**

| Option | Problem |
|--------|---------|
| i | `findOne` returns only one record |
| ii | `{$lt: 1957}` compares to integer, not date |
| iii, iv, v, viii | `"<"` is not a valid MongoDB operator |
| vi | Exact match, not less than |

**MongoDB Comparison Operators:**
- `$lt` - less than
- `$lte` - less than or equal
- `$gt` - greater than
- `$gte` - greater than or equal
- `$ne` - not equal
- `$eq` - equal

---

## Question 1(j) [4 marks]

**Question:** Given the RecipeML DTD:
```dtd
<!ELEMENT recipe (head, description*, equipment?, ingredients,
                  directions, nutrition?, diet-exchanges?)>
```

Select all true statements.

---

### Answer: **i, ii** (and arguably iv)

---

### Revision Notes

**Core Concept:** DTD element declarations and occurrence indicators.

**DTD Occurrence Indicators:**

| Symbol | Meaning |
|--------|---------|
| (none) | Exactly one (required) |
| `?` | Zero or one (optional) |
| `*` | Zero or more |
| `+` | One or more |

**Analysis:**
- `ingredients` has no modifier → exactly one required → **(i) TRUE**
- Order in DTD is significant → ingredients before directions → **(ii) TRUE**
- **(iii) FALSE** - order IS important in DTD sequences
- **(iv) TRUE** - "can have one" is technically true (it MUST have exactly one)
- **(v) FALSE** - can only have ONE (no `*` or `+` modifier)

---

# Section B

---

# Question 2: Database Design and Querying [30 marks]

## Context

An organisation monitoring non-verbal reasoning tests maintains a database. A sociologist runs:

```sql
SELECT AVG(Score) AS Average,
       Year(TestDate) AS TestYear,
       Gender,
       TIMESTAMPDIFF(YEAR, BirthDate, TestDate) AS Age,
       Student.City as City
FROM Test INNER JOIN Student ON Test.Student=Student.ID
GROUP BY TestYear, Gender, Age, City
```

---

## Question 2(a) [1 mark]

**Question:** Which aggregate function is used here?

---

### Answer

**`AVG()`** - calculates the arithmetic mean of Score values.

---

## Question 2(b) [6 marks]

**Question:** There is a problem with the database design that risks making the aggregation incorrect. What is it, and how could it be resolved?

---

### Answer

**Problems:**

1. **City stored as free text:**
   - "Birmingham, AL" vs "Birmingham" vs "Birmingham, USA" could be treated as different cities
   - Leads to incorrect groupings in aggregation

2. **School stored as free text:**
   - Same issue - inconsistent naming prevents proper aggregation

3. **Potential data inconsistency:**
   - If student details change, historical test records become inaccurate

**Solutions:**

1. **Normalize City and School:**
   ```sql
   CREATE TABLE Cities (
       CityId INT PRIMARY KEY AUTO_INCREMENT,
       CityName VARCHAR(100),
       Country VARCHAR(50)
   );

   CREATE TABLE Schools (
       SchoolId INT PRIMARY KEY AUTO_INCREMENT,
       SchoolName VARCHAR(130),
       CityId INT,
       FOREIGN KEY (CityId) REFERENCES Cities(CityId)
   );
   ```

2. **Reference by foreign key instead of storing text:**
   - Student table references CityId and SchoolId
   - Ensures consistent grouping in aggregations

---

## Question 2(c) [4 marks]

**Question:** For security reasons, the researcher should be given minimal, read-only access. Give a suitable command.

---

### Answer

```sql
CREATE USER 'researcher'@'localhost' IDENTIFIED BY 'securepassword';
GRANT SELECT ON database_name.* TO 'researcher'@'localhost';
```

Or in older MySQL syntax:
```sql
GRANT SELECT ON database_name.*
      TO 'researcher'@'localhost'
      IDENTIFIED BY 'securepassword';
```

**Key Points:**
- `SELECT` only - no INSERT, UPDATE, DELETE
- Principle of least privilege
- Read-only access as requested

---

## Question 2(d) [4 marks]

**Question:** From the point of view of handling confidential information about minors, it would be better to give access only to aggregated data. How would you achieve that?

---

### Answer

**Create a VIEW that exposes only aggregated data:**

```sql
CREATE VIEW AggregatedTestData AS
SELECT Gender,
       City,
       AVG(Score) AS AvgScore,
       COUNT(*) AS SampleSize,
       YEAR(TestDate) AS TestYear
FROM Test
INNER JOIN Student ON Test.Student = Student.ID
GROUP BY Gender, City, YEAR(TestDate)
HAVING COUNT(*) >= 5;  -- Minimum group size for privacy
```

**Then grant access only to the view:**
```sql
GRANT SELECT ON database_name.AggregatedTestData TO 'researcher'@'localhost';
```

**Benefits:**
- Researcher cannot see individual student records
- Only aggregated statistics are visible
- HAVING clause ensures minimum group sizes to prevent re-identification

---

## Question 2(e) [1 mark]

**Question:** What limitation would that create for the researcher?

---

### Answer

They cannot:
- Access individual-level records
- Perform outlier detection or analysis
- Conduct correlation studies at the individual level
- Verify data quality or identify data entry errors
- Analyze small subgroups that get filtered out

---

## Question 2(f) [8 marks]

**Question:** The Student table is defined as:

```sql
CREATE TABLE Student(
  ID VARCHAR(25) PRIMARY KEY,
  GivenName VARCHAR(80) NOT NULL,
  FamilyName VARCHAR(80) NOT NULL,
  Gender ENUM('M','F') NOT NULL,
  BirthDate DATE NOT NULL,
  School VARCHAR(130),
  City VARCHAR(130));
```

What problems can you see, and how would you resolve them?

---

### Answer

| Problem | Issue | Resolution |
|---------|-------|------------|
| **VARCHAR(25) as PK** | Inefficient for indexing, harder to join | Use INT AUTO_INCREMENT for internal ID |
| **Gender ENUM('M','F')** | Binary-only, doesn't accommodate non-binary | Use VARCHAR or add more options |
| **School as free text** | Inconsistent entries, can't enforce FK | Create Schools table, use FK reference |
| **City as free text** | Same issue - duplicates, typos | Create Cities table, use FK reference |
| **No referential integrity** | Can't ensure valid school/city | Add foreign key constraints |
| **School/City can be NULL** | Data quality issues | Consider NOT NULL or separate lookup |

**Improved Design:**

```sql
CREATE TABLE Cities (
    CityId INT PRIMARY KEY AUTO_INCREMENT,
    CityName VARCHAR(100) NOT NULL,
    Country VARCHAR(50)
);

CREATE TABLE Schools (
    SchoolId INT PRIMARY KEY AUTO_INCREMENT,
    SchoolName VARCHAR(130) NOT NULL,
    CityId INT,
    FOREIGN KEY (CityId) REFERENCES Cities(CityId)
);

CREATE TABLE Students (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    ExternalId VARCHAR(25) UNIQUE,  -- Keep external reference if needed
    GivenName VARCHAR(80) NOT NULL,
    FamilyName VARCHAR(80) NOT NULL,
    Gender VARCHAR(20),  -- More flexible
    BirthDate DATE NOT NULL,
    SchoolId INT,
    CityId INT,
    FOREIGN KEY (SchoolId) REFERENCES Schools(SchoolId),
    FOREIGN KEY (CityId) REFERENCES Cities(CityId)
);
```

---

## Question 2(g) [6 marks]

**Question:** How well would this data work in an object database like MongoDB? What would be the advantages or disadvantages?

---

### Answer

**Advantages of MongoDB:**

| Advantage | Explanation |
|-----------|-------------|
| **Flexible schema** | Can add fields without ALTER TABLE |
| **Embedded documents** | Test scores can be embedded in student documents |
| **No rigid structure** | Easy to handle varying data formats |
| **Horizontal scaling** | Built for distributed systems |
| **JSON-like documents** | Natural fit for modern web applications |

**Disadvantages of MongoDB:**

| Disadvantage | Explanation |
|--------------|-------------|
| **No traditional JOINs** | Cross-collection queries more complex |
| **Data duplication** | City/School info repeated in each document |
| **Weaker referential integrity** | No enforced foreign keys |
| **Update anomalies** | Changing a school name requires many updates |
| **Aggregation complexity** | GROUP BY operations less straightforward |

**Example MongoDB Document:**
```json
{
  "_id": "student123",
  "givenName": "Alice",
  "familyName": "Smith",
  "gender": "F",
  "birthDate": ISODate("2005-05-10"),
  "school": "Birmingham High School",
  "city": "Birmingham",
  "tests": [
    {"date": ISODate("2019-01-10"), "score": 50.5},
    {"date": ISODate("2019-09-10"), "score": 55.0}
  ]
}
```

**Conclusion:** Relational model is better for this use case due to:
- Need for consistent aggregations across students
- Importance of data integrity
- Complex analytical queries

---

# Question 3: XML, XPath, and Relational Models [30 marks]

## Context

An entry in the Oxford Medieval Manuscript catalogue begins as follows:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://raw.githubusercontent.com/bodleian/
    consolidated-tei-schema/master/msdesc.rng"
    type="application/xml"
    schematypens="http://relaxng.org/ns/structure/1.0"?>
<TEI xml:id="manuscript_3945" xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader xmlns:tei="http://www.tei-c.org/ns/1.0">
    <fileDesc>
      <titleStmt>
        <title>Christ Church MS. 341</title>
        <title type="collection">Christ Church MSS.</title>
        <respStmt>
          <resp>Cataloguer</resp>
          <persName>Ralph Hanna</persName>
          <persName>David Rundle</persName>
        </respStmt>
      </titleStmt>
    </fileDesc>
  </teiHeader>
</TEI>
```

---

## Question 3(a) [2 marks]

**Question:** What markup language is being used? And what is the root node?

---

### Answer

- **Markup Language:** XML (specifically TEI - Text Encoding Initiative)
- **Root Node:** `<TEI>`

---

## Question 3(b) [3 marks]

**Question:** Is this fragment well-formed? Justify your answer.

---

### Answer

**Likely NOT well-formed** as presented, because:

1. If `<fileDesc>` and `<teiHeader>` are not properly closed
2. The fragment appears truncated

**For well-formedness, XML must have:**
- Exactly one root element ✓
- All tags properly opened and closed
- Proper nesting (no overlapping tags)
- Attribute values in quotes ✓
- Valid characters in element/attribute names ✓

**If all closing tags are present, it would be well-formed.**

---

## Question 3(c) [2 marks]

**Question:** What would be selected by evaluating `//fileDesc//title/@type`?

---

### Answer

The `type` attribute value from `<title>` elements under `<fileDesc>`:

**Result:** `"collection"`

This is the value of the `type` attribute on `<title type="collection">Christ Church MSS.</title>`.

---

## Question 3(d) [2 marks]

**Question:** What would be selected by `//resp[text()='Cataloguer']/../persName`?

---

### Answer

All `<persName>` elements that are siblings of a `<resp>` element containing "Cataloguer".

**Result:**
- `<persName>Ralph Hanna</persName>`
- `<persName>David Rundle</persName>`

**How it works:**
1. `//resp[text()='Cataloguer']` - Find `<resp>` with text "Cataloguer"
2. `/..` - Navigate to parent (`<respStmt>`)
3. `/persName` - Select `<persName>` children

---

## Question 3(e) [4 marks]

**Question:** Why might you choose the expression in (d) rather than the simpler `persName`? Give two situations where it would be preferable.

---

### Answer

**Situations where the complex XPath is preferable:**

1. **Disambiguation:** The document may have multiple `<persName>` elements in different contexts (authors, editors, scribes). This XPath specifically gets people associated with the "Cataloguer" role.

2. **Role-specific queries:** You only want cataloguers, not all people mentioned. Other `<respStmt>` elements might have different roles like "Editor" or "Transcriber".

3. **Context preservation:** The relationship between the person and their role is maintained - you know these people ARE cataloguers, not just any named person.

4. **Precision in large documents:** In a catalogue with thousands of entries, `//persName` would return all people, but you only want those in cataloguer role.

---

## Question 3(f) [8 marks]

**Question:** The `<msItem n="2">` element refers to the second textual item in the manuscript. How well would this way of listing contents work in a relational model? How would you approach the problem?

---

### Answer

**Problems with `n="2"` in relational model:**

1. **Ordering not implicit:** Relational tables have no inherent row order
2. **Attribute vs column:** The `n` attribute would need explicit storage
3. **Nested structure:** Manuscripts contain items which may have sub-items

**Relational Approach:**

```sql
CREATE TABLE Manuscripts (
    ManuscriptId VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(200)
);

CREATE TABLE ManuscriptItems (
    ItemId INT PRIMARY KEY AUTO_INCREMENT,
    ManuscriptId VARCHAR(50),
    ItemNumber INT NOT NULL,  -- Explicit ordering
    Incipit TEXT,
    Explicit TEXT,
    Notes TEXT,
    FOREIGN KEY (ManuscriptId) REFERENCES Manuscripts(ManuscriptId),
    UNIQUE (ManuscriptId, ItemNumber)  -- Enforce uniqueness
);

-- Query to get items in order:
SELECT * FROM ManuscriptItems
WHERE ManuscriptId = 'manuscript_3945'
ORDER BY ItemNumber;
```

**Key Points:**
- Store sequence number explicitly in `ItemNumber` column
- Use `ORDER BY` for retrieval in correct sequence
- UNIQUE constraint ensures no duplicate item numbers per manuscript
- Consider hierarchical items with ParentItemId for nested structures

---

## Question 3(g) [3 marks]

**Question:** What is the file `msdesc.rng`, and why is it referenced in the catalogue entry?

---

### Answer

**What it is:**
- A **Relax NG schema** file (`.rng` extension)
- Defines the structure, elements, attributes, and constraints for valid TEI manuscript descriptions

**Why it's referenced:**
1. **Validation:** Allows XML documents to be validated against the schema
2. **Structure definition:** Specifies which elements are required, optional, and their allowed order
3. **Interoperability:** Ensures all catalogue entries follow the same structure
4. **Documentation:** Provides machine-readable specification of the format

The `<?xml-model?>` processing instruction tells validators which schema to use.

---

## Question 3(h) [2 marks]

**Question:** What is the difference between valid and well-formed XML?

---

### Answer

| Aspect | Well-Formed | Valid |
|--------|-------------|-------|
| **Definition** | Follows XML syntax rules | Well-formed AND conforms to a schema/DTD |
| **Requirements** | Proper nesting, one root, closed tags | All schema constraints satisfied |
| **Can be checked** | By any XML parser | Only with schema/DTD available |
| **Relationship** | Prerequisite for validity | Subset of well-formed documents |

**Examples:**
- Well-formed but not valid: Syntactically correct but missing required elements
- Valid: Syntactically correct AND follows schema rules
- Not well-formed: Has syntax errors (can't be valid)

---

## Question 3(i) [1 mark]

**Question:** If the first extract had omitted the `respStmt` element, would the XML have been legal?

---

### Answer

**Well-formed:** Yes (if tags are still properly closed)

**Valid:** Depends on schema - likely **No** if TEI schema requires `<respStmt>` within `<titleStmt>`.

The schema snippet shows `<zeroOrMore><ref name="model.respLike"/></zeroOrMore>`, suggesting `respStmt` is optional, so it might still be valid.

---

## Question 3(j) [1 mark]

**Question:** If the first extract had omitted the `title` elements, would the XML have been legal?

---

### Answer

**Well-formed:** Yes (syntactically correct)

**Valid:** **No** - The schema shows `<oneOrMore><ref name="title"/></oneOrMore>`, meaning at least one `<title>` is required in `<titleStmt>`.

---

## Question 3(k) [2 marks]

**Question:** This catalogue entry is converted automatically to HTML whenever it changes. What two technologies would most likely be considered for the conversion?

---

### Answer

1. **XSLT (Extensible Stylesheet Language Transformations)**
   - Purpose-built for transforming XML to other formats (HTML, text, different XML)
   - Uses template matching to process XML nodes

2. **XSLT Processor** (e.g., Saxon, Xalan, libxslt)
   - Executes the XSLT transformations
   - Can be integrated into automated pipelines

**Alternative answer:** XQuery could also be used for XML-to-HTML transformation.

---

# Question 4: RDF, Ontologies, and Linked Data [30 marks]

## Context

Here is data presented in a serialisation of a data interchange model:

```turtle
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix oa: <http://www.w3.org/ns/oa#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix myrdf: <http://example.org/> .
@prefix armadale: <https://literary-greats.com/WCollins/Armadale/>;

myrdf:anno-001 a oa:Annotation ;
    dcterms:created "2015-10-13T13:00:00+00:00"^^xsd:dateTime ;
    dcterms:creator myrdf:DL192 ;
    oa:hasBody [
        a oa:TextualBody ;
        rdf:value "Note the use of visual language here."
    ];
    oa:hasTarget [
        a oa:SpecificResource ;
        oa:hasSelector [
            a oa:TextPositionSelector ;
            oa:start 235 ^^xsd:nonNegativeInteger;
            oa:end 300 ^^xsd:nonNegativeInteger ;
        ];
        oa:hasSource armadale:Chapter3/ ;
    oa:motivatedBy oa:commenting ;

myrdf:DL192 a foaf:Person ;
    foaf:name "David Lewis" .
```

---

## Question 4(a)(i) [1 mark]

**Question:** What is the model?

---

### Answer

**RDF (Resource Description Framework)**

---

## Question 4(a)(ii) [1 mark]

**Question:** What is the serialisation format?

---

### Answer

**Turtle (Terse RDF Triple Language)**

---

## Question 4(b) [3 marks]

**Question:** Name two ontologies used in this document.

---

### Answer

1. **Dublin Core** (`dcterms:`) - http://purl.org/dc/terms/
2. **FOAF** (`foaf:`) - http://xmlns.com/foaf/0.1/

Also acceptable:
- **Open Annotation** (`oa:`) - http://www.w3.org/ns/oa#

---

## Question 4(c) [5 marks]

**Question:** For each ontology named, list all properties from the ontology used in this document.

---

### Answer

**Dublin Core (dcterms:):**
- `dcterms:created` - date/time of creation
- `dcterms:creator` - person who created the annotation

**FOAF (foaf:):**
- `foaf:name` - name of the person

**Open Annotation (oa:):**
- `oa:hasBody` - the content of the annotation
- `oa:hasTarget` - what is being annotated
- `oa:hasSelector` - specific selection within target
- `oa:hasSource` - the source document
- `oa:motivatedBy` - reason for annotation
- `oa:start` - start position
- `oa:end` - end position

---

## Question 4(d) [7 marks]

**Question:** A scholar wants annotations about `armadale:Chapter3` with the annotation text and creator name. The following SPARQL doesn't work. Write a correct version.

**Broken query:**
```sparql
SELECT ?body ?creator
WHERE {
  ?annotation a oa:Annotation .
  ?creator ;
  oa:hasBody body .
  hasSource armadale:Chapter3 }
```

---

### Answer

**Corrected SPARQL:**

```sparql
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX armadale: <https://literary-greats.com/WCollins/Armadale/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?bodyText ?creatorName
WHERE {
  ?annotation a oa:Annotation ;
              dcterms:creator ?creator ;
              oa:hasBody ?body ;
              oa:hasTarget ?target .
  ?body rdf:value ?bodyText .
  ?target oa:hasSource armadale:Chapter3 .
  ?creator foaf:name ?creatorName .
}
```

**Fixes made:**
1. Added proper PREFIX declarations
2. Fixed variable syntax (`?body` not `body`)
3. Added `dcterms:creator` predicate
4. Navigated through `oa:hasTarget` to get to `oa:hasSource`
5. Retrieved actual text with `rdf:value`
6. Retrieved creator name with `foaf:name`

---

## Question 4(e) [5 marks]

**Question:** Draw an E/R diagram for web annotations like this, for a backend database.

---

### Answer

**E/R Diagram (using Triple Store approach):**

```
┌─────────────────────────────────────────┐
│                Triples                  │
├─────────────────────────────────────────┤
│ Subject   VARCHAR(256)  PK              │
│ Predicate VARCHAR(256)  PK              │
│ Object    VARCHAR(512)  PK              │
└─────────────────────────────────────────┘
```

**Alternative: Traditional E/R approach:**

```
┌──────────────┐         ┌──────────────┐
│  Annotations │         │   Persons    │
├──────────────┤         ├──────────────┤
│ AnnotationId │──────┐  │ PersonId PK  │
│ Created      │      │  │ Name         │
│ Motivation   │      │  └──────────────┘
│ CreatorId FK │──────┘
└──────┬───────┘
       │
       │ 1:1
       ▼
┌──────────────┐         ┌──────────────┐
│    Bodies    │         │   Targets    │
├──────────────┤         ├──────────────┤
│ BodyId PK    │         │ TargetId PK  │
│ AnnotationId │         │ AnnotationId │
│ BodyType     │         │ SourceURI    │
│ Value        │         │ StartPos     │
└──────────────┘         │ EndPos       │
                         └──────────────┘
```

---

## Question 4(f) [5 marks]

**Question:** Identify the tables needed for a relational implementation and list the keys.

---

### Answer

**Single Triple Table Approach:**

| Table | Primary Key | Description |
|-------|-------------|-------------|
| **Triples** | (Subject, Predicate, Object) | Composite PK, stores all RDF triples |

**OR Traditional Relational Approach:**

| Table | Primary Key | Foreign Keys |
|-------|-------------|--------------|
| **Persons** | PersonId | - |
| **Annotations** | AnnotationId | CreatorId → Persons(PersonId) |
| **Bodies** | BodyId | AnnotationId → Annotations(AnnotationId) |
| **Targets** | TargetId | AnnotationId → Annotations(AnnotationId) |
| **Sources** | SourceId | - |
| **Selectors** | SelectorId | TargetId → Targets(TargetId) |

---

## Question 4(g) [3 marks]

**Question:** Give a MySQL query equivalent for the scholar's SPARQL query from 4(d).

---

### Answer

**Using Triple Store design:**

```sql
SELECT tBodyVal.Object AS BodyText,
       tCreatorName.Object AS CreatorName
FROM Triples tAnno
INNER JOIN Triples tType
    ON tAnno.Subject = tType.Subject
INNER JOIN Triples tBody
    ON tAnno.Subject = tBody.Subject
INNER JOIN Triples tBodyVal
    ON tBody.Object = tBodyVal.Subject
INNER JOIN Triples tCreator
    ON tAnno.Subject = tCreator.Subject
INNER JOIN Triples tCreatorName
    ON tCreator.Object = tCreatorName.Subject
INNER JOIN Triples tTarget
    ON tAnno.Subject = tTarget.Subject
INNER JOIN Triples tSource
    ON tTarget.Object = tSource.Subject
WHERE tType.Predicate = 'rdf:type'
  AND tType.Object = 'oa:Annotation'
  AND tBody.Predicate = 'oa:hasBody'
  AND tBodyVal.Predicate = 'rdf:value'
  AND tCreator.Predicate = 'dcterms:creator'
  AND tCreatorName.Predicate = 'foaf:name'
  AND tTarget.Predicate = 'oa:hasTarget'
  AND tSource.Predicate = 'oa:hasSource'
  AND tSource.Object = 'armadale:Chapter3';
```

**Note:** This demonstrates why SPARQL is more natural for RDF data - the SQL requires many self-joins.

---

# Quick Reference Summary

## SQL Essentials

```sql
-- Transaction control
START TRANSACTION;
-- ... operations ...
COMMIT;  -- or ROLLBACK;

-- User permissions
GRANT SELECT ON database.* TO 'user'@'localhost';

-- View for aggregated data
CREATE VIEW AggView AS SELECT ... GROUP BY ...;
```

## XPath Essentials

```xpath
//element[@attr="value"]  -- Find by attribute
//parent/child/*          -- All children of matching elements
//elem[text()='value']    -- Match by text content
/..                       -- Navigate to parent
```

## SPARQL Essentials

```sparql
PREFIX oa: <http://www.w3.org/ns/oa#>
SELECT ?var1 ?var2
WHERE {
  ?s a oa:Annotation ;
     oa:hasBody ?body .
  ?body rdf:value ?var1 .
}
```

## MongoDB Query Operators

```javascript
db.collection.find({
  "field": {$lt: value}   // Less than
  "field": {$gt: value}   // Greater than
  "date": {$lt: ISODate("YYYY-MM-DD")}
});
```

---

*End of Solution Sheet - September 2022*
