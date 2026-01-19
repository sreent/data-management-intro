# Solution Sheet - September 2024

## Exam Overview

| Section | Questions | Marks |
|---------|-----------|-------|
| Section A | 10 MCQs (Q1a-j) | 40 |
| Section B | Answer 2 of 3 | 60 |
| **Total** | | **100** |

**Note:** Part A and Part B are completed online together on the Inspera platform. This solution sheet covers Section B questions.

---

# Section B

Candidates answer TWO of the following THREE questions.

---

# Question 2: Historical Lute Music Database [30 marks]

## Context

An enthusiast website for historical lute music stores data in CSV files:
- **Sources file**: Library references, names, dates, instruments
- **Concordances file**: Work IDs, composers, locations where work occurs
- **Individual source files** (e.g., NL-At.csv): Pieces with page numbers, keys, titles, composers

---

## Q2(a): Database vs File-Based Approach [6 marks]

**Question:** What might be the advantages and disadvantages of a database approach compared to the file-based approach used here?

---

### Answer

**Advantages of Database Approach:**

| Advantage | Example from Data |
|-----------|-------------------|
| **Data Integrity** | Enforce that `Conc_no` in pieces matches valid concordance |
| **Reduced Redundancy** | Composer names stored once, not repeated |
| **Query Capabilities** | Find all pieces by "V. Gaultier" across all sources |
| **Concurrent Access** | Multiple users can edit safely with transactions |
| **Referential Integrity** | Foreign keys prevent orphaned records |

**Disadvantages of Database Approach:**

| Disadvantage | Impact |
|--------------|--------|
| **Setup Complexity** | Need database server, schema design |
| **Learning Curve** | Users must know SQL instead of editing CSV |
| **Version Control** | Harder to use GitHub for tracking changes |
| **Migration Effort** | Converting existing CSV files requires work |

---

### Revision Notes

**Core Concept:** File-based vs Database Systems

| Aspect | File-Based | Database |
|--------|------------|----------|
| Data Independence | Low | High |
| Redundancy Control | Manual | Automatic |
| Integrity Constraints | None | Enforced |
| Concurrent Access | Problematic | Managed |
| Query Language | None (custom scripts) | SQL |
| Backup/Recovery | Manual | Built-in |

---

## Q2(b): Recommended Database Model [2 marks]

**Question:** What database model would you recommend as the easiest to use, given the current state of the data? Why?

---

### Answer

**Document database (e.g., MongoDB)** would be easiest because:

1. **Semi-structured data**: The CSV files have varying fields and the Concordances field contains a list of locations
2. **Flexible schema**: Can import CSV directly without strict schema
3. **Nested data**: The "Concordances" field contains multiple source/page references that map naturally to arrays

Alternative acceptable answer: **Relational database** because the data already has clear entities (Sources, Concordances, Pieces) with relationships.

---

### Revision Notes

**Choosing a Database Model:**

| Data Characteristic | Best Model |
|--------------------|------------|
| Tabular, fixed schema | Relational |
| Nested, variable fields | Document |
| Highly connected | Graph |
| Key-value lookups | Key-Value |

---

## Q2(c): Relational Database Model [12 marks]

**Question:** Propose a relational model, listing tables, fields, and keys. List any concerns about the data.

---

### Answer

**Proposed Tables:**

```sql
CREATE TABLE Source (
    RefShort VARCHAR(50) PRIMARY KEY,
    RefLong VARCHAR(200),
    Library VARCHAR(200),
    NameGerman VARCHAR(200),
    NameEnglish VARCHAR(200),
    DateRange VARCHAR(50),
    Instrument VARCHAR(100)
);

CREATE TABLE Composer (
    ComposerId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Concordance (
    ConcNo VARCHAR(20) PRIMARY KEY,
    ComposerId INT,
    FOREIGN KEY (ComposerId) REFERENCES Composer(ComposerId)
);

CREATE TABLE Piece (
    PieceId INT PRIMARY KEY AUTO_INCREMENT,
    SourceRef VARCHAR(50) NOT NULL,
    PieceNo INT NOT NULL,
    MusicalKey VARCHAR(20),
    PageNo VARCHAR(20),
    Title VARCHAR(200),
    ComposerId INT,
    ConcNo VARCHAR(20),
    FOREIGN KEY (SourceRef) REFERENCES Source(RefShort),
    FOREIGN KEY (ComposerId) REFERENCES Composer(ComposerId),
    FOREIGN KEY (ConcNo) REFERENCES Concordance(ConcNo),
    UNIQUE (SourceRef, PieceNo)
);

-- Junction table for concordance locations
CREATE TABLE ConcordanceLocation (
    ConcNo VARCHAR(20),
    SourceRef VARCHAR(50),
    PageNo VARCHAR(20),
    PRIMARY KEY (ConcNo, SourceRef, PageNo),
    FOREIGN KEY (ConcNo) REFERENCES Concordance(ConcNo),
    FOREIGN KEY (SourceRef) REFERENCES Source(RefShort)
);
```

**Concerns:**

| Concern | Issue | Resolution |
|---------|-------|------------|
| **Composer ambiguity** | "V. Gaultier or D. Gaultier" - uncertain attribution | Add `Uncertain` boolean field or separate attribution table |
| **Date format** | "1600-1680" is a range, not a date | Store as `DateStart` and `DateEnd` or VARCHAR |
| **Page numbering** | "2v", "24v" uses folio notation | Keep as VARCHAR, add numeric sort field |
| **Concordance parsing** | "NL-At/2v – F-PnVmb7/188" needs splitting | Parse into ConcordanceLocation table |

---

### Revision Notes

**Normalization Applied:**
- **1NF**: All fields atomic (split Concordances list)
- **2NF**: No partial dependencies (Composer separate from Piece)
- **3NF**: No transitive dependencies (Instrument depends on Source, not Piece)

---

## Q2(d): Query for Ungrouped Lachrimae Pieces [6 marks]

**Question:** Write a query that finds all pieces with 'lachrimae' or 'flow' in their names that are not included in a Concordance associated with composer 'John Dowland'.

---

### Answer

```sql
SELECT p.PieceId, p.Title, p.SourceRef, p.PageNo
FROM Piece p
WHERE (LOWER(p.Title) LIKE '%lachrimae%'
       OR LOWER(p.Title) LIKE '%flow%')
  AND (p.ConcNo IS NULL
       OR p.ConcNo NOT IN (
           SELECT c.ConcNo
           FROM Concordance c
           INNER JOIN Composer comp ON c.ComposerId = comp.ComposerId
           WHERE LOWER(comp.Name) LIKE '%john dowland%'
       ));
```

**Alternative using LEFT JOIN:**

```sql
SELECT p.PieceId, p.Title, p.SourceRef, p.PageNo
FROM Piece p
LEFT JOIN Concordance c ON p.ConcNo = c.ConcNo
LEFT JOIN Composer comp ON c.ComposerId = comp.ComposerId
                        AND LOWER(comp.Name) LIKE '%john dowland%'
WHERE (LOWER(p.Title) LIKE '%lachrimae%'
       OR LOWER(p.Title) LIKE '%flow%')
  AND comp.ComposerId IS NULL;
```

---

### Revision Notes

**Query Pattern:** Finding records NOT in a related set

| Method | Syntax |
|--------|--------|
| NOT IN | `WHERE x NOT IN (SELECT ...)` |
| NOT EXISTS | `WHERE NOT EXISTS (SELECT 1 FROM ... WHERE ...)` |
| LEFT JOIN + IS NULL | `LEFT JOIN ... WHERE joined.id IS NULL` |

---

## Q2(e): GRANT Command for Web Application [4 marks]

**Question:** Write an appropriate GRANT command for the account that the web application will use.

---

### Answer

```sql
CREATE USER 'webapp'@'localhost' IDENTIFIED BY 'secure_password';

GRANT SELECT, INSERT ON lutemusic.Source TO 'webapp'@'localhost';
GRANT SELECT, INSERT ON lutemusic.Piece TO 'webapp'@'localhost';
GRANT SELECT, INSERT ON lutemusic.Concordance TO 'webapp'@'localhost';
GRANT SELECT, INSERT ON lutemusic.ConcordanceLocation TO 'webapp'@'localhost';
GRANT SELECT ON lutemusic.Composer TO 'webapp'@'localhost';
```

**Key Points:**
- **SELECT**: Read existing data
- **INSERT**: Add new sources and pieces
- **No UPDATE/DELETE**: Prevent accidental data loss
- **No GRANT on Composer**: Prevent arbitrary composer creation (use admin process)

---

### Revision Notes

**Principle of Least Privilege:**

| Operation | When to Grant |
|-----------|---------------|
| SELECT | Read access needed |
| INSERT | Adding new records |
| UPDATE | Modifying existing records |
| DELETE | Removing records (rarely for web apps) |
| ALL PRIVILEGES | Never for web applications |

---

# Question 3: Poetry Contest XML/TEI [30 marks]

## Context

XML file collecting poetry contest entries with TEI namespace elements for poem structure.

```xml
<competition theme="limericks" date="2024-01-03">
  <entry>
    <authors>
      <author viaf="23156">Edward Lear</author>
    </authors>
    <poem>
      <tei:lg type="stanza">
        <tei:l>There was an old man of Dumbree</tei:l>
        ...
      </tei:lg>
    </poem>
  </entry>
</competition>
```

---

## Q3(a): File Format [1 mark]

**Question:** What is the format of this file?

---

### Answer

**XML (Extensible Markup Language)**

---

## Q3(b): TEI Claim Assessment [3 marks]

**Question:** The competition website says they save data as Text Encoding Initiative files. Are they correct? Give a more specific statement.

---

### Answer

**They are partially correct but imprecise.**

More accurate statement: "The file is **XML that incorporates TEI elements** (specifically `tei:lg` and `tei:l` for line groups and lines) within a custom schema. It is **not a pure TEI document** because:
- The root element and structure (`<competition>`, `<entry>`, `<authors>`) are not TEI elements
- TEI elements are used only for the poem content via a namespace prefix
- A true TEI document would have `<TEI>` as root with `<teiHeader>` and `<text>` children"

---

### Revision Notes

**TEI (Text Encoding Initiative):**
- Standard XML vocabulary for humanities texts
- Root element: `<TEI>`
- Required sections: `<teiHeader>` (metadata), `<text>` (content)
- Common elements: `<lg>` (line group), `<l>` (line), `<p>` (paragraph)

---

## Q3(c): XPath for First Lines [3 marks]

**Question:** Write a simple XPath expression to retrieve the first line from all entries to competitions with theme 'limericks'.

---

### Answer

```xpath
//competition[@theme='limericks']//entry//tei:l[1]
```

Or more explicitly:

```xpath
//competition[@theme='limericks']/entry/poem/tei:lg/tei:l[1]
```

**Explanation:**
- `//competition[@theme='limericks']` - Find competition elements with theme attribute = 'limericks'
- `//entry` - All entry descendants
- `//tei:l[1]` - First line element in each entry (requires namespace binding for `tei:`)

---

### Revision Notes

**XPath Position Predicates:**

| Expression | Meaning |
|------------|---------|
| `[1]` | First child at that level |
| `[last()]` | Last child |
| `[position() <= 3]` | First three |

---

## Q3(d): Relational Model with Judging [12 marks]

**Question:** Design a relational model for the files, adding the ability for judges to give numerical assessments of each entry. Give CREATE commands. Explain choices and Normal Forms.

---

### Answer

```sql
CREATE TABLE Competition (
    CompetitionId INT PRIMARY KEY AUTO_INCREMENT,
    Theme VARCHAR(100) NOT NULL,
    CompDate DATE NOT NULL,
    UNIQUE (Theme, CompDate)
);

CREATE TABLE Author (
    AuthorId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(200) NOT NULL,
    ViafId VARCHAR(50)
);

CREATE TABLE Entry (
    EntryId INT PRIMARY KEY AUTO_INCREMENT,
    CompetitionId INT NOT NULL,
    PoemText TEXT NOT NULL,
    SubmittedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CompetitionId) REFERENCES Competition(CompetitionId)
);

CREATE TABLE EntryAuthor (
    EntryId INT,
    AuthorId INT,
    PRIMARY KEY (EntryId, AuthorId),
    FOREIGN KEY (EntryId) REFERENCES Entry(EntryId),
    FOREIGN KEY (AuthorId) REFERENCES Author(AuthorId)
);

CREATE TABLE Judge (
    JudgeId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(200) NOT NULL
);

CREATE TABLE Assessment (
    AssessmentId INT PRIMARY KEY AUTO_INCREMENT,
    EntryId INT NOT NULL,
    JudgeId INT NOT NULL,
    Score DECIMAL(4,2) NOT NULL,
    AssessedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EntryId) REFERENCES Entry(EntryId),
    FOREIGN KEY (JudgeId) REFERENCES Judge(JudgeId),
    UNIQUE (EntryId, JudgeId)  -- One score per judge per entry
);
```

**Design Choices:**

| Choice | Rationale |
|--------|-----------|
| Separate Author table | Authors may enter multiple competitions |
| EntryAuthor junction | Entries can have multiple authors |
| VIAF ID in Author | Links to authority file for identification |
| PoemText as TEXT | Preserves full poem without line parsing |
| Assessment separate | Allows multiple judges per entry |
| UNIQUE on Assessment | Prevents duplicate judging |

**Normal Forms:**
- **1NF**: All atomic values, no repeating groups
- **2NF**: No partial dependencies (Author info separate from Entry)
- **3NF**: No transitive dependencies (Judge info not dependent on Entry)
- **BCNF**: All determinants are candidate keys

---

## Q3(e): Winning Entry Query [5 marks]

**Question:** Give a query that retrieves the winning (highest scoring) entry for the Limerick challenge of 3 Jan 2024.

---

### Answer

```sql
SELECT e.EntryId, e.PoemText, AVG(a.Score) AS AvgScore
FROM Entry e
INNER JOIN Competition c ON e.CompetitionId = c.CompetitionId
INNER JOIN Assessment a ON e.EntryId = a.EntryId
WHERE c.Theme = 'limericks'
  AND c.CompDate = '2024-01-03'
GROUP BY e.EntryId, e.PoemText
ORDER BY AvgScore DESC
LIMIT 1;
```

**Alternative using subquery:**

```sql
SELECT e.EntryId, e.PoemText,
       (SELECT AVG(Score) FROM Assessment WHERE EntryId = e.EntryId) AS AvgScore
FROM Entry e
INNER JOIN Competition c ON e.CompetitionId = c.CompetitionId
WHERE c.Theme = 'limericks'
  AND c.CompDate = '2024-01-03'
ORDER BY AvgScore DESC
LIMIT 1;
```

---

### Revision Notes

**Finding Maximum with GROUP BY:**

| Method | Use Case |
|--------|----------|
| `ORDER BY ... DESC LIMIT 1` | Simple, gets one winner |
| `HAVING AVG(x) = (SELECT MAX...)` | Gets all ties |
| Window function `RANK()` | Advanced, handles ties elegantly |

---

## Q3(f): XML vs Relational Comparison [6 marks]

**Question:** How do the XML document-based approach and the relational model compare? What works best in each? Would there be any benefit to a hybrid approach?

---

### Answer

**Comparison:**

| Aspect | XML Approach | Relational Approach |
|--------|--------------|---------------------|
| **Poem Storage** | Excellent - preserves structure, line breaks, formatting | Poor - TEXT blob loses structure |
| **Judging/Scores** | Poor - requires custom queries | Excellent - easy aggregation |
| **Author Queries** | Moderate - XPath works but verbose | Excellent - simple JOINs |
| **Schema Flexibility** | High - can add elements easily | Low - requires ALTER TABLE |
| **Data Integrity** | Low - no referential constraints | High - foreign keys enforced |

**What Works Best:**

| Task | Best Approach |
|------|---------------|
| Store poem with formatting | XML |
| Calculate average scores | Relational |
| Find entries by author | Relational |
| Display poem as submitted | XML |
| Generate reports | Relational |

**Hybrid Approach Benefits:**

1. **Store poems as XML in database**: Use MySQL's XML data type or TEXT column
2. **Relational for metadata**: Competition, Author, Judge, Assessment tables
3. **Best of both**: SQL for queries and aggregation, XPath for poem content
4. **Example**: `SELECT EXTRACTVALUE(PoemXml, '//tei:l[1]') FROM Entry`

---

### Revision Notes

**Hybrid Database Approaches:**

| Database | XML Support |
|----------|-------------|
| MySQL | `EXTRACTVALUE()`, `UPDATEXML()` |
| PostgreSQL | `xml` data type, XPath functions |
| SQL Server | `xml` data type, `.query()` method |
| Oracle | `XMLType`, `XMLQUERY()` |

---

# Question 4: Wikidata SPARQL and Belgian Artists [30 marks]

## Context

A researcher queries Wikidata for Belgian artists born before 1600.

---

## Q4(a): Query Language [1 mark]

**Question:** What language does this query use?

---

### Answer

**SPARQL (SPARQL Protocol and RDF Query Language)**

---

## Q4(b): Syntax Corrections [2 marks]

**Question:** Some of the syntax of this query is wrong. Correct it.

---

### Answer

**Errors and Corrections:**

| Error | Line | Correction |
|-------|------|------------|
| `SHOW` should be `SELECT` | Line 1 | `SELECT ?person ?personLabel ?placeLabel ?dob` |
| `{{` should be `{` | Line 2 | Single braces for WHERE clause |
| `}}` should be `}` | End | Single closing brace |
| Missing `?` on `person` | Line 4 | `?person wdt:P19 ?place` |
| Missing `?` on `place` | Line 7 | `?place wdt:P17 ?country` |
| `,` should be `;` | Lines 4-5 | Same subject, different predicates use `;` not `,` |
| `;` should be `.` | Line 6 | End of `?person` triples before new subject `?place` |

**Corrected Query:**

```sparql
SELECT ?person ?personLabel ?placeLabel ?dob
WHERE {
  BIND (wd:Q31 AS ?country)
  BIND (wd:Q483501 AS ?job)

  ?person wdt:P19 ?place ;
          wdt:P569 ?dob ;
          wdt:P106 ?job .

  ?place wdt:P17 ?country .

  FILTER(YEAR(?dob) < 1600)

  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en" .
  }
}
```

---

### Revision Notes

**SPARQL Syntax:**

| Element | Usage |
|---------|-------|
| `.` | End of triple pattern |
| `;` | Same subject, different predicate |
| `,` | Same subject and predicate, different object |
| `{ }` | Single braces for WHERE clause |

---

## Q4(c): Retrieval Less Than 100% [4 marks]

**Question:** What might cause the retrieval of this query to be less than 100%?

---

### Answer

**Reasons for Incomplete Retrieval:**

| Issue | Example |
|-------|---------|
| **Missing data** | Artist has no `wdt:P569` (date of birth) recorded |
| **Missing place link** | Birth place exists but no `wdt:P17` country link |
| **Different occupation** | Artist listed as "painter" not "artist" (Q483501) |
| **Place not in Belgium** | Birth place's country is "Spanish Netherlands" not Belgium |
| **Date precision** | Birth date recorded as century only, not year |
| **No English label** | Artist has name only in Dutch/French |

---

### Revision Notes

**Linked Data Retrieval Issues:**

| Type | Description |
|------|-------------|
| **Coverage** | Not all entities have all properties |
| **Granularity** | Dates may lack precision |
| **Classification** | Multiple valid types for same concept |
| **Historical changes** | Country boundaries change over time |

---

## Q4(d): Unwanted Results [3 marks]

**Question:** Given the purpose of the query, what results might be returned that are not wanted?

---

### Answer

**Unwanted Results:**

| Issue | Example |
|-------|---------|
| **Non-visual artists** | Musicians, writers born in Belgium (occupation = "artist" is broad) |
| **Born in Belgium but not Belgian** | Foreign visitor's child born while traveling |
| **Modern Belgium boundaries** | Places now in Belgium but historically in France/Netherlands |
| **Amateur artists** | People with "artist" as secondary occupation |

---

### Revision Notes

**Precision vs Recall Trade-off:**

| More Specific Query | Effect |
|--------------------|--------|
| Add `wdt:P31 wd:Q5` | Ensure human (not mythological) |
| Use `wdt:P101` (field of work) | Filter to visual arts |
| Check `wdt:P27` too | Cross-reference citizenship |

---

## Q4(e): Place of Birth vs Country of Citizenship [4 marks]

**Question:** How does the query avoid the problem of Belgium not existing before 1830?

---

### Answer

**The query uses place of birth (P19) instead of country of citizenship (P27).**

**How this works:**

1. Query finds the **place** where artist was born (e.g., Antwerp)
2. Then checks if that place's **current country** (P17) is Belgium
3. Wikidata records Antwerp's country as Belgium (Q31) today
4. This works even though in 1525, Antwerp was in Habsburg Netherlands

**Key insight:** Geographic locations persist through political changes. The city of Antwerp still exists and is now in Belgium, even though the country didn't exist when the artist was born there.

**Limitation:** This approach might include artists born in places that are now Belgian but weren't culturally/historically connected to the region (e.g., border towns).

---

### Revision Notes

**Temporal vs Current Data in Wikidata:**

| Property | Typical Value |
|----------|---------------|
| P17 (country) | Usually current country |
| P27 (citizenship) | Historical, may be defunct state |
| P19 (place of birth) | Physical location (persists) |

---

## Q4(f): MongoDB Query for Artworks [6 marks]

**Question:** Give a query for a MongoDB database that returns all artworks made between 1520 and 1530 by artists born in Antwerp.

---

### Answer

**Assuming embedded artist data:**

```javascript
db.artworks.find({
  "dateOfCreation": {
    $gte: ISODate("1520-01-01"),
    $lte: ISODate("1530-12-31")
  },
  "artist.placeOfBirth": "Antwerp"
})
```

**If using year integers:**

```javascript
db.artworks.find({
  "yearCreated": { $gte: 1520, $lte: 1530 },
  "artist.birthPlace": /Antwerp/i
})
```

**If artist is a reference (requires aggregation):**

```javascript
db.artworks.aggregate([
  {
    $lookup: {
      from: "artists",
      localField: "artistId",
      foreignField: "_id",
      as: "artistInfo"
    }
  },
  { $unwind: "$artistInfo" },
  {
    $match: {
      "yearCreated": { $gte: 1520, $lte: 1530 },
      "artistInfo.placeOfBirth": "Antwerp"
    }
  }
])
```

---

### Revision Notes

**MongoDB Query Operators:**

| Operator | Meaning |
|----------|---------|
| `$gte` | Greater than or equal |
| `$lte` | Less than or equal |
| `$regex` or `/pattern/` | Regular expression match |
| `$lookup` | Join with another collection |

---

## Q4(g): Database Model Evaluation [10 marks]

**Question:** Do you think the researcher was right to use an object database for this? Evaluate graph, object, and relational models.

---

### Answer

**Evaluation of Database Models:**

| Model | Pros | Cons |
|-------|------|------|
| **Graph (RDF/SPARQL)** | Natural fit for Wikidata integration; follows links easily; handles varied relationships | Complex for aggregation; requires SPARQL knowledge; may have performance issues |
| **Document/Object (MongoDB)** | Flexible schema for varied artwork metadata; easy to store images; good for read-heavy access | Harder to query across artists; no referential integrity; duplication of artist data |
| **Relational (MySQL)** | Strong for queries and aggregation; data integrity; familiar SQL | Rigid schema; harder to store varying metadata; many tables for artwork attributes |

**Special Considerations for This Case:**

| Factor | Impact |
|--------|--------|
| **Wikidata integration** | Graph model aligns with source data format |
| **Varied metadata** | Document model handles diverse artwork attributes |
| **Analysis queries** | Relational model best for aggregation |
| **Image links** | All models handle equally well |

**Recommendation:**

**Hybrid approach would be best:**

1. **Keep Wikidata as source** for artist biographical data (graph)
2. **Use MongoDB** for artwork details (flexible schema for medium, materials, dimensions)
3. **Cache artist IDs** to link artworks to Wikidata entities

**Why MongoDB alone is suboptimal:**
- Duplicates artist data across artworks
- Harder to update when Wikidata changes
- Loses the rich relationship data from Wikidata

**Assessment:** The researcher's choice is **reasonable but not optimal**. MongoDB works for the artwork catalog but loses the benefits of Wikidata's graph structure for artist relationships.

---

### Revision Notes

**Choosing Database Models:**

| Use Case | Best Model |
|----------|------------|
| Social networks, knowledge graphs | Graph |
| Content management, catalogs | Document |
| Financial, transactional | Relational |
| Mixed requirements | Polyglot persistence |

---

# Quick Reference Summary

## File-Based vs Database Systems

| Aspect | File-Based | Database |
|--------|------------|----------|
| Data Independence | Low | High |
| Redundancy | High | Controlled |
| Integrity | Manual | Enforced |
| Concurrent Access | Problematic | Managed |
| Query Language | Custom scripts | SQL/SPARQL |

## SPARQL Syntax

```sparql
SELECT ?var1 ?var2
WHERE {
  ?subject predicate ?object .    # Triple pattern
  ?subject pred1 ?obj1 ;          # Same subject
           pred2 ?obj2 .          # semicolon continues
  FILTER(condition)
  SERVICE wikibase:label { ... }  # Get labels
}
```

## MongoDB Query Patterns

```javascript
// Simple find
db.collection.find({ field: value })

// Range query
db.collection.find({ year: { $gte: 1520, $lte: 1530 } })

// Aggregation with lookup
db.collection.aggregate([
  { $lookup: { from: "other", localField: "x", foreignField: "y", as: "joined" } },
  { $match: { condition } }
])
```

## XPath Expressions

| Pattern | Meaning |
|---------|---------|
| `//element` | Any descendant |
| `/element` | Direct child |
| `[@attr='value']` | Attribute filter |
| `[1]` | First occurrence |
| `text()` | Text content |

## SQL GRANT Syntax

```sql
GRANT SELECT, INSERT ON database.table TO 'user'@'host';
```

---

*End of Solution Sheet - September 2024*
