from modul_graph.models.study_exam_rules import StudyExamRules
from modul_graph.static.spo_2017_inf_wise._semesters import semesters

spo_2017_inf_wise = StudyExamRules()
spo_2017_inf_wise.name = "SPO 2017 Informatik (Start Wintersemester)"

for s in semesters:
    spo_2017_inf_wise.specifies_semester.connect(s)

spo_2017_inf_wise.save()