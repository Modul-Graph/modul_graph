from neomodel import config, db
from .utils.controller import is_feasible

config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # default
# results, meta = db.cypher_query("MATCH (n) DETACH DELETE n")
# import modul_graph.static.spo_2017_inf_wise._standard_curriculums


# rune's experiments -----------------------------------------------------------------------------------------------------------
# write functions in __main__.py (after data has been added to DB)
# console: python -m modul_graph

comps: list = ['Analysis', 'Numerik']
modules: list = ['Schlüsselkompetenzen I', 'Algorithmen und Datenstrukturen']

print(is_feasible(""))