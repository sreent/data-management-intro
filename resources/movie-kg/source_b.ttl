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
