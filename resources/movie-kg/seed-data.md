# Movie Knowledge Graph — Slide-Ready Seed Data

A minimal dataset for Chapters 8–9 (RDF and SPARQL), small enough to trace by hand on teaching slides. Designed to demonstrate: URI-based identity, cross-source integration by URI alignment, ontology as descriptive contract, hand-traced traversals, and XML/JSON → RDF conversion.

**1 ontology | 2 data sources | 3 directors | 9 films | 3 actors | 6 genres | 3 awards**

---

## File Inventory

| File | Purpose | Used in |
|------|---------|---------|
| `movie_ontology.ttl` | Ontology contract — classes, properties, domain/range | Lab Parts 1, 4 (property cards, validation) |
| `source_a.ttl` | Filmography source — directors, actors, films, directed/actedIn edges | Lab Parts 2–3 (source reading, traversals) |
| `source_b.ttl` | Genres and awards source — genre/award entities, hasGenre/wonAward edges | Lab Parts 2–3 (integration, cross-source traversal) |

---

## Domain Context

A simplified movie knowledge graph inspired by linked-data film databases (IMDB, Wikidata, TMDb). Two independent sources contribute data about the same films using shared IMDB-based URIs. The domain demonstrates:

- **Cross-source integration:** Source A has filmography data (who directed/acted in what). Source B has classification data (genres, awards). Both use the same film URIs → edges connect automatically.
- **URI-based identity:** All entity URIs use IMDB identifiers (`tt` for films, `nm` for persons), ensuring global uniqueness.
- **Strings vs things:** Genre is modelled as a URI (`ex:genre_scifi`) not a literal string, making it traversable.

---

## Ontology Summary

### Classes

| Class | Superclass | Description |
|-------|-----------|-------------|
| `ex:Person` | — | Any person (parent class for Director and Actor) |
| `ex:Director` | `ex:Person` | A film director |
| `ex:Actor` | `ex:Person` | A film actor |
| `ex:Film` | — | A film |
| `ex:Genre` | — | A film genre |
| `ex:Award` | — | An award |

### Object Properties (entity → entity)

| Property | Domain | Range | Meaning |
|----------|--------|-------|---------|
| `ex:directed` | `ex:Person` | `ex:Film` | This person directed this film |
| `ex:actedIn` | `ex:Person` | `ex:Film` | This person acted in this film |
| `ex:hasGenre` | `ex:Film` | `ex:Genre` | This film belongs to this genre |
| `ex:wonAward` | `ex:Film` | `ex:Award` | This film won this award |
| `ex:sequelOf` | `ex:Film` | `ex:Film` | This film is a sequel of that film |

### Datatype Properties (entity → literal)

| Property | Domain | Range | Meaning |
|----------|--------|-------|---------|
| `ex:hasName` | (any) | `xsd:string` | Display name for persons, genres, awards |
| `ex:hasTitle` | `ex:Film` | `xsd:string` | Display title for films |
| `ex:releaseYear` | `ex:Film` | `xsd:integer` | Release year |
| `ex:runtime` | `ex:Film` | `xsd:integer` | Runtime in minutes |

**Design note:** `ex:hasName` has no domain constraint (can be used on any entity), while `ex:hasTitle` is restricted to films. This creates an intentional friction: to resolve a URI to a display name, you must know the entity's type first. Chapter 9 introduces `rdfs:label` as the universal solution.

---

## Source A — Filmography Data

### Directors

| URI | `ex:hasName` | Also typed as |
|-----|-------------|---------------|
| `ex:person_nm0634240` | Christopher Nolan | — |
| `ex:person_nm0898288` | Denis Villeneuve | — |
| `ex:person_nm1950086` | Greta Gerwig | `ex:Actor` (dual type) |

### Films

| URI | `ex:hasTitle` | `ex:releaseYear` | Notes |
|-----|-------------|-----------------|-------|
| `ex:film_tt1375666` | Inception | 2010 | |
| `ex:film_tt0816692` | Interstellar | 2014 | |
| `ex:film_tt15398776` | Oppenheimer | 2023 | Won 3 Academy Awards (Source B) |
| `ex:film_tt1160419` | Dune | 2021 | |
| `ex:film_tt4925292` | Lady Bird | 2017 | |
| `ex:film_tt1517268` | Barbie | 2023 | |
| `ex:film_tt0372784` | Batman Begins | 2005 | Sequel chain start |
| `ex:film_tt0468569` | The Dark Knight | 2008 | `sequelOf` Batman Begins |
| `ex:film_tt1345836` | The Dark Knight Rises | 2012 | `sequelOf` The Dark Knight |

### Actors

| URI | `ex:hasName` | Films (`actedIn`) |
|-----|-------------|-------------------|
| `ex:person_nm3154303` | Timothée Chalamet | Interstellar, Dune |
| `ex:person_nm0614165` | Cillian Murphy | The Dark Knight, Inception, Oppenheimer |
| `ex:person_nm3053338` | Margot Robbie | Barbie |

### Directed Edges

| Director | Films |
|----------|-------|
| Nolan | Inception, Interstellar, Oppenheimer, Batman Begins, The Dark Knight, The Dark Knight Rises |
| Villeneuve | Dune |
| Gerwig | Lady Bird, Barbie |

---

## Source B — Genre and Award Data

### Genres

| URI | `ex:hasName` |
|-----|-------------|
| `ex:genre_scifi` | Science Fiction |
| `ex:genre_action` | Action |
| `ex:genre_drama` | Drama |
| `ex:genre_comedy` | Comedy |
| `ex:genre_crime` | Crime |
| `ex:genre_biography` | Biography |

### Genre Assignments

| Film | Genres |
|------|--------|
| Inception | Science Fiction, Action |
| Interstellar | Science Fiction, Drama |
| Oppenheimer | Drama, Biography |
| The Dark Knight | Action, Crime, Drama |
| Dune | Science Fiction, Action, Drama |
| Lady Bird | Comedy, Drama |
| Barbie | Comedy |

### Awards

| URI | `ex:hasName` |
|-----|-------------|
| `ex:award_bestpicture` | Academy Award for Best Picture |
| `ex:award_bestdirector` | Academy Award for Best Director |
| `ex:award_bestactor` | Academy Award for Best Actor |

All three awards won by Oppenheimer (`ex:film_tt15398776`).

---

## Integration Points

These film URIs appear in **both** Source A and Source B, creating cross-source edges:

| Film URI | Source A provides | Source B provides |
|----------|-------------------|-------------------|
| `ex:film_tt1375666` | Title, year, directed, actedIn | Genres |
| `ex:film_tt0816692` | Title, year, directed, actedIn | Genres |
| `ex:film_tt15398776` | Title, year, directed, actedIn | Genres, awards |
| `ex:film_tt0468569` | Title, year, directed, actedIn, sequelOf | Genres |
| `ex:film_tt1160419` | Title, year, directed, actedIn | Genres |
| `ex:film_tt4925292` | Title, year, directed | Genres |
| `ex:film_tt1517268` | Title, year, directed, actedIn | Genres |

Films `ex:film_tt0372784` (Batman Begins) and `ex:film_tt1345836` (The Dark Knight Rises) appear only in Source A — they have no genre data in Source B.

---

## Teaching Scenarios Supported

| Scenario | Concept | What to show on slide |
|----------|---------|----------------------|
| **Strings vs things** | URI identity | "Crash" (2004) vs "Crash" (1996) — same string, different URIs. Genre as URI vs literal: URI is traversable, literal is a dead end. |
| **Cross-source integration** | URI alignment | Nolan → (directed, Source A) → Inception → (hasGenre, Source B) → Sci-Fi. Traversal crosses source boundary at the film URI. |
| **Sequel chain** | Multi-hop same-predicate | Dark Knight Rises → sequelOf → Dark Knight → sequelOf → Batman Begins. Like walking a linked list. |
| **Intersection query** | Multi-hop + set operation | Actors in both Nolan and Villeneuve films → Chalamet (Interstellar ∩ Dune). No single source contains this answer. |
| **Reverse traversal** | Edge direction | Start at genre_scifi, follow hasGenre backward → Inception, Interstellar, Dune. Then directed backward → Nolan, Villeneuve. |
| **Ontology validation** | Domain/range checking | `ex:genre_scifi ex:directed ex:genre_action` — Genre in Person domain → invalid. But triple store accepts it. |
| **Factual vs structural** | Ontology limitations | `ex:person_nm0634240 ex:actedIn ex:film_tt1375666` — Nolan acting in Inception is structurally valid (Person→Film) but factually wrong. |
| **Enforcement spectrum** | Cross-chapter arc | Engine rejects (Ch 5) → Validator rejects (Ch 7) → Nothing rejects (Ch 8). Three positions, three chapters. |
| **Associative entity** | Relationship attributes | Performance node for character role "Paul Atreides" — same pattern as Ch 2's junction table. |
| **XML/JSON → RDF** | Format conversion | Nested XML hierarchy flattened to typed edges. JSON nesting flattened to typed edges. Both produce identical triples when URIs align. |

---

## Triple Counts

| Source | Triples |
|--------|---------|
| Ontology (classes + properties) | 34 |
| Source A (entities + edges) | 58 |
| Source B (entities + edges) | 36 |
| **Total** | **128** |

Small enough to count and trace by hand. Large enough for meaningful cross-source traversals.
