
---

### **Question 1: Database Design for Real Estate Agency**

---

**a. Add cardinality indications for this diagram.** [3 marks]

**Answer:**
The cardinalities are as follows:
- **Sellers to Properties:** One seller can have many properties (1:M).
- **Properties to Agents:** Each property is handled by one agent (1:1).
- **Properties to Viewings:** Each property can have many viewings (1:M).
- **Viewings to Buyers:** Each viewing can involve multiple buyers (M:M).
- **Offers to Properties:** Each property can receive multiple offers (1:M).

**Detailed Explanation:**
- **Cardinality in ER Diagrams:** Cardinality represents the number of entities that can participate in a relationship, reflecting real-world scenarios accurately.
- **Examples in Real Estate:** For instance, properties typically receive multiple offers, but each offer is associated with a single property (1:M).

**Real-World Scenario Connection:**
In real estate management systems, ensuring correct cardinality is crucial for representing relationships such as properties handled by agents and multiple offers per property.

**Common Pitfalls and Mistakes:**
- **Incorrect Cardinality Representation:** Misrepresenting one-to-many or many-to-many relationships can lead to flawed database designs.
- **Ignoring Optionality:** Failing to indicate whether relationships are mandatory or optional can lead to misunderstandings in design.

**Important Points to Remember:**
- Correctly defining cardinality is key to structuring relational databases and understanding the relationships between entities.
- Always review real-world scenarios to ensure that your cardinality matches business rules.

**Key Takeaways:**
Understanding and correctly assigning cardinalities is a fundamental step in ER diagram design. Proper representation of relationships leads to more accurate and scalable databases.

---

**b. How would you adapt this to a relational model? Be specific, naming any new entities, relations, or attributes.** [5 marks]

**Answer:**
The relational model would involve:
- **Tables:** Sellers, Properties, Agents, Viewings, Buyers, Offers
- **Relations/Attributes:**
  - **Sellers Table:** SellerID (Primary Key), Name, ContactInfo
  - **Properties Table:** PropertyID (Primary Key), SellerID (Foreign Key), AgentID (Foreign Key), Type, Bedrooms, AskingPrice
  - **Agents Table:** AgentID (Primary Key), Name, CommissionRate
  - **Viewings Table:** ViewingID (Primary Key), PropertyID (Foreign Key), BuyerID (Foreign Key), DateTime
  - **Buyers Table:** BuyerID (Primary Key), Name, ContactInfo
  - **Offers Table:** OfferID (Primary Key), PropertyID (Foreign Key), OfferStage, OfferAmount

**Detailed Explanation:**
- **Entities and Relationships:** Each table represents an entity, and foreign keys enforce relationships, maintaining referential integrity.
- **Normalization:** The design adheres to normalization principles to reduce redundancy and prevent data anomalies.

**Real-World Scenario Connection:**
In real estate systems, data models must accurately capture the relationships between agents, properties, buyers, and offers. This structure supports key functions like managing listings, scheduling viewings, and processing offers.

**Common Pitfalls and Mistakes:**
- **Improper Normalization:** Skipping normalization can lead to redundant data and update issues.
- **Unclear Foreign Key Definitions:** Ensure that foreign keys correctly reference primary keys in related tables.

**Important Points to Remember:**
- The goal of converting an ER diagram to a relational model is to create a well-structured, normalized database that minimizes redundancy and ensures data integrity.

**Key Takeaways:**
Adapting an ER diagram into a relational model involves creating tables, defining relationships, and setting up primary and foreign keys. Properly structured tables result in an efficient and reliable database.

---

**c. List the tables, primary and foreign keys for a relational implementation of this database.** [6 marks]

**Answer:**
- **Sellers Table:** Primary Key: SellerID
- **Properties Table:** Primary Key: PropertyID, Foreign Keys: SellerID, AgentID
- **Agents Table:** Primary Key: AgentID
- **Viewings Table:** Primary Key: ViewingID, Foreign Keys: PropertyID, BuyerID
- **Buyers Table:** Primary Key: BuyerID
- **Offers Table:** Primary Key: OfferID, Foreign Key: PropertyID

**Detailed Explanation:**
- **Primary Keys:** Uniquely identify each record within a table.
- **Foreign Keys:** Link related data across tables, ensuring that relationships like “which agent handles which property” are correctly enforced.

**Real-World Scenario Connection:**
Relational databases are widely used in real estate management systems to maintain clear and accurate relationships between properties, agents, buyers, and offers.

**Common Pitfalls and Mistakes:**
- **Mismatched Key Types:** Ensure that primary and foreign keys are of compatible data types.
- **Omitting Foreign Keys:** Missing foreign keys can lead to orphaned records and broken relationships in the database.

**Important Points to Remember:**
- Correctly defining primary and foreign keys is crucial for maintaining relational integrity and supporting effective query performance.

**Key Takeaways:**
Defining primary and foreign keys ensures robust data relationships, facilitating efficient queries and maintaining database consistency.

---

**d. Give the MySQL command for creating one of those tables.** [3 marks]

**Answer:**
```sql
CREATE TABLE Properties (
    PropertyID INT PRIMARY KEY AUTO_INCREMENT,
    SellerID INT,
    AgentID INT,
    Type VARCHAR(50),
    Bedrooms INT,
    AskingPrice DECIMAL(10, 2),
    FOREIGN KEY (SellerID) REFERENCES Sellers(SellerID),
    FOREIGN KEY (AgentID) REFERENCES Agents(AgentID)
);
```

**Detailed Explanation:**
- **Table Structure:** The table includes fields like `PropertyID`, `SellerID`, and `AgentID`, with appropriate data types.
- **Foreign Key Constraints:** Foreign keys ensure that each property is linked to a valid seller and agent.

**Real-World Scenario Connection:**
Creating tables using SQL is a fundamental task in any relational database, allowing businesses to store and query structured data.

**Common Pitfalls and Mistakes:**
- **Incorrect Data Types:** Be careful to use the right data types for each attribute.
- **Missing Constraints:** Ensure that foreign key constraints are in place to prevent invalid data entries.

**Important Points to Remember:**
- Pay attention to SQL syntax, data types, and constraints to ensure that tables are well-structured and maintain data integrity.

**Key Takeaways:**
Mastering SQL for table creation is essential for database design and implementation, ensuring that data is organized, consistent, and ready for querying.

---

**e. Agents are paid a commission on property where the offer gets to ‘sale completed’ status. The commission is 1% of the sale price.**

**i. Write a MySQL query to calculate and list the commission earned since 1 January 2023 for each Estate Agent.** [6 marks]

**Answer:**
```sql
SELECT AgentID, SUM(AskingPrice * 0.01) AS TotalCommission
FROM Properties
JOIN Offers ON Properties.PropertyID = Offers.PropertyID
WHERE Offers.OfferStage = 'sale completed' AND Offers.Date >= '2023-01-01'
GROUP BY AgentID;
```

**Detailed Explanation:**
- **Calculation Logic:** The query multiplies the sale price by 1% to calculate the commission.
- **Grouping by Agent:** `GROUP BY AgentID` aggregates commissions for each agent, showing total earnings.

**Real-World Scenario Connection:**
This query could be used in real estate businesses to generate reports on agent performance and calculate sales commissions.

**Common Pitfalls and Mistakes:**
- **Incorrect Grouping:** Forgetting to group results can lead to incorrect calculations.
- **Date Format Issues:** Ensure that date conditions are in the correct format (YYYY-MM-DD) to avoid query errors.

**Important Points to Remember:**
- Use aggregate functions like `SUM` and `GROUP BY` for financial calculations involving multiple records.

**Key Takeaways:**
SQL’s grouping and aggregation features are crucial for business analytics, enabling organizations to generate insights from large datasets.

---

**ii. Modify your query from (i) above to list just the top-earning agent.** [2 marks]

**Answer:**
```sql
SELECT AgentID, SUM(AskingPrice * 0.01) AS TotalCommission
FROM Properties
JOIN Offers ON Properties.PropertyID = Offers.PropertyID
WHERE Offers.OfferStage = 'sale completed' AND Offers.Date >= '2023-01-01'
GROUP BY AgentID
ORDER BY TotalCommission DESC
LIMIT 1;
```

**Detailed Explanation:**
- **Sorting:** The query uses `ORDER BY TotalCommission DESC` to rank agents by earnings and `LIMIT 1` to return only the top result.

**Real-World Scenario Connection:**
Businesses often need to identify top performers, whether for recognition or targeted improvement efforts.

**Common Pitfalls and Mistakes:**
- **Incorrect Ordering:** Ensure that results are sorted in the right direction (e.g., descending for top earners).

**Important Points to Remember:**
- Use `ORDER BY` and `LIMIT` to refine query results when specific ranking or filtering is required.

**Key Takeaways:**
Filtering and ranking query results are key skills for generating actionable insights in data analytics.

---

**f. The IT specialist at the agency is considering using a document database instead of a relational database. Give reasons specific to this use case for why this might be a good or bad idea (general observations about the difference between models do not receive marks).** [5 marks]

**Answer:**
Using a document database could be beneficial if:
- The agency deals with unstructured

 or semi-structured data (e.g., varying property details).
- Flexibility is needed in data schema as different properties might have diverse attributes.

However, it might be a bad idea because:
- Relationships between entities (e.g., sellers, properties, agents) are better handled in a relational database.
- Querying complex relationships (e.g., calculating commissions) is more straightforward in a relational model.

**Detailed Explanation:**
- **Document Database vs. Relational Database:** While document databases like MongoDB offer flexibility, they may fall short when managing highly structured, relational data.

**Real-World Scenario Connection:**
In real estate, relational databases are commonly preferred for managing structured data relationships, while document databases are more suitable for handling varied or nested data types.

**Important Points to Remember:**
- The choice of database model should be driven by the specific data structure and business needs of the application.

**Key Takeaways:**
Selecting the right database model requires understanding the strengths and limitations of each approach, especially in terms of scalability, query complexity, and data consistency.

---

### **Question 3: Machine Learning Metrics and Document Databases**

---

**a. If the system lists 2,200,000 books as being in German, how many of these are likely to be in German?** [2 marks]

**Answer:**
\[ \text{True Positives} = 2,200,000 \times 0.8 = 1,760,000 \] books are likely to be in German.

**Detailed Explanation:**
- **Understanding Precision:** Precision represents the proportion of correctly identified positives out of all identified positives. Here, 80% of the books classified as German are indeed in German.

**Real-World Scenario Connection:**
In text classification tasks like language detection, precision ensures that the identified items are mostly correct, reducing noise in the dataset.

**Common Pitfalls and Mistakes:**
- **Misinterpreting Precision and Recall:** Precision focuses only on the positive predictions, not the overall dataset.

**Important Points to Remember:**
- Precision is critical when false positives are costly, as in cases of spam detection or medical diagnoses.

**Key Takeaways:**
Understanding model evaluation metrics is essential for assessing the performance of classification models in real-world applications.

---

**b. Given your answer to (a), how many books in the whole collection are likely to be in German (including those that haven’t been classified as German)?** [3 marks]

**Answer:**
Let \( x \) be the total number of German books. The recall (88%) implies:

\[ \frac{1,760,000}{x} = 0.88 \Rightarrow x = \frac{1,760,000}{0.88} \approx 2,000,000 \]

So, approximately 2,000,000 books in the whole collection are likely to be in German.

**Detailed Explanation:**
- **Recall Calculation:** Recall measures how well the model identifies actual positives. In this case, 88% of all German books are correctly identified.

**Real-World Scenario Connection:**
Recall is critical in fields where missing a positive instance is more concerning than having false positives, like disease screening.

**Common Pitfalls and Mistakes:**
- **Confusing Precision with Recall:** Precision focuses on the proportion of true positives among predicted positives, while recall considers true positives among all actual positives.

**Important Points to Remember:**
- Balancing precision and recall depends on the context and the cost of false positives versus false negatives.

**Key Takeaways:**
Understanding the trade-off between precision and recall helps in optimizing machine learning models based on specific application needs.

---

**c. Danish language fiction is identified with 100% precision and 76% recall. If texts from the labelled books are going to be used for machine learning systems, why might this performance be more useful than the accuracy of German classification?** [5 marks]

**Answer:**
For building training datasets, high precision (100%) ensures that all selected texts are indeed in Danish, leading to high-quality training data. Even though the recall is 76%, meaning some Danish books are missed, the precision guarantees that the model isn't trained on irrelevant data, which is crucial for model accuracy.

**Detailed Explanation:**
- **Importance of Precision in Training Data:** High precision is more valuable for training data as it ensures that the input data is accurate and consistent.

**Real-World Scenario Connection:**
In natural language processing (NLP), having a clean dataset (with high precision) is often more beneficial than having a large dataset with potential noise.

**Common Pitfalls and Mistakes:**
- **Overemphasizing Quantity:** Collecting large amounts of training data with low precision can lead to poor model performance.

**Important Points to Remember:**
- Prioritize high precision when selecting training data to avoid introducing noise and inaccuracies into the model.

**Key Takeaways:**
For tasks requiring high-quality training data, high precision ensures that only relevant data is included, leading to better model performance.

---

**d. The F1 measure for these are (German) and (Danish). What is an F1-measure?** [2 marks]

**Answer:**
The F1-measure is the harmonic mean of precision and recall, providing a single metric that balances both. It is defined as:

\[ F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \]

**Detailed Explanation:**
- **When to Use F1:** The F1 score is most useful when there is a need to balance precision and recall, particularly in cases where there is an uneven class distribution.

**Real-World Scenario Connection:**
The F1 score is commonly used in imbalanced classification tasks, such as fraud detection, where both false positives and false negatives have significant costs.

**Common Pitfalls and Mistakes:**
- **Overreliance on Accuracy:** In scenarios with imbalanced data, accuracy can be misleading, making F1 a better metric.

**Important Points to Remember:**
- F1 score provides a more balanced evaluation when both false positives and false negatives matter.

**Key Takeaways:**
F1 is a valuable metric when you need to consider both precision and recall, offering a holistic view of model performance.

---

**e. The researcher has made a local document database to store a selection of transcribed books. They run the following command:**

```plaintext
db.books.find({ lang: "German" })
```

**What does this command do?** [1 mark]

**Answer:**
The command retrieves all documents from the "books" collection where the language is "German."

**Detailed Explanation:**
- **Basic MongoDB Queries:** MongoDB’s `find` method allows you to query documents based on specific criteria, in this case filtering by language.

**Real-World Scenario Connection:**
Document databases like MongoDB are widely used for managing large collections of unstructured text, such as digital libraries or content management systems.

**Common Pitfalls and Mistakes:**
- **Incorrect Filter Criteria:** Ensure that the filter accurately represents the condition you want to query.

**Important Points to Remember:**
- MongoDB’s `find` method is a fundamental operation for retrieving specific data from a document store.

**Key Takeaways:**
Understanding how to perform basic queries in document databases is essential for working with unstructured data collections.

---

**f. Books in the database have a ‘year’ field. Rewrite the command to include only volumes published in the nineteenth century.** [5 marks]

**Answer:**
```plaintext
db.books.find({ lang: "German", year: { $gte: 1800, $lt: 1900 } })
```

**Detailed Explanation:**
- **Date Range Queries:** The query filters results based on a range of years using MongoDB’s `$gte` (greater than or equal to) and `$lt` (less than) operators.

**Real-World Scenario Connection:**
Date-based filtering is commonly used in libraries, archives, and historical research databases to retrieve records within specific time frames.

**Common Pitfalls and Mistakes:**
- **Incorrect Date Range:** Ensure the range accurately represents the intended period (in this case, 1800 to 1899).

**Important Points to Remember:**
- MongoDB’s query operators allow for precise filtering based on numeric ranges, dates, and more.

**Key Takeaways:**
Mastering query operators is key to retrieving relevant records from document databases, especially when working with time-sensitive or historical data.

---

**g. Book contents are included in a single textual field called “text”. How would you adjust your query to include only books containing the word “Strudel”?** [2 marks]

**Answer:**
```plaintext
db.books.find({ lang: "German", year: { $gte: 1800, $lt: 1900 }, text: /Strudel/ })
```

**Detailed Explanation:**
- **Using Regular Expressions:** The query uses a regular expression `/Strudel/` to search for books containing the specified word within the text field.

**Real-World Scenario Connection:**
Regular expressions are commonly used in search engines, text analysis tools, and content management systems to locate specific words or patterns.

**Common Pitfalls and Mistakes:**
- **Case Sensitivity:** Regular expressions in MongoDB are case-sensitive by default; consider adding options if needed.

**Important Points to Remember:**
- Regular expressions are a powerful tool for searching unstructured text fields in document databases.

**Key Takeaways:**
Leveraging regular expressions allows for flexible and powerful text searches in document-oriented databases.

---

**h. In order to represent the books’ content and structure more accurately, the researcher is trying to choose between enriching this database or switching to an XML database using TEI to encode book content and catalogue information. What factors should the researcher take into account in their decision

?** [10 marks]

**Answer:**
The researcher should consider the following factors:
- **Data Flexibility vs Structure:** A document database like MongoDB offers flexibility for unstructured data, whereas an XML database using TEI (Text Encoding Initiative) provides a structured and hierarchical format ideal for detailed textual analysis.
- **Query Complexity:** While MongoDB is suitable for straightforward text search, TEI in an XML database allows for more complex queries using XPath or XQuery.
- **Interoperability:** TEI is a widely accepted standard in the humanities, facilitating collaboration and data exchange between institutions.
- **Scalability and Performance:** MongoDB is optimized for large-scale datasets, while XML databases may face performance issues when handling large volumes of complex documents.
- **Data Integrity and Preservation:** TEI’s structure is better suited for long-term preservation and scholarly integrity in digital humanities projects.

**Detailed Explanation:**
- The decision involves trade-offs between flexibility, structure, and long-term sustainability. XML databases with TEI encoding offer rich metadata and hierarchical structures that are ideal for scholarly work, while MongoDB provides scalability and ease of use.

**Real-World Scenario Connection:**
Researchers in the digital humanities often choose between these options depending on whether they prioritize structured metadata (XML/TEI) or flexibility and scalability (document databases).

**Common Pitfalls and Mistakes:**
- **Choosing the Wrong Model:** Select the model that aligns with both current project needs and future scalability or preservation requirements.

**Important Points to Remember:**
- The choice between database models should be guided by the specific requirements of the project, including data complexity, query needs, and the intended audience.

**Key Takeaways:**
Understanding the trade-offs between different data models is crucial for designing effective and sustainable systems for scholarly research.

---

### **Question 4: SPARQL and RDF Models**

---

**a. The fragment below shows a serialization of a data interchange model. Give a brief explanation of each prefix used.**

```plaintext
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix oa: <http://www.w3.org/ns/oa#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix myrdf: <http://example.org/> .
@prefix armadale: <https://literary-greats.com/WCollins/Armadale/> ;
```

**Answer:**

- **dcterms:** Refers to the Dublin Core Metadata Terms vocabulary, commonly used for describing resources (e.g., creator, date, subject).
- **foaf:** Refers to the Friend of a Friend (FOAF) ontology, used to describe people, their relationships, and online accounts.
- **oa:** Refers to the Open Annotation Data Model, used for describing annotations and their relationships to resources.
- **rdf:** Refers to the core RDF schema namespace, providing basic RDF constructs like `rdf:type`.
- **xsd:** Refers to XML Schema Definition, defining data types such as `xsd:dateTime`.
- **myrdf:** A custom namespace used in the RDF model for defining specific resources or terms within the example domain.
- **armadale:** A custom namespace likely referring to a literary resource, e.g., a work by W. Collins titled "Armadale."

**Detailed Explanation:**

- The prefixes are used to simplify RDF statements by avoiding the need to write full URIs for every resource or property. By associating a prefix with a namespace, the RDF model becomes more concise and readable.

**Real-World Scenario Connection:**

Using these prefixes is essential when working with RDF data in contexts such as publishing linked open data, annotating resources, or integrating different vocabularies in semantic web applications. RDF prefixes make the data easier to query and understand, especially in large-scale datasets.

**Common Pitfalls and Mistakes:**

- **Misunderstanding Prefix Usage:** Forgetting to declare prefixes or mixing up namespaces can lead to invalid RDF or SPARQL queries.
- **Confusing Standard and Custom Prefixes:** Always be clear which prefixes are standard (like `rdf` or `xsd`) and which are custom for your specific dataset (like `myrdf`).

**Important Points to Remember:**

- Understand the commonly used prefixes like `rdf`, `xsd`, and `dcterms` since they are widely adopted across RDF datasets.
- Use namespaces consistently and document any custom prefixes clearly.

**Key Takeaways:**

Understanding and correctly using namespaces and prefixes is crucial when working with RDF models in SPARQL or linked data contexts.

---

**b. Name two ontologies used in this document.** [3 marks]

**Answer:**

1. **Dublin Core Terms (dcterms):** Used for metadata descriptions such as the date and creator of the resource.
2. **Friend of a Friend (FOAF):** Used to describe people and relationships.

**Detailed Explanation:**

- The document uses well-known ontologies (Dublin Core and FOAF) to represent metadata and relationships between entities. These ontologies are widely adopted across various domains and provide a standard way of describing common attributes like names, dates, and relationships.

**Real-World Scenario Connection:**

These ontologies are standard across libraries, archives, and semantic web applications where data needs to be described consistently and interoperably. Using recognized ontologies ensures that data is easily shareable and understood across different systems.

**Common Pitfalls and Mistakes:**

- **Ignoring Standard Ontologies:** Re-inventing attributes or classes instead of using existing standards can reduce data interoperability and make integration more difficult.

**Important Points to Remember:**

- Leveraging well-established ontologies makes your data more compatible with other datasets and easier to integrate into larger knowledge graphs.

**Key Takeaways:**

Selecting the right ontologies and integrating them into your RDF data model is key to successful linked data projects. Familiarity with common ontologies like Dublin Core and FOAF is essential for creating interoperable and reusable RDF data.

---

**c. For each ontology named in your previous answer, name all the properties from the ontology that are used in this document.** [5 marks]

**Answer:**

1. **Dublin Core Terms (dcterms):**
   - **dcterms:created:** Specifies the creation date of the annotation.
   - **dcterms:creator:** Specifies the creator of the annotation.

2. **Friend of a Friend (FOAF):**
   - **foaf:name:** Specifies the name of the person (in this case, "David Lewis").

**Detailed Explanation:**

- The document uses the `dcterms` ontology to describe metadata (like the creation date and creator of an annotation) and the `foaf` ontology to describe personal information (like the name of a creator). These properties are widely used and recognized in RDF datasets, ensuring compatibility and ease of querying.

**Real-World Scenario Connection:**

Libraries, archives, and knowledge graphs often use these properties for cataloging digital objects and representing relationships between people and resources. The consistent use of properties across datasets enhances interoperability and data sharing.

**Common Pitfalls and Mistakes:**

- **Overlooking Available Properties:** Always check existing ontologies before creating custom properties, as using standard properties enhances data compatibility.

**Important Points to Remember:**

- Reusing properties from standard ontologies ensures consistency across RDF datasets and makes your data easier to query.

**Key Takeaways:**

Familiarity with common properties in widely used ontologies is essential for RDF data modeling and semantic web applications.

---

**d. This structure is a Web Annotation (previously called Open Annotation). The BODY of the annotation contains a comment on the TARGET, which is often a part of a SOURCE. In this case, an online chapter of a book is the source, some part of which is being selected as a target. A scholar would like to get all the annotations in a database about this particular chapter – they just want the annotation text and the name of the author. They have tried the following SPARQL, but it doesn’t work. Write a correct version that will do what they ask.**

```plaintext
SELECT ?body ?creator
WHERE {
  ?annotation a oa:Annotation .
  ?creator ;
  oa:hasBody ?body .
  oa:hasSource armadale:Chapter3 .
}
```

**Answer:**

Correct SPARQL query:
```sparql
SELECT ?body ?creator
WHERE {
  ?annotation a oa:Annotation ;
              oa:hasBody ?body ;
              oa:hasTarget [
                oa:hasSource armadale:Chapter3
              ] ;
              dcterms:creator ?creator .
}
```

**What will it return:**
- The query returns the body of each annotation (`?body`) and the creator’s name (`?creator`) for annotations targeting Chapter 3 of the work "Armadale."

**Detailed Explanation:**

- The `oa:hasTarget` property is used to specify the target of the annotation, which includes a nested structure using square brackets to reference the source (`armadale:Chapter3`).
- The `dcterms:creator` property is used to fetch the author of the annotation, ensuring that only the relevant annotations are returned.

**Real-World Scenario Connection:**

SPARQL queries like this are common in digital humanities projects, where scholars query linked data repositories for annotations, notes, and references in literary texts.

**Common Pitfalls and Mistakes:**

- **Incorrect Use of Square Brackets:** Forgetting the square brackets when navigating nested relationships can lead to incorrect or incomplete query results.
- **Inconsistent Property Usage:** Be consistent in using properties defined in the ontology, like `oa:hasTarget` and `dcterms:creator`.

**Important Points to Remember:**

- Understanding how to navigate relationships in RDF data is critical for constructing effective SPARQL queries.
- The correct structure for `oa:hasTarget` includes using square brackets `[ ]` to define nested relationships.

**Key Takeaways:**

Mastering SPARQL is essential for querying complex RDF datasets and retrieving exactly the information needed. Understanding RDF relationships and how to represent them in SPARQL is key for effective data retrieval.

---

**e. Some linked data systems use a backend database to store the data and for quick retrieval, exporting it as needed. Draw an ER diagram for web annotations like this.** [5 marks]

**Answer:**
The ER diagram for a web annotation system might include the following entities:
- **Annotation** (with attributes like AnnotationID, Body, Creator, Date)
- **Target** (with attributes like TargetID, Source, Selector)
- **Source** (with attributes like SourceID, Title, URI)

**Relationships:**
- Annotation **targets** Target (1:M)
- Target **refers to** Source (1:1)

**ER Diagram:**
```mermaid
erDiagram
    Annotation {
        AnnotationID PK
        Body TEXT
        Creator VARCHAR
        Date DATE
    }
    Target {
        TargetID PK
        Source VARCHAR
        Selector VARCHAR
    }
    Source {
        SourceID PK
        Title VARCHAR
        URI VARCHAR
    }
    Annotation ||--o{ Target : targets
    Target ||--|| Source : refers_to
```

**Detailed Explanation:**

- The diagram represents how annotations relate to targets and how those targets map to

 specific sources in web annotation systems. The 1:M relationship between Annotation and Target indicates that multiple annotations can refer to the same target, while each target is linked to one source.

**Real-World Scenario Connection:**

Annotations and targets are common in academic research, where scholars annotate digital documents and link annotations to specific text fragments.

**Common Pitfalls and Mistakes:**

- **Incorrect Relationship Representation:** Ensure that relationships accurately reflect the connections between entities in your data model.
- **Overcomplicating the Model:** Keep the diagram focused on core entities and relationships relevant to the use case.

**Important Points to Remember:**

- ER diagrams are useful for conceptualizing relational databases, even in linked data contexts.
- Consider how RDF triples and relationships map to relational database structures.

**Key Takeaways:**

Understanding how to model relationships between annotations, targets, and sources is key for building systems that manage scholarly notes and references.

---

**f. Identify the tables that you would need for a relational implementation and list the keys for each.** [5 marks]

**Answer:**

1. **Annotations Table:**
   - **Primary Key:** AnnotationID
   - **Foreign Key:** TargetID

2. **Targets Table:**
   - **Primary Key:** TargetID
   - **Foreign Key:** SourceID

3. **Sources Table:**
   - **Primary Key:** SourceID

**Detailed Explanation:**

- The relational model mirrors the ER diagram, ensuring that each annotation is linked to a target, which in turn is linked to a source. This structure supports efficient querying and maintains data integrity.

**Real-World Scenario Connection:**

This structure could be used in digital libraries, where annotations need to be linked to specific sections of digital texts, allowing for detailed analysis and referencing.

**Common Pitfalls and Mistakes:**

- **Unclear Foreign Key Definitions:** Ensure that foreign keys are correctly defined to maintain referential integrity across tables.

**Important Points to Remember:**

- Relational models often require breaking down entities and relationships from an RDF model into related tables.

**Key Takeaways:**

Mapping RDF structures to relational tables involves carefully defining foreign keys and ensuring that relationships are maintained across tables.

---

**g. Give a MySQL query equivalent for the scholar’s query you corrected in question (d).** [3 marks]

**Answer:**
```sql
SELECT a.Body, a.Creator
FROM Annotations a
JOIN Targets t ON a.TargetID = t.TargetID
JOIN Sources s ON t.SourceID = s.SourceID
WHERE s.Title = 'Armadale' AND s.Chapter = 'Chapter3';
```

**Detailed Explanation:**

- The SQL query joins the annotations, targets, and sources tables to retrieve the annotation body and creator for entries related to Chapter 3 of "Armadale." The relational approach captures the same relationships that would be expressed in SPARQL, but using SQL.

**Real-World Scenario Connection:**

SQL queries like this are common when retrieving annotations, comments, or notes from relational databases, especially in digital archives and content management systems.

**Common Pitfalls and Mistakes:**

- **Incorrect Joins:** Ensure that joins are correctly defined to link related tables without introducing errors or duplicate results.

**Important Points to Remember:**

- SQL’s `JOIN` operations allow linking related data across multiple tables, just like navigating relationships in SPARQL.

**Key Takeaways:**

Translating SPARQL queries into SQL involves understanding how RDF relationships map to joins and foreign keys in a relational database.

---
