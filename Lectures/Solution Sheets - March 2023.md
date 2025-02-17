
## **Question 2: OpenDocument Format (ODF) and RelaxNG Schema**

### (a) What language is this encoded in? [1]

**Answer:**  
**XML**.

**Key Point:** ODF files are essentially ZIP containers holding XML files and other resources (images, metadata). The snippet clearly shows tags (`<office:text>`, `<text:p>`, etc.) typical of XML.

---

### (b) What data structure does it use? [1]

**Answer:**  
A **tree** structure.

**Key Point:**  
- XML is hierarchical: a single root element contains nested child elements, forming a tree.

---

### (c) List the two namespaces that this document uses. [2]

**Answer:**  
1. `urn:oasis:names:tc:opendocument:xmlns:office:1.0`  
2. `urn:oasis:names:tc:opendocument:xmlns:text:1.0`

**Key Point:**  
- In the snippet, elements like `<office:text>` and `<text:p>` demonstrate these two namespaces, commonly declared as `xmlns:office="..."` and `xmlns:text="..."`.

---

### (d) What would the XPath expression `//text:list-item/text:p` return? Would it be different from `//text:list//text:p`? [4]

**Answer (Short Form):**

- `//text:list-item/text:p` returns all `<text:p>` elements that are **direct children** of `<text:list-item>`.  
- `//text:list//text:p` returns **all descendant** `<text:p>` elements (any level below `<text:list>`).

In **this** snippet, both yield the same three strings—“Trees,” “Graphs,” “Relations”—because the `<text:p>` elements happen to be direct children anyway. In a more deeply nested document, the results could differ.

---

### (e) How does this code help us assess if the document above is **well‑formed**? [2]

**Answer:**  
Strictly speaking, **it does not**. A RelaxNG schema checks higher-level structure and element rules, but **well‑formedness** concerns basic XML syntax (properly nested tags, one root element, matching start/end tags). The XML parser itself enforces well‑formedness **before** applying the schema.

---

### (f) How does this code help us assess if the document above is **valid**? [2]

**Answer:**  
By comparing the document’s elements, attributes, and order against the RelaxNG schema definitions. If the XML follows these structural rules (e.g., `<text:list>` can have optional `<text:list-header>` and multiple `<text:list-item>`), it is **valid**. Otherwise, validation fails.

---

### (g) Which part or parts of the document is this relevant to? [2]

**Answer:**  
Specifically to `<text:list>` elements and their children (`<text:list-header>`, `<text:list-item>`). The RelaxNG snippet shown defines these list structures.

---

### (h) Give an example of an element that would **not** be valid given this schema code (assume that `text-list-attr` only defines attributes). [3]

**Answer (Example):**
```xml
<text:list>
  <text:list-header>Header Content</text:list-header>
  <text:list-item>Item Content</text:list-item>
  <text:invalid-element>Invalid Content</text:invalid-element>
</text:list>
```
`<text:invalid-element>` is not in the schema, so it is invalid.

---

### (i) Assess the suitability of this data structure for encoding word processing documents. What advantages or disadvantages would a relational model bring? [13]

**Answer (Outline):**

1. **XML/Tree Advantages**  
   - **Natural Hierarchy**: Word processing often involves nested structures (sections → paragraphs → runs). XML fits well.  
   - **Flexibility**: Easy to embed metadata, styles, or additional elements (footnotes, comments).  
   - **Interoperability**: ODF and other office formats (like OOXML) are standardized XML-based formats.

2. **XML/Tree Disadvantages**  
   - **Verbosity**: Repeated tags lead to larger file size.  
   - **Complex Queries**: Though XPath and XQuery are powerful, they can be less intuitive than SQL for large-scale tabular queries.

3. **Relational Model Advantages**  
   - **Strong Data Integrity**: Primary/foreign keys, constraints, and transaction safety.  
   - **Well-Suited to Tabular Queries**: If queries involve counting, aggregating, or filtering by structured fields (e.g., all docs authored by X in 2022).

4. **Relational Model Disadvantages**  
   - **Poor Fit for Deeply Nested Data**: Document sections, paragraphs, headings, etc. can require many join tables to replicate the natural XML tree.  
   - **Less Flexible for Markup**: A word-processing document may have unpredictable structure (variable depth, embedded styles), which is cumbersome in rigid schemas.

5. **Conclusion**  
   - **XML** is ideal for hierarchical, text-centric word-processing docs with complex markup.  
   - **Relational** is great for structured, tabular data. Trying to store *complete* document markup in SQL tables can become unwieldy.

---

## **Question 3: MusicBrainz / Linked Data**

The snippet given shows Turtle (RDF) data from MusicBrainz, e.g.:

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix schema: <http://schema.org/> .

<http://musicbrainz.org/artist/0d79fe8e-ba27-4859-bb8c-2f255f346853>
   schema:foundingDate "2013-06-13"^^schema:Date ;
   schema:member [
      schema:member <http://musicbrainz.org/artist/09720eec-3871-49d5-932d-eb7542768cd3> ;
      schema:startDate "2013-06-13"^^schema:Date ;
      rdf:type schema:OrganizationRole
   ],
   [ ... another role blank node ... ] ;
   schema:name "BTS" ;
   schema:sameAs <http://bts-official.jp/> .
```
…and so on.

### (a) What (approximately) was the type that we put into the Accept header? [1]

**Answer:**  
**`text/turtle`** (sometimes also written as `text/turtle` or `application/turtle`).  

**Reasoning:** The snippet is in Turtle format, indicated by the `@prefix` lines and the dot-terminated triples.

---

### (b) To indicate that someone is a member of a band using this model, the person is associated with a role (schema:OrganizationRole) via `schema:member`, and that role is also associated with the group via `schema:member`. What is the **full URL** of the predicate `schema:member`? [1]

**Answer:**  
```
http://schema.org/member
```

---

### (c) How many band members of BTS are listed in this snippet? [1]

**Answer:**  
**2** members.

**Reasoning:** The snippet shows two separate blank nodes under `schema:member`, each linking to a different individual artist’s URI (e.g., JIN and at least one other member). The rest (like Megan Thee Stallion) are not counted as “BTS members” in that sense.

---

### (d) Comment on the way the `schema:member` predicate is used in this context. [3]

**Answer (Short Explanation):**

- The data uses a **role-based** structure:  
  1. The **band** (`<http://musicbrainz.org/artist/0d79fe8e-...>`) has `schema:member` references to **blank nodes** (of type `schema:OrganizationRole`).  
  2. Each blank node *itself* has a `schema:member` property pointing to an actual person’s URI (e.g., `<http://musicbrainz.org/artist/09720eec-...>`).  
  3. This approach allows storing **additional attributes** (like `schema:startDate`) on the membership role (rather than directly on the band–person relationship).  

It’s effectively reifying the membership so that more details (start date, role name) can be attached.

---

### (e) What type(s) are associated with the entity having a `schema:name` of "JIN"? [1]

**Answer:**  
He is typed as both **`schema:MusicGroup`** and **`schema:Person`**.

**Comment:** The snippet includes:
```
<http://musicbrainz.org/artist/09720eec-...>
    schema:name "JIN" ;
    rdf:type schema:MusicGroup ,
             schema:Person .
```
(It’s common in MusicBrainz data that an individual can also appear with `schema:MusicGroup` due to how the RDF is generated.)

---

### (f) Consider the SPARQL query:

```sparql
SELECT ?a ?b WHERE {
  mba:9fe8e-ba27-4859-bb8c-2f255f346853 schema:member ?c .
  ?c schema:startDate ?b ;
     schema:member ?d .
  ?d schema:name ?a .
}
```
What prefixes need to be defined for this to work (give the full declarations)? [1]

**Answer:**
```sparql
PREFIX mba: <http://musicbrainz.org/artist/>
PREFIX schema: <http://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
```
(At minimum, the first two are essential for `mba:` and `schema:`, while `rdf:` is often needed if we rely on `rdf:type` in the query.)

---

### (g) What would the query return? [2]

**Answer (Short Explanation):**  
- The query returns pairs of `(?a, ?b)` where `?a` is the **name** of a BTS member (e.g., “JIN”) and `?b` is the **start date** stored on that member’s “OrganizationRole”.  
- Essentially: **“member name”** and **“the date they started”** for all membership roles connected to the band entity `mba:9fe8e-ba27-...`.

---

### (h) This data represents an export from a relational database. Construct an ER diagram providing a model that could accommodate the instance data above. [6]

**Answer (One Possible Model):**

A simple approach is:

- **`Artist`** entity  
  - PK: `ArtistID`  
  - Attributes: `Name`, `Type` (“Person” or “MusicGroup”), `FoundingDate` (when `Type=MusicGroup`)

- **`Membership`** bridging entity  
  - PK: `MembershipID`  
  - FK1: `BandID` → `Artist(ArtistID)` (the group)  
  - FK2: `MemberID` → `Artist(ArtistID)` (the person)  
  - Attributes: `StartDate`, possibly `RoleName` or similar

Diagrammatically (simplified notation):
```
[Artist] 1 --< (Membership) >-- 1 [Artist]

   Artist(ArtistID, Name, Type, FoundingDate)
   Membership(MembershipID, BandID, MemberID, StartDate, RoleName)
```
Where `BandID` references an Artist row of `Type=MusicGroup`, and `MemberID` references an Artist row of `Type=Person`.

---

### (i) Give the CREATE TABLE commands for two tables based on your ER diagram. [4]

**Answer (Illustrative Example):**

```sql
CREATE TABLE Artist (
  ArtistID      INT PRIMARY KEY,
  Name          VARCHAR(100) NOT NULL,
  Type          VARCHAR(20)  NOT NULL,   -- e.g. 'Person' or 'MusicGroup'
  FoundingDate  DATE         NULL        -- only relevant if Type='MusicGroup'
);

CREATE TABLE Membership (
  MembershipID  INT PRIMARY KEY,
  BandID        INT NOT NULL,
  MemberID      INT NOT NULL,
  StartDate     DATE,
  RoleName      VARCHAR(100),
  FOREIGN KEY (BandID) REFERENCES Artist(ArtistID),
  FOREIGN KEY (MemberID) REFERENCES Artist(ArtistID)
);
```
- Real-world schemas might add indexes, constraints, or other fields, but this covers the basic relationships and keys.

---

### (j) Suggest a MySQL query to check whether any band member in the database is recorded as joining **before** the founding date of their band. [5]

**Answer:**
```sql
SELECT aMember.Name AS MemberName,
       aBand.Name   AS BandName,
       m.StartDate,
       aBand.FoundingDate
FROM Membership m
JOIN Artist aBand
  ON m.BandID = aBand.ArtistID
JOIN Artist aMember
  ON m.MemberID = aMember.ArtistID
WHERE m.StartDate < aBand.FoundingDate;
```
- This identifies anomalies where the membership `StartDate` precedes the band’s `FoundingDate`.

---

### (k) MusicBrainz make their data available as both a downloadable database dump and as Linked Data. What are the benefits and disadvantages of each approach? [5]

**Answer (Summary):**

1. **Database Dump**  
   - **Pros**:  
     - Full offline snapshot for large-scale or analytical use; no network delays.  
     - You fully control indexing, queries, backups once downloaded.  
   - **Cons**:  
     - Data can become **stale** quickly; must re-download or sync to stay updated.  
     - Large storage overhead.

2. **Linked Data**  
   - **Pros**:  
     - **Real-time** updates: always the latest data from the provider.  
     - **Easy interlinking**: Connect with other linked datasets using common URIs (semantic web).  
   - **Cons**:  
     - Dependent on network/connectivity; queries can be slow or unavailable if the endpoint is down.  
     - Less local control: formatting or structural changes on the remote side can break clients.

---

## **Question 4: 16th-Century European Music Records**

### (a) This model doesn't allow storing the order or coordinates for lines of music on a page. How could this be fixed? [3]

**Answer:**  
Include attributes (in the **Line** entity) such as:
1. `LineOrder` (an integer) to preserve the correct sequence of lines on a page.  
2. `XCoordinate`, `YCoordinate` (floats/integers) to store the visual position of each line if needed for layout.

**Reasoning:** This prevents “jumbled” retrieval (since lines can be sorted by `LineOrder`) and supports precise layout if x/y coordinates matter.

---

### (b) Some books are published in tablebook format with multiple parts/voices and different regions on each page. Add these aspects to the model. [8]

**Answer (Outline):**

You can add:
1. An **`InstrumentOrVoicePart`** entity to handle multiple parts/voices.  
2. A **`Region`** entity to subdivide each page into distinct areas (especially for lines running in different directions).

**Possible ER Extension (simplified):**
```
Piece --< Line >-- Region
       |
       --> (InstrumentOrVoicePart)
Page --< Region
```
Where each **Line** record references:
- which **Piece** it belongs to,  
- which **Page** (and thus possibly which **Region** on that page),  
- which **Part** (soprano, tenor, violin, etc.).

---

### (c) List the tables, primary keys, and foreign keys for a relational implementation of your modified model. [7]

**Answer (Example Schema):**

1. **Piece**  
   - PK: `PieceID`  
   - Attributes: `Title`, etc.

2. **Page**  
   - PK: `PageID`  
   - Attributes: `BookID` (FK to `Book(BookID)` if the Book table exists), etc.

3. **Region**  
   - PK: `RegionID`  
   - FK: `PageID` → `Page(PageID)`  
   - Attributes: `Description` (optionally `RegionCoordinates`, etc.)

4. **InstrumentOrVoicePart**  
   - PK: `PartID`  
   - Attributes: `PartName`

5. **Line**  
   - PK: `LineID`  
   - FKs:  
     - `PageID` → `Page(PageID)`  
     - `PieceID` → `Piece(PieceID)`  
     - `RegionID` → `Region(RegionID)` (optional if lines must belong to a region)  
     - `PartID` → `InstrumentOrVoicePart(PartID)`  
   - Attributes: `LineOrder`, `XCoordinate`, `YCoordinate`, etc.

---

### (d) Give a query to list pieces with the total number of lines of music that they occupy. [5]

**Answer:**
```sql
SELECT p.Title, COUNT(*) AS TotalLines
FROM Piece p
JOIN Line l ON p.PieceID = l.PieceID
GROUP BY p.Title;
```
- Aggregates how many lines (`COUNT(*)`) each piece has, grouping by piece title.

---

### (e) Assess the suitability of this data structure for a relational model, and compare it with ONE other database model (XML-based, document-based, or Linked Data graph). [7]

**Answer (Overview):**

1. **Relational Model Suitability**  
   - **Pros**: Clear, tabular structure for pages, lines, pieces.  SQL handles numeric queries (like how many lines per piece) very well.  Strong integrity via FK constraints.  
   - **Cons**: Complex hierarchical layouts (tablebook with different voices, rotating staves) may require multiple extra tables or cross‐references.  Unstructured or highly variable data can be awkward.

2. **Comparison Example—XML-Based Tree**  
   - **XML Pros**: Easily models **hierarchical** or nested document structures (like lines, sublines, textual annotations). Native tagging for “voice,” “layout,” etc.  
   - **XML Cons**: Large overhead for frequent queries or aggregations.  Not as straightforward for “relational” queries with lots of joins.

3. **Conclusion**  
   - **Relational**: Great if the primary operations are tabular queries (counts, listing pieces vs. lines).  
   - **XML**: More natural if you must preserve or manipulate **complex hierarchical** or “markup-like” information.  

