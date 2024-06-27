from neomodel import config, db
from .utils.controller import is_feasible
from .utils.data_access import da_get_provided_comps_for_module_list_plus_sem_of_provision_without_duplicates
from .utils.std_curr import instantiate_std_curr_obj

config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # default
# results, meta = db.cypher_query("MATCH (n) DETACH DELETE n")
# import modul_graph.static.spo_2017_inf_wise._standard_curricula


# rune's experiments -----------------------------------------------------------------------------------------------------------
# write functions in __main__.py (after data has been added to DB)
# console: python -m modul_graph

# comps: list = ['Analysis', 'Numerik']
# modules: list = ['Schlüsselkompetenzen I', 'Algorithmen und Datenstrukturen']
# instantiate_std_curr_obj("SPO 2017 Informatik (Start Wintersemester)")

print(f"\nFeasible? {is_feasible("SPO 2017 Informatik (Start Wintersemester)")}\n")