
---

### **Question 2: RDF, SPARQL, and Linked Open Data**

#### **a. The above text is from the Carnegie Hall data lab. You can request their data in various RDF serialisations:**

**i. Which RDF serialisation is this?** [1 mark]

**Answer:**
This RDF serialization is **Turtle (Terse RDF Triple Language).**

**Detailed Explanation:**
- Turtle is a compact and readable format for expressing RDF data, known for its user-friendly syntax.
- The format uses prefixes to simplify the representation of URIs and supports both triples and nested structures.

**Real-World Scenario Connection:**
- Turtle is extensively used in Linked Open Data projects for representing data in cultural institutions, research data repositories, and government data portals.

**Important Points to Remember:**
- Turtle’s readability makes it a popular choice for both developers and data scientists working with RDF datasets.
  
**Key Takeaways:**
- Understanding different RDF serialization formats is key for working with Linked Data and ensuring interoperability across systems.

---

**ii. Name ONE other serialisation and briefly describe the difference.** [2 marks]

**Answer:**
Another RDF serialization is **RDF/XML.** Unlike Turtle, RDF/XML is an XML-based format that is less human-readable but better suited for integration with XML tools and systems.

**Detailed Explanation:**
- RDF/XML leverages the XML structure to represent RDF triples, offering a structured and hierarchical approach to data representation. However, it’s often considered verbose and less intuitive compared to Turtle.

**Real-World Scenario Connection:**
- RDF/XML is commonly used in enterprise systems where XML workflows are already established, making it easier to integrate with existing software.

**Important Points to Remember:**
- RDF/XML’s structure is more rigid and verbose compared to Turtle, which is designed for readability and ease of use.

**Key Takeaways:**
- Choosing the right RDF serialization depends on your project’s requirements, balancing readability, integration needs, and data processing efficiency.

---

**iii. How many triples are shown here?** [1 mark]

**Answer:**
There are **10 triples** shown in the original RDF snippet.

**Detailed Explanation:**
- RDF triples follow the subject-predicate-object structure. In this example, the triples include properties like `schema:birthDate`, `schema:birthPlace`, and `skos:exactMatch`.

**Real-World Scenario Connection:**
- Knowing how to count and interpret triples is critical when working with RDF graphs in data management or knowledge representation projects.

**Important Points to Remember:**
- Each triple forms a complete statement in RDF, representing a unique fact in the dataset.

**Key Takeaways:**
- Counting triples is a fundamental skill for analyzing RDF data and ensuring the accuracy of data modeling.

---

#### **b. Following two of the URLs in the above – chi:61 and wd:Q128297 – gives the following extra triples:**

**i. What is the full URL of wd:Q128297?** [1 mark]

**Answer:**
The full URL of `wd:Q128297` is **`http://www.wikidata.org/entity/Q128297`**.

**Detailed Explanation:**
- The URL is part of the Wikidata namespace and uniquely identifies the resource.

**Real-World Scenario Connection:**
- Resolving URIs in Linked Data systems is critical for accessing resources and integrating data across distributed datasets.

**Important Points to Remember:**
- Uniform Resource Identifiers (URIs) are crucial for establishing unique and persistent references in the semantic web.

**Key Takeaways:**
- Understanding how to dereference URIs is essential when navigating RDF datasets and performing linked data queries.

---

**ii. Given a triplestore with the RDF from these resources and a SPARQL endpoint, what query would list the birth name of all Sopranos?** [5 marks]

**Answer:**
```sparql
SELECT ?birthName
WHERE {
  ?soprano a <http://purl.org/ontology/mo/Instrument> ;
           rdfs:label "soprano" .
  ?soprano <http://www.wikidata.org/prop/direct/P1477> ?birthName .
}
```

**What will it return:**
- The query retrieves the birth names of all entities classified as "soprano," returning results such as "Maria Callas."

**Detailed Explanation:**
- The query filters entities labeled as “soprano” and retrieves their birth names using the property `wdt:P1477`. The use of standard ontologies like Music Ontology (MO) helps standardize classification.

**Real-World Scenario Connection:**
- Such queries are common in music databases and digital libraries where biographical data is integrated with performance information.

**Important Points to Remember:**
- Proper filtering and selecting properties in RDF queries is crucial for retrieving relevant and accurate data.

**Key Takeaways:**
- SPARQL’s ability to query structured and linked RDF data makes it indispensable in semantic web applications.

---

**iii. Both Wikidata and Carnegie Hall have SPARQL endpoints, but the Carnegie Hall triplestore does not include Wikidata's triples, and Wikidata does not have Carnegie Hall data. Give TWO ways that queries like the one you give in (ii) could still be carried out.** [5 marks]

**Answer:**
1. **Federated SPARQL Queries:** Use the `SERVICE` keyword in SPARQL to query multiple endpoints, allowing for combined data retrieval across distributed sources.

2. **Data Integration with a Custom Triplestore:** Download and merge RDF datasets from both sources into a single local triplestore, enabling comprehensive queries.

**Detailed Explanation:**
- Federated queries are useful when combining data from different endpoints in real-time. Alternatively, creating a local integrated triplestore offers more control and consistency at the cost of real-time updates.

**Real-World Scenario Connection:**
- Federated querying is often used in research environments where data from multiple sources must be harmonized for analysis.

**Important Points to Remember:**
- Depending on your project’s needs, trade-offs between real-time data access and control over integrated datasets must be considered.

**Key Takeaways:**
- Effective data integration strategies ensure comprehensive access to linked open data while balancing performance and complexity.

---

#### **c. Your project wants to use biographical data from Wikidata, concert listings from Carnegie Hall, and MusicBrainz discographies. Consider the relative merits and practicality of using the THREE existing resources as live Linked Open Data as opposed to downloading the data from each and creating a relational database for the data you need.** [9 marks]

**Answer:**
Using live Linked Open Data provides real-time updates and easier interoperability, while downloading data and creating a relational database offers more control and efficiency for complex queries.

**Detailed Explanation:**
- **Live Linked Open Data:** Ensures that you have the most up-to-date information across multiple sources and enables dynamic querying across distributed datasets. However, it may involve more complex query handling and performance trade-offs.
- **Downloaded Data in a Relational Database:** Supports optimized queries and faster performance but requires regular updates and lacks real-time data. It is more suited for predefined analyses and reporting.

**Real-World Scenario Connection:**
- This dilemma is typical in digital humanities projects where data freshness, integration, and query complexity must be balanced.

**Important Points to Remember:**
- Consider the trade-offs between real-time access, query performance, and data consistency when designing your solution.

**Key Takeaways:**
- Choose your approach based on project requirements, balancing the need for up-to-date information with system performance and flexibility.

---

#### **d. Wikidata uses almost exclusively their own ontology with a bespoke set of properties and classes. Carnegie Hall Data Labs primarily use ontologies from other projects, especially schema.org. Why might they have chosen different approaches? What are the benefits of each?** [6 marks]

**Answer:**
- **Wikidata’s Bespoke Ontology:** Provides flexibility and allows the community to create properties tailored to the platform’s wide-ranging data needs. This adaptability supports the diverse nature of Wikidata, accommodating everything from biographies to technical data.
  
- **Carnegie Hall’s Use of Established Ontologies:** Prioritizes compatibility and ease of integration with other linked data systems. Using widely accepted standards like schema.org reduces redundancy and makes their data more accessible to other platforms.

**Detailed Explanation:**
- Wikidata’s model favors adaptability, allowing for rapid growth and customized data entry, whereas Carnegie Hall’s strategy ensures interoperability, crucial for integrating with other cultural heritage data sources.

**Real-World Scenario Connection:**
- In digital libraries and archives, the choice between bespoke and standard ontologies affects data sharing and system integration.

**Important Points to Remember:**
- Both approaches have distinct advantages: bespoke ontologies offer customization, while standard ontologies promote compatibility.

**Key Takeaways:**
- The choice of ontology reflects project goals, whether prioritizing flexibility or interoperability in a broader linked data ecosystem.

---

### **Question 3: Exam Attainment Data and Normalization**

#### **a. What Normal Forms (if any) is this table in? Justify your answer.** [2 marks]

**Answer:**
The table is in **First Normal Form (1NF)** but not in **Second Normal Form (2NF)** due to partial dependency.

**Detailed Explanation:**
- The table satisfies 1NF requirements by having atomic values and no repeating groups. However, it does not meet 2NF as some non-key attributes are dependent on only part of the composite key.

**Real-World Scenario Connection:**
- Educational databases benefit from normalization as it prevents redundancy and maintains data integrity, which is crucial when

 handling large datasets across multiple academic years.

**Important Points to Remember:**
- Higher normalization forms help eliminate redundancy but may increase the complexity of queries and data retrieval.

**Key Takeaways:**
- Understanding normalization principles is essential for designing scalable and maintainable databases, especially in structured data environments like education.

---

#### **b. The CSV uses “Z” to indicate “not applicable”. What problems might this create for SQL implementations? How would you avoid them?** [3 marks]

**Answer:**
Using "Z" as a placeholder creates issues with data type mismatches and can complicate statistical analysis.

**Solution:**
Replace "Z" with `NULL` in the dataset to represent missing or inapplicable values and ensure queries handle `NULL` values correctly.

**Detailed Explanation:**
- SQL expects consistent data types within columns, and non-numeric placeholders like "Z" can cause errors or produce incorrect results in numeric operations.

**Real-World Scenario Connection:**
- Handling missing or inapplicable data is a common challenge in analytics, especially in standardized testing or survey datasets where not every question applies to every respondent.

**Important Points to Remember:**
- Use appropriate SQL functions like `COALESCE` to handle missing data and ensure consistency in your database schema.

**Key Takeaways:**
- Proper data handling practices are essential for ensuring accuracy in data analysis and avoiding errors due to inconsistent or placeholder values.

---

#### **c. Design a relational model for the files, and give the CREATE commands needed. Explain your choices and show what Normal Forms your solution is in.** [15 marks]

**Answer:**
The relational model involves three key tables:
1. **Characteristics Table:** `CharacteristicID`, `CharacteristicType`
2. **Subjects Table:** `SubjectID`, `SubjectName`, `SubjectArea`
3. **Results Table:** `ResultID`, `CharacteristicID`, `SubjectID`, `Grade`, `StudentCount`, `Percentage`

**CREATE Statements:**
```sql
CREATE TABLE Characteristics (
  CharacteristicID INT PRIMARY KEY AUTO_INCREMENT,
  CharacteristicType VARCHAR(50)
);

CREATE TABLE Subjects (
  SubjectID INT PRIMARY KEY AUTO_INCREMENT,
  SubjectName VARCHAR(100),
  SubjectArea VARCHAR(100)
);

CREATE TABLE Results (
  ResultID INT PRIMARY KEY AUTO_INCREMENT,
  CharacteristicID INT,
  SubjectID INT,
  Grade CHAR(1),
  StudentCount INT,
  Percentage DECIMAL(5, 2),
  FOREIGN KEY (CharacteristicID) REFERENCES Characteristics(CharacteristicID),
  FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
);
```

**Detailed Explanation:**
- The model ensures normalization by splitting the data into separate tables for characteristics, subjects, and results, reaching at least **Third Normal Form (3NF).**

**Real-World Scenario Connection:**
- Similar models are used in educational institutions to track performance data across different demographics, allowing for detailed reporting and analysis.

**Important Points to Remember:**
- Proper use of foreign keys maintains referential integrity across the tables and supports accurate data retrieval.

**Key Takeaways:**
- Normalized models reduce redundancy, simplify updates, and ensure data consistency across large-scale datasets.

---

#### **d. Give a query for your database that retrieves the percentage of A*-C grades for Classical Studies for each 'Characteristic' that the files track.** [4 marks]

**Answer:**
```sql
SELECT c.CharacteristicType, r.Percentage
FROM Results r
JOIN Characteristics c ON r.CharacteristicID = c.CharacteristicID
JOIN Subjects s ON r.SubjectID = s.SubjectID
WHERE s.SubjectName = 'Classical Studies' AND r.Grade IN ('A', 'B', 'C');
```

**What will it return:**
- The query returns the percentage of students who achieved A*-C grades in Classical Studies, grouped by characteristics like gender or socioeconomic status.

**Detailed Explanation:**
- The query joins the `Results`, `Characteristics`, and `Subjects` tables to filter for relevant grades and subjects, providing insight into student performance across different groups.

**Real-World Scenario Connection:**
- Similar queries are used in education systems for evaluating curriculum effectiveness and equity in academic performance.

**Important Points to Remember:**
- Use `JOIN` operations effectively to combine data from multiple tables and apply the necessary filters for meaningful analysis.

**Key Takeaways:**
- Structuring your queries correctly in a normalized database is key for extracting actionable insights from complex datasets.

---

#### **e. Is a relational model the best approach for this sort of data? Evaluate (briefly) this approach and at least two alternative models.** [6 marks]

**Answer:**
- **Relational Model:** Ideal for structured, consistent data where relationships are clearly defined, offering strong data integrity and query performance.
- **Document Model (e.g., MongoDB):** Better suited for semi-structured or varied data, providing flexibility but at the cost of complex querying.
- **Graph Model (e.g., Neo4j):** Excels at representing interconnected data, such as social networks or complex relationships, but can be overkill for tabular educational data.

**Detailed Explanation:**
- The relational model remains the most efficient for structured educational data, but document models offer more flexibility, and graph databases can handle more intricate relationships.

**Real-World Scenario Connection:**
- In large-scale educational platforms, relational models are typically used for storing exam records, while document or graph models might support adjunct services like student surveys or relationship mapping.

**Important Points to Remember:**
- Always choose your data model based on your dataset's structure, the complexity of relationships, and your application’s scalability needs.

**Key Takeaways:**
- Understanding the strengths and limitations of different data models is crucial for designing effective and scalable solutions.

---

### **Question 4: JSON Documents and Data Models in MongoDB**

#### **a. Given a database of documents like this:**

**i. What query would return documents for people who like spas?** [2 marks]

**Answer:**
```json
db.people.find({ "likes": "spas" })
```

**What will it return:**
- The query returns all documents where the "likes" array contains the value "spas," such as profiles of users who have listed spas as an interest.

**Detailed Explanation:**
- MongoDB’s ability to query embedded arrays makes it an ideal database for flexible data models where attributes like "likes" can vary between users.

**Real-World Scenario Connection:**
- This query pattern is common in recommendation engines, where users’ preferences are matched to products, services, or experiences.

**Important Points to Remember:**
- Querying arrays is straightforward in MongoDB, allowing you to filter data based on user preferences or behaviors.

**Key Takeaways:**
- Understanding array queries is fundamental when working with semi-structured data in document-based databases like MongoDB.

---

**ii. What query would find individuals with businesses founded before the first of March, 2020, who also have at least one business with the status of "Bankrupt"?** [4 marks]

**Answer:**
```json
db.people.find({
  "businesses": {
    $elemMatch: {
      "status": "Bankrupt",
      "date_founded": { $lt: new Date("2020-03-01") }
    }
  }
})
```

**What will it return:**
- The query returns all documents where at least one business in the array was founded before March 2020 and has a status of "Bankrupt."

**Detailed Explanation:**
- The `$elemMatch` operator is critical for applying multiple conditions to array elements, enabling precise queries in semi-structured datasets.

**Real-World Scenario Connection:**
- Financial institutions often use similar queries to track historical business performance or flag risk indicators in client portfolios.

**Important Points to Remember:**
- MongoDB’s `$elemMatch` is powerful for filtering within arrays, making it ideal for handling nested or hierarchical data.

**Key Takeaways:**
- Mastering advanced array queries allows for more nuanced data retrieval in document-based systems.

---

#### **b. A bug in the data entry form for this database created several records with "likes” including "fashun" rather than "fashion".**

**i. How would you construct a query that would fix entries with the wrong data? (Explain in words – you do not need to know the full syntax).** [4 marks]

**Answer:**
You would write a query that identifies documents containing "fashun" in the "likes" array and then updates those entries to replace "fashun" with "fashion". The process involves:
- Using the `find()` method to locate incorrect entries.
- Applying the `$set` operator within an `updateMany()` command to fix the values.

**Real-World Scenario Connection:**
- Data cleaning is a critical aspect of maintaining database integrity, especially when dealing with user-generated content where errors are common.

**Important Points to Remember:**
- Automating data correction processes can save time and improve consistency in large datasets.

**Key Takeaways:**
- Keeping your data clean and consistent is essential for maintaining the reliability and accuracy of your database.

---

**ii. A colleague argues that this is a problem of referential integrity, and that you would be able to avoid this issue using a Linked Data database or a relational database. In each case, what strategy would you use?** [4 marks]

**Answer:**
- **Linked Data Database:** Implement a controlled vocabulary or ontology, ensuring that only validated terms like "fashion" are allowed.
- **Relational Database:** Use foreign key constraints with a reference table for valid entries, where only predefined values (like "fashion") are permitted.

**Real-World Scenario Connection:**
- Referential integrity is crucial in systems where certain fields must adhere to strict predefined standards, such as product catalogs or educational metadata.

**Important Points to Remember:**
- Enforcing refer

ential integrity prevents data inconsistency and ensures that only valid, authorized values are stored.

**Key Takeaways:**
- Implementing data validation mechanisms is a fundamental practice in both relational and linked data models.

---

**iii. List all the tables you would need for a relational model of this data, including primary and foreign keys for each.** [8 marks]

**Answer:**
1. **People Table:** `PersonID (Primary Key)`, `FirstName`, `Email`, `Cell`
2. **Likes Table:** `LikeID (Primary Key)`, `PersonID (Foreign Key)`, `Interest`
3. **Businesses Table:** `BusinessID (Primary Key)`, `PersonID (Foreign Key)`, `Name`, `Partner`, `Status`, `DateFounded`

**Detailed Explanation:**
- The relational model splits the JSON document into normalized tables, with `PersonID` used to link related records.

**Real-World Scenario Connection:**
- Normalizing data into a relational structure is common in traditional enterprise applications, where consistent relationships and data integrity are prioritized.

**Important Points to Remember:**
- Foreign keys enforce relationships between tables, maintaining data consistency across multiple entities.

**Key Takeaways:**
- Converting complex document structures into relational tables requires careful design to maintain data integrity while supporting complex queries.

---

**iv. Evaluate these THREE models (document, relational, and Linked Data/graph) for this sort of data. What would you need to know about the intended application to decide between them?** [8 marks]

**Answer:**
- **Document Model (e.g., MongoDB):** Best for semi-structured data where flexibility and varied schemas are required. Ideal for scenarios where quick iteration and adaptability are key.
- **Relational Model:** Provides strong consistency, enforceable relationships, and optimized queries. Best suited for applications with clearly defined data structures and heavy reliance on complex queries.
- **Graph/Linked Data Model:** Excels at representing and querying complex relationships, particularly in highly connected data like social graphs or knowledge networks.

**Real-World Scenario Connection:**
- E-commerce platforms may choose document models for product catalogs, while traditional business applications often rely on relational models for transaction processing. Linked Data models are favored in research and knowledge representation.

**Important Points to Remember:**
- The choice of data model should be informed by factors such as query complexity, data variability, and the scalability requirements of the application.

**Key Takeaways:**
- Different models serve different use cases, and selecting the right one requires understanding the specific needs of your project.

---
