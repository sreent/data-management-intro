# Solution Sheet - September 2023

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

# Question 1: Linked Data Question [30 marks]

## Context

RDF document retrieved from http://babelnet.org/rdf/post_n_EN:

```turtle
@prefix bn: <http://babelnet.org/rdf/> .
@prefix lemon: <http://www.lemon-model.net/lemon#> .
@prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#> .

bn:post_n_EN a lemon:LexicalEntry ;
    lemon:canonicalForm <http://babelnet.org/rdf/post_n_EN/canonicalForm> ;
    lemon:language "EN" ;
    lexinfo:partOfSpeech lexinfo:noun .
```

---

## Q1(a)(i): Generic Data Model [1 mark]

**Question:** What is the generic data model this information is represented in?

---

### Answer

**RDF (Resource Description Framework)**

---

### Revision Notes

**RDF Basics:**
- Data model for describing resources as subject-predicate-object triples
- Foundation for the Semantic Web and Linked Data
- Can be serialized in multiple formats (Turtle, RDF/XML, N-Triples, JSON-LD)

---

## Q1(a)(ii): Serialization Format [1 mark]

**Question:** What is the serialisation format used for the data model?

---

### Answer

**Turtle (Terse RDF Triple Language)**

Evidence:
- `@prefix` declarations
- Semicolon (`;`) to continue same subject with different predicates
- Period (`.`) to end statement

---

### Revision Notes

**RDF Serialization Formats:**

| Format | Characteristics |
|--------|-----------------|
| Turtle | Human-readable, `@prefix`, `;` and `.` syntax |
| RDF/XML | XML-based, verbose |
| N-Triples | One triple per line, no prefixes |
| JSON-LD | JSON-compatible, uses `@context` |

---

## Q1(b): Interpretation Debate [4 marks]

**Question:** One friend says it's impossible to know what word this RDF is talking about without more triples. Another says it's clearly the English word "post" as a noun. To what extent is either right? What further information would help?

---

### Answer

**Both friends have a point:**

| Friend | Argument | Validity |
|--------|----------|----------|
| Friend 1 (Skeptic) | The actual word "post" isn't shown in these triples - only a URI reference to `canonicalForm` | **Partially correct** - strictly speaking, the written representation is in a linked resource |
| Friend 2 (Pragmatist) | The URI `post_n_EN` strongly suggests "post", and we see language="EN" and partOfSpeech=noun | **Practically correct** - context clues are clear |

**What's Missing:**
- The actual `writtenRep` property value "post" is in the linked document at `/canonicalForm`
- Without following that link, the word itself isn't explicitly stated

**Further information needed:**
- Fetch `<http://babelnet.org/rdf/post_n_EN/canonicalForm>` to see `lemon:writtenRep "post"`

---

### Revision Notes

**Linked Data Principles:**
- URIs identify things
- Dereferencing URIs should return useful information
- Link to other URIs to enable discovery

---

## Q1(c)(i): SPARQL Query for All Nouns [6 marks]

**Question:** Write a SPARQL query that finds the written representation and language for all nouns.

---

### Answer

```sparql
PREFIX lemon:   <http://www.lemon-model.net/lemon#>
PREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>

SELECT ?writtenRep ?lang
WHERE {
  ?lexEntry a lemon:LexicalEntry ;
            lemon:canonicalForm ?form ;
            lemon:language ?lang ;
            lexinfo:partOfSpeech lexinfo:noun .

  ?form lemon:writtenRep ?writtenRep .
}
```

**Explanation:**
- Find all `LexicalEntry` resources with `partOfSpeech` = `noun`
- Follow the `canonicalForm` link to get the `writtenRep`
- Return both the written form and language

---

### Revision Notes

**SPARQL Pattern Matching:**

| Pattern | Meaning |
|---------|---------|
| `?x a :Class` | Find instances of Class |
| `?x :prop ?y` | Match property values |
| `;` | Same subject, different predicate |
| `.` | End of triple pattern |

---

## Q1(c)(ii): SPARQL Query for "post" [4 marks]

**Question:** Write a SPARQL query that finds the language and part of speech for all words whose canonical form is written "post".

---

### Answer

```sparql
PREFIX lemon:   <http://www.lemon-model.net/lemon#>
PREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>

SELECT ?language ?pos
WHERE {
  ?lexEntry a lemon:LexicalEntry ;
            lemon:canonicalForm ?form ;
            lemon:language ?language ;
            lexinfo:partOfSpeech ?pos .

  ?form lemon:writtenRep "post" .
}
```

**Explanation:**
- Filter for entries where the canonical form's `writtenRep` is exactly "post"
- Return the language and part of speech for each match

---

## Q1(d)(i): Role of Ontology Document [1 mark]

**Question:** What is the role of this document (the lemon ontology extract)?

---

### Answer

**Ontology/Schema Definition**

It defines the classes (`LexicalSense`, `SenseDefinition`) and properties (`:definition`, `:value`) that structure lexical data in the Lemon model.

---

## Q1(d)(ii): Format of Ontology [1 mark]

**Question:** What format is it in?

---

### Answer

**Turtle (RDF serialization format)**

Could also be RDF/XML depending on how it's served.

---

## Q1(d)(iii): OWL Prefix [1 mark]

**Question:** To what does the 'owl' prefix refer?

---

### Answer

**OWL (Web Ontology Language)**

- Namespace: `http://www.w3.org/2002/07/owl#`
- Provides expressive ontology constructs like `owl:Class`, `owl:ObjectProperty`, `owl:disjointWith`

---

## Q1(d)(iv): Write Definition Triples [4 marks]

**Question:** Write triples to provide one definition for the English noun "post".

---

### Answer

```turtle
@prefix lemon: <http://www.lemon-model.net/lemon#> .
@prefix bn: <http://babelnet.org/rdf/> .
@prefix ex: <http://example.org/> .

bn:post_n_EN_sense a lemon:LexicalSense ;
    lemon:definition ex:post_n_EN_def .

ex:post_n_EN_def a lemon:SenseDefinition ;
    lemon:value "A piece of wood or metal set upright to support something, or a position of employment."@en .
```

**Structure:**
1. Create a `LexicalSense` for the word
2. Link it to a `SenseDefinition` via `:definition`
3. Provide the actual text via `:value`

---

## Q1(e): ER Diagram for Relational Implementation [7 marks]

**Question:** Sketch an ER diagram for a relational implementation of this model. Include cardinality.

---

### Answer

**Entities and Relationships:**

```
LexicalEntry (1) ----< (M) Form
     |
     | (1)
     |
     v
    (M)
LexicalSense (1) ----< (M) SenseDefinition
```

**Tables:**

| Table | Columns | Keys |
|-------|---------|------|
| LexicalEntry | LexicalEntryId (PK), Language, PartOfSpeech | PK: LexicalEntryId |
| Form | FormId (PK), LexicalEntryId (FK), WrittenRep | FK → LexicalEntry |
| LexicalSense | SenseId (PK), LexicalEntryId (FK) | FK → LexicalEntry |
| SenseDefinition | DefId (PK), SenseId (FK), TextValue | FK → LexicalSense |

**Cardinalities:**
- One LexicalEntry can have many Forms (1:M)
- One LexicalEntry can have many LexicalSenses (1:M)
- One LexicalSense can have many SenseDefinitions (1:M)

---

# Question 2: ER Question - Estate Agency [30 marks]

## Context

Estate agency database tracking sellers, properties, agents, buyers, offers, and viewings.

---

## Q2(a): Add Cardinality [3 marks]

**Question:** Add cardinality indications for the ER diagram.

---

### Answer

| Relationship | Cardinality | Explanation |
|--------------|-------------|-------------|
| Seller - Property | 1:M | One seller can own many properties; each property has one seller |
| Estate Agent - Property | 1:M | One agent handles many properties; each property has one agent |
| Property - Offers | 1:M | One property can have many offers; each offer is for one property |
| Property - Views | 1:M | One property can have many viewings |
| Buyer - Offers | 1:M | One buyer can make many offers; each offer is from one buyer |
| Buyer - Views | 1:M | One buyer can have many viewings |

---

## Q2(b): Adapt to Relational Model [5 marks]

**Question:** How would you adapt this to a relational model? Be specific about new entities, relations, or attributes.

---

### Answer

**Adaptations needed:**

1. **Convert diamond relationships to tables:**
   - `Offers` becomes a table with FKs to Property and Buyer
   - `Views` becomes a table with FKs to Property and Buyer

2. **Add surrogate keys** (recommended but optional if using natural keys):
   - PropertyId, SellerId, AgentId, BuyerId, OfferId, ViewId

3. **Resolve M:N if present:**
   - Views and Offers are already associative entities

4. **Add timestamp/date columns:**
   - OfferDate, ViewDate for tracking when events occur

---

## Q2(c): List Tables, Primary and Foreign Keys [6 marks]

**Question:** List the tables, primary and foreign keys for a relational implementation.

---

### Answer

| Table | Columns | PK | Foreign Keys |
|-------|---------|-----|--------------|
| Seller | Name (PK), Address, PhoneNumber | Name | - |
| EstateAgent | Name (PK) | Name | - |
| Buyer | Name (PK), Address, PhoneNumber | Name | - |
| Property | Address (PK), Type, Bedrooms, AskingPrice, SellerName, AgentName | Address | SellerName → Seller, AgentName → EstateAgent |
| Offers | PropertyAddress, BuyerName, OfferDate, OfferStatus, OfferValue | (PropertyAddress, BuyerName, OfferDate) | PropertyAddress → Property, BuyerName → Buyer |
| Views | PropertyAddress, BuyerName, ViewDate | (PropertyAddress, BuyerName, ViewDate) | PropertyAddress → Property, BuyerName → Buyer |

---

## Q2(d): MySQL CREATE Command [3 marks]

**Question:** Give the MySQL command for creating one of those tables.

---

### Answer

```sql
CREATE TABLE Property (
    Address VARCHAR(200) PRIMARY KEY,
    Type VARCHAR(50),
    Bedrooms INT,
    AskingPrice DECIMAL(12, 2),
    SellerName VARCHAR(100) NOT NULL,
    AgentName VARCHAR(100) NOT NULL,
    FOREIGN KEY (SellerName) REFERENCES Seller(Name),
    FOREIGN KEY (AgentName) REFERENCES EstateAgent(Name)
);
```

---

## Q2(e)(i): Commission Query [6 marks]

**Question:** Write a MySQL query to calculate and list the commission earned since 1 January 2023 for each Estate Agent. Commission is 1% of sale price.

---

### Answer

```sql
SELECT
    p.AgentName AS EstateAgent,
    SUM(o.OfferValue * 0.01) AS TotalCommission
FROM Property p
INNER JOIN Offers o ON p.Address = o.PropertyAddress
WHERE o.OfferStatus = 'sale completed'
  AND o.OfferDate >= '2023-01-01'
GROUP BY p.AgentName;
```

**Explanation:**
- Join Property with Offers to get agent for each sale
- Filter for completed sales since Jan 1, 2023
- Calculate 1% commission and sum per agent

---

## Q2(e)(ii): Top Earning Agent [2 marks]

**Question:** Modify your query to list just the top earning agent.

---

### Answer

```sql
SELECT
    p.AgentName AS EstateAgent,
    SUM(o.OfferValue * 0.01) AS TotalCommission
FROM Property p
INNER JOIN Offers o ON p.Address = o.PropertyAddress
WHERE o.OfferStatus = 'sale completed'
  AND o.OfferDate >= '2023-01-01'
GROUP BY p.AgentName
ORDER BY TotalCommission DESC
LIMIT 1;
```

---

## Q2(f): Document Database Consideration [5 marks]

**Question:** Give reasons specific to this use case for why a document database might be good or bad.

---

### Answer

**Reasons FOR Document Database:**

| Advantage | Specific Example |
|-----------|------------------|
| Flexible property details | Different property types have different attributes (flat vs house vs land) |
| Embedded media | Store property photos, descriptions as embedded documents |
| Variable offer history | Embed all offers within property document |

**Reasons AGAINST Document Database:**

| Disadvantage | Specific Example |
|--------------|------------------|
| Commission queries harder | Aggregating across agents requires map-reduce or complex pipelines |
| Transactional integrity | Offer status changes need ACID guarantees (made → accepted → completed) |
| Cross-entity queries | Finding all properties viewed by a buyer requires joins |
| Data duplication | Agent info repeated in each property document |

**Conclusion:** Relational is better for this use case due to structured relationships and transactional requirements.

---

# Question 3: IR/Document DB Question - Hathi Trust [30 marks]

## Context

Hathi Trust Digital Library uses ML to classify book languages. German classifier: 80% precision, 88% recall.

---

## Q3(a): True German Books Calculation [2 marks]

**Question:** If the system lists 2,200,000 books as being in German, how many are likely to be in German?

---

### Answer

**Precision = True Positives / (True Positives + False Positives) = 80%**

True Positives = 2,200,000 × 0.80 = **1,760,000 books**

---

### Revision Notes

**Precision vs Recall:**

| Metric | Formula | Meaning |
|--------|---------|---------|
| Precision | TP / (TP + FP) | Of retrieved items, how many are relevant |
| Recall | TP / (TP + FN) | Of relevant items, how many were retrieved |

---

## Q3(b): Total German Books Estimate [3 marks]

**Question:** How many books in the whole collection are likely to be in German?

---

### Answer

**Recall = True Positives / All Actual German Books = 88%**

All German Books = True Positives / Recall = 1,760,000 / 0.88 = **2,000,000 books**

---

## Q3(c): Why Danish 100% Precision is Better for ML [5 marks]

**Question:** Danish is identified with 100% precision and 76% recall. Why might this be more useful for ML training than German's accuracy?

---

### Answer

**For ML training data, precision is more important than recall:**

| Factor | Impact |
|--------|--------|
| **Data purity** | 100% precision means every labeled Danish book IS Danish - no noise |
| **Training quality** | ML models learn wrong patterns from mislabeled examples |
| **Smaller but clean** | Better to have 76% of Danish books that are ALL correct than 88% with 20% wrong |
| **False positives hurt more** | A non-Danish book labeled Danish teaches wrong language patterns |

**Trade-off:** You miss 24% of Danish books (lower recall), but what you have is guaranteed correct.

---

## Q3(d): F1 Measure Definition [2 marks]

**Question:** What is an F1-measure?

---

### Answer

**F1 = Harmonic mean of Precision and Recall**

$$F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}$$

- Balances precision and recall into single metric
- Ranges from 0 to 1 (higher is better)
- Penalizes extreme imbalance between precision and recall

---

## Q3(e): MongoDB Find Command [1 mark]

**Question:** What does `db.books.find({ lang: "German" })` do?

---

### Answer

**Queries the `books` collection and returns all documents where the `lang` field equals "German".**

---

## Q3(f): 19th Century Query [5 marks]

**Question:** Rewrite the command to include only volumes published in the nineteenth century.

---

### Answer

```javascript
db.books.find({
    lang: "German",
    year: { $gte: 1800, $lt: 1900 }
})
```

**Explanation:**
- `$gte: 1800` - year greater than or equal to 1800
- `$lt: 1900` - year less than 1900
- This selects years 1800-1899 (the 19th century)

---

## Q3(g): Add Text Search for "Strudel" [2 marks]

**Question:** How would you adjust your query to include only books containing the word "Strudel"?

---

### Answer

```javascript
db.books.find({
    lang: "German",
    year: { $gte: 1800, $lt: 1900 },
    text: { $regex: /Strudel/i }
})
```

**Alternative with text index:**
```javascript
db.books.find({
    lang: "German",
    year: { $gte: 1800, $lt: 1900 },
    $text: { $search: "Strudel" }
})
```

---

## Q3(h): Document DB vs XML/TEI Decision Factors [10 marks]

**Question:** What factors should the researcher consider when choosing between enriching the document database or switching to XML/TEI?

---

### Answer

**Factors to Consider:**

| Factor | Document DB (MongoDB) | XML/TEI Database |
|--------|----------------------|------------------|
| **Structural encoding** | Limited - flat or nested JSON | Excellent - hierarchical markup for chapters, paragraphs, footnotes |
| **Query capability** | Simple field queries, aggregation pipeline | XQuery/XPath for fine-grained text structure queries |
| **Standards compliance** | Proprietary format | TEI is scholarly standard, aids interoperability |
| **Scalability** | Excellent horizontal scaling | Can be challenging for very large corpora |
| **Flexibility** | Easy schema changes | Schema is more rigid but well-defined |
| **Existing tools** | Many general-purpose tools | Specialized TEI tools, scholarly community support |
| **Preservation** | Format may change | TEI is archival standard for humanities |
| **Mixed content** | Harder to represent | Natural fit for text with inline markup |
| **Full-text search** | Good with text indexes | Native support in XML databases |
| **Integration** | Easy with web APIs | May need transformation for web use |

**Recommendation depends on:**
1. **Primary use case** - If detailed textual analysis, TEI is better
2. **Scale** - If millions of books with simple queries, MongoDB is better
3. **Interoperability** - If sharing with other scholars, TEI is standard
4. **Development resources** - MongoDB has more general developer familiarity

---

# Quick Reference Summary

## RDF/SPARQL

```sparql
PREFIX prefix: <uri>
SELECT ?vars
WHERE {
  ?s ?p ?o .           # Triple pattern
  ?s a :Class .        # Type check
  FILTER (condition)   # Filter results
}
```

## MongoDB Query Patterns

```javascript
// Basic find
db.collection.find({ field: value })

// Range query
db.collection.find({ year: { $gte: 1800, $lt: 1900 } })

// Text search
db.collection.find({ text: { $regex: /pattern/i } })

// Aggregation
db.collection.aggregate([
  { $match: { ... } },
  { $group: { _id: "$field", total: { $sum: 1 } } }
])
```

## Precision and Recall

| Metric | Formula | Use Case |
|--------|---------|----------|
| Precision | TP/(TP+FP) | When false positives are costly |
| Recall | TP/(TP+FN) | When missing items is costly |
| F1 | 2PR/(P+R) | Balance both concerns |

---

*End of Solution Sheet - September 2023*
