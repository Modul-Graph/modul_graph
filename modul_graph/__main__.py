from neomodel import config, db
from .utils.service import get_start_competences_plus_semester
from .utils.repository import get_possible_modules_plus_provided_comps_via_existing_comps
from .utils.repository import get_possible_modules_via_existing_comps
from .utils.repository import get_provided_comps_for_module_list
from .utils.controller import is_feasible

config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # default
# results, meta = db.cypher_query("MATCH (n) DETACH DELETE n")
# import modul_graph.static.spo_2017_inf_wise.SER


# rune's experiments -----------------------------------------------------------------------------------------------------------
# write functions in __main__.py (after data has been added to DB)
# console: python -m modul_graph
comps: list = ['Analysis', 'Numerik']
modules: list = ['Schlüsselkompetenzen I', 'Algorithmen und Datenstrukturen']
# print(get_start_competences_plus_semester())
is_feasible("")