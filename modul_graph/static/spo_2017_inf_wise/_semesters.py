from modul_graph.models.semester import Semester
from modul_graph.models.study_exam_rules import StudyExamRules

semesters: list[Semester] = []

for i in range(7):
    semester = Semester()
    semester.number = i + 1

    semesters.append(semester)
