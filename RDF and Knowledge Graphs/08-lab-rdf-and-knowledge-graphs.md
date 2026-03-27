# Topic 8 Lab — RDF and Knowledge Graphs: Read, Trace, Validate, Convert

This lab is **hand-worked** — no code, no Colab. You work with printed Turtle files, trace traversals by circling URIs and drawing lines between matching URIs across sheets, fill in property cards, validate triples against the ontology, and convert XML to RDF triples by hand.

Use the formal vocabulary (URI, triple, subject, predicate, object, literal, ontology, domain, range, object property, datatype property, class hierarchy, open-world assumption) throughout your work.

**Time budget:** Part 1 ~15 min | Part 2 ~10 min | Part 3 ~30 min | Part 4 ~15 min | Part 5 ~15 min | Part 6 ~5 min | **Total ~90 min**

**Materials required:** Printed copies of the three Turtle files below, plus the XML snippet in Part 5. A pen or pencil for circling URIs and drawing traversal lines.

---

## Provided Files

### File 1 — `movie_ontology.ttl` (the contract)

```turtle
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <http://example.org/movie#> .

# ── Classes ──────────────────────────────────────────
ex:Person    rdf:type  owl:Class .
ex:Director  rdf:type  owl:Class ;
             rdfs:subClassOf  ex:Person .
ex:Actor     rdf:type  owl:Class ;
             rdfs:subClassOf  ex:Person .
ex:Film      rdf:type  owl:Class .
ex:Genre     rdf:type  owl:Class .
ex:Award     rdf:type  owl:Class .

# ── Object Properties (entity → entity) ─────────────
ex:directed    rdf:type      owl:ObjectProperty ;
               rdfs:domain   ex:Person ;
               rdfs:range    ex:Film .

ex:actedIn     rdf:type      owl:ObjectProperty ;
               rdfs:domain   ex:Person ;
               rdfs:range    ex:Film .

ex:hasGenre    rdf:type      owl:ObjectProperty ;
               rdfs:domain   ex:Film ;
               rdfs:range    ex:Genre .

ex:wonAward    rdf:type      owl:ObjectProperty ;
               rdfs:domain   ex:Film ;
               rdfs:range    ex:Award .

ex:sequelOf    rdf:type      owl:ObjectProperty ;
               rdfs:domain   ex:Film ;
               rdfs:range    ex:Film .

# ── Datatype Properties (entity → literal value) ────
ex:hasName     rdf:type      owl:DatatypeProperty ;
               rdfs:range    xsd:string .

ex:hasTitle    rdf:type      owl:DatatypeProperty ;
               rdfs:domain   ex:Film ;
               rdfs:range    xsd:string .

ex:releaseYear rdf:type      owl:DatatypeProperty ;
               rdfs:domain   ex:Film ;
               rdfs:range    xsd:integer .

ex:runtime     rdf:type      owl:DatatypeProperty ;
               rdfs:domain   ex:Film ;
               rdfs:range    xsd:integer .
```

Note: `ex:hasName` has no domain constraint — it can be used on any entity (persons, genres, awards). `ex:hasTitle` is specific to films. To look up a human-readable display name, you need to know which property to follow, which means you must know the entity's type first.

---

### File 2 — `source_a.ttl` (Filmography)

```turtle
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <http://example.org/movie#> .

# ── Directors ────────────────────────────────────────
ex:person_nm0634240   rdf:type     ex:Director ;
                      ex:hasName   "Christopher Nolan" .

ex:person_nm0898288   rdf:type     ex:Director ;
                      ex:hasName   "Denis Villeneuve" .

ex:person_nm1950086   rdf:type     ex:Director , ex:Actor ;
                      ex:hasName   "Greta Gerwig" .

# ── Films ────────────────────────────────────────────
ex:film_tt1375666     rdf:type     ex:Film ;
                      ex:hasTitle  "Inception" ;
                      ex:releaseYear "2010"^^xsd:integer .

ex:film_tt0816692     rdf:type     ex:Film ;
                      ex:hasTitle  "Interstellar" ;
                      ex:releaseYear "2014"^^xsd:integer .

ex:film_tt15398776    rdf:type     ex:Film ;
                      ex:hasTitle  "Oppenheimer" ;
                      ex:releaseYear "2023"^^xsd:integer .

ex:film_tt1160419     rdf:type     ex:Film ;
                      ex:hasTitle  "Dune" ;
                      ex:releaseYear "2021"^^xsd:integer .

ex:film_tt4925292     rdf:type     ex:Film ;
                      ex:hasTitle  "Lady Bird" ;
                      ex:releaseYear "2017"^^xsd:integer .

ex:film_tt1517268     rdf:type     ex:Film ;
                      ex:hasTitle  "Barbie" ;
                      ex:releaseYear "2023"^^xsd:integer .

# ── Sequel chain ─────────────────────────────────────
ex:film_tt0372784     rdf:type     ex:Film ;
                      ex:hasTitle  "Batman Begins" ;
                      ex:releaseYear "2005"^^xsd:integer .

ex:film_tt0468569     rdf:type     ex:Film ;
                      ex:hasTitle  "The Dark Knight" ;
                      ex:releaseYear "2008"^^xsd:integer ;
                      ex:sequelOf    ex:film_tt0372784 .

ex:film_tt1345836     rdf:type     ex:Film ;
                      ex:hasTitle  "The Dark Knight Rises" ;
                      ex:releaseYear "2012"^^xsd:integer ;
                      ex:sequelOf    ex:film_tt0468569 .

# ── Actors ───────────────────────────────────────────
ex:person_nm3154303   rdf:type     ex:Actor ;
                      ex:hasName   "Timothée Chalamet" .

ex:person_nm0614165   rdf:type     ex:Actor ;
                      ex:hasName   "Cillian Murphy" .

ex:person_nm3053338   rdf:type     ex:Actor ;
                      ex:hasName   "Margot Robbie" .

# ── Directed edges ───────────────────────────────────
ex:person_nm0634240   ex:directed  ex:film_tt1375666 .
ex:person_nm0634240   ex:directed  ex:film_tt0816692 .
ex:person_nm0634240   ex:directed  ex:film_tt15398776 .
ex:person_nm0634240   ex:directed  ex:film_tt0372784 .
ex:person_nm0634240   ex:directed  ex:film_tt0468569 .
ex:person_nm0634240   ex:directed  ex:film_tt1345836 .

ex:person_nm0898288   ex:directed  ex:film_tt1160419 .

ex:person_nm1950086   ex:directed  ex:film_tt4925292 .
ex:person_nm1950086   ex:directed  ex:film_tt1517268 .

# ── ActedIn edges ────────────────────────────────────
ex:person_nm3154303   ex:actedIn   ex:film_tt0816692 .
ex:person_nm3154303   ex:actedIn   ex:film_tt1160419 .

ex:person_nm0614165   ex:actedIn   ex:film_tt0468569 .
ex:person_nm0614165   ex:actedIn   ex:film_tt1375666 .
ex:person_nm0614165   ex:actedIn   ex:film_tt15398776 .

ex:person_nm3053338   ex:actedIn   ex:film_tt1517268 .

ex:person_nm1950086   ex:actedIn   ex:film_tt1517268 .
```

---

### File 3 — `source_b.ttl` (Genres and Awards)

```turtle
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <http://example.org/movie#> .

# ── Genres ───────────────────────────────────────────
ex:genre_scifi       rdf:type     ex:Genre ;
                     ex:hasName   "Science Fiction" .

ex:genre_action      rdf:type     ex:Genre ;
                     ex:hasName   "Action" .

ex:genre_drama       rdf:type     ex:Genre ;
                     ex:hasName   "Drama" .

ex:genre_comedy      rdf:type     ex:Genre ;
                     ex:hasName   "Comedy" .

ex:genre_crime       rdf:type     ex:Genre ;
                     ex:hasName   "Crime" .

ex:genre_biography   rdf:type     ex:Genre ;
                     ex:hasName   "Biography" .

# ── Genre assignments ────────────────────────────────
ex:film_tt1375666    ex:hasGenre  ex:genre_scifi .
ex:film_tt1375666    ex:hasGenre  ex:genre_action .

ex:film_tt0816692    ex:hasGenre  ex:genre_scifi .
ex:film_tt0816692    ex:hasGenre  ex:genre_drama .

ex:film_tt15398776   ex:hasGenre  ex:genre_drama .
ex:film_tt15398776   ex:hasGenre  ex:genre_biography .

ex:film_tt0468569    ex:hasGenre  ex:genre_action .
ex:film_tt0468569    ex:hasGenre  ex:genre_crime .
ex:film_tt0468569    ex:hasGenre  ex:genre_drama .

ex:film_tt1160419    ex:hasGenre  ex:genre_scifi .
ex:film_tt1160419    ex:hasGenre  ex:genre_action .
ex:film_tt1160419    ex:hasGenre  ex:genre_drama .

ex:film_tt4925292    ex:hasGenre  ex:genre_comedy .
ex:film_tt4925292    ex:hasGenre  ex:genre_drama .

ex:film_tt1517268    ex:hasGenre  ex:genre_comedy .

# ── Awards ───────────────────────────────────────────
ex:award_bestpicture    rdf:type     ex:Award ;
                        ex:hasName   "Academy Award for Best Picture" .

ex:award_bestdirector   rdf:type     ex:Award ;
                        ex:hasName   "Academy Award for Best Director" .

ex:award_bestactor      rdf:type     ex:Award ;
                        ex:hasName   "Academy Award for Best Actor" .

# ── Award wins ───────────────────────────────────────
ex:film_tt15398776      ex:wonAward  ex:award_bestpicture .
ex:film_tt15398776      ex:wonAward  ex:award_bestdirector .
ex:film_tt15398776      ex:wonAward  ex:award_bestactor .
```

---

## Part 1 — Read the Ontology (the Contract)

The ontology is the contract for graph-shaped data. In Chapter 7, the XSD told you which elements could appear, in what order, with what types. The ontology tells you which classes of entity exist, which properties connect them, and what types sit on each side. The difference: the XSD *enforced* the contract (xmllint rejected violations). The ontology *describes* the contract (triple stores accept anything).

### Q1. Property cards

For each property in the ontology, fill in the card. The first one is done for you.

| Property | Type (Object / Datatype) | Domain (subject must be…) | Range (object must be…) | Meaning |
|---|---|---|---|---|
| `ex:directed` | Object | `ex:Person` | `ex:Film` | This person directed this film |
| `ex:actedIn` | | | | |
| `ex:hasGenre` | | | | |
| `ex:wonAward` | | | | |
| `ex:sequelOf` | | | | |
| `ex:hasName` | | | | |
| `ex:hasTitle` | | | | |
| `ex:releaseYear` | | | | |
| `ex:runtime` | | | | |

Two of these properties give entities human-readable display names. Which two? One of them has a domain constraint and one does not — which is which, and why does this matter when you resolve a URI to a name during traversal?

### Q2. Class hierarchy

Draw the class hierarchy as a tree diagram. Which classes are subclasses of `ex:Person`?

A single entity can have multiple `rdf:type` triples. Find the entity in `source_a.ttl` that has two type declarations. What are they? Write out the two triples.

### Q3. Contract enforcement: XSD vs ontology

In Chapter 7, if an XML document placed `<TaxAmount>` before `<LineExtensionAmount>`, `xmllint` rejected it — the XSD enforced the contract.

Suppose someone adds this triple to the movie graph:

```turtle
ex:genre_scifi  ex:directed  ex:genre_action .
```

A Genre "directing" another Genre — this violates the ontology's domain and range for `ex:directed`.

(a) Would a triple store reject this triple?

(b) How does this differ from Chapter 7's schema validation?

(c) In one sentence, state the difference between a contract that *enforces* and a contract that *describes*.

---

## Part 2 — Read Two Sources

### Q4. Read Source A

Examine `source_a.ttl`. Answer by scanning the file:

(a) How many distinct directors? List their URIs and `ex:hasName` values.

| URI | `ex:hasName` |
|---|---|
| | |
| | |
| | |

(b) How many distinct films? How many distinct actors?

(c) Which entity has both `rdf:type ex:Director` and `rdf:type ex:Actor`? Write its URI and name.

(d) Find the sequel chain. Starting from `ex:film_tt1345836`, list the `sequelOf` edges. What is the chain in order (most recent → oldest)?

### Q5. Read Source B

Examine `source_b.ttl`. Answer:

(a) List all genre URIs and their `ex:hasName` values.

(b) Which film URIs from Source A also appear in Source B? (These are the integration points — same URI, different facts.)

(c) **Predict:** after merging both sources, which films will have *both* cast data (from Source A) AND genre data (from Source B)?

(d) Does Source B contain any `ex:directed` or `ex:actedIn` triples? What kind of information does Source B add that Source A lacks?

---

## Part 3 — Hand-Trace Traversals

For each traversal, work on your printed Turtle files. Circle URIs and draw lines between matching URIs to trace the path. When you reach a URI node, resolve it to a display name — but notice you need to know which property to follow: `ex:hasTitle` for films, `ex:hasName` for everything else.

### Q6. Nolan's films and genres (single-hop + cross-source two-hop)

**(a)** **Before tracing**, predict: how many `ex:directed` edges leave `ex:person_nm0634240`? Write your predicted count: ____

Start at `ex:person_nm0634240`. Follow all outgoing `ex:directed` edges. For each film node you reach, look up its `ex:hasTitle`.

| Film URI | `ex:hasTitle` |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |

How many films? Which source did the `directed` edges come from?

**(b)** **Before tracing**, predict: of Nolan's films from part (a), how many have `ex:hasGenre` edges in `source_b.ttl`? (Not all films may appear in Source B.) Write your predicted count: ____

Now continue the trace. From each film, follow `ex:hasGenre` edges to genres. Resolve each genre's `ex:hasName`.

Write out the traversal path for one film as an example:

```
ex:person_nm0634240 ──directed──→ ex:film_tt1375666 ──hasGenre──→ ex:genre_scifi
                                                      ──hasGenre──→ ex:genre_action
```

**(c)** Collect all unique genres across all of Nolan's films:

| Genre URI | `ex:hasName` |
|---|---|
| | |
| | |
| | |
| | |
| | |

Note: the `ex:directed` edges came from Source A. The `ex:hasGenre` edges came from Source B. This traversal works because both sources used the same film URIs. If Source B had used `ex:Inception` instead of `ex:film_tt1375666`, the edges would not connect.

### Q7. Sequel chain traversal

**Before tracing**, predict: how many hops will the `ex:sequelOf` chain be? (Scan `source_a.ttl` for `ex:sequelOf` triples — how many exist?) Write your predicted chain length: ____

Now trace. Start at `ex:film_tt1345836`. Follow `ex:sequelOf` edges. At each node, look up the title. Continue until there is no further `ex:sequelOf` edge.

```
ex:film_tt1345836  ──sequelOf──→  ???  ──sequelOf──→  ???
```

| Film URI | `ex:hasTitle` | Follows from |
|---|---|---|
| `ex:film_tt1345836` | ? | (start) |
| ? | ? | `sequelOf` from above |
| ? | ? | `sequelOf` from above |

This is a different traversal pattern from Q6: you follow the *same* predicate multiple hops deep, like walking a linked list. Write the chain in chronological order (oldest → newest).

### Q8. Multi-hop intersection: actors in both Nolan and Villeneuve films

**"Actors who appeared in films directed by both Nolan AND Villeneuve."**

**Before tracing**, predict: how many actors in the dataset have `ex:actedIn` edges to at least one Nolan film AND at least one Villeneuve film? Write your predicted count: ____

Trace it step by step on your printed Turtle files:

**Step 1 — Nolan's films:** Start at `ex:person_nm0634240`, follow `directed` edges. List the film URIs.

**Step 2 — Villeneuve's films:** Start at `ex:person_nm0898288`, follow `directed` edges. List the film URIs.

**Step 3 — Actors in Nolan's films:** For each film from Step 1, find all entities with an `actedIn` edge pointing to that film. List actor URIs.

**Step 4 — Actors in Villeneuve's films:** For each film from Step 2, find all entities with an `actedIn` edge pointing to that film. List actor URIs.

**Step 5 — Intersection:** Which actor URIs appear in *both* Step 3 and Step 4?

Actor URI: __________________ `ex:hasName`: __________________

This question — which no single source contains — was answered by traversing the graph and computing an intersection.

### Q9. Reverse traversal: directors of Sci-Fi films

**Before tracing**, predict: how many films have `ex:hasGenre ex:genre_scifi` in `source_b.ttl`? How many distinct directors will you find for those films? Write your predictions: ____ films, ____ directors.

Now trace. Start at `ex:genre_scifi`. Follow `ex:hasGenre` edges *backward* (find films that point to this genre). From each film, follow `ex:directed` edges *backward* (find persons that point to these films). Resolve names.

Note: edge direction matters. `ex:hasGenre` points Film → Genre, so "which films are Sci-Fi?" means following the edge in reverse. On your printed files, this means finding lines where `ex:genre_scifi` appears as the *object* of `ex:hasGenre`, then tracing back to the *subject*.

| Sci-Fi Film URI | `ex:hasTitle` | Director URI | Director `ex:hasName` |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

### Q10. Strings vs URIs: dead ends and disambiguation

**(a)** **Before tracing**, predict: if you start from the string `"Inception"`, how many outgoing edges can you follow? If you start from `ex:film_tt1375666`, how many outgoing edges exist in `source_a.ttl` alone?

**(b)** On your printed Turtle files, find the literal `"Inception"` (the string value in `ex:film_tt1375666 ex:hasTitle "Inception"`). Starting from the literal `"Inception"`, can you follow any outgoing edges? Why not?

**(c)** Starting from the entity `ex:film_tt1375666`, can you follow edges to find the director? Trace the path.

**(d)** Suppose someone wrote this triple instead of using a URI for the genre:

```turtle
ex:film_tt1375666  ex:hasGenre  "Science Fiction" .
```

Could you traverse from `"Science Fiction"` to find other films in the same genre? Why not? What happens to the traversal "all Sci-Fi films" if some films use the URI `ex:genre_scifi` and others use the literal string `"Science Fiction"`?

**(e)** Now consider disambiguation. Two films share the title "Crash" (not in the current data, but imagine adding them):

```turtle
ex:film_tt0375679   rdf:type     ex:Film ;
                    ex:hasTitle  "Crash" ;
                    ex:releaseYear "2004"^^xsd:integer .

ex:film_tt0115964   rdf:type     ex:Film ;
                    ex:hasTitle  "Crash" ;
                    ex:releaseYear "1996"^^xsd:integer .
```

Are these the same film? If you searched for the *string* "Crash", which film would you find? If you start traversing from the *URI* `ex:film_tt0375679`, which film do you reach? In one sentence: what role does the URI play that the title cannot?

---

## Part 4 — Validate Triples Against the Ontology

The ontology describes domain and range for each property. For each triple below, check it against your property cards from Q1. Mark it valid (✓) or invalid (✗). If invalid, state the specific violation. Remember: `ex:Director rdfs:subClassOf ex:Person`, so a Director in a `ex:Person` domain position is valid.

| # | Triple | Valid? | If invalid, which rule is violated? |
|---|---|---|---|
| 1 | `ex:person_nm0634240  ex:directed  ex:film_tt1375666 .` | | |
| 2 | `ex:genre_scifi  ex:directed  ex:genre_action .` | | |
| 3 | `ex:film_tt1375666  ex:hasGenre  "Science Fiction" .` | | |
| 4 | `ex:film_tt1375666  ex:hasTitle  "Inception" .` | | |
| 5 | `ex:person_nm0634240  ex:actedIn  ex:film_tt1375666 .` | | |
| 6 | `ex:film_tt1375666  ex:directed  ex:person_nm0634240 .` | | |
| 7 | `"Christopher Nolan"  ex:directed  ex:film_tt1375666 .` | | |
| 8 | `ex:person_nm1950086  ex:directed  ex:film_tt4925292 .` | | |
| 9 | `ex:film_tt1375666  ex:releaseYear  "July 2010" .` | | |
| 10 | `ex:person_nm0614165  ex:actedIn  ex:award_bestactor .` | | |
| 11 | `ex:person_nm0634240  ex:hasTitle  "Christopher Nolan" .` | | |

### Q11. Validation discussion

(a) Triple #5 is factually wrong — Nolan did not act in Inception. But does it pass domain/range validation? What does this tell you about what the ontology can and cannot catch?

(b) Triple #7 uses a literal string as the subject. Is this valid RDF? (Hint: RDF requires subjects to be URIs or blank nodes, never literals.)

(c) Triple #9 has the right property and the right entity, but the literal value is `"July 2010"` instead of `"2010"^^xsd:integer`. The ontology says `ex:releaseYear rdfs:range xsd:integer`. In a relational database (Chapter 5), a CHECK constraint would reject this at insert time. What happens here?

(d) Triple #11 uses `ex:hasTitle` on a Person. The ontology says `ex:hasTitle rdfs:domain ex:Film`. Is this valid? Now look at the other naming property, `ex:hasName` — it has no domain constraint. Could you use `ex:hasName` on a Film? Would it mean the same thing as `ex:hasTitle`? Every time you resolved a URI to a display name in Part 3, you had to check: is this a Film (follow `ex:hasTitle`) or something else (follow `ex:hasName`). What problem does having two different naming properties create?

(e) Compare the validation experience across three chapters:

| Chapter | Contract | What catches violations? | When? |
|---|---|---|---|
| 5 (Relational) | DDL + constraints | Database engine | At insert time (immediate) |
| 7 (XML) | XSD | `xmllint --schema` | At boundary, before submission |
| 8 (RDF) | Ontology | ? | ? |

Fill in the last row.

---

## Part 5 — Convert XML to RDF

### Given: movie filmography XML

A film database exports Villeneuve's filmography as XML:

```xml
<filmography>
    <director id="nm0898288" name="Denis Villeneuve">
        <film id="tt1160419" year="2021">
            <title>Dune</title>
            <genre>Sci-Fi</genre>
            <genre>Action</genre>
            <genre>Drama</genre>
            <cast>
                <actor id="nm3154303" role="Paul Atreides">
                    Timothée Chalamet
                </actor>
            </cast>
        </film>
        <film id="tt2543164" year="2016">
            <title>Arrival</title>
            <genre>Sci-Fi</genre>
            <genre>Drama</genre>
            <cast>
                <actor id="nm0000210" role="Louise Banks">
                    Amy Adams
                </actor>
            </cast>
        </film>
    </director>
</filmography>
```

### Q12. Design decisions and convert the first film (Dune)

Before converting, make several design decisions. For each, state your choice and reason:

(a) The `<director>` element has `id="nm0898288"` and `name="Denis Villeneuve"`. Which attribute becomes part of the URI? Which becomes the value of `ex:hasName`? Look at how the provided Turtle files handle person identity for guidance.

(b) The `<genre>` elements contain text: `Sci-Fi`, `Action`, `Drama`. Should these become literal objects or URI objects in the RDF? What happens to traversal if you use literals? (Refer back to Q10.) What URIs would you use? (Hint: check `source_b.ttl`.)

(c) The `<actor>` element has three pieces of information: `id` attribute, text content (the name), and `role` attribute (the character name). The `role` "Paul Atreides" describes neither Chalamet (the person) nor Dune (the film) — it describes their *relationship*. In Chapter 2, what was this pattern called? (An associative entity.) How would you handle this in RDF?

(d) The XML `<title>` element maps to which RDF property? The XML `name` attribute maps to which RDF property? Notice: you need to choose the right naming property based on what kind of entity you are describing. Films get `ex:hasTitle`, people get `ex:hasName`.

**(e)** Now write out all Turtle triples for the director, the first film (Dune), its genres, and its cast member. Use the URI patterns from the provided Turtle files (e.g., `ex:person_nm0898288`, `ex:film_tt1160419`).

Start (complete the blanks and add the remaining triples):

```turtle
# Director
ex:person_nm0898288   rdf:type     ex:Director ;
                      ex:hasName   __________________ .

# Film
ex:film_tt1160419     rdf:type     __________ ;
                      ex:hasTitle  __________________ ;
                      ex:releaseYear __________________ .

# Directed edge
ex:person_nm0898288   ex:directed  __________________ .

# Genre edges
ex:film_tt1160419     ex:hasGenre  __________________ .
ex:film_tt1160419     ex:hasGenre  __________________ .
ex:film_tt1160419     ex:hasGenre  __________________ .

# Actor
ex:person_nm3154303   rdf:type     __________ ;
                      ex:hasName   __________________ .

# ActedIn edge
ex:person_nm3154303   ex:actedIn   __________________ .
```

Now check: compare your triples against `source_a.ttl` and `source_b.ttl`. Which of your triples already appear in the provided files? This is integration in action — the same facts, from different source formats, producing the same triples because the URI scheme is aligned.

### Q13. Convert the second film (Arrival)

Write out all Turtle triples for the second film (Arrival), its genres, and its cast member (Amy Adams).

Note: Arrival (`ex:film_tt2543164`) and Amy Adams (`ex:person_nm0000210`) do *not* appear in `source_a.ttl` or `source_b.ttl`. These are new entities entering the graph. After merging, what happens?

- Villeneuve (`ex:person_nm0898288`) now has a `ex:directed` edge to Arrival in addition to Dune.
- The genre `ex:genre_scifi` now has one more film pointing to it.
- Amy Adams is a new node — she can be traversed to from Arrival, and Arrival can be traversed to from Villeneuve.

The graph grows by absorbing new triples. No schema change. No ALTER TABLE. No migration.

### Q14. Handle the character role

The XML has `role="Paul Atreides"` on the actor element. This attribute describes the *relationship* between Chalamet and Dune, not either entity alone. In Chapter 2, you solved this with an associative entity (a junction table with its own attributes). In RDF, the approach is similar — create an intermediate node:

```turtle
ex:performance_001    rdf:type       ex:Performance ;
                      ex:hasName     "Chalamet as Paul Atreides in Dune" ;
                      ex:performer   ex:person_nm3154303 ;
                      ex:film        ex:film_tt1160419 ;
                      ex:character   "Paul Atreides" .
```

(a) How many edges connect the three nodes (Chalamet, the performance, and Dune)?

(b) If you used the simple `ex:actedIn` edge (`ex:person_nm3154303 ex:actedIn ex:film_tt1160419`), where would `"Paul Atreides"` go? Can you attach it to Chalamet? (No — he plays different characters in different films.) Can you attach it to Dune? (No — different actors play different characters in the same film.)

(c) The Performance node is like a row in a junction table from Chapter 2. What is its "composite key" equivalent? (The combination of performer + film makes it unique.)

### Q15. What was lost and gained?

(a) **Lost:** The XML elements appear in a defined order: `<title>` before `<genre>` before `<cast>`. In the RDF, is there any ordering among the triples? Does this matter for the movie domain? (Compare: would it matter if you were converting music notation, where note order determines melody?)

(b) **Lost:** The XML has a containment hierarchy — `<filmography>` contains `<director>` contains `<film>` contains `<cast>` contains `<actor>`. In the RDF, what happened to this hierarchy? (It was flattened into typed relationships: `directed`, `actedIn`. The nesting became explicit edges.)

(c) **Gained:** In the XML, Chalamet's identity is the string `id="nm3154303"` inside an `<actor>` element nested under a specific `<film>`. Can a second XML file reference this exact actor without duplicating the element? (Not easily — XML cross-document references are cumbersome.) In the RDF, what makes cross-source linking trivial? (The URI `ex:person_nm3154303` is globally unique and referenceable from any graph.)

---

## Part 6 — Comparison and Reflection

### Q16. Four-model comparison and applied scenarios

**(a)** Complete the RDF column. The other columns are pre-filled from Chapters 2–7.

| Dimension | Relational (Ch 2–5) | Document/JSON (Ch 6) | XML/XSD (Ch 7) | RDF (Ch 8) |
|---|---|---|---|---|
| Atomic unit | Row | Document (aggregate) | Element (tree node) | |
| Identity scope | PK (one database) | `_id` (one collection) | Namespace + element name | |
| Schema posture | Schema-on-write (DDL) | Schema-on-read (default) | Contract-first (XSD) | |
| World assumption | Closed | Closed | Closed (validated) | |
| Structural variation | Requires ALTER TABLE | Natural (different fields) | Must be declared in XSD | |
| Cross-source integration | Requires key mapping + schema agreement | Aggregate-internal; cross-doc requires app logic | Validated document exchange | |
| Relationship traversal | JOIN (pre-declared FK paths) | `$lookup` (costly) | XPath (within document tree) | |
| Primary workload | OLTP transactions | Aggregate read/write | Cross-boundary document exchange | |

**(b)** For each scenario, state which model fits best and why (2–3 sentences each):

(i) A streaming platform stores user watch history with embedded show metadata, optimised for "load my homepage recommendations on login."

(ii) A film distributor must submit metadata to a national film registry. The registry publishes an XSD that all distributors must conform to. Submissions that fail validation are rejected.

(iii) A film research project linking directors, films, actors, awards, and box-office data across IMDB, Wikidata, Rotten Tomatoes, and The Movie Database — each maintained independently, each with its own identifier scheme.

(iv) A cinema chain's booking system tracking screenings, ticket sales, payments, and seat assignments with ACID guarantees.

---

## Submission Checklist

Before submitting, verify you have:

- [ ] Nine completed property cards plus class hierarchy diagram (Q1–Q2)
- [ ] Enforcement discussion: enforced vs descriptive contracts (Q3)
- [ ] Source inspection with entity counts and integration-point predictions (Q4–Q5)
- [ ] Five hand-traced traversals with resolved display names (Q6–Q10)
- [ ] Eleven triples validated with violation explanations (Part 4)
- [ ] Validation discussion including cross-chapter enforcement comparison (Q11)
- [ ] XML → RDF conversion with design decisions (Q12–Q13)
- [ ] Associative entity (Performance node) with analysis (Q14)
- [ ] Lost/gained analysis for XML → RDF conversion (Q15)
- [ ] Four-model comparison table with RDF column completed and applied scenarios (Q16)
