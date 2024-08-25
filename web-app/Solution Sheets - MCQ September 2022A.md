
---

### Question 1(a):

**What is missing from the following set of commands?**

```sql
START TRANSACTION;
UPDATE Account SET Balance = Balance-100 WHERE AccNo=21430885;
UPDATE Account SET Balance = Balance+100 WHERE AccNo=29584776;
SELECT SUM(Balance) FROM Account;
```

**Answer: iv. COMMIT**

**Detailed Explanation and Working:**

- **Choice i. ROLLBACK:** Incorrect. It undoes the changes instead of finalizing them.
- **Choice ii. INSERT INTO Account VALUES (100):** Incorrect. Irrelevant to the current transaction.
- **Choice iii. END TRANSACTION:** Incorrect. Not a valid SQL command.
- **Choice iv. COMMIT:** Correct. Finalizes the transaction and applies all changes permanently.
- **Choice v. UPDATE Account SET Balance = Balance+100 WHERE AccNo=21430885:** Incorrect. Unnecessary and would revert one of the previous updates.

**Real-World Example:**
In a banking application, when transferring money between accounts, the transaction should either fully succeed or fully fail. A `COMMIT` ensures the transfer completes, while a `ROLLBACK` would revert changes if there’s an issue.

**Common Pitfalls:**
- Forgetting to `COMMIT` can cause unsaved data.
- Using invalid commands like `END TRANSACTION`.

**Important Point to Remember:**
- Always use `COMMIT` to finalize a transaction in SQL. Without it, your changes remain temporary and can be lost.

---

### Question 1(b):

**The following query should return the name of the city of Cristiano Ronaldo’s birth. Why doesn’t it?**

SPARQL Query:

```sparql
SELECT DISTINCT * 
WHERE 
{ 
  "Cristiano Ronaldo"@en dbo:birthPlace   
    [ 
       a            dbo:City ; 
       rdfs:label   ?cityName  
    ] . 
  FILTER ( LANG(?cityName) = 'en' ) 
}
```

**Answer: ii. "Cristiano Ronaldo"@en is a string, not a URL. It can’t be the subject of a triple.**

**Detailed Explanation and Working:**

- **Choice i. The city is not in England, so the filter removes it:** Incorrect. The filter is based on language, not location.
- **Choice ii. "Cristiano Ronaldo"@en is a string, not a URL:** Correct. In RDF, subjects must be URIs, not literal strings like `"Cristiano Ronaldo"@en`.
- **Choice iii. The first part of the WHERE clause is a duple, not a triple:** Incorrect. The syntax is correct.
- **Choice iv. Ronaldo’s place of birth is not in Wikipedia in a way that DBpedia can access:** Incorrect. This might be an issue, but it’s not the main problem here.

**Real-World Example:**
In linked data systems, using URIs instead of literal strings ensures consistent identification of resources across datasets.

**Common Pitfalls:**
- Using literals as subjects in RDF triples.
- Failing to differentiate between literals and URIs.

**Important Point to Remember:**
- In RDF and SPARQL, always use URIs for subjects in triples. Literal strings cannot act as subjects.

---

### Question 1(c):

**How many predicates does this extract contain?**

Extract:

```ttl
card:I a :Male 
       foaf:family_name "Berners-Lee"; 
       foaf:givenname "Timothy"; 
       foaf:title "Sir".
```

**Answer: i. 4**

**Detailed Explanation and Working:**

- **Choice i. 4:** Correct. The predicates are `a`, `foaf:family_name`, `foaf:givenname`, and `foaf:title`.
- **Choice ii. 7:** Incorrect. Overcounts by including objects or subjects as predicates.
- **Choice iii. 5:** Incorrect. Adds an extra predicate that does not exist.
- **Choice iv. 8:** Incorrect. Overcounts by misinterpreting the structure.

**Real-World Example:**
In creating digital profiles for people or entities, predicates define properties such as names, titles, and roles.

**Common Pitfalls:**
- Misinterpreting RDF syntax.
- Confusing literals and predicates.

**Important Point to Remember:**
- RDF predicates describe relationships and properties. Always count them accurately in Turtle syntax.

---

### Question 1(d):

**Given this XML, how many results does the query select?**

XML:

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

XPath Query:

```xpath
//disk[@xml:id="1847336"]/track[@duration>150]/*
```

**Answer: ii. 4**

**Detailed Explanation and Working:**

- **Choice i. 5:** Incorrect. Overestimates the number of selected elements.
- **Choice ii. 4:** Correct. Tracks 1 and 2 meet the criteria, and each has two child elements (`<title>` and `<artist>`), totaling 4.
- **Choice iii. 1:** Incorrect. Underestimates the count.
- **Choice iv. 6:** Incorrect. Includes elements that don’t match the criteria.

**Real-World Example:**
In XML-based media catalogs, XPath can be used to filter and retrieve specific metadata, like tracks longer than a certain duration.

**Common Pitfalls:**
- Misinterpreting XPath logic.
- Confusing element and attribute selection.

**Important Point to Remember:**
- Use XPath carefully when navigating hierarchical data. Understand how to target specific elements or attributes to get accurate results.

---

### Question 1(e):

**Which parameter setting for the tool is likely to be best (in the sense that I spend the least time on the task)?**

#### Problem Context:
- Total Archive Size: 50,000 items.
- Relevant Items: 30 items.
- Manual Time to Find Each Relevant Item (if missed): 15 minutes.
- Time Wasted on Each False Positive: 0.5 minutes (30 seconds).

**Answer: i. Just right of the center of the graph, where precision goes up again.**

**Detailed Explanation and Working:**

#### Choice-by-Choice Analysis:

1. **Option i: Just right of the center (80% precision, 90% recall):**
    - **Calculations:**
      - False Negatives: \( (1 - 0.90) \times 30 = 3 \)
      - False Positives: \( \frac{30 \times (1 - 0.80)}{0.80} = 8 \)
      - Total Time: 49 minutes.

2. **Option ii: To the right (68% precision, 90% recall):**
    - **Calculations:**
      - False Negatives: 3
      - False Positives: 14
      - Total Time: 52 minutes.

3. **Option iii: Manual search (100% recall):**
    - **Calculations:**
      - Irrelevant Items: 49,970 × 0.5 minutes
      - Total Time: 25,435 minutes.

4. **Option iv: To the left (100% precision, 17% recall):**
    - **Calculations:**
      - False Negatives: 25
      - Total Time: 450 minutes.

5. **Option v: To the left (100% precision, 17% recall with 30 seconds/item):**
    - **Calculations:**
      - False Negatives: 25
      - Total Time: 88 minutes.

**Conclusion:**
- Option (i) has the lowest time (49 minutes) and is the most efficient.

**Real-World Example:**
In search engines, balancing precision and recall helps users find the most relevant results without wasting time on irrelevant ones.

**Common Pitfalls:**
- Focusing solely on either precision or recall can lead to inefficiency.
- Misunderstanding how false positives and false negatives affect total time.

**Important Point to Remember:**
- Always consider the trade-offs between precision and recall when optimizing information retrieval tasks.

---

### Question 1(f):

**Which normal forms does this table satisfy?**

| Chart         | Date       | Position | Title           | Artist         | Date of Birth |
|---------------|------------|----------|----------------|----------------|---------------|
| RIAS          | 2022-04-14 | 1        | As It Was       | Harry Styles   | 1994-02-01    |
| UK Singles    | 2012-04-08 | 4        | Starships       | Nicki Minaj    | 1982-12-08    |
| Billboard Hot | 2022-04-22 | 1        | First Class     | Jack Harlow    | 199

8-03-13    |
| SNEP          | 1993-11-20 | 5        | Il me dit ...   | Patricia Kaas  | 1966-12-05    |

**Answer: iv. 1NF**

**Detailed Explanation and Working:**

- **Choice i. 2NF:** Incorrect. Likely has partial dependencies.
- **Choice ii. 3NF:** Incorrect. May have transitive dependencies.
- **Choice iii. 5NF:** Incorrect. Not applicable to this table structure.
- **Choice iv. 1NF:** Correct. The table meets the requirements of 1NF by having atomic values.

**Real-World Example:**
In customer databases, ensuring each attribute (like address, phone number) is atomic is the first step in normalization.

**Common Pitfalls:**
- Confusing atomic values with composite attributes.
- Assuming a table automatically satisfies higher normal forms without verifying dependencies.

**Important Point to Remember:**
- 1NF ensures that all attributes are atomic and contain only single values, laying the foundation for further normalization.

---

### Question 1(g):

**Why is this E/R diagram not a good design?**

**Answer: i, ii, iii, iv, vi, viii**

**Detailed Explanation and Working:**

- **Choice i. Cardinality is only given between entities:** Correct. Cardinality should describe relationships between entities.
- **Choice ii. Entities are connected without explicit relationships:** Correct. Entities need relationships like "has" or "belongs to."
- **Choice iii. The arrow is meaningless:** Correct. The diagram uses an invalid arrow notation.
- **Choice iv. Spaces are not permitted in attribute names:** Correct. Attribute names should not include spaces.
- **Choice v. An attribute can’t be shared between entities:** Incorrect. In some cases, shared attributes are valid.
- **Choice vi. Cardinalities like ‘21’ are not allowed:** Correct. Only standard notations like "1", "n", "m" should be used.
- **Choice viii. Cardinalities like ß and x are inadvisable:** Correct. Stick to standard notations.

**Real-World Example:**
In retail inventory systems, clear E/R diagrams are crucial for tracking relationships between products, categories, and suppliers.

**Common Pitfalls:**
- Using incorrect notations or connecting entities without relationships.
- Misusing attribute names and cardinalities.

**Important Point to Remember:**
- Proper E/R diagram conventions are essential for accurate database modeling, ensuring clarity and correctness in the design.

---

### Question 1(h):

**How might the query to find all staff members who have had interactions with a client called "Shug Avery" continue?**

**Answer: iii, iv**

**Detailed Explanation and Working:**

- **Choice i. LEFT JOIN on Client:** Incorrect. It doesn’t properly link `Meeting` and `Employee`.
- **Choice ii. Complex LEFT JOIN structure:** Incorrect. Overcomplicated with unnecessary `LIKE` clauses.
- **Choice iii. INNER JOIN structure:** Correct. Links `Client`, `Meeting`, and `Employee` logically.
- **Choice iv. WHERE-based JOIN structure:** Correct. An older but still valid join syntax.

**Real-World Example:**
In CRM systems, querying interactions between clients and staff members is common for tracking service history or performance metrics.

**Common Pitfalls:**
- Using the wrong type of join (e.g., `LEFT JOIN` instead of `INNER JOIN`).
- Confusing syntax when performing multi-table joins.

**Important Point to Remember:**
- Choose the correct join type based on the query’s goal. In cases like this, `INNER JOIN` ensures that only relevant records are returned.

---

### Question 1(i):

**Which of these queries is likely to represent a successful MongoDB search for actors born before 1957?**

**Answer: i, vii**

**Detailed Explanation and Working:**

- **Choice i. Using `$lt` with `ISODate`:** Correct. Properly uses MongoDB syntax.
- **Choice ii. Using `$lt` with an integer:** Incorrect. Dates should be in `ISODate` format.
- **Choice iii. Using `"<"` as an operator:** Incorrect. Not valid in MongoDB.
- **Choice iv. Similar misuse of `"<"` operator:** Incorrect.
- **Choice v. Incorrect syntax for date comparison:** Incorrect.
- **Choice vi. Exact year matching with 1957:** Incorrect. Not appropriate for this query.
- **Choice vii. Correct use of `$lt` and `ISODate`:** Correct.
- **Choice viii. Invalid use of `"<"` operator:** Incorrect.

**Real-World Example:**
In media databases, date-based queries help filter content by release year, birthdate, or historical relevance.

**Common Pitfalls:**
- Using incorrect operators in MongoDB queries.
- Failing to correctly format dates using `ISODate`.

**Important Point to Remember:**
- In MongoDB, always use `$lt`, `$gt`, and similar operators for date comparisons, and ensure dates are in `ISODate` format.

---

### Question 1(j):

**What are the true statements based on RecipeML's .dtd file?**

**Answer: i, ii, iv**

**Detailed Explanation and Working:**

- **Choice i. `<recipe>` must have one `<ingredients>` element:** Correct. Required based on the DTD structure.
- **Choice ii. The `<ingredients>` element must come before `<directions>`:** Correct. The order is specified in the DTD.
- **Choice iii. The order of children is not important:** Incorrect. Order is important according to the DTD.
- **Choice iv. `<recipe>` can have one `<ingredients>` element:** Correct. The DTD allows for one `<ingredients>` element.
- **Choice v. Multiple `<ingredients>` elements:** Incorrect. Only one `<ingredients>` element is allowed.

**Real-World Example:**
In applications that store recipes, following DTD rules ensures that the XML structure is consistent and parseable.

**Common Pitfalls:**
- Misunderstanding the structure and ordering specified in DTDs.
- Incorrectly assuming multiple elements are allowed when they are not.

**Important Point to Remember:**
- Always follow DTD rules for XML structure to ensure consistency and avoid errors when parsing or validating documents.

---
