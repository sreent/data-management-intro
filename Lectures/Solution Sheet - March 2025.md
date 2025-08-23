
## Part B — **Question 2** (Mortality bills dataset)

We’re given three delimited text files: `ages.txt`, `counts.txt`, `ParcodeDict.txt`, plus a city‑wide cause-of-death file (`codID|weekID|cod|codn`).

### (a) **Logical schema for MySQL** — tables, fields, keys, normal forms  **\[12]**

**Design goals**

* Separate *dimensions* (week, parish, age group, cause) from *facts* (weekly counts); enable integrity, reproducibility, and flexible aggregation.
* Ensure stable keys (e.g., `week_id` is the canonical `YYYY/WW` string from the data).

**Tables**

1. **`week`**  *(dimension)*

* `week_id` **CHAR(7)** **PK** — e.g., `'1729/01'` (as supplied)
* `year` **SMALLINT** — e.g., 1729
* `week_no` **TINYINT** — 1–53 (note 1752 exception)
* `week_seq` **INT** **UNIQUE** — optional monotonically increasing ordering across the entire series (helps time-series analysis)
* `calendar_note` **VARCHAR(32)** NULL — e.g., `'1752-short'`

*Rationale:* Store the canonical label as the key; avoid forcing Gregorian dates where they’re ambiguous.

2. **`parish`**  *(dimension; from `ParcodeDict.txt`)*

* `parcode` **CHAR(4)** **PK** — e.g., `STEP`
* `parish_name` **VARCHAR(100)** — e.g., `St Dunstan Stepney`
* `alias1` **VARCHAR(100)** NULL
* `alias2` **VARCHAR(100)** NULL
* `bills_group_before_1660` **VARCHAR(30)** NULL — e.g., `other|without|outparishes`
* `bills_group_after_1660` **VARCHAR(30)** NULL

3. **`age_group`**  *(dimension; normalizes `ages.txt` groups)*

* `age_group_id` **INT** **PK** AUTO\_INCREMENT
* `label` **VARCHAR(30)** **UNIQUE** — e.g., `under 2`, `2-5`
* `age_year_min` **TINYINT** NOT NULL
* `age_year_max` **TINYINT** NOT NULL

4. **`cause`**  *(dimension; from city-wide causes)*

* `cause_id` **INT** **PK** AUTO\_INCREMENT
* `cause_name` **VARCHAR(100)** **UNIQUE** — e.g., `Aged`, `Consumption`, `Plague`

5. **`parish_weekly_count`**  *(fact; from `counts.txt`)*

* `count_id` **INT** **PK** AUTO\_INCREMENT  *(or use supplied `countID` if globally unique)*
* `week_id` **CHAR(7)** **FK → week**
* `parcode` **CHAR(4)** **FK → parish**
* `count_type` **VARCHAR(20)** — e.g., `'plague'`, `'total'` *(see note below)*
* `count_n` **INT** NOT NULL
* **UNIQUE(week\_id, parcode, count\_type)**

*Note:* If `counts.txt` includes only plague, retain `count_type='plague'` now; add `'total'` (or similar) if/when a parish total file exists. Keeping the type column future‑proofs the schema.

6. **`age_weekly_count`**  *(fact; from `ages.txt`)*

* `week_id` **CHAR(7)** **FK → week**
* `age_group_id` **INT** **FK → age\_group**
* `count_n` **INT** NOT NULL
* **PK(week\_id, age\_group\_id)**

7. **`city_weekly_cause_count`**  *(fact; from city-wide causes)*

* `week_id` **CHAR(7)** **FK → week**
* `cause_id` **INT** **FK → cause**
* `count_n` **INT** NOT NULL
* **PK(week\_id, cause\_id)**

**Normal forms**

* All tables are in **1NF** (atomic fields, no repeating groups).
* Dimensions (`week`, `parish`, `age_group`, `cause`) are in **3NF/BCNF**: every non‑key attribute depends on the key, the whole key, and nothing but the key.
* Fact tables use **surrogate or composite keys**; non‑key attributes depend only on the key (e.g., `count_n` depends on `(week_id, parcode, count_type)` or `(week_id, cause_id)`).

**Removed/added fields**

* Replaced string `agegroup` with a normalized `age_group` table (prevents typos and supports ordering by range).
* Added `week_seq` and `calendar_note` to `week` for robust time‑series handling and 1752 documentation.
* Kept alias fields for parishes (historical names) but separated them from facts.

---

### (b) **Date representation & the 1752 skip**  **\[3]**

* **Representation choice:** Use **`week_id` (`YYYY/WW`)** as the canonical week key and store `year`, `week_no` separately; optionally add `week_seq` for strictly increasing ordering.
* **Issues raised by 1752 skip:**

  * There are **only 51 bills** in 1752; one “week” covers fewer than 7 days. Any logic that assumes 52–53 weeks/year or 7 days/week will miscompute rates.
  * **Gregorian dates** for week boundaries are **non‑uniform**; avoid deriving `DATE` start/end from `YYYY/WW` without a curated mapping.
  * For comparability (e.g., weekly rates per 100k), you may need a **`week_length_days`** metadata field or adjust rates using known span lengths.

---

### (c) **MySQL query — plague deaths in St Dunstan, Stepney, week 2 of 1729**  **\[2]**

```sql
SELECT c.count_n
FROM parish_weekly_count AS c
JOIN week AS w      ON w.week_id = c.week_id
WHERE c.parcode = 'STEP'
  AND w.year = 1729
  AND w.week_no = 2
  AND c.count_type = 'plague';
```

---

### (d) **MySQL query — annual deaths by age group, 1760–1790**  **\[4]**

```sql
SELECT
  w.year,
  ag.label AS age_group,
  SUM(a.count_n) AS total_deaths
FROM age_weekly_count AS a
JOIN week      AS w  ON w.week_id = a.week_id
JOIN age_group AS ag ON ag.age_group_id = a.age_group_id
WHERE w.year BETWEEN 1760 AND 1790
GROUP BY w.year, ag.label;
```

---

### (e) **Adding city-wide causes & parity check vs parish totals**  **\[5]**

**Add tables:** `cause` and `city_weekly_cause_count` (see part (a)). Load `cod` values into `cause(cause_name)` and `codn` into `city_weekly_cause_count(count_n)` keyed by `week_id`.

**Check:** If you have a **parish total** in `parish_weekly_count` (`count_type='total'`), verify that **sum of parish totals** matches **sum of city causes** per week:

```sql
WITH parish_totals AS (
  SELECT w.year, SUM(c.count_n) AS total_parish
  FROM parish_weekly_count c
  INNER JOIN week w
  ON c.week_id = w.week_id
  WHERE c.count_type = 'total'
  GROUP BY w.year
),
city_totals AS (
  SELECT w.year, SUM(c.count_n) AS total_city
  FROM city_weekly_cause_count c
  INNER JOIN week w
  ON c.week_id = w.week_id
  GROUP BY w.year
)
SELECT
  p.year,
  p.total_parish,
  c.total_city,
  (p.total_parish = c.total_city) AS matches
FROM parish_totals p 
LEFT JOIN city_totals c 
ON p.year = c.year;
```

*If `counts.txt` lacks an “all deaths” (`total`) row, you can only check specific causes that appear in both sources (e.g., `Plague`) by comparing the city’s `Plague` total to the sum of parish `count_type='plague'`.*

---

### (f) **Using the dataset for population‑health trends: issues & needed context**  **\[4]**

**Issues**

* **Case definition drift:** cause names and diagnostic practices change over 205 years (e.g., “Consumption” vs tuberculosis).
* **Coverage and boundary shifts:** parish borders, mergers/splits, and “within/without” groupings change; parish populations are not constant.
* **Data quality:** under‑registration, wartime disruptions, epidemic spikes, and missing or duplicated weeks.
* **Temporal irregularities:** the **1752** calendar anomaly; possible week-length variability.
* **Age‑mix confounding:** age structure changes over time; crude death counts are not comparable.

**Helpful external data**

* **Population denominators** by parish/year (or better, by week) to compute **rates**.
* **Age‑structure estimates** to produce **age‑standardized** rates.
* **Administrative boundary histories** and GIS shapes for parish mapping.
* **Tax/price indices, weather, epidemic timelines, wars**, major events for context.
* **Cause‑name concordance** to map historical labels to modern categories.

---

## Part B — **Question 3** (BeerXML snippet)

### (a) **Format?**  **\[1]**

**XML** in the **BeerXML** vocabulary (the comment notes BeerXML; encoding ISO‑8859‑1).

### (b) **Root node?**  **\[1]**

`<RECIPES>` is the document element (root), containing one or more `<RECIPE>` elements.

### (c) **Schema & validation?**  **\[3]**

The instance shows **no namespace or schema reference**. BeerXML defines an element vocabulary; validation can be done by:

* Using a published **XSD** (if provided by the BeerXML spec) and validating with an XML Schema validator, or
* Creating a **DTD**/**RELAX NG**/**Schematron** for structural and semantic rules (e.g., units, allowed child elements).

### (d) **XPath — names of all hops in recipe “Burton Ale”**  **\[4]**

```xpath
//RECIPE[NAME='Burton Ale']/HOPS/HOP/NAME/text()
```

### (e) **10‑fold cross‑validation — meaning**  **\[3]**

Split the dataset into **10 approximately equal folds**. Train on 9 folds, test on the held‑out fold; **repeat 10 times** with different held‑out folds; report the **average (and variance)** of the metrics across the 10 runs.

### (f) **50% accuracy — is it good? What else to know?**  **\[6]**

* **Baselines:** majority‑class accuracy; **random baseline ≈ 1/15 ≈ 6.7%**; per‑style support.
* **Class imbalance & confusion:** per‑class **precision/recall/F1**, confusion matrix.
* **Variance:** fold‑to‑fold spread; **confidence intervals**.
* **Data size & leakage:** number of recipes, duplicates, near‑duplicates across folds.
* **Calibration & top‑k:** probability calibration, **Top‑k** accuracy (e.g., Top‑3).
* **External validity:** performance on a **held‑out test set** or time‑based split.

### (g) **Document DB vs data interchange?**  **\[3]**

Primarily **data interchange**: BeerXML is a portable, structured format exchanged between brewing tools. The tree mirrors a single recipe, not an optimized query model across many documents; it lacks cross‑document identifiers and indexing typical of a document database deployment.

### (h) **Tree vs graph vs relational for this domain**  **\[9]**

* **Tree (XML/JSON):** Natural for a **single recipe** (one‑to‑many subelements like hops, fermentables). Self‑contained, readable, good for interchange and transport.

  * *Cons:* Hard to **deduplicate** ingredients across recipes; cross‑recipe queries (e.g., “all recipes using East Kent Goldings over 5% alpha”) require scanning documents.
* **Relational:** Normalize **Ingredient**, **Hop**, **Recipe**, **RecipeHop** (many‑to‑many), etc. Strong **integrity**, **joins**, powerful aggregation/filtering, indexing.

  * *Cons:* More upfront modeling; schema migrations when adding optional fields.
* **Graph (RDF/property graph):** Best when modeling **relationships** like substitutions, origin regions, supplier networks, or similarity between recipes. Flexible schema evolution and **path queries** (e.g., “hops grown in regions within the UK or substitutes-of‑substitutes”).

  * *Cons:* Additional infrastructure; need careful ontology/labels.

**Recommendation depends on:** query workload (per‑recipe vs cross‑corpus analytics), need for global identifiers, data integration with external knowledge (e.g., geography, supply chain), and governance (constraints vs flexibility).

---

## Part B — **Question 4** (MusicBrainz JSON‑LD → triples)

You `curl`ed JSON‑LD and converted it into RDF triples shown in Turtle‑like syntax.

### (a) **What did it convert into? Relation to JSON‑LD**  **\[2]**

It was converted to **RDF in Turtle** (Terse RDF Triple Language). **JSON‑LD** and **Turtle** are just two serializations of the **same RDF graph**.

### (b) **Which ontology is used? (ONE answer)**  **\[1]**

**`schema.org`** (every class/property shown is `schema:*`).

### (c) **Example triple where the requested URL does not occur**  **\[1]**

Example (none of subject/object is the requested artist IRI):

```
mbarea:489ce91b-6658-3307-9877-795b68554c98 a schema:Country .
```

### (d) **Bug in `schema:MusicAlbum` export — what & why**  **\[2]**

Two clear issues in the shown snippet:

1. **Undefined prefix**: `schema:byArtist mbartist:183d6ef6-…` uses **`mbartist:`** but only **`mbart:`** is declared. That breaks the link to the artist.
2. **Quoted IRIs for enumerations**: values like `"http://schema.org/StudioAlbum"` are **string literals**, not IRIs; they should be `<http://schema.org/StudioAlbum>` (or an unquoted prefixed name).
   **Likely cause:** errors in the JSON‑LD→RDF conversion or mapping (treating `@id` values as strings; typo in prefix mapping).

### (e) **“Two members” vs “impossible to know how many” — who’s right?**  **\[2]**

**“Impossible to know”** is correct. The graph asserts **at least two** members via two `schema:member` organization roles, but under the **open‑world assumption** absence of additional triples doesn’t mean they don’t exist.

### (f) **SPARQL — all groups founded in the United States**  **\[4]**

Assuming `schema:groupOrigin` points to a place and places can be nested via `schema:containedIn`:

```sparql
PREFIX schema: <http://schema.org/>

SELECT DISTINCT ?group ?name
WHERE {
  ?group a schema:MusicGroup ;
         schema:name ?name ;
         schema:groupOrigin/schema:containedIn* ?country .
  ?country a schema:Country ;
           schema:name "United States" .
}
ORDER BY ?name
```

### (g) **Ensure results are real groups, not persons**  **\[2]**

Filter out resources also typed as `schema:Person`, **or** require a group‑specific property such as `schema:member`:

```sparql
# Option A: exclude persons
FILTER NOT EXISTS { ?group a schema:Person }

# Option B: require group-specific structure
?group schema:member ?role .
?role a schema:OrganizationRole .
```

### (h) **SPARQL — list all albums made by bands of which John Linnell has been a member**  **\[4]**

Covers either direction of the album relation (`schema:album` on the group, or `schema:byArtist` on the album):

```sparql
PREFIX schema: <http://schema.org/>

SELECT DISTINCT ?album ?albumName ?bandName
WHERE {
  # Identify John Linnell node
  ?john a schema:Person ; schema:name "John Linnell" .

  # Find bands where John is/was a member (via OrganizationRole)
  ?band a schema:MusicGroup ; schema:name ?bandName ;
        schema:member [ a schema:OrganizationRole ; schema:member ?john ] .

  # Albums associated with that band (either direction)
  {
    ?album a schema:MusicAlbum ;
           schema:byArtist ?band ;
           schema:name ?albumName .
  }
  UNION
  {
    ?band schema:album ?album .
    ?album a schema:MusicAlbum ; schema:name ?albumName .
  }
}
ORDER BY ?bandName ?albumName
```

### (i) **Why no public SPARQL endpoint?**  **\[2]**

* **Operational cost/abuse risk:** arbitrary queries are expensive, hard to rate‑limit; vulnerability to denial‑of‑service.
* **Stability/governance:** evolving schema and data; hard to guarantee backward compatibility and predictable performance for public queries.

### (j) **Relational schema mirroring the RDF view**  **\[10]**

**Core entities**

* **`area`**: `area_id` (PK), `area_type` (`'Country'|'AdministrativeArea'|'City'`), `name`, `parent_area_id` (FK→`area`)
* **`artist`**: `artist_id` (PK), `name`, `is_group` **BOOLEAN**, `founding_date` **DATE** NULL, `group_origin_area_id` **FK→area** NULL
  *(Both persons and groups are “artists”; `is_group` distinguishes type.)*
* **`group_membership`**: `group_id` **FK→artist**, `person_id` **FK→artist**, `start_date` **DATE** NULL, `end_date` **DATE** NULL, **PK(group\_id, person\_id, start\_date)**
  *(Implements `schema:OrganizationRole`.)*
* **`album`**: `album_id` (PK), `name`, `production_type` (FK→`schema_enum`), `release_type` (FK→`schema_enum`)
* **`album_artist`**: `album_id` **FK→album**, `artist_id` **FK→artist**, `credited_to_text` **VARCHAR(200)** NULL, **PK(album\_id, artist\_id)**

**Auxiliary**

* **`schema_enum`**: `enum_id` (PK), `iri` **UNIQUE**, `label` — e.g., `<http://schema.org/StudioAlbum>`, `<http://schema.org/AlbumRelease>`
* **`artist_album_link`** (optional mirror of `schema:album` on the group): `artist_id` **FK→artist**, `album_id` **FK→album**, **PK(artist\_id, album\_id)**

**Normalization**

* **3NF/BCNF:** each non‑key attribute depends only on its key. Enumerations are normalized (`schema_enum`) to avoid string‑literal IRIs and support referential integrity. Areas form a **self‑referencing tree** matching `containedIn`.

---
