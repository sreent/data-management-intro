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
