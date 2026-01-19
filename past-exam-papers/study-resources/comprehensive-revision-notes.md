# Comprehensive Revision Notes: Data Management

## Exam Preparation Guide

---

### How to Use This Guide

This revision guide covers all topics tested in the Data Management exam, organized by priority based on analysis of past papers (March 2021 - October 2025).

**Priority Legend:**

| Tag | Meaning | Exam Frequency |
|-----|---------|----------------|
| 🔴 **MUST MASTER** | Core topics tested in almost every exam | 90-100% |
| 🟠 **HIGH PRIORITY** | Frequently tested, essential knowledge | 70-80% |
| 🟡 **MEDIUM PRIORITY** | Regularly appears, important to understand | 50-60% |
| 🟢 **KNOW THE BASICS** | Occasional appearances, know fundamentals | 30-40% |

---

# 1. SQL & Relational Databases 🔴 MUST MASTER

> **Exam Frequency: 100%** - Tested in every single exam

## 1.1 Entity-Relationship (E/R) Modeling

### Core Concepts

An E/R diagram represents the logical structure of a database before implementation.

**Key Components:**

| Component | Symbol | Description |
|-----------|--------|-------------|
| **Entity** | Rectangle | A thing we store data about (Person, Book, Order) |
| **Attribute** | Oval | A property of an entity (name, date, price) |
| **Primary Key** | Underlined attribute | Uniquely identifies each entity instance |
| **Relationship** | Diamond | How entities are connected |
| **Cardinality** | 1, M, N notation | How many of each entity participate |

### Cardinality Types

| Type | Meaning | Example |
|------|---------|---------|
| **1:1** | One-to-one | Person ↔ Passport |
| **1:M** | One-to-many | Department → Employees |
| **M:N** | Many-to-many | Students ↔ Courses |

### Resolving M:N with Junction Tables (Associative Entities)

M:N relationships **cannot be directly implemented** in relational databases. You must create a **junction table** (also called associative entity, bridge table, or linking table).

**Why?** A foreign key can only hold ONE value, but M:N requires multiple values on both sides.

**Pattern:**
```
┌───────────┐         ┌─────────────────┐         ┌───────────┐
│  Student  │───M:N───│   Enrollment    │───M:N───│  Course   │
├───────────┤         ├─────────────────┤         ├───────────┤
│student_id │◄───────►│ student_id (FK) │◄───────►│ course_id │
│name       │         │ course_id (FK)  │         │title      │
└───────────┘         │ grade           │         └───────────┘
                      │ enrollment_date │
                      └─────────────────┘
                         Junction Table
                      (can have its own attributes!)
```

**SQL Implementation:**
```sql
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE Course (
    course_id INT PRIMARY KEY,
    title VARCHAR(200)
);

-- Junction table resolves M:N
CREATE TABLE Enrollment (
    student_id INT,
    course_id INT,
    grade DECIMAL(3,2),           -- Junction tables can have attributes!
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id),  -- Composite primary key
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);
```

**Key Points:**
- Junction table has **composite primary key** (both FKs together)
- Can include **relationship attributes** (grade, date, role, etc.)
- Query using JOINs through the junction table

### Worked Example: Library Database

**Scenario:** A library tracks books, members, and loans. Each book has one author (simplified). Members can borrow multiple books. Each loan records the date borrowed and returned.

**Step 1: Identify Entities**
- Book (book_id, title, isbn, year_published)
- Author (author_id, name, birth_year)
- Member (member_id, name, email, join_date)
- Loan (loan_id, date_borrowed, date_returned)

**Step 2: Identify Relationships**
- Author WRITES Book (1:M - one author writes many books)
- Member BORROWS Book (M:N - resolved via Loan entity)

**Step 3: E/R Diagram**

```
┌──────────┐       ┌──────────┐       ┌──────────┐
│  AUTHOR  │──1:M──│   BOOK   │──M:N──│  MEMBER  │
├──────────┤       ├──────────┤       ├──────────┤
│author_id │       │ book_id  │       │member_id │
│name      │       │ title    │       │name      │
│birth_year│       │ isbn     │       │email     │
└──────────┘       │ year     │       │join_date │
                   │author_id │       └──────────┘
                   └──────────┘             │
                        │                   │
                        └───────┬───────────┘
                                │
                          ┌─────┴─────┐
                          │   LOAN    │
                          ├───────────┤
                          │ loan_id   │
                          │ book_id   │
                          │ member_id │
                          │ date_borr │
                          │ date_ret  │
                          └───────────┘
```

### Common Exam Patterns

1. **"Design an E/R model for..."** - Identify entities, attributes, relationships, cardinalities
2. **"What problems might arise?"** - Discuss M:N relationships, NULL handling, optional relationships
3. **"Convert to relational schema"** - Translate E/R to CREATE TABLE statements

### Common Pitfalls

- **Forgetting junction tables for M:N relationships** - Always resolve M:N with an intermediate entity
- **Storing derived data** - Don't store "age" when you have "birth_date"
- **Using meaningful primary keys** - Prefer surrogate keys (auto-increment IDs) over natural keys (ISBN can have errors)

---

## 1.2 Normalization

### Why Normalize?

Normalization eliminates redundancy and prevents anomalies:

| Anomaly | Problem | Example |
|---------|---------|---------|
| **Insert** | Can't add data without unrelated data | Can't add a new department until it has employees |
| **Update** | Must update multiple rows | Changing department name requires updating all employee rows |
| **Delete** | Lose unrelated data | Deleting last employee loses department info |

### Normal Forms

#### First Normal Form (1NF)

**Rule:** All attributes must be atomic (no repeating groups or arrays).

**Violation:**
```
Student(id, name, phone_numbers)
         1, "Alice", "123-456, 789-012"  ← Multiple values in one cell
```

**Fixed (1NF):**
```
Student(id, name)
StudentPhone(student_id, phone_number)
```

#### Second Normal Form (2NF)

**Rule:** Must be in 1NF + no partial dependencies (all non-key attributes depend on the *whole* primary key).

**Violation:** (Composite key: student_id + course_id)
```
Enrollment(student_id, course_id, student_name, grade)
                                  ↑
                     Depends only on student_id, not full key
```

**Fixed (2NF):**
```
Student(student_id, student_name)
Enrollment(student_id, course_id, grade)
```

#### Third Normal Form (3NF)

**Rule:** Must be in 2NF + no transitive dependencies (non-key attributes shouldn't depend on other non-key attributes).

**Violation:**
```
Employee(emp_id, emp_name, dept_id, dept_name, dept_location)
                                    ↑          ↑
                          These depend on dept_id, not emp_id
```

**Fixed (3NF):**
```
Employee(emp_id, emp_name, dept_id)
Department(dept_id, dept_name, dept_location)
```

### Quick Normalization Test

| Check | Question | If Yes → |
|-------|----------|----------|
| 1NF | Are there any multi-valued attributes? | Split into separate table |
| 2NF | Does any non-key attribute depend on only PART of a composite key? | Move to separate table |
| 3NF | Does any non-key attribute depend on ANOTHER non-key attribute? | Move to separate table |

### Worked Example: Conference Registration

**Unnormalized:**
```
Registration(
  reg_id,
  attendee_name,
  attendee_email,
  conference_name,
  conference_date,
  conference_venue,
  workshops_attended,      ← Multi-valued (violates 1NF)
  ticket_price
)
```

**To 1NF:** Remove multi-valued attribute
```
Registration(reg_id, attendee_name, attendee_email,
             conference_name, conference_date, conference_venue, ticket_price)
WorkshopAttendance(reg_id, workshop_name)
```

**To 2NF:** (Already OK - single-column primary key)

**To 3NF:** Remove transitive dependencies
```
Attendee(attendee_id, name, email)
Conference(conference_id, name, date, venue)
Registration(reg_id, attendee_id, conference_id, ticket_price)
WorkshopAttendance(reg_id, workshop_name)
```

---

## 1.3 SQL: CREATE TABLE

### Syntax Template

```sql
CREATE TABLE table_name (
    column_name data_type [constraints],
    column_name data_type [constraints],
    ...
    [table_constraints]
);
```

### Common Data Types

| Type | Use For | Example |
|------|---------|---------|
| `INT` / `INTEGER` | Whole numbers | `age INT` |
| `VARCHAR(n)` | Variable-length text | `name VARCHAR(100)` |
| `TEXT` | Long text | `description TEXT` |
| `DATE` | Dates | `birth_date DATE` |
| `DATETIME` / `TIMESTAMP` | Date and time | `created_at TIMESTAMP` |
| `DECIMAL(p,s)` | Precise numbers | `price DECIMAL(10,2)` |
| `BOOLEAN` | True/false | `is_active BOOLEAN` |

### Constraints

| Constraint | Purpose | Example |
|------------|---------|---------|
| `PRIMARY KEY` | Unique identifier | `id INT PRIMARY KEY` |
| `NOT NULL` | Must have value | `name VARCHAR(50) NOT NULL` |
| `UNIQUE` | No duplicates | `email VARCHAR(100) UNIQUE` |
| `FOREIGN KEY` | References another table | `FOREIGN KEY (dept_id) REFERENCES Department(id)` |
| `CHECK` | Value validation | `CHECK (age >= 0)` |
| `DEFAULT` | Default value | `status VARCHAR(20) DEFAULT 'pending'` |

### Worked Example: Conference Database

```sql
-- Conference table
CREATE TABLE Conference (
    conference_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    venue VARCHAR(200),
    CHECK (end_date >= start_date)
);

-- Person table (can be author, reviewer, or attendee)
CREATE TABLE Person (
    person_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    affiliation VARCHAR(200)
);

-- Paper table
CREATE TABLE Paper (
    paper_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(300) NOT NULL,
    abstract TEXT,
    status ENUM('submitted', 'under_review', 'accepted', 'rejected')
           DEFAULT 'submitted',
    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Paper-Author relationship (M:N)
CREATE TABLE PaperAuthor (
    paper_id INT,
    person_id INT,
    author_order INT NOT NULL,
    is_corresponding BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (paper_id, person_id),
    FOREIGN KEY (paper_id) REFERENCES Paper(paper_id),
    FOREIGN KEY (person_id) REFERENCES Person(person_id)
);

-- Review table
CREATE TABLE Review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    paper_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    score INT CHECK (score BETWEEN 1 AND 10),
    feedback TEXT,
    recommendation ENUM('accept', 'weak_accept', 'weak_reject', 'reject'),
    FOREIGN KEY (paper_id) REFERENCES Paper(paper_id),
    FOREIGN KEY (reviewer_id) REFERENCES Person(person_id)
);
```

---

## 1.4 SQL Queries

### SELECT Basics

```sql
-- Basic structure
SELECT columns
FROM table
WHERE conditions
GROUP BY columns
HAVING group_conditions
ORDER BY columns;

-- Use DISTINCT to eliminate duplicates (frequently forgotten!)
SELECT DISTINCT column FROM table;
```

### JOINs

| JOIN Type | Returns | Use When |
|-----------|---------|----------|
| `INNER JOIN` | Only matching rows from both tables | You need data that exists in both |
| `LEFT JOIN` | All left rows + matching right rows | You want all from left, even without matches |
| `RIGHT JOIN` | All right rows + matching left rows | You want all from right, even without matches |
| `FULL OUTER JOIN` | All rows from both tables | You want everything (NULLs for non-matches) |

### JOIN Visualization

```
Table A         Table B
┌───┬───┐      ┌───┬───┐
│ 1 │ a │      │ 1 │ x │
│ 2 │ b │      │ 3 │ y │
│ 3 │ c │      │ 4 │ z │
└───┴───┘      └───┴───┘

INNER JOIN: (1,a,x), (3,c,y)
LEFT JOIN:  (1,a,x), (2,b,NULL), (3,c,y)
RIGHT JOIN: (1,a,x), (3,c,y), (4,NULL,z)
```

### Aggregation Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `COUNT(*)` | Count rows | `SELECT COUNT(*) FROM Orders` |
| `COUNT(column)` | Count non-NULL values | `SELECT COUNT(email) FROM Users` |
| `SUM(column)` | Sum values | `SELECT SUM(amount) FROM Orders` |
| `AVG(column)` | Average | `SELECT AVG(score) FROM Reviews` |
| `MAX(column)` | Maximum | `SELECT MAX(price) FROM Products` |
| `MIN(column)` | Minimum | `SELECT MIN(date) FROM Events` |

### GROUP BY and HAVING

```sql
-- Count papers per status
SELECT status, COUNT(*) as paper_count
FROM Paper
GROUP BY status;

-- Only show statuses with more than 5 papers
SELECT status, COUNT(*) as paper_count
FROM Paper
GROUP BY status
HAVING COUNT(*) > 5;
```

### Worked Examples

**Example 1: Find all papers with their authors**
```sql
SELECT p.title, pe.name AS author_name, pa.author_order
FROM Paper p
JOIN PaperAuthor pa ON p.paper_id = pa.paper_id
JOIN Person pe ON pa.person_id = pe.person_id
ORDER BY p.title, pa.author_order;
```

**Example 2: Average review score per paper**
```sql
SELECT p.title,
       AVG(r.score) AS avg_score,
       COUNT(r.review_id) AS num_reviews
FROM Paper p
LEFT JOIN Review r ON p.paper_id = r.paper_id
GROUP BY p.paper_id, p.title
ORDER BY avg_score DESC;
```

**Example 3: Find papers with no reviews**
```sql
SELECT p.title
FROM Paper p
LEFT JOIN Review r ON p.paper_id = r.paper_id
WHERE r.review_id IS NULL;
```

**Example 4: Papers with average score above 7 and at least 3 reviews**
```sql
SELECT p.title, AVG(r.score) AS avg_score, COUNT(*) AS review_count
FROM Paper p
JOIN Review r ON p.paper_id = r.paper_id
GROUP BY p.paper_id, p.title
HAVING AVG(r.score) > 7 AND COUNT(*) >= 3;
```

**Example 5: Subquery - Find reviewers who reviewed more than average**
```sql
SELECT name, review_count
FROM (
    SELECT pe.name, COUNT(*) AS review_count
    FROM Person pe
    JOIN Review r ON pe.person_id = r.reviewer_id
    GROUP BY pe.person_id, pe.name
) AS reviewer_counts
WHERE review_count > (SELECT AVG(cnt) FROM (
    SELECT COUNT(*) AS cnt FROM Review GROUP BY reviewer_id
) AS avg_calc);
```

---

### Advanced Query Patterns

The following patterns appear frequently in exams and build on the basics above.

### Common Table Expressions (CTEs) - WITH Clause

CTEs create temporary named result sets that make complex queries readable.

```sql
-- Basic CTE syntax
WITH cte_name AS (
    SELECT ...
)
SELECT * FROM cte_name;

-- Multiple CTEs
WITH
    first_cte AS (SELECT ...),
    second_cte AS (SELECT ...)
SELECT * FROM first_cte JOIN second_cte ON ...;
```

**Example: Compare yearly totals from two sources**
```sql
WITH parish_totals AS (
    SELECT year, SUM(count_n) AS total
    FROM parish_counts
    GROUP BY year
),
city_totals AS (
    SELECT year, SUM(count_n) AS total
    FROM city_counts
    GROUP BY year
)
SELECT
    p.year,
    p.total AS parish_total,
    c.total AS city_total,
    (p.total - c.total) AS difference
FROM parish_totals p
LEFT JOIN city_totals c ON p.year = c.year;
```

### Finding Records NOT in a Set

Three equivalent patterns for finding items that DON'T match:

**Method 1: NOT IN**
```sql
-- Find pieces NOT associated with a specific composer
SELECT * FROM Piece
WHERE ConcNo NOT IN (
    SELECT ConcNo FROM Concordance
    WHERE ComposerId = (SELECT ComposerId FROM Composer WHERE Name = 'John Dowland')
);
```

**Method 2: NOT EXISTS**
```sql
-- Same query using NOT EXISTS
SELECT * FROM Piece p
WHERE NOT EXISTS (
    SELECT 1 FROM Concordance c
    JOIN Composer comp ON c.ComposerId = comp.ComposerId
    WHERE c.ConcNo = p.ConcNo AND comp.Name = 'John Dowland'
);
```

**Method 3: LEFT JOIN + IS NULL**
```sql
-- Same query using LEFT JOIN
SELECT p.*
FROM Piece p
LEFT JOIN Concordance c ON p.ConcNo = c.ConcNo
LEFT JOIN Composer comp ON c.ComposerId = comp.ComposerId
                        AND comp.Name = 'John Dowland'
WHERE comp.ComposerId IS NULL;
```

| Method | Best For | Caveat |
|--------|----------|--------|
| `NOT IN` | Simple cases | Fails with NULLs in subquery |
| `NOT EXISTS` | Complex conditions | Most reliable |
| `LEFT JOIN + IS NULL` | When you need other columns | Verbose but clear |

### DISTINCT Keyword

`DISTINCT` eliminates duplicate rows - **frequently forgotten in exams!**

```sql
-- Without DISTINCT: may return same species multiple times
SELECT SpeciesName FROM Sightings WHERE Date > '2021-01-01';

-- With DISTINCT: each species appears once
SELECT DISTINCT SpeciesName FROM Sightings WHERE Date > '2021-01-01';

-- COUNT with DISTINCT
SELECT COUNT(DISTINCT SpeciesName) AS unique_species FROM Sightings;
```

### Star Schema / Dimensional Modeling 🟢 KNOW THE BASICS

*This schema design pattern affects how you write SQL queries, particularly for aggregation and reporting.*

Used for analytical databases (data warehouses). Separates:
- **Fact tables**: Measurements/events (sales, counts, transactions)
- **Dimension tables**: Descriptive attributes (who, what, when, where)

```
        ┌──────────┐
        │   Date   │ (Dimension)
        └────┬─────┘
             │
┌──────────┐ │ ┌──────────┐
│ Product  │─┼─│  Sales   │ (Fact)
└──────────┘ │ └──────────┘
             │
        ┌────┴─────┐
        │  Store   │ (Dimension)
        └──────────┘
```

**Example: Mortality data schema**
```sql
-- Dimension tables (slowly changing)
CREATE TABLE week (week_id CHAR(7) PRIMARY KEY, year INT, week_no INT);
CREATE TABLE parish (parcode CHAR(4) PRIMARY KEY, parish_name VARCHAR(100));

-- Fact table (transactional)
CREATE TABLE weekly_count (
    week_id CHAR(7),
    parcode CHAR(4),
    count_type VARCHAR(20),
    count_n INT,
    PRIMARY KEY (week_id, parcode, count_type),
    FOREIGN KEY (week_id) REFERENCES week(week_id),
    FOREIGN KEY (parcode) REFERENCES parish(parcode)
);
```

---

## 1.5 SQL Transactions 🟢 KNOW THE BASICS

### ACID Properties

| Property | Meaning | Example |
|----------|---------|---------|
| **Atomicity** | All or nothing | Bank transfer: both debit and credit succeed, or neither |
| **Consistency** | Valid state to valid state | Can't have negative balance if CHECK constraint exists |
| **Isolation** | Concurrent transactions don't interfere | Two users buying last ticket: only one succeeds |
| **Durability** | Committed changes persist | After commit, data survives power failure |

### Transaction Syntax

```sql
START TRANSACTION;

UPDATE Account SET balance = balance - 100 WHERE account_id = 1;
UPDATE Account SET balance = balance + 100 WHERE account_id = 2;

-- If everything OK:
COMMIT;

-- If something wrong:
ROLLBACK;
```

### When Transactions Matter

- **Banking**: Transfer money between accounts
- **E-commerce**: Reserve inventory + create order
- **Registration**: Create user + assign role + send email trigger

---

## 1.6 SQL Permissions (GRANT) 🟢 KNOW THE BASICS

### Basic Syntax

```sql
-- Grant specific privileges
GRANT SELECT, INSERT ON table_name TO user_name;

-- Grant all privileges
GRANT ALL PRIVILEGES ON database_name.* TO user_name;

-- Revoke privileges
REVOKE DELETE ON table_name FROM user_name;
```

### Common Privileges

| Privilege | Allows |
|-----------|--------|
| `SELECT` | Read data |
| `INSERT` | Add new rows |
| `UPDATE` | Modify existing rows |
| `DELETE` | Remove rows |
| `CREATE` | Create tables/databases |
| `DROP` | Delete tables/databases |
| `ALL PRIVILEGES` | Everything |

### Principle of Least Privilege

Give users only the minimum permissions needed for their role.

### Worked Example: Double-Blind Review System

From October 2025 exam - implementing anonymity in peer review:

```sql
-- Create roles
CREATE ROLE reviewer_role;
CREATE ROLE author_role;
CREATE ROLE pc_chair_role;

-- View for reviewers: papers without author info
CREATE VIEW ReviewerPaperView AS
SELECT paper_id, title, abstract, pdf_path, status
FROM Paper;

-- View for authors: reviews without reviewer info
CREATE VIEW AuthorReviewView AS
SELECT paper_id, score, feedback, recommendation
FROM Review;

-- Grant permissions
GRANT SELECT ON ReviewerPaperView TO reviewer_role;
GRANT SELECT, INSERT, UPDATE ON Review TO reviewer_role;

GRANT SELECT ON Paper TO author_role;
GRANT SELECT ON AuthorReviewView TO author_role;

-- PC Chair sees everything
GRANT ALL ON Paper, Review, PaperAuthor, Person TO pc_chair_role;
```

**Key Insight:** Use VIEWS to implement column-level security. Grant access to views, not base tables.

---

# 2. Data Model Comparison 🔴 MUST MASTER

> **Exam Frequency: 90%** - Almost always includes a "which database type" question

## 2.1 File-Based vs Database Systems

A common exam question asks about advantages/disadvantages of databases over file-based systems.

| Aspect | File-Based (CSV, JSON files) | Database System |
|--------|------------------------------|-----------------|
| **Data Independence** | Low - apps tied to file format | High - apps use queries |
| **Redundancy Control** | Manual - must enforce consistency | Automatic via normalization |
| **Integrity Constraints** | None - any data allowed | Enforced (FK, CHECK, NOT NULL) |
| **Concurrent Access** | Problematic - file locks | Managed via transactions |
| **Query Language** | None (custom scripts) | SQL, SPARQL, etc. |
| **Backup/Recovery** | Manual | Built-in |
| **Version Control** | Easy (Git works well) | Harder to track changes |

**When Files Are Appropriate:**
- Small datasets
- Simple read-only access
- Version control needed (Git)
- Human-editable data

**When Database Is Better:**
- Multiple users/applications
- Complex queries needed
- Data integrity critical
- Large datasets

---

## 2.2 Database Types Overview

| Type | Structure | Query Language | Best For |
|------|-----------|----------------|----------|
| **Relational** | Tables with rows/columns | SQL | Structured data, complex queries, ACID |
| **Document** | JSON/BSON documents | MongoDB queries | Flexible schema, hierarchical data |
| **Graph** | Nodes and edges | SPARQL, Cypher | Highly connected data, relationships |
| **Key-Value** | Simple key→value pairs | GET/PUT | Caching, session storage |
| **XML** | Hierarchical markup | XPath, XQuery | Document-centric, markup preservation |

## 2.3 Decision Framework

### When to Use Relational (SQL)

✅ **Use when:**
- Data has clear structure with relationships
- Need complex queries with JOINs
- ACID transactions are critical
- Data integrity is paramount
- Reporting and analytics

❌ **Avoid when:**
- Schema changes frequently
- Handling deeply nested/hierarchical data
- Need horizontal scaling for massive writes

### When to Use Document (MongoDB)

✅ **Use when:**
- Schema varies between records
- Data is naturally hierarchical (nested objects)
- Rapid development with evolving requirements
- Each document is self-contained

❌ **Avoid when:**
- Need complex joins across collections
- Strong consistency is required
- Data has many relationships

### When to Use Graph (RDF/Neo4j)

✅ **Use when:**
- Relationships ARE the data (social networks, recommendations)
- Need to traverse connections (friends-of-friends)
- Data is highly interconnected
- Relationship types vary

❌ **Avoid when:**
- Simple tabular data
- Need aggregation queries
- Data isn't relationship-focused

## 2.4 Comparison Table

| Factor | Relational | Document | Graph |
|--------|------------|----------|-------|
| **Schema** | Fixed, predefined | Flexible | Flexible |
| **Relationships** | Foreign keys + JOINs | Embedded or references | Native edges |
| **Query complexity** | SQL - very powerful | Good for document retrieval | Great for traversals |
| **Scalability** | Vertical (mostly) | Horizontal | Varies |
| **Transactions** | Strong ACID | Varies (often eventual) | Varies |
| **Best query type** | Analytical, aggregation | Document retrieval | Path finding |

## 2.5 Worked Example: Choosing a Database

**Scenario:** A university needs a system to track:
- Students and their enrollments
- Courses and prerequisites
- Grades and transcripts

**Analysis:**

| Requirement | Best Fit | Reasoning |
|-------------|----------|-----------|
| Student-Course enrollments | Relational | Classic M:N relationship |
| Prerequisites (course→course) | Graph OR Relational | Graph good for "all prerequisites of prerequisites" |
| Grade calculations | Relational | Aggregation queries (AVG, SUM) |
| Transcript reports | Relational | Structured reporting |

**Recommendation:** **Relational database** - The data is highly structured with clear relationships, needs aggregation for GPA calculations, and requires consistency for official records.

**When Graph might help:** If you frequently need queries like "find all prerequisite chains" or "what courses can I take given my completed courses" - these traverse relationships recursively.

## 2.6 Common Exam Question Patterns

1. **"What database would you recommend for X? Justify."**
   - State your choice
   - Give 2-3 reasons based on the data characteristics
   - Mention what you'd lose with alternatives

2. **"Convert this relational schema to document/graph"**
   - Show the transformation
   - Discuss trade-offs (denormalization, redundancy)

3. **"Compare relational and document for this scenario"**
   - Create a comparison table
   - Discuss query patterns
   - Consider future requirements

---

# 3. XML Technologies 🟠 HIGH PRIORITY

> **Exam Frequency: 80%** - XPath especially common

## 3.1 XML Fundamentals

### Well-Formed vs Valid

| Property | Well-Formed | Valid |
|----------|-------------|-------|
| Definition | Follows XML syntax rules | Well-formed + conforms to schema |
| Requirements | Proper nesting, closing tags, one root | DTD/XSD/RelaxNG compliance |
| Check with | Any XML parser | Validating parser + schema |

### Well-Formed Rules

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- 1. Single root element -->
<library>
    <!-- 2. All tags properly closed -->
    <book id="1">
        <!-- 3. Proper nesting (not <a><b></a></b>) -->
        <title>Data Management</title>
        <!-- 4. Attribute values in quotes -->
        <author name="Smith"/>
        <!-- 5. Case sensitive (<Book> ≠ </book>) -->
    </book>
</library>
```

### Common Well-Formedness Errors

| Error | Example | Fix |
|-------|---------|-----|
| Unclosed tag | `<p>text` | `<p>text</p>` |
| Wrong nesting | `<a><b></a></b>` | `<a><b></b></a>` |
| Unquoted attribute | `<book id=1>` | `<book id="1">` |
| Multiple roots | `<a/><b/>` | `<root><a/><b/></root>` |
| Case mismatch | `<Book></book>` | `<book></book>` |

---

## 3.2 XPath Navigation

### Axes and Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `/` | Root or child step | `/library/book` |
| `//` | Descendant (any depth) | `//title` |
| `.` | Current node | `.//author` |
| `..` | Parent node | `../title` |
| `@` | Attribute | `@id`, `@name` |
| `*` | Any element | `/library/*` |
| `@*` | Any attribute | `//@*` |

### Predicates (Filters)

| Predicate | Meaning | Example |
|-----------|---------|---------|
| `[n]` | Position (1-indexed) | `//book[1]` - first book |
| `[last()]` | Last element | `//book[last()]` |
| `[@attr]` | Has attribute | `//book[@id]` |
| `[@attr='val']` | Attribute equals | `//book[@id='1']` |
| `[element]` | Has child element | `//book[author]` |
| `[element='val']` | Child element equals | `//book[title='XML']` |

### Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `text()` | Get text content | `//title/text()` |
| `contains()` | String contains | `//title[contains(., 'Data')]` |
| `starts-with()` | String starts with | `//name[starts-with(., 'Dr')]` |
| `count()` | Count nodes | `count(//book)` |
| `sum()` | Sum numeric values | `sum(//price)` |
| `not()` | Negation | `//book[not(@id)]` |
| `position()` | Current position | `//book[position() <= 3]` |

### Worked Examples

**Sample XML:**
```xml
<?xml version="1.0"?>
<library>
    <book id="1" genre="fiction">
        <title>Pride and Prejudice</title>
        <author>Jane Austen</author>
        <year>1813</year>
        <price>12.99</price>
    </book>
    <book id="2" genre="science">
        <title>A Brief History of Time</title>
        <author>Stephen Hawking</author>
        <year>1988</year>
        <price>15.99</price>
    </book>
    <book id="3" genre="fiction">
        <title>1984</title>
        <author>George Orwell</author>
        <year>1949</year>
        <price>10.99</price>
    </book>
</library>
```

| Query | XPath | Result |
|-------|-------|--------|
| All book titles | `//title/text()` | Pride and Prejudice, A Brief History of Time, 1984 |
| First book's author | `//book[1]/author/text()` | Jane Austen |
| Books from 1900s | `//book[year >= 1900]/title/text()` | A Brief History of Time, 1984 |
| Fiction books | `//book[@genre='fiction']/title/text()` | Pride and Prejudice, 1984 |
| Books with price > 12 | `//book[price > 12]/title/text()` | Pride and Prejudice, A Brief History of Time |
| Count of books | `count(//book)` | 3 |
| ID of last book | `//book[last()]/@id` | 3 |
| Books by authors starting with 'J' | `//book[starts-with(author, 'J')]/title/text()` | Pride and Prejudice |

### MARC XML Example (from Oct 2025)

```xml
<record>
    <datafield tag="100" ind1="1" ind2=" ">
        <subfield code="a">Lindgren, Astrid,</subfield>
        <subfield code="d">1907-2002.</subfield>
    </datafield>
    <datafield tag="041" ind1="1" ind2=" ">
        <subfield code="a">engswe</subfield>
    </datafield>
    <datafield tag="245" ind1="1" ind2="0">
        <subfield code="a">Pippi Longstocking</subfield>
    </datafield>
</record>
```

| Query | XPath |
|-------|-------|
| Is it a translation? | `//datafield[@tag='041']/@ind1` (returns "1" = yes) |
| Get author name | `//datafield[@tag='100']/subfield[@code='a']/text()` |
| Get title | `//datafield[@tag='245']/subfield[@code='a']/text()` |
| All datafield tags | `//datafield/@tag` |

### XML Namespaces in XPath

When XML uses namespaces (common with TEI, MEI, XSLT), XPath queries must account for them.

**Example with TEI namespace:**
```xml
<competition xmlns:tei="http://www.tei-c.org/ns/1.0">
  <entry>
    <poem>
      <tei:lg type="stanza">
        <tei:l>There was an old man of Dumbree</tei:l>
        <tei:l>Who taught little owls to drink tea</tei:l>
      </tei:lg>
    </poem>
  </entry>
</competition>
```

**Querying namespaced elements:**

| Wrong | Correct | Why |
|-------|---------|-----|
| `//lg` | `//tei:lg` | Must use namespace prefix |
| `//l/text()` | `//tei:l/text()` | `l` is in TEI namespace |

**XPath with namespace prefixes:**
```xpath
//tei:lg[@type='stanza']/tei:l/text()
```

**Common namespaces in exams:**
| Prefix | Namespace | Domain |
|--------|-----------|--------|
| `tei:` | TEI | Text encoding |
| `mei:` | MEI | Music encoding |
| `xsl:` | XSLT | Transformations |
| `xs:` | XSD | Schema |

**Key Point:** The prefix in your XPath must match the prefix declared in the XML document (or be registered in your XPath processor).

---

## 3.3 XML Validation 🟢 KNOW THE BASICS

### DTD (Document Type Definition)

**Pros:** Simple syntax, widely supported
**Cons:** No data types, limited expressiveness

```dtd
<!DOCTYPE library [
    <!ELEMENT library (book+)>
    <!ELEMENT book (title, author, year, price?)>
    <!ELEMENT title (#PCDATA)>
    <!ELEMENT author (#PCDATA)>
    <!ELEMENT year (#PCDATA)>
    <!ELEMENT price (#PCDATA)>
    <!ATTLIST book id ID #REQUIRED>
    <!ATTLIST book genre CDATA #IMPLIED>
]>
```

**DTD Symbols:**

| Symbol | Meaning |
|--------|---------|
| `+` | One or more |
| `*` | Zero or more |
| `?` | Zero or one (optional) |
| `\|` | Choice (or) |
| `,` | Sequence |
| `#PCDATA` | Parsed character data (text) |
| `#REQUIRED` | Attribute required |
| `#IMPLIED` | Attribute optional |

### XSD (XML Schema Definition)

**Pros:** Data types, namespaces, more expressive
**Cons:** More complex, verbose

```xml
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="library">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="book" maxOccurs="unbounded">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="title" type="xs:string"/>
                            <xs:element name="author" type="xs:string"/>
                            <xs:element name="year" type="xs:gYear"/>
                            <xs:element name="price" type="xs:decimal" minOccurs="0"/>
                        </xs:sequence>
                        <xs:attribute name="id" type="xs:ID" use="required"/>
                        <xs:attribute name="genre" type="xs:string"/>
                    </xs:complexType>
                </xs:element>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
```

### RelaxNG

**Pros:** Simpler than XSD, supports data types
**Cons:** Less tool support

```xml
<element name="library" xmlns="http://relaxng.org/ns/structure/1.0">
    <oneOrMore>
        <element name="book">
            <attribute name="id"/>
            <optional><attribute name="genre"/></optional>
            <element name="title"><text/></element>
            <element name="author"><text/></element>
            <element name="year"><text/></element>
            <optional><element name="price"><text/></element></optional>
        </element>
    </oneOrMore>
</element>
```

### Comparison

| Feature | DTD | XSD | RelaxNG |
|---------|-----|-----|---------|
| Data types | No | Yes | Yes (with library) |
| Namespace support | Limited | Yes | Yes |
| Complexity | Low | High | Medium |
| XML syntax | No | Yes | Yes |
| Industry adoption | Legacy | High | Moderate |

---

## 3.4 TEI (Text Encoding Initiative) 🟢 KNOW THE BASICS

TEI is a standard for encoding literary and linguistic texts.

### Common TEI Elements

```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title>Poem Collection</title>
            </titleStmt>
        </fileDesc>
    </teiHeader>
    <text>
        <body>
            <lg type="sonnet">           <!-- Line group (stanza) -->
                <l n="1">Shall I compare thee to a summer's day?</l>
                <l n="2">Thou art more lovely and more temperate:</l>
            </lg>
        </body>
    </text>
</TEI>
```

| Element | Purpose |
|---------|---------|
| `<TEI>` | Root element |
| `<teiHeader>` | Metadata about the document |
| `<text>` | The actual text content |
| `<body>` | Main content |
| `<lg>` | Line group (stanza, verse paragraph) |
| `<l>` | Single line of verse |
| `<p>` | Paragraph (prose) |
| `<pb/>` | Page break |
| `<note>` | Editorial note |

### XPath for TEI

```xpath
-- Count stanzas
count(//lg)

-- Get all lines from first stanza
//lg[1]/l/text()

-- Find lines with specific word
//l[contains(., 'summer')]
```

---

## 3.5 XSLT Basics 🟢 KNOW THE BASICS

XSLT transforms XML into other formats (HTML, text, different XML).

### Basic Structure

```xml
<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
            <body>
                <xsl:apply-templates select="//book"/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="book">
        <div>
            <h2><xsl:value-of select="title"/></h2>
            <p>By: <xsl:value-of select="author"/></p>
        </div>
    </xsl:template>

</xsl:stylesheet>
```

### Key XSLT Elements

| Element | Purpose |
|---------|---------|
| `<xsl:template match="...">` | Define transformation for matching nodes |
| `<xsl:apply-templates>` | Process child nodes |
| `<xsl:value-of select="...">` | Output value |
| `<xsl:for-each select="...">` | Loop over nodes |
| `<xsl:if test="...">` | Conditional |
| `<xsl:choose>/<xsl:when>/<xsl:otherwise>` | Switch/case |

---

# 4. RDF & Linked Data 🟠 HIGH PRIORITY

> **Exam Frequency: 80%** - Triple counting and SPARQL are very common

## 4.1 RDF Fundamentals

### The Triple Model

Everything in RDF is expressed as **subject-predicate-object** triples:

```
Subject    Predicate       Object
───────    ─────────       ──────
:book1     :hasTitle       "Pride and Prejudice"
:book1     :hasAuthor      :austen
:austen    :name           "Jane Austen"
:austen    rdf:type        :Person
```

### URIs and Literals

| Type | Example | Use For |
|------|---------|---------|
| **URI** | `<http://example.org/book1>` | Identifying resources |
| **Prefixed URI** | `:book1` or `ex:book1` | Shorthand for URIs |
| **Literal** | `"Jane Austen"` | String values |
| **Typed Literal** | `"1813"^^xsd:integer` | Values with data types |
| **Language Literal** | `"Bonjour"@fr` | Strings with language |

---

## 4.2 Turtle Syntax

### Basic Syntax

```turtle
@prefix : <http://example.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:book1 rdf:type :Book ;           # Same subject, different predicates
       :title "Pride and Prejudice" ;
       :author :austen ;
       :year "1813"^^xsd:integer .

:austen rdf:type :Person ;
        :name "Jane Austen" ;
        :birthYear "1775"^^xsd:integer .
```

### Turtle Shortcuts

| Shortcut | Meaning | Example |
|----------|---------|---------|
| `;` | Same subject, new predicate | `:book1 :title "X" ; :author :y .` |
| `,` | Same subject AND predicate, new object | `:book1 :tag "fiction", "classic" .` |
| `a` | Short for `rdf:type` | `:book1 a :Book .` |
| `[]` | Blank node | `:book1 :publisher [ :name "Penguin" ] .` |

### Triple Counting (VERY COMMON IN EXAMS)

**Rules:**
1. Each complete subject-predicate-object = 1 triple
2. `;` starts new triple (same subject)
3. `,` starts new triple (same subject AND predicate)
4. Count `a` as a triple too

**Example:**
```turtle
:book1 a :Book ;                    # Triple 1
       :title "1984" ;              # Triple 2
       :author :orwell ;            # Triple 3
       :genre "dystopia", "fiction" . # Triples 4, 5

:orwell a :Person ;                 # Triple 6
        :name "George Orwell" .     # Triple 7
```

**Total: 7 triples**

### Worked Example: Count the Triples

```turtle
@prefix : <http://example.org/> .

:concert1 a :Concert ;
          :performer :beatles, :stones ;
          :venue :wembley ;
          :date "1965-08-15" .

:beatles a :Band ;
         :member :lennon, :mccartney, :harrison, :starr .
```

**Counting:**
1. `:concert1 a :Concert` → 1
2. `:concert1 :performer :beatles` → 1
3. `:concert1 :performer :stones` → 1 (comma = new triple)
4. `:concert1 :venue :wembley` → 1
5. `:concert1 :date "1965-08-15"` → 1
6. `:beatles a :Band` → 1
7. `:beatles :member :lennon` → 1
8. `:beatles :member :mccartney` → 1
9. `:beatles :member :harrison` → 1
10. `:beatles :member :starr` → 1

**Total: 10 triples**

---

## 4.3 SPARQL Queries

### Basic Query Structure

```sparql
PREFIX : <http://example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?variable1 ?variable2
WHERE {
    ?subject ?predicate ?object .
    # More patterns...
}
ORDER BY ?variable1
LIMIT 10
```

### Query Types

| Type | Purpose | Example |
|------|---------|---------|
| `SELECT` | Return variable bindings | `SELECT ?name WHERE {...}` |
| `CONSTRUCT` | Create new triples | `CONSTRUCT { ?s :label ?name } WHERE {...}` |
| `ASK` | Return true/false | `ASK { :book1 :author :austen }` |
| `DESCRIBE` | Return description of resource | `DESCRIBE :book1` |

### Pattern Matching

```sparql
# Find all books and their authors
SELECT ?book ?authorName
WHERE {
    ?book a :Book .
    ?book :author ?author .
    ?author :name ?authorName .
}
```

### FILTER Clauses

```sparql
# Books published after 1900
SELECT ?title ?year
WHERE {
    ?book :title ?title ;
          :year ?year .
    FILTER (?year > 1900)
}

# Authors whose name contains "Jane"
SELECT ?name
WHERE {
    ?person a :Person ;
            :name ?name .
    FILTER (CONTAINS(?name, "Jane"))
}
```

### OPTIONAL

```sparql
# All books, with author if available
SELECT ?title ?authorName
WHERE {
    ?book :title ?title .
    OPTIONAL {
        ?book :author ?author .
        ?author :name ?authorName .
    }
}
```

### Aggregation

```sparql
# Count books per author
SELECT ?authorName (COUNT(?book) AS ?bookCount)
WHERE {
    ?book :author ?author .
    ?author :name ?authorName .
}
GROUP BY ?authorName
HAVING (COUNT(?book) > 2)
ORDER BY DESC(?bookCount)
```

### Property Paths

| Path | Meaning | Example |
|------|---------|---------|
| `/` | Sequence | `:author/:name` |
| `\|` | Alternative | `:author\|:editor` |
| `*` | Zero or more | `:knows*` |
| `+` | One or more | `:parent+` |
| `?` | Zero or one | `:spouse?` |
| `^` | Inverse | `^:author` (things that author this) |

```sparql
# Find all ancestors (parent, grandparent, etc.)
SELECT ?ancestor
WHERE {
    :person1 :parent+ ?ancestor .
}

# Find colleagues (people who know someone I know)
SELECT ?colleague
WHERE {
    :me :knows/:knows ?colleague .
    FILTER (?colleague != :me)
}
```

### Wikidata SPARQL 🟢 KNOW THE BASICS

Wikidata uses property codes (P-numbers):

| Property | Meaning |
|----------|---------|
| `wdt:P31` | instance of |
| `wdt:P279` | subclass of |
| `wdt:P17` | country |
| `wdt:P131` | located in administrative entity |
| `wdt:P569` | date of birth |
| `wdt:P570` | date of death |

```sparql
# Belgian artists born after 1900
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?artist ?artistLabel ?birthDate
WHERE {
    ?artist wdt:P31 wd:Q5 .           # instance of human
    ?artist wdt:P27 wd:Q31 .          # country of citizenship: Belgium
    ?artist wdt:P106 wd:Q483501 .     # occupation: artist
    ?artist wdt:P569 ?birthDate .
    FILTER (YEAR(?birthDate) > 1900)
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}
```

### SERVICE (Federated Queries)

```sparql
# Query external endpoint
SELECT ?item ?itemLabel
WHERE {
    SERVICE <https://query.wikidata.org/sparql> {
        ?item wdt:P31 wd:Q5 .
    }
}
```

---

## 4.4 Linked Data Principles 🟡 MEDIUM PRIORITY

### Tim Berners-Lee's 4 Principles

1. **Use URIs as names for things**
   - Not just documents, but people, places, concepts

2. **Use HTTP URIs so people can look them up**
   - Dereferenceable - you can GET information about them

3. **When someone looks up a URI, provide useful information using standards (RDF, SPARQL)**
   - Return structured data, not just HTML

4. **Include links to other URIs to discover more things**
   - Connect your data to the web of data

### 5-Star Open Data

| Stars | Requirements |
|-------|--------------|
| ★ | Available on web (any format) with open license |
| ★★ | Machine-readable structured data (e.g., Excel) |
| ★★★ | Non-proprietary format (e.g., CSV) |
| ★★★★ | Use URIs to identify things |
| ★★★★★ | Link to other data sources |

### BIBFRAME (from Oct 2025)

BIBFRAME is the Library of Congress's Linked Data standard to replace MARC:

| BIBFRAME | Purpose |
|----------|---------|
| `bf:Work` | Conceptual essence (the story) |
| `bf:Instance` | Publication (specific edition) |
| `bf:Item` | Single copy |

**Benefits:**
- Web integration via URIs
- Deduplication through shared authority URIs (VIAF, Wikidata)
- Richer relationship expression

**Risks:**
- Massive migration cost (billions of MARC records)
- Training requirements for librarians
- Tool ecosystem changes

---

## 4.5 Ontologies 🟡 MEDIUM PRIORITY

### Common Vocabularies

| Vocabulary | Purpose | Example Properties |
|------------|---------|-------------------|
| **schema.org** | Web content | `schema:name`, `schema:author`, `schema:datePublished` |
| **FOAF** | People/social | `foaf:name`, `foaf:knows`, `foaf:mbox` |
| **Dublin Core** | Metadata | `dc:title`, `dc:creator`, `dc:date` |
| **SKOS** | Taxonomies | `skos:broader`, `skos:narrower`, `skos:prefLabel` |

### OWL (Web Ontology Language)

```turtle
:Person a owl:Class .
:Author a owl:Class ;
        rdfs:subClassOf :Person .

:hasAuthor a owl:ObjectProperty ;
           rdfs:domain :Book ;
           rdfs:range :Person .

:isbn a owl:DatatypeProperty ;
      a owl:FunctionalProperty ;  # Each book has exactly one ISBN
      rdfs:domain :Book ;
      rdfs:range xsd:string .
```

### Open World vs Closed World 🟢 KNOW THE BASICS

| Aspect | Closed World (SQL) | Open World (RDF) |
|--------|-------------------|------------------|
| Missing data | Assumed false | Unknown |
| Example | No row for "John's wife" → John unmarried | No triple for "John's wife" → might be married |
| Reasoning | What's not in DB doesn't exist | What's not stated is unknown |
| Typical system | Relational database | Semantic web/RDF |

---

# 5. Document Databases (MongoDB) 🟠 HIGH PRIORITY

> **Exam Frequency: 70%** - Common alternative to relational in exam questions

## 5.1 Document Model

### JSON Documents

```json
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "title": "Pride and Prejudice",
    "author": {
        "name": "Jane Austen",
        "birth_year": 1775
    },
    "year": 1813,
    "genres": ["fiction", "romance", "classic"],
    "reviews": [
        { "user": "alice", "rating": 5, "text": "Loved it!" },
        { "user": "bob", "rating": 4, "text": "Great book" }
    ]
}
```

### When Documents Work Well

✅ **Good for:**
- Self-contained records (all data in one document)
- Variable schema (not all books have same fields)
- Nested data (embedded author, reviews)
- Arrays of values (genres, tags)

❌ **Problematic for:**
- Many-to-many relationships
- Complex joins across collections
- Strict consistency requirements

---

## 5.2 MongoDB Query Syntax

### Basic Queries

```javascript
// Find all documents
db.books.find()

// Find with condition
db.books.find({ year: 1813 })

// Find with multiple conditions (AND)
db.books.find({ year: 1813, "author.name": "Jane Austen" })

// Projection (select specific fields)
db.books.find({ year: 1813 }, { title: 1, author: 1, _id: 0 })
```

### Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `$eq` | Equals (default) | `{ year: { $eq: 1813 } }` |
| `$ne` | Not equals | `{ year: { $ne: 1813 } }` |
| `$gt` | Greater than | `{ year: { $gt: 1900 } }` |
| `$gte` | Greater than or equal | `{ year: { $gte: 1900 } }` |
| `$lt` | Less than | `{ year: { $lt: 1900 } }` |
| `$lte` | Less than or equal | `{ year: { $lte: 1900 } }` |
| `$in` | In array | `{ year: { $in: [1813, 1949, 1984] } }` |
| `$nin` | Not in array | `{ year: { $nin: [1813, 1949] } }` |

### Logical Operators

```javascript
// OR
db.books.find({
    $or: [
        { year: { $lt: 1900 } },
        { "author.name": "George Orwell" }
    ]
})

// AND (explicit)
db.books.find({
    $and: [
        { year: { $gte: 1900 } },
        { year: { $lt: 2000 } }
    ]
})

// NOT
db.books.find({
    year: { $not: { $gt: 1900 } }
})
```

### Array Queries

```javascript
// Array contains value
db.books.find({ genres: "fiction" })

// Array contains all values
db.books.find({ genres: { $all: ["fiction", "classic"] } })

// Array size
db.books.find({ genres: { $size: 3 } })

// $elemMatch - element matching multiple conditions
db.books.find({
    reviews: {
        $elemMatch: {
            rating: { $gte: 4 },
            user: "alice"
        }
    }
})
```

### ⚠️ $elemMatch vs Dot Notation - IMPORTANT DISTINCTION

This is **frequently tested** and commonly misunderstood!

**Document:**
```json
{
    "reviews": [
        { "user": "alice", "rating": 3 },
        { "user": "bob", "rating": 5 }
    ]
}
```

**Dot notation (ANY element matches):**
```javascript
// This matches! alice has a review AND someone gave rating 5
// (but NOT the same review)
db.books.find({
    "reviews.user": "alice",
    "reviews.rating": 5
})
```

**$elemMatch (SAME element must match all):**
```javascript
// This does NOT match! No single review has both
// user="alice" AND rating=5
db.books.find({
    reviews: {
        $elemMatch: { user: "alice", rating: 5 }
    }
})
```

| Method | Use When |
|--------|----------|
| **Dot notation** | Single condition on array, OR conditions can be on different elements |
| **$elemMatch** | Multiple conditions that must ALL be true for the SAME array element |

### Regular Expressions

```javascript
// Titles starting with "Pride"
db.books.find({ title: /^Pride/ })

// Titles containing "and" (case insensitive)
db.books.find({ title: { $regex: "and", $options: "i" } })
```

### Nested Document Queries

```javascript
// Query nested field using dot notation
db.books.find({ "author.name": "Jane Austen" })

// Query nested field with comparison
db.books.find({ "author.birth_year": { $lt: 1800 } })
```

---

## 5.3 Aggregation Pipeline

```javascript
db.books.aggregate([
    // Stage 1: Filter
    { $match: { year: { $gte: 1900 } } },

    // Stage 2: Group and count
    { $group: {
        _id: "$author.name",
        bookCount: { $sum: 1 },
        avgYear: { $avg: "$year" }
    }},

    // Stage 3: Sort
    { $sort: { bookCount: -1 } },

    // Stage 4: Limit
    { $limit: 5 }
])
```

### Common Aggregation Stages

| Stage | Purpose | Example |
|-------|---------|---------|
| `$match` | Filter documents | `{ $match: { status: "active" } }` |
| `$group` | Group and aggregate | `{ $group: { _id: "$category", count: { $sum: 1 } } }` |
| `$sort` | Order results | `{ $sort: { date: -1 } }` |
| `$limit` | Limit results | `{ $limit: 10 }` |
| `$project` | Select/reshape fields | `{ $project: { title: 1, year: 1 } }` |
| `$unwind` | Flatten arrays | `{ $unwind: "$genres" }` |

---

## 5.4 Worked Examples

**Example 1: Find fiction books published after 1900**
```javascript
db.books.find({
    genres: "fiction",
    year: { $gt: 1900 }
})
```

**Example 2: Find books with at least one 5-star review**
```javascript
db.books.find({
    reviews: { $elemMatch: { rating: 5 } }
})
```

**Example 3: Count books per genre**
```javascript
db.books.aggregate([
    { $unwind: "$genres" },
    { $group: {
        _id: "$genres",
        count: { $sum: 1 }
    }},
    { $sort: { count: -1 } }
])
```

**Example 4: Find authors with more than 3 books**
```javascript
db.books.aggregate([
    { $group: {
        _id: "$author.name",
        bookCount: { $sum: 1 }
    }},
    { $match: { bookCount: { $gt: 3 } } }
])
```

**Example 5: Average rating per book**
```javascript
db.books.aggregate([
    { $unwind: "$reviews" },
    { $group: {
        _id: "$title",
        avgRating: { $avg: "$reviews.rating" },
        reviewCount: { $sum: 1 }
    }},
    { $sort: { avgRating: -1 } }
])
```

---

# 6. Information Retrieval 🟡 MEDIUM PRIORITY

> **Exam Frequency: 50%** - Precision/Recall calculations common

## 6.1 Core Metrics

### Confusion Matrix

|  | Predicted Positive | Predicted Negative |
|--|-------------------|-------------------|
| **Actual Positive** | True Positive (TP) | False Negative (FN) |
| **Actual Negative** | False Positive (FP) | True Negative (TN) |

### Formulas

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Precision** | TP / (TP + FP) | Of items retrieved, how many are relevant? |
| **Recall** | TP / (TP + FN) | Of relevant items, how many did we retrieve? |
| **F1 Score** | 2 × (P × R) / (P + R) | Harmonic mean of precision and recall |
| **Accuracy** | (TP + TN) / Total | Overall correct predictions |

### Intuitive Understanding

- **Precision** = "Don't show me junk" (quality of results)
- **Recall** = "Don't miss anything" (completeness)

**Trade-off:** Returning more results typically increases recall but decreases precision.

---

## 6.2 Worked Examples

### Example 1: Search Engine Results

A search for "python programming" returns 20 results. Of these, 15 are actually about Python programming. The total number of relevant pages on the web for this query is 100.

| Metric | Calculation | Result |
|--------|-------------|--------|
| **TP** | Relevant and retrieved | 15 |
| **FP** | Not relevant but retrieved | 5 |
| **FN** | Relevant but not retrieved | 85 |
| **Precision** | 15 / (15 + 5) | **0.75 (75%)** |
| **Recall** | 15 / (15 + 85) | **0.15 (15%)** |
| **F1** | 2 × (0.75 × 0.15) / (0.75 + 0.15) | **0.25** |

### Example 2: Spam Filter

A spam filter processes 1000 emails:
- 200 actual spam, 800 legitimate
- Filter flags 180 as spam
- Of those 180, 150 are actually spam

| Value | Calculation |
|-------|-------------|
| TP | 150 (spam correctly identified) |
| FP | 30 (legitimate marked as spam) |
| FN | 50 (spam missed) |
| TN | 770 (legitimate correctly passed) |
| **Precision** | 150/180 = **83.3%** |
| **Recall** | 150/200 = **75%** |
| **F1** | 2 × (0.833 × 0.75) / (0.833 + 0.75) = **0.789** |

### Example 3: Document Classification

From March 2025 exam - London mortality data classification:

| Category | Retrieved | Relevant in Retrieved | Total Relevant |
|----------|-----------|----------------------|----------------|
| Disease | 45 | 40 | 50 |
| Accident | 30 | 25 | 35 |
| Other | 25 | 20 | 30 |

**Disease category:**
- Precision = 40/45 = 88.9%
- Recall = 40/50 = 80%
- F1 = 2 × (0.889 × 0.8) / (0.889 + 0.8) = 84.2%

---

## 6.3 When to Prioritize Which Metric

| Scenario | Priority | Reason |
|----------|----------|--------|
| Medical diagnosis | **Recall** | Don't miss any disease cases |
| Spam filter | **Precision** | Don't block legitimate emails |
| Legal discovery | **Recall** | Find all relevant documents |
| Product recommendations | **Precision** | Don't annoy with irrelevant suggestions |
| Balanced needs | **F1** | Trade-off between precision and recall |

---

## 6.4 Cross-Validation 🟢 KNOW THE BASICS

### k-Fold Cross-Validation

1. Split data into k equal parts (folds)
2. For each fold:
   - Train on k-1 folds
   - Test on remaining fold
3. Average results across all folds

```
Data: [1][2][3][4][5]  (5-fold)

Round 1: Train [2,3,4,5], Test [1]
Round 2: Train [1,3,4,5], Test [2]
Round 3: Train [1,2,4,5], Test [3]
Round 4: Train [1,2,3,5], Test [4]
Round 5: Train [1,2,3,4], Test [5]

Final score = average of 5 test scores
```

**Why use it?**
- More reliable than single train/test split
- Uses all data for both training and testing
- Reduces overfitting risk

---

# 7. Quick Reference Cards

## 7.1 SQL Cheat Sheet

```sql
-- SELECT template
SELECT columns
FROM table
[JOIN other_table ON condition]
[WHERE conditions]
[GROUP BY columns]
[HAVING group_conditions]
[ORDER BY columns [ASC|DESC]]
[LIMIT n];

-- Common JOINs
INNER JOIN  -- matching rows only
LEFT JOIN   -- all left + matching right
RIGHT JOIN  -- all right + matching left

-- Aggregation
COUNT(*), COUNT(col), SUM(col), AVG(col), MAX(col), MIN(col)

-- Common patterns
WHERE col IN (val1, val2)
WHERE col BETWEEN a AND b
WHERE col LIKE 'pattern%'
WHERE col IS NULL / IS NOT NULL

-- Subquery
SELECT * FROM t1 WHERE col IN (SELECT col FROM t2 WHERE ...)

-- CTE (Common Table Expression)
WITH cte AS (SELECT ...) SELECT * FROM cte;

-- Finding records NOT in a set
WHERE col NOT IN (SELECT ...)           -- Simple (watch for NULLs)
WHERE NOT EXISTS (SELECT 1 FROM ...)    -- Most reliable
LEFT JOIN ... WHERE id IS NULL          -- When need other columns

-- DISTINCT (don't forget!)
SELECT DISTINCT col FROM ...
SELECT COUNT(DISTINCT col) FROM ...
```

## 7.2 XPath Cheat Sheet

```xpath
/          Root or child step
//         Descendant (any depth)
.          Current node
..         Parent
@          Attribute
*          Any element
@*         Any attribute
text()     Text content

-- Predicates
[1]                     First element
[last()]                Last element
[@attr]                 Has attribute
[@attr='value']         Attribute equals
[element]               Has child element
[contains(., 'text')]   Contains text
[position() < 3]        First two elements

-- Examples
//book[@id='1']/title/text()
//book[year > 1900]/@genre
count(//chapter)
```

## 7.3 SPARQL Cheat Sheet

```sparql
PREFIX ex: <http://example.org/>

-- Basic SELECT
SELECT ?var1 ?var2
WHERE {
    ?subject ?predicate ?object .
}

-- With FILTER
FILTER (?year > 1900)
FILTER (CONTAINS(?name, "John"))
FILTER (LANG(?label) = "en")

-- OPTIONAL
OPTIONAL { ?s ?p ?o }

-- Aggregation
SELECT (COUNT(?x) AS ?count)
GROUP BY ?category
HAVING (COUNT(?x) > 5)

-- Property paths
:parent+        One or more
:knows*         Zero or more
:a/:b           Sequence
:a|:b           Alternative
^:prop          Inverse
```

## 7.4 MongoDB Cheat Sheet

```javascript
// Find
db.collection.find({ field: value })
db.collection.find({ field: { $gt: value } })
db.collection.find({ $or: [{...}, {...}] })

// Operators
$eq, $ne, $gt, $gte, $lt, $lte
$in, $nin
$and, $or, $not
$regex
$elemMatch (arrays)
$exists

// Array queries
{ tags: "value" }           // contains
{ tags: { $all: [...] } }   // contains all
{ tags: { $size: 3 } }      // exact size

// Aggregation
db.collection.aggregate([
    { $match: {...} },
    { $group: { _id: "$field", count: { $sum: 1 } } },
    { $sort: { count: -1 } },
    { $limit: 10 }
])
```

## 7.5 Turtle Triple Counting

```turtle
:s a :Class .              # 1 triple
:s :p1 :o1 ;              # 1 triple
   :p2 :o2 ;              # 1 triple (;)
   :p3 :o3, :o4 .         # 2 triples (,)
```

**Rules:**
- Period (`.`) = end of statement
- Semicolon (`;`) = new predicate, same subject
- Comma (`,`) = new object, same subject+predicate
- `a` = `rdf:type` (counts as triple)

## 7.6 Normal Forms Quick Check

| NF | Violation | Fix |
|----|-----------|-----|
| 1NF | Multi-valued attributes | Separate table |
| 2NF | Partial key dependency | Split table by key |
| 3NF | Transitive dependency | Extract to new table |

## 7.7 Database Selection Guide

| Data Characteristic | Choose |
|--------------------|--------|
| Structured + relationships | Relational (SQL) |
| Flexible schema, nested data | Document (MongoDB) |
| Many relationships to traverse | Graph (RDF/Neo4j) |
| Simple key→value lookups | Key-Value |
| Hierarchical documents with markup | XML Database |

---

*End of Comprehensive Revision Notes*

*Last updated: Covering Mock March 2021 - Mock October 2025*
