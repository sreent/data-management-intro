
# **Question 1: Linked Data Question**

### (a)  

```turtle
@prefix bn: <http://babelnet.org/rdf/> .
@prefix lemon: <http://www.lemon-model.net/lemon#> .
@prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#> .

bn:post_n_EN a lemon:LexicalEntry ;
    lemon:canonicalForm <http://babelnet.org/rdf/post_n_EN/canonicalForm> ;
    lemon:language "EN" ;
    lexinfo:partOfSpeech lexinfo:noun .
```

**(i) What is the generic data model?**  
**Answer (1 mark):**  
This is **RDF** (Resource Description Framework).

**(ii) What is the serialization format?**  
**Answer (1 mark):**  
It’s in **Turtle** format (Terse RDF Triple Language), evidenced by the `@prefix` notation and the `;`/`.` structure.

---

### (b)  

> *Friend 1 claims it’s impossible to know the actual word or part of speech without more triples; Friend 2 claims it’s obviously the English noun “post.”*

**Answer (4 marks):**

1. **Why it might be “impossible to know”**  
   - The snippet alone only shows `bn:post_n_EN` is a `lemon:LexicalEntry` with language `"EN"` and part‐of‐speech `noun`. The **actual written representation** (“post”) is hidden behind `<…/canonicalForm>` and not yet shown directly.

2. **Why it “might be the English word ‘post’”**  
   - If you follow the linked resource `<.../canonicalForm>` and see `lemon:writtenRep "post"`, you confirm the word is “post.” So if Friend 2 has that extra triple, they’re correct.

3. **Conclusion and further info**  
   - Both friends have a point. By RDF alone, you need to dereference the `canonicalForm` node to see `writtenRep "post"`. Additional data clarifies that this is indeed the English noun “post.”

---

### (c)  

When you request `<http://babelnet.org/rdf/post_n_EN/canonicalForm>`, it returns `lemon:writtenRep "post"`.  

**(i)** **SPARQL**: *Find the written representation and language for all nouns.*  
**Answer (6 marks):**

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

**(ii)** **SPARQL**: *Find the language and part of speech for words whose canonical form is “post.”*  
**Answer (4 marks):**

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

---

### (d)  

We have an excerpt from [lemon‐model.net/lemon\#](http://www.lemon-model.net/lemon#) describing classes like `:LexicalSense`, `:SenseDefinition`, and properties like `:definition`, `:value`.

**(i) What is the role of this document?**  
**Answer (1 mark):**  
It’s an **ontology (schema) definition** for the Lemon lexical model, specifying classes and properties for lexical/semantic descriptions.

**(ii) What format is it in?**  
**Answer (1 mark):**  
Likely **RDF** (e.g., Turtle or RDF/XML).

**(iii) To what does the ‘owl’ prefix refer?**  
**Answer (1 mark):**  
The **OWL** (Web Ontology Language) namespace (`http://www.w3.org/2002/07/owl#`) for more expressive ontology constructs.

**(iv)** *Provide one definition for the English noun “post” in RDF.*  
**Answer (4 marks):**  
Example in Turtle:

```turtle
@prefix : <http://example.org/lemonDefs#> .
@prefix lemon: <http://www.lemon-model.net/lemon#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

:post_n_EN_sense a :LexicalSense ;
    :definition :post_n_EN_def .

:post_n_EN_def a :SenseDefinition ;
    :value "A piece of wood or metal set upright to support something."@en .
```

---

### (e)  

> *Sketch an ER diagram for a relational implementation of this model (Lemon style). Include cardinalities.*

Below is a **Mermaid ER diagram** in code.  It shows how you might map *LexicalEntry*, *Form*, *LexicalSense*, and *SenseDefinition* into a relational schema:

```mermaid
erDiagram
    %% Entities:
    LexicalEntry ||--o{ Form : "has_form"
    LexicalEntry ||--|{ LexicalSense : "has_sense"
    LexicalSense ||--o{ SenseDefinition : "has_definition"

    %% Now define attributes (Mermaid must have type + name):
    LexicalEntry {
        int LexicalEntryID     %% (Primary Key)
        string language
        string partOfSpeech
        %% Possibly more columns, e.g. lexicalEntryType, etc.
    }

    Form {
        int FormID             %% (Primary Key)
        string writtenRep
        %% Foreign key link to LexicalEntry
    }

    LexicalSense {
        int LexicalSenseID     %% (Primary Key)
        %% Foreign key link to LexicalEntry
    }

    SenseDefinition {
        int SenseDefinitionID  %% (Primary Key)
        string textValue
        %% Foreign key link to LexicalSense
    }
```

**Explanations**:  
- One **LexicalEntry** can have multiple **Forms** (1:M).  
- One **LexicalEntry** can have multiple **LexicalSenses** (1:M).  
- One **LexicalSense** can have multiple **SenseDefinitions** (1:M).  

---

# **Question 2: ER Question (Real‐Estate Agency)**

The exam’s ER diagram has **Seller**, **Estate Agent**, **Property**, **Offers**, **Buyer**, **Views**, etc.

### (a) Add cardinality indications  
**Answer (3 marks):**  
- **Seller–Property**: (1 : M) (one seller owns many properties)  
- **Agent–Property**: (1 : M) (one agent can handle many properties, each property has exactly one agent)  
- **Property–Offers**: (1 : M) (one property can have many offers)  
- **Property–Views**: (1 : M) (one property can have many viewings)  
- **Buyer–Offers**: (1 : M) (one buyer can make many offers)  
- **Buyer–Views**: (M : N) if a buyer can view multiple properties, and a property can be viewed by multiple buyers.

Below is an **optional** Mermaid diagram showing some of these relationships:

```mermaid
erDiagram
    SELLER ||--|{ PROPERTY : "owns"
    ESTATE_AGENT ||--|{ PROPERTY : "assigned_to"
    PROPERTY ||--|{ OFFERS : "receives"
    PROPERTY ||--|{ VIEWINGS : "has"
    BUYER ||--|{ OFFERS : "makes"
    BUYER }|--|{ VIEWINGS : "attends"

    SELLER {
        PK SellerID
        Name VARCHAR
        PhoneNumber VARCHAR
        ...
    }

    ESTATE_AGENT {
        PK AgentID
        Name VARCHAR
        ...
    }

    PROPERTY {
        PK PropertyID
        type VARCHAR
        bedrooms INT
        askingPrice DECIMAL
        ...
    }

    OFFERS {
        PK OfferID
        offerValue DECIMAL
        offerStatus VARCHAR
        ...
    }

    VIEWINGS {
        PK ViewingID
        date DATE
        ...
    }

    BUYER {
        PK BuyerID
        Name VARCHAR
        ...
    }
```

---

### (b) How to adapt to a relational model  
**Answer (5 marks)**

**Main tables (example):**

1. **Sellers**(SellerID PK, Name, PhoneNumber, Address, …)  
2. **EstateAgents**(AgentID PK, Name, ContactDetails, …)  
3. **Properties**(PropertyID PK, SellerID→Sellers, AgentID→EstateAgents, Type, Bedrooms, AskingPrice, …)  
4. **Buyers**(BuyerID PK, Name, PhoneNumber, …)  
5. **Offers**(OfferID PK, PropertyID→Properties, BuyerID→Buyers, OfferDate, OfferValue, OfferStatus, …)  
6. **Viewings**(ViewingID PK, PropertyID→Properties, BuyerID→Buyers, ViewingDate, …)  

If we allow multiple buyers per viewing in one row, you might need a bridging table, e.g. **`ViewingAttendees`(ViewingID, BuyerID)**.

---

### (c) List the tables, primary and foreign keys  
**Answer (6 marks):**

- **Sellers**:  
  - **PK**: `SellerID`

- **EstateAgents**:  
  - **PK**: `AgentID`

- **Properties**:  
  - **PK**: `PropertyID`  
  - **FK**: `SellerID` → `Sellers(SellerID)`  
  - **FK**: `AgentID` → `EstateAgents(AgentID)`

- **Buyers**:  
  - **PK**: `BuyerID`

- **Offers**:  
  - **PK**: `OfferID`  
  - **FK**: `PropertyID` → `Properties(PropertyID)`  
  - **FK**: `BuyerID` → `Buyers(BuyerID)`

- **Viewings**:  
  - **PK**: `ViewingID`  
  - **FK**: `PropertyID` → `Properties(PropertyID)`  
  - **FK**: `BuyerID` → `Buyers(BuyerID)`  
  - (Or use a many‐to‐many bridging table if needed.)

---

### (d) MySQL command (example: `Properties` table)  
**Answer (3 marks):**

```sql
CREATE TABLE Properties (
  PropertyID INT PRIMARY KEY AUTO_INCREMENT,
  SellerID INT NOT NULL,
  AgentID INT NOT NULL,
  Type VARCHAR(50),
  Bedrooms INT,
  AskingPrice DECIMAL(12, 2),
  Address VARCHAR(100),
  FOREIGN KEY (SellerID) REFERENCES Sellers(SellerID),
  FOREIGN KEY (AgentID) REFERENCES EstateAgents(AgentID)
);
```

---

### (e) Commission Query (1% of final sale price)

#### (i) Query: total commission per agent since 2023‐01‐01  
**Answer (6 marks):**

```sql
SELECT 
    p.AgentID,
    SUM(o.OfferValue * 0.01) AS TotalCommission
FROM Properties p
JOIN Offers o
  ON p.PropertyID = o.PropertyID
WHERE o.OfferStatus = 'sale completed'
  AND o.OfferDate >= '2023-01-01'
GROUP BY p.AgentID;
```
- Multiplies `OfferValue` by 0.01.

#### (ii) Query: top‐earning agent  
**Answer (2 marks):**

```sql
SELECT 
    p.AgentID,
    SUM(o.OfferValue * 0.01) AS TotalCommission
FROM Properties p
JOIN Offers o
  ON p.PropertyID = o.PropertyID
WHERE o.OfferStatus = 'sale completed'
  AND o.OfferDate >= '2023-01-01'
GROUP BY p.AgentID
ORDER BY TotalCommission DESC
LIMIT 1;
```

---

### (f) Using a document DB instead of a relational DB  
**Answer (5 marks, real‐estate–specific):**

1. **Why it could be good**  
   - Flexible schema for varied property attributes or embedded arrays for pictures/metadata.  
   - Easier horizontal scaling if you store large unstructured listings or docs.

2. **Why it could be bad**  
   - The relationships between Sellers, Agents, Buyers, and Offers are highly relational and easier to handle in SQL.  
   - Complex queries for commission, statuses, and cross‐table joins are simpler in a relational system.  
   - Ensuring data consistency across offers, status changes, etc. can be more challenging in a NoSQL model.

Hence, a document DB might work well for very flexible listings or heavy unstructured data, but for transactional/structured aspects, a relational DB is usually more straightforward.

---

# **Question 3: IR/doc db Question**

### (a) If 2,200,000 books are labeled German at 80% precision, how many are truly German?  
**Answer (2 marks):**  
True positives = 2,200,000 × 0.80 = **1,760,000**.

---

### (b) How many German books in total (including those missed) if recall is 88%?  
**Answer (3 marks):**

\[
\text{All German} = \frac{\text{True Positives}}{\text{Recall}}
                  = \frac{1,760,000}{0.88}
                  \approx 2,000,000.
\]

---

### (c) Danish classifier: 100% precision, 76% recall. Why more useful for ML training than German’s 80% precision?  
**Answer (5 marks):**  
- **Training sets** value extremely high precision, because you don’t want noisy examples (false positives).  
- 76% recall means some Danish books are missed, but *every* labeled Danish book is *actually* Danish. That yields a **pure** dataset for ML training, often better than a bigger but contaminated set.

---

### (d) F1 measure (German & Danish). What is F1?  
**Answer (2 marks):**  
F1 = Harmonic mean of precision and recall:
\[
F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}.
\]

---

### (e) `db.books.find({ lang: "German" })`  
**(1 mark)**  
This **queries all documents** in the `books` collection with `lang` = `"German"`.

---

### (f) Rewrite to get only 19th‐century volumes  
**Answer (5 marks):**

```js
db.books.find({
  lang: "German",
  year: { $gte: 1800, $lt: 1900 }
})
```
- Finds volumes from 1800 to 1899.

---

### (g) Single textual field called “text”; filter for “Strudel”  
**(2 marks)**

```js
db.books.find({
  lang: "German",
  year: { $gte: 1800, $lt: 1900 },
  text: /Strudel/
})
```
- Uses a regex to match documents whose `text` field contains “Strudel.”

---

### (h) TEI/XML vs. enriching a document DB  
**Answer (10 marks):**  
1. **Structured encoding:** TEI is superb for detailed textual markup (chapters, footnotes, critical apparatus). A JSON store is more flexible but less specialized for hierarchical text.  
2. **Query complexity:** XML DB + XQuery can handle fine‐grained queries by XML elements. MongoDB supports simpler doc queries, possibly less powerful for nested text structures.  
3. **Standards & Interoperability:** TEI is widely used in digital humanities, enabling data sharing with other TEI projects.  
4. **Performance & scale:** Large TEI corpora can be stored in specialized XML databases, but a NoSQL doc DB might scale horizontally.  
5. **Long‐term preservation:** TEI is a recognized standard for scholarly text encoding, often important for academic or library contexts.

The choice depends on how much *structural*, *semantic*, and *scholarly* detail you want to preserve vs. the need for flexible indexing or large‐scale doc management.

