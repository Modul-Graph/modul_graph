from neomodel import config, db, remove_all_labels, install_all_labels
from .utils.computations import get_start_competences_plus_semester

from neomodel import install_labels

config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # default
# results, meta = db.cypher_query("MATCH (n) DETACH DELETE n")

# import modul_graph.static.spo_2017_inf_wise.SER

print(get_start_competences_plus_semester())