import modul_graph.static.spo_2017_inf_wise._modules as _modules
from modul_graph.models.module import Module
from modul_graph.models.standard_curriculum import StandardCurriculum
from modul_graph.static.spo_2017_inf_wise._semesters import semesters

spo_2017_inf_wise = StandardCurriculum()
spo_2017_inf_wise.name = "SPO 2017 Informatik (Start Wintersemester)"
spo_2017_inf_wise.start_winter = True
spo_2017_inf_wise.save()

for s in semesters:
    spo_2017_inf_wise.specifies_semester.connect(s)

for v in _modules.__dict__.values():
    if isinstance(v, Module):
        v.belongs_to_standard_curriculum.connect(spo_2017_inf_wise)
