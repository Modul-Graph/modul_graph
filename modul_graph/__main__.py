from neomodel import config, db, remove_all_labels, install_all_labels

config.DATABASE_URL = 'bolt://neo4j:dev_pw@neo4j:7687'  # default
results, meta = db.cypher_query("MATCH (n) DETACH DELETE n")

import modul_graph.static.spo_2017_inf_wise.SER

results, meta = db.cypher_query("MATCH (n) RETURN n")c

"""
print(results)
remove_all_labels()
install_all_labels()

c1 = Competence(name="C1").save()
c2 = Competence(name="C2").save()
c3 = Competence(name="C3").save()
m1 = Module(name="M1").save()
m2 = Module(name="M2").save()
m3 = Module(name="M3").save()
m4 = Module(name="M4").save()
r1 = Requirement(name="R1", semester=1).save()
r2 = Requirement(name="R2", semester=2).save()
r3 = Requirement(name="R3", semester=3).save()

m1.fulfills.connect(r1)
m1.fulfills.connect(r2)
m1.provides.connect(c1)


m2.needs.connect(c1)
m2.provides.connect(c2)
m2.fulfills.connect(r3)

m3.needs.connect(c2)
m3.provides.connect(c3)
m3.fulfills.connect(r3)

m4.requires.connect(r1)
m4.requires.connect(r2)
m4.requires.connect(r3)
"""
