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
