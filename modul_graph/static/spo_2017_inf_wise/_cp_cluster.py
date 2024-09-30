from uuid import uuid4

from modul_graph.models.cp_cluster import CpCluster
from modul_graph.static.spo_2017_inf_wise._module_cells import module_cells

# CP Cluster 1 (Einfinf)
cp_cluster_1 = CpCluster()
cp_cluster_1.identifier = uuid4()
cp_cluster_1.cp_number = 8
cp_cluster_1.cp_number_grade = 1
cp_cluster_1.save()

cp_cluster_1.consists_of_module_cell.connect(module_cells[0])

# CP Cluster 2 (DB)
cp_cluster_2 = CpCluster()
cp_cluster_2.identifier = uuid4()
cp_cluster_2.cp_number = 6
cp_cluster_2.cp_number_grade = -1
cp_cluster_2.save()

cp_cluster_2.consists_of_module_cell.connect(module_cells[1])
cp_cluster_2.consists_of_module_cell.connect(module_cells[5])
cp_cluster_2.consists_of_module_cell.connect(module_cells[6])

# CP Cluster 3 (TI)
cp_cluster_3 = CpCluster()
cp_cluster_3.identifier = uuid4()
cp_cluster_3.cp_number = 5
cp_cluster_3.cp_number_grade = -1
cp_cluster_3.save()

cp_cluster_3.consists_of_module_cell.connect(module_cells[2])
cp_cluster_2.consists_of_module_cell.connect(module_cells[7])

# CP Cluster 4 (Mathe I)
cp_cluster_4 = CpCluster()
cp_cluster_4.identifier = uuid4()
cp_cluster_4.cp_number = 12
cp_cluster_4.cp_number_grade = -1
cp_cluster_4.save()

cp_cluster_4.consists_of_module_cell.connect(module_cells[3])
cp_cluster_4.consists_of_module_cell.connect(module_cells[8])
cp_cluster_4.consists_of_module_cell.connect(module_cells[9])

# CP Cluster 5 (Schlüko)
cp_cluster_5 = CpCluster()
cp_cluster_5.identifier = uuid4()
cp_cluster_5.cp_number = 6
cp_cluster_5.cp_number_grade = -1
cp_cluster_5.save()

cp_cluster_5.consists_of_module_cell.connect(module_cells[4])
cp_cluster_5.consists_of_module_cell.connect(module_cells[10])

# CP Cluster 6 (SiSi)
cp_cluster_6 = CpCluster()
cp_cluster_6.identifier = uuid4()
cp_cluster_6.cp_number = 10
cp_cluster_6.cp_number_grade = -1
cp_cluster_6.save()

cp_cluster_6.consists_of_module_cell.connect(module_cells[11])
cp_cluster_6.consists_of_module_cell.connect(module_cells[18])
cp_cluster_6.consists_of_module_cell.connect(module_cells[19])

# CP Cluster 7 (IT-PM)
cp_cluster_7 = CpCluster()
cp_cluster_7.identifier = uuid4()
cp_cluster_7.cp_number = 3
cp_cluster_7.cp_number_grade = -1
cp_cluster_7.save()

cp_cluster_7.consists_of_module_cell.connect(module_cells[12])
cp_cluster_7.consists_of_module_cell.connect(module_cells[20])

# CP Cluster 8 (WPF TI)
cp_cluster_8 = CpCluster()
cp_cluster_8.identifier = uuid4()
cp_cluster_8.cp_number = 5
cp_cluster_8.cp_number_grade = -1
cp_cluster_8.save()

cp_cluster_8.consists_of_module_cell.connect(module_cells[13])
cp_cluster_8.consists_of_module_cell.connect(module_cells[34])

# CP Cluster 9 (Mathe III)
cp_cluster_9 = CpCluster()
cp_cluster_9.identifier = uuid4()
cp_cluster_9.cp_number = 10
cp_cluster_9.cp_number_grade = -1
cp_cluster_9.save()

cp_cluster_9.consists_of_module_cell.connect(module_cells[14])
cp_cluster_9.consists_of_module_cell.connect(module_cells[15])
cp_cluster_9.consists_of_module_cell.connect(module_cells[21])

# CP Cluster 10 (Nebenfach)
cp_cluster_10 = CpCluster()
cp_cluster_10.identifier = uuid4()
cp_cluster_10.cp_number = 10
cp_cluster_10.cp_number_grade = -1
cp_cluster_10.save()

cp_cluster_10.consists_of_module_cell.connect(module_cells[16])
cp_cluster_10.consists_of_module_cell.connect(module_cells[22])
cp_cluster_10.consists_of_module_cell.connect(module_cells[28])

# CP Cluster 11 (Trainingsmodul SMK)
cp_cluster_11 = CpCluster()
cp_cluster_11.identifier = uuid4()
cp_cluster_11.cp_number = 0
cp_cluster_11.cp_number_grade = -1
cp_cluster_11.save()

cp_cluster_11.consists_of_module_cell.connect(module_cells[17])

# CP Cluster 12 (Softwareorojekt)
cp_cluster_12 = CpCluster()
cp_cluster_12.identifier = uuid4()
cp_cluster_12.cp_number = 8
cp_cluster_12.cp_number_grade = -1
cp_cluster_12.save()

cp_cluster_12.consists_of_module_cell.connect(module_cells[23])
cp_cluster_12.consists_of_module_cell.connect(module_cells[29])
cp_cluster_12.consists_of_module_cell.connect(module_cells[35])

# CP Cluster 13 (WPF Informatik)
cp_cluster_13 = CpCluster()
cp_cluster_13.identifier = uuid4()
cp_cluster_13.cp_number = 20
cp_cluster_13.cp_number_grade = -1
cp_cluster_13.save()

cp_cluster_13.consists_of_module_cell.connect(module_cells[24])
cp_cluster_13.consists_of_module_cell.connect(module_cells[25])
cp_cluster_13.consists_of_module_cell.connect(module_cells[26])
cp_cluster_13.consists_of_module_cell.connect(module_cells[27])
cp_cluster_13.consists_of_module_cell.connect(module_cells[30])
cp_cluster_13.consists_of_module_cell.connect(module_cells[31])
cp_cluster_13.consists_of_module_cell.connect(module_cells[32])
cp_cluster_13.consists_of_module_cell.connect(module_cells[33])

# CP Cluster 14 (Bachelorarbeit/Praktikum)
cp_cluster_14 = CpCluster()
cp_cluster_14.identifier = uuid4()
cp_cluster_14.cp_number = 30
cp_cluster_14.cp_number_grade = -1
cp_cluster_14.save()

cp_cluster_14.consists_of_module_cell.connect(module_cells[36])
