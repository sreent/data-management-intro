### Solution Sheet for Questions 2, 3, and 4

---

### Question 2: ER Diagram and Relational Database for an Estate Agency

**a. Add cardinality indications for this diagram.** [3 marks]

**Answer:**
The cardinalities are as follows:
- **Sellers to Properties:** One seller can have many properties (1:M).
- **Properties to Agents:** Each property is handled by one agent (1:1).
- **Properties to Viewings:** Each property can have many viewings (1:M).
- **Viewings to Buyers:** Each viewing can involve multiple buyers (M:M).
- **Offers to Properties:** Each property can receive multiple offers (1:M).

**Detailed Explanation:**
- Cardinalities define the nature of relationships between entities in an ER diagram.
- The estate agency example shows common 1:M relationships, e.g., a property can have many offers, but each offer is related to one property.

**Real-World Scenario Connection:**
These cardinality relationships reflect typical business scenarios in real estate where agents handle multiple properties and properties receive multiple offers.

**Important Points to Remember:**
- Cardinality is essential for structuring relational databases correctly.
- Misrepresenting cardinalities can lead to inaccurate data models and database queries.

**Key Takeaways:**
Understanding and correctly assigning cardinalities is a fundamental step in ER diagram design.

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
- The relational model converts each entity and relationship from the ER diagram into a table.
- Foreign keys enforce relationships between tables, ensuring data integrity.

**Real-World Scenario Connection:**
In real estate systems, the relational model aligns with how databases track properties, agents, buyers, and offers.

**Important Points to Remember:**
- Properly defining primary and foreign keys ensures data relationships are maintained.

**Key Takeaways:**
Adapting an ER diagram into a relational model involves creating tables and setting up relationships using primary and foreign keys.

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
- Primary keys uniquely identify each record in a table.
- Foreign keys establish relationships between tables by linking related data.

**Real-World Scenario Connection:**
Relational databases are commonly used in real estate agencies to manage data relationships effectively.

**Important Points to Remember:**
- Defining primary and foreign keys correctly is crucial for relational database design.

**Key Takeaways:**
Correctly identifying primary and foreign keys is a key aspect of transitioning an ER model to a relational database.

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
- The command creates a Properties table with relevant fields and sets up foreign keys to the Sellers and Agents tables.

**Real-World Scenario Connection:**
SQL is the primary language used in relational databases to create, query, and manage tables in various industries.

**Important Points to Remember:**
- SQL syntax and accurate data types are critical for database integrity.
- Use `AUTO_INCREMENT` for primary keys to automatically generate unique IDs.

**Key Takeaways:**
Writing MySQL commands requires understanding the structure of your data model and translating it into code.

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
- The query calculates the commission by multiplying the sale price by 1% and groups results by agent.

**Real-World Scenario Connection:**
Sales commissions are calculated in many business contexts, especially in sales-driven fields like real estate.

**Important Points to Remember:**
- `GROUP BY` is crucial for aggregating results by a specific field, such as AgentID.
- Always ensure date filters use the correct format (YYYY-MM-DD).

**Key Takeaways:**
Understanding how to perform calculations and group results in SQL is essential for generating business insights.

---

**ii. Modify your query from (i) above to list just the top earning agent.** [2 marks]

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
- The query now orders results by the total commission in descending order and uses `LIMIT 1` to get the top earning agent.

**Real-World Scenario Connection:**
Identifying top performers is a common requirement in business analytics.

**Important Points to Remember:**
- `ORDER BY` and `LIMIT` are powerful tools for ranking and filtering results.

**Key Takeaways:**
Filtering and sorting are critical skills for advanced SQL queries.

---

**f. The IT specialist at the agency is considering using a document database instead of a relational database. Give reasons specific to this use case for why this might be a good or bad idea (general observations about the difference between models do not receive marks).** [5 marks]

**Answer:**
Using a document database could be beneficial if:
- The agency deals with unstructured or semi-structured data (e.g., different formats of property details).
- Flexibility is needed in data schema as different properties might have varying attributes.

However, it might be a bad idea because:
- Relationships between entities (e.g., sellers, properties, agents) are better handled in a relational database.
- Querying complex relationships (e.g., calculating commissions) is more straightforward in a relational model.

**Detailed Explanation:**
- Document databases (e.g., MongoDB) excel in scenarios requiring flexibility, but relational databases are preferred for structured, relational data.

**Real-World Scenario Connection:**
Businesses often need to evaluate the trade-offs between different database models depending on their use case.

**Important Points to Remember:**
- The choice between database models should be based on the data structure, query needs, and expected scalability.

**Key Takeaways:**
Understanding when to use different database models is key to designing efficient data solutions.

---

### Question 3: Machine Learning and Document Databases in Digital Libraries

**a. If the system lists 2,200,000 books as being in German, how many of these are likely to be in German?** [2 marks]

**Answer:**
\( \text{True Positives} = 2,200,000 \times 0.8 = 1,760,000 \) books are likely to be in German.

**Detailed Explanation:**
- The precision (80%) tells us that 80% of the classified books are indeed in German.

**Real-World Scenario Connection:**
Precision is used to measure the accuracy of classification models in various domains, such as text classification and spam detection.

**Important Points to Remember:**
- Precision is the ratio of true positives to all positives predicted by the model.

**Key Takeaways:**
Understanding model evaluation metrics like precision is crucial for assessing machine learning performance.

---

**b. Given your answer to (a), how many books in the whole collection are likely to be in German (including those that haven’t been classified as German)?** [3 marks]

**Answer:**
Let \( x \) be the total number of German books. The recall (88%) implies:

\[ \frac{1,760,000}{x} = 0.88 \Rightarrow x = \frac{1,760,000}{0.88} \approx

 2,000,000 \]

So, approximately 2,000,000 books in the whole collection are likely to be in German.

**Detailed Explanation:**
- Recall measures the proportion of actual positives (German books) correctly identified by the model.

**Real-World Scenario Connection:**
Recall is particularly important in scenarios where missing true positives can be costly, such as medical diagnoses.

**Important Points to Remember:**
- Recall is the ratio of true positives to all actual positives in the dataset.

**Key Takeaways:**
Balancing precision and recall is key for optimizing classification models.

---

**c. Danish language fiction is identified with 100% precision and 76% recall. If texts from the labelled books are going to be used for machine learning systems, why might this performance be more useful than the accuracy of German classification?** [5 marks]

**Answer:**
For building training datasets for machine learning models, high precision (100%) ensures that all selected texts are indeed in Danish, leading to high-quality training data. Even though the recall is 76%, meaning some Danish books are missed, the precision guarantees that the model isn't trained on irrelevant data, which is critical for model accuracy.

**Detailed Explanation:**
- High precision ensures the correctness of the data used for training, which is more important than quantity when quality is crucial.

**Real-World Scenario Connection:**
In NLP tasks, having a cleaner dataset (with high precision) is often more valuable than having a larger but noisier dataset.

**Important Points to Remember:**
- Precision matters more when false positives can degrade the performance of downstream models.

**Key Takeaways:**
When preparing training datasets, prioritizing high precision ensures that only relevant and accurate data is included.

---

**d. The F1 measure for these are (German) and (Danish). What is an F1-measure?** [2 marks]

**Answer:**
The F1-measure is the harmonic mean of precision and recall, providing a single metric that balances both. It is defined as:

\[ F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \]

**Detailed Explanation:**
- The F1 score is used when there is a need to balance precision and recall, particularly in cases of uneven class distribution.

**Real-World Scenario Connection:**
F1 score is often used in imbalanced classification tasks, such as fraud detection or disease screening.

**Important Points to Remember:**
- The F1 score is most useful when there is a trade-off between precision and recall.

**Key Takeaways:**
Understanding the F1 score is critical for evaluating models where false positives and false negatives have different costs.

---

**e. The researcher has made a local document database to store a selection of transcribed books. They run the following command:**

```plaintext
db.books.find({ lang: "German" })
```

**What does this command do?** [1 mark]

**Answer:**
The command retrieves all documents from the "books" collection where the language is "German."

**Detailed Explanation:**
- In MongoDB, the `find` method searches the collection based on the specified filter criteria.

**Real-World Scenario Connection:**
Document databases like MongoDB are popular for handling large text datasets, such as digital libraries.

**Important Points to Remember:**
- The `find` method is the most commonly used query operation in MongoDB.

**Key Takeaways:**
Knowing basic MongoDB commands is essential for working with unstructured or semi-structured data.

---

**f. Books in the database have a ‘year’ field. Rewrite the command to include only volumes published in the nineteenth century.** [5 marks]

**Answer:**
```plaintext
db.books.find({ lang: "German", year: { $gte: 1800, $lt: 1900 } })
```

**Detailed Explanation:**
- The query uses MongoDB’s comparison operators `$gte` (greater than or equal to) and `$lt` (less than) to filter records based on the year.

**Real-World Scenario Connection:**
Time-based queries are common in historical archives and digital libraries.

**Important Points to Remember:**
- MongoDB’s query operators provide powerful filtering capabilities for date ranges.

**Key Takeaways:**
Understanding how to filter results based on time ranges is crucial for working with historical datasets.

---

**g. Book contents are included in a single textual field called “text”. How would you adjust your query to include only books containing the word “Strudel”?** [2 marks]

**Answer:**
```plaintext
db.books.find({ lang: "German", year: { $gte: 1800, $lt: 1900 }, text: /Strudel/ })
```

**Detailed Explanation:**
- The query uses a regular expression `/Strudel/` to search for books containing the specified word.

**Real-World Scenario Connection:**
Text search is a common feature in digital libraries and search engines, enabling precise content retrieval.

**Important Points to Remember:**
- Regular expressions are powerful tools for text-based search queries in MongoDB.

**Key Takeaways:**
Using regular expressions in queries allows for flexible and powerful text searches in document databases.

---

**h. In order to represent the books’ content and structure more accurately, the researcher is trying to choose between enriching this database or switching to an XML database using TEI to encode book content and catalogue information. What factors should the researcher take into account in their decision?** [10 marks]

**Answer:**
The researcher should consider the following factors:
- **Flexibility vs Structure:** A document database like MongoDB offers flexibility for unstructured data, whereas an XML database with TEI provides a highly structured and hierarchical format, ideal for complex literary metadata.
- **Query Complexity:** MongoDB’s query language is straightforward for text search but limited in hierarchical querying. TEI in an XML database supports complex querying using XPath/XQuery, ideal for detailed text analysis.
- **Interoperability:** TEI is a widely adopted standard in humanities research, enabling easier collaboration and data sharing with other institutions.
- **Scalability:** MongoDB is better suited for large-scale datasets due to its horizontal scalability, whereas XML databases might struggle with performance at scale.
- **Existing Data Structure:** If the researcher’s existing data is already structured for document-based storage, enriching MongoDB may be easier than migrating to an XML format.
- **Long-term Preservation:** TEI’s structured format may be more sustainable for archival purposes and maintaining scholarly integrity.

**Detailed Explanation:**
- The decision involves trade-offs between flexibility, data complexity, and scalability. While MongoDB offers rapid deployment and easy management, TEI in an XML database is better suited for detailed, semantically rich text.

**Real-World Scenario Connection:**
Digital humanities projects often face this decision when choosing between flexible document stores and semantically rich, structured formats.

**Important Points to Remember:**
- Choosing the right database model depends on the complexity of the data, the types of queries needed, and the long-term goals of the project.

**Key Takeaways:**
Understanding the trade-offs between document databases and XML databases is key for designing systems that handle complex textual data in the humanities.

---

This solution sheet incorporates the requested format with detailed explanations, real-world applications, common pitfalls, and important points to remember, ensuring students have a comprehensive guide for their revision.
