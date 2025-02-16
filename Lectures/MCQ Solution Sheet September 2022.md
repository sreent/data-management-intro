
# **Question 1(a)**

### **Context**
We have a set of transactional SQL commands transferring money between two accounts, but something is missing to finalize the transaction.

### **Question**
**Which command is missing from the following set?**

```sql
START TRANSACTION;
UPDATE Account SET Balance = Balance-100 WHERE AccNo=21430885;
UPDATE Account SET Balance = Balance+100 WHERE AccNo=29584776;
SELECT SUM(Balance) FROM Account;
```

### **Answer: iv. COMMIT**

### **Explanation**
- Without a **COMMIT**, the updates remain uncommitted and could be rolled back or lost.
- `ROLLBACK` (choice i) reverses changes, not the intent here.
- `END TRANSACTION` (choice iii) is not standard SQL syntax (some systems allow `END` but typically you use `COMMIT`).

### **Real‐World Example**
In a **bank transfer**, you want the debit/credit to commit atomically. A commit ensures both sub-updates finalize together.

### **Common Pitfalls**
- Omitting `COMMIT` leaves changes pending.
- Mistaking `END TRANSACTION` or `ROLLBACK` for finalizing.

### **Short Answer Summary**
- A transaction in SQL typically ends with either **COMMIT** (make changes permanent) or **ROLLBACK** (undo them). Here, we need `COMMIT`.

---

# **Question 1(b)**

### **Context**
A SPARQL query that attempts to retrieve Cristiano Ronaldo’s birth city from DBpedia fails to return a result.

### **Question**
**Why doesn’t the query below return the expected city name?**

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

### **Answer: ii. "**Cristiano Ronaldo"@en is a string, not a URL.** It can’t be the subject of a triple.

### **Explanation**
- In **RDF**/SPARQL, **subjects** must be **URIs**. A literal string `"Cristiano Ronaldo"@en` cannot act as a subject.
- The correct approach typically references `<http://dbpedia.org/resource/Cristiano_Ronaldo>` or uses a variable that matches that URI.

### **Real‐World Example**
Linked Data queries must reference the **URI** (e.g., `<dbpedia:Cristiano_Ronaldo>`) rather than a raw string.

### **Common Pitfalls**
- Confusing literal strings with resource URIs.
- Attempting to treat `"Name"@en` as a subject in RDF.

### **Short Answer Summary**
- You need a **URI** for Cristiano Ronaldo as the subject; a string literal won’t function in a triple.

---

# **Question 1(c)**

### **Context**
An RDF snippet from Tim Berners‐Lee’s v‐card:

```turtle
card:I a :Male;
       foaf:family_name "Berners-Lee";
       foaf:givenname "Timothy";
       foaf:title "Sir".
```

### **Question**
**How many predicates does this contain?**

### **Answer: i. 4**

### **Explanation**
- The predicates are:
  1. `a` (shorthand for `rdf:type`)
  2. `foaf:family_name`
  3. `foaf:givenname`
  4. `foaf:title`
- Choices like 5 or 7 over‐ or under‐count.

### **Real‐World Example**
RDF statements always take the form (subject, predicate, object). Counting the distinct predicates is key in interpreting triples.

### **Common Pitfalls**
- Counting objects or subjects as predicates.
- Overlooking the `a` (alias for `rdf:type`).

### **Short Answer Summary**
- This snippet has **four** distinct predicates.

---

# **Question 1(d)**

### **Context**
We have an XML snippet with a `<disk>` of ID `1847336` having multiple `<track>` elements. The query seeks `<track>` child elements with `duration>150` and selects their children.

### **Question**
**How many results does the XPath** `//disk[@xml:id="1847336"]/track[@duration>150]/*` **return?**

### **Answer: ii. 4**

### **Explanation**
- Tracks with `duration>150` are track #1 (duration=193) and track #2 (duration=167).  
- Each track has 2 child elements `<title>` and `<artist>`. So total = **4**.

### **Real‐World Example**
In media catalogs, you might filter tracks by length (in seconds) and retrieve subelements like title/artist.

### **Common Pitfalls**
- Overlooking child elements or including siblings erroneously.
- Confusing attribute or element conditions.

### **Short Answer Summary**
- The two qualifying tracks each have two children, hence 4 matching nodes.

---

# **Question 1(e):**

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
      - False Negatives: $ (1 - 0.90) \times 30 = 3 $
      - False Positives: $ \frac{30 \times (1 - 0.80)}{0.80} = 8 $
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

# **Question 1(f)**

### **Context**
A table with columns (Chart, Date, Position, Title, Artist, Date of Birth). We suspect it’s only in 1NF.

### **Question**
**Which normal forms does the table satisfy?**

### **Answer: iv. 1NF**

### **Explanation**
- The data is atomic in each column (no repeating groups), so 1NF is met.
- 2NF/3NF can’t be guaranteed without analyzing a key and dependencies. The partial or transitive dependencies might exist.

### **Real‐World Example**
Music chart info, each row is a single chart entry. At least 1NF because no multivalue columns, but no guarantee of higher forms.

### **Common Pitfalls**
- Assuming it’s in 2NF or 3NF without actual functional dependency checks.

### **Short Answer Summary**
- It’s certainly in **1NF**, but we can’t confirm higher normal forms from the snippet.

---

# **Question 1(g)**

### **Context**
An E/R diagram for a plant identification DB is poorly drawn, using weird cardinalities, arrow notations, etc.

### **Question**
**Why is the diagram not good? (Select all that apply)**

### **Answer: i, ii, iii, iv, vi, viii**

### **Explanation**
1. **(i)** By convention, cardinalities appear between entities, not attributes.
2. **(ii)** Entities connect with explicit relationships, not arbitrary lines.
3. **(iii)** The arrow is meaningless in standard E/R notation.
4. **(iv)** Spaces in attribute names is discouraged.
5. **(v)** “An attribute can’t be shared” is not always true. (Hence not correct)
6. **(vi)** Cardinalities “21” aren’t allowed. Should use “1”, “n”, “m”, etc.
7. **(vii)** Ternary relationship? Not necessarily. So not correct.
8. **(viii)** ß and x cardinalities are odd; best to use “n” or “m”.

### **Real‐World Example**
Proper E/R diagrams clearly indicate relationships, cardinalities (like 1..n), and attribute names without spaces.

### **Common Pitfalls**
- Combining notation from different modeling styles incorrectly.
- Using ambiguous cardinalities.

### **Short Answer Summary**
- The diagram uses invalid cardinalities, missing relationship lines, arrow notation incorrectly, etc.

---

# **Question 1(h)**

### **Context**
A database query to find all staff who’ve interacted with a client named “Shug Avery.” We see partial SQL statements and must choose which ones might be correct.

### **Question**
**Which queries likely produce the correct result?**

### **Answer: iii and iv**

### **Explanation**
- (iii) and (iv) each properly join **Meeting** to **Client** and **Employee**, with correct `WHERE` conditions on the client’s name.
- (i)/(ii)/(v) either fail to join properly or use non‐matching conditions.

### **Real‐World Example**
In CRMs, you frequently link employees to meetings to clients for cross references.

### **Common Pitfalls**
- Wrong type of join, or omitting a join condition.

### **Short Answer Summary**
- The correct approach typically does a multi‐table join: `Client -> Meeting -> Employee`.

---

# **Question 1(i)**

### **Context**
MongoDB queries for actors born before 1957. Which is correct?

### **Question**
**Which code snippet properly finds actors with `dateOfBirth < 1957-01-01`?**

### **Answer: i, vii**  
(They each do `db.actors.find(...)` with `"$lt": ISODate("1957-01-01")`.)

### **Explanation**
- (i) `db.actors.findOne({"dateOfBirth": {$lt: ISODate("1957-01-01")}})` is correct.
- (vii) `db.actors.find({"dateOfBirth": {$lt: ISODate("1957-01-01")}})` also correct.
- Others either misuse operators or compare with just an integer.

### **Real‐World Example**
In a film/TV database, queries by birth date must use **Mongo’s `$lt`** operator with a proper `ISODate`.

### **Common Pitfalls**
- Using `"<"` or a raw integer for date queries in MongoDB.

### **Short Answer Summary**
- Use `$lt` with `ISODate(...)` for date comparisons in MongoDB.

### Why `findOne` is also correct?

Because **the exam question focuses on *syntax* correctness and using the right comparison operator** rather than on retrieving *all* matching documents, `findOne` is still considered **“correct”** as a MongoDB query. In other words, **it successfully searches** for an actor born before 1957 (and returns the first match).

- **Syntactically**:  
  ```js
  db.actors.findOne({
    "dateOfBirth": { $lt: ISODate("1957-01-01") }
  });
  ```
  is perfectly valid MongoDB syntax—no errors, `$lt` is used properly, and `ISODate` is in the right format.

- **Semantically**:  
  - `findOne(...)` returns only the first document that meets the condition, whereas `find(...)` returns all matching documents.  
  - Even though you only get one actor (instead of all), it is still a **successful search** in that it correctly applies the `$lt: ISODate(…)` condition.  

**Hence,** for the purposes of the exam question (which asked “Which query is *likely* to represent a successful MongoDB search for actors born before 1957?”), **both**:
```js
db.actors.findOne({ "dateOfBirth": { $lt: ISODate("1957-01-01") } })
```
and
```js
db.actors.find({ "dateOfBirth": { $lt: ISODate("1957-01-01") } })
```
are considered “correct” *syntax* for searching before 1957. The difference is purely **how many matches** they return—**one** versus **many**—but **both** queries *“work”* in the sense of using proper operators/format and retrieving actors with `dateOfBirth < 1957-01-01`.

---

# **Question 1(j)**

### **Context**
Recipe Markup Language (RecipeML) snippet:  
```dtd
<!ELEMENT recipe (head, description*, equipment?, ingredients, directions, nutrition?, diet‐exchanges?)>
<!ATTLIST recipe
  %common.att;
  %measurement.att;
>
```
We want to see which statements are true about `<recipe>` children.

### **Question**
**Which statements about `<recipe>` and `<ingredients>` are true?**

### **Answer: i, ii, iv**

### **Explanation**
- (i) `<recipe>` must have exactly one `<ingredients>` child: True according to `ingredients` (no plus sign).
- (ii) `<ingredients>` must come before `<directions>`: True by the order in the DTD.
- (iv) `<recipe>` can have one `<ingredients>` element: Essentially the same concept as (i).
- The other options about multiple `<ingredients>` or ignoring order are incorrect.

### **Real‐World Example**
DTDs strictly define order and occurrence of child elements, important for standardizing recipe data.

### **Common Pitfalls**
- Misreading the occurrence indicators (`?`, `*`, `+`, etc.) in DTDs.
- Overlooking the explicit child order.

### **Short Answer Summary**
- Exactly one `<ingredients>` child is required, and it appears in a specific sequence before `<directions>`.

