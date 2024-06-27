import asyncio
import gettext

import uvicorn
from neomodel import config, db

from .utils.controller import is_feasible

config.DATABASE_URL = 'bolt://neo4j:dev_pw@neo4j:7687'  # default
results, meta = db.cypher_query("MATCH (n) DETACH DELETE n")
import modul_graph.static.spo_2017_inf_wise._standard_curricula


# rune's experiments -----------------------------------------------------------------------------------------------------------
# write functions in __main__.py (after data has been added to DB)
# console: python -m modul_graph

# comps: list = ['Analysis', 'Numerik']
# modules: list = ['Schlüsselkompetenzen I', 'Algorithmen und Datenstrukturen']
# instantiate_std_curr_obj("SPO 2017 Informatik (Start Wintersemester)")


print(f"\nFeasible? {is_feasible("SPO 2017 Informatik (Start Wintersemester)")}\n")
translation = gettext.translation(domain="modul_graph", localedir="./locales", languages=["de"])
translation.install()

uvicorn.run(app="modul_graph.fastapi:app", port=8080, reload=True)
