from modul_graph.models.semester import Semester
from modul_graph.models.study_exam_rules import StudyExamRules
from modul_graph.static.spo_2017_inf_wise._cp_cluster import *
from modul_graph.static.spo_2017_inf_wise._module_cells import module_cells

semesters: list[Semester] = []

for i in range(7):
    semester = Semester()
    semester.number = i + 1
    semester.save()

    semesters.append(semester)

# module cells for semester 1
for module_cell in module_cells[:5]:
    semesters[0].contains_module_cell.connect(module_cell)

# module cells for semester 2
for module_cell in module_cells[5:11]:
    semesters[1].contains_module_cell.connect(module_cell)

# module cells for semester 3
for module_cell in module_cells[11:18]:
    semesters[2].contains_module_cell.connect(module_cell)

# module cells for semester 4
for module_cell in module_cells[18:24]:
    semesters[3].contains_module_cell.connect(module_cell)

# module cells for semester 5
for module_cell in module_cells[24:30]:
    semesters[4].contains_module_cell.connect(module_cell)

# module cells for semester 6
for module_cell in module_cells[30:36]:
    semesters[5].contains_module_cell.connect(module_cell)

# module cells for semester 7
for module_cell in module_cells[36:37]:
    semesters[6].contains_module_cell.connect(module_cell)

# connect CP clusters

semesters[0].consists_of_cp_cluster.connect(cp_cluster_1)

semesters[0].consists_of_cp_cluster.connect(cp_cluster_2)
semesters[1].consists_of_cp_cluster.connect(cp_cluster_2)

semesters[0].consists_of_cp_cluster.connect(cp_cluster_3)
semesters[1].consists_of_cp_cluster.connect(cp_cluster_3)

semesters[0].consists_of_cp_cluster.connect(cp_cluster_4)
semesters[1].consists_of_cp_cluster.connect(cp_cluster_4)

semesters[0].consists_of_cp_cluster.connect(cp_cluster_5)
semesters[1].consists_of_cp_cluster.connect(cp_cluster_5)

semesters[2].consists_of_cp_cluster.connect(cp_cluster_6)
semesters[3].consists_of_cp_cluster.connect(cp_cluster_6)

semesters[2].consists_of_cp_cluster.connect(cp_cluster_7)
semesters[3].consists_of_cp_cluster.connect(cp_cluster_7)

semesters[2].consists_of_cp_cluster.connect(cp_cluster_8)
semesters[5].consists_of_cp_cluster.connect(cp_cluster_8)

semesters[2].consists_of_cp_cluster.connect(cp_cluster_9)
semesters[3].consists_of_cp_cluster.connect(cp_cluster_9)

semesters[2].consists_of_cp_cluster.connect(cp_cluster_10)
semesters[3].consists_of_cp_cluster.connect(cp_cluster_10)
semesters[4].consists_of_cp_cluster.connect(cp_cluster_10)

semesters[2].consists_of_cp_cluster.connect(cp_cluster_11)

semesters[3].consists_of_cp_cluster.connect(cp_cluster_12)
semesters[4].consists_of_cp_cluster.connect(cp_cluster_12)
semesters[5].consists_of_cp_cluster.connect(cp_cluster_12)

semesters[4].consists_of_cp_cluster.connect(cp_cluster_13)
semesters[5].consists_of_cp_cluster.connect(cp_cluster_13)

semesters[6].consists_of_cp_cluster.connect(cp_cluster_14)
