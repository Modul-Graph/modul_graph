import asyncio
import gettext
import uvicorn
from neomodel import config, db
from .utils.controller import is_feasible, get_example_graph

config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # default
results, meta = db.cypher_query("MATCH (n) DETACH DELETE n")
import modul_graph.static.spo_2017_inf_wise._standard_curricula


# rune's experiments -----------------------------------------------------------------------------------------------------------
# write functions in __main__.py (after data has been added to DB)
# console: python -m modul_graph

# comps: list = ['Analysis', 'Numerik']
# modules: list = ['Schlüsselkompetenzen I', 'Algorithmen und Datenstrukturen']
# instantiate_std_curr_obj("SPO 2017 Informatik (Start Wintersemester)")


# print(f"\nFeasible? {is_feasible("SPO 2017 Informatik (Start Wintersemester)")}\n")
print(get_example_graph("Algebra", "SPO 2017 Informatik (Start Wintersemester)"))

'''
╒════════════════════════════════════════╕
│COMPETENCES                             │
╞════════════════════════════════════════╡
│"Algorithmen und Datenstrukturen"       │
├────────────────────────────────────────┤
│"Analysis"                              │
├────────────────────────────────────────┤
│"Numerik"                               │
├────────────────────────────────────────┤
│"Betriebssysteme"                       │
├────────────────────────────────────────┤
│"Datenbanken und Informationssysteme"   │
├────────────────────────────────────────┤
│"Digitaltechnik und Rechnerorganisation"│
├────────────────────────────────────────┤
│"Diskrete Strukturen"                   │
├────────────────────────────────────────┤
│"Logik"                                 │
├────────────────────────────────────────┤
│"Algebra"                               │
├────────────────────────────────────────┤
│"lineare Algebra"                       │
├────────────────────────────────────────┤
│"Formale Sprachen und Automaten"        │
├────────────────────────────────────────┤
│"Informatik als Disziplin"              │
├────────────────────────────────────────┤
│"Informatik und Gesellschaft"           │
├────────────────────────────────────────┤
│"IT-Sicherheit"                         │
├────────────────────────────────────────┤
│"Mensch-Computer-Interaktion"           │
├────────────────────────────────────────┤
│"Modellierung"                          │
├────────────────────────────────────────┤
│"Programmiersprachen und -methodik"     │
├────────────────────────────────────────┤
│"Projekt- und Teamkompetenz"            │
├────────────────────────────────────────┤
│"Rechnernetze und verteilte Systeme"    │
├────────────────────────────────────────┤
│"Software-Engineering"                  │
├────────────────────────────────────────┤
│"Wahrscheinlichkeitstheorie"            │
├────────────────────────────────────────┤
│"Statistik"                             │
├────────────────────────────────────────┤
│"Topologie"                             │
├────────────────────────────────────────┤
│"Differentialgeometrie"                 │
├────────────────────────────────────────┤
│"Robotik"                               │
├────────────────────────────────────────┤
│"Künstliche Intelligenz"                │
├────────────────────────────────────────┤
│"Analytische Geometrie"                 │
├────────────────────────────────────────┤
│"Dummy Competence"                      │
└────────────────────────────────────────┘
'''



# stuff that makes everything fail -------------------------------------------------------------------------------------
# translation = gettext.translation(domain="modul_graph", localedir="./locales", languages=["de"])
# translation.install()
# uvicorn.run(app="modul_graph.fastapi:app", port=8080, reload=True)
