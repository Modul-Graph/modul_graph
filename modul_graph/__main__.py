import gettext

import uvicorn
from neomodel import config, db  # type: ignore
from rich.pretty import pretty_repr

from modul_graph.experiments.pygad_suggestions import Suggestion
from modul_graph.models.competence import Competence
from modul_graph.models.module import Module
from modul_graph.models.semester import Semester
from modul_graph.models.standard_curriculum import StandardCurriculum

# from modul_graph.utils.std_curr import instantiate_std_curr_obj

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
# print(get_example_graph("Diskrete Strukturen", "SPO 2017 Informatik (Start Wintersemester)"))

# sc = StandardCurriculum.nodes.get(name="SPO 2017 Informatik (Start Wintersemester)")
# sem = Semester.nodes.get(number=2)
# module = Module.nodes.get(name="Grundlagen der Theoretischen Informatik II")
# competence = Competence.nodes.get(name="Informatik als Disziplin")
#
# s = Suggestion(sc, {competence})
# print(pretty_repr(s.__gen_suggested_wpf()))

#print(get_unmet_prerequisites_of_module(module, sc, sem, set()))


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

translation = gettext.translation(domain="modul_graph", localedir="./locales", languages=["de"])
translation.install()
uvicorn.run(app="modul_graph.fast_api:app", port=8080, workers=4)
