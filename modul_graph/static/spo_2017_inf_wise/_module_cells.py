import uuid

from modul_graph.models.module_cell import ModuleCell
from modul_graph.static.spo_2017_inf_wise._module_area import *

module_cells: list[ModuleCell] = []

for i in range(37):
    module_cell = ModuleCell()
    module_cell.identifier = uuid.uuid4()
    module_cell.save()
    module_cells.append(module_cell)

# Semester 1
module_cells[0].filled_by_module_area.connect(einf_inf)
module_cells[1].filled_by_module_area.connect(datenbanken)
module_cells[2].filled_by_module_area.connect(ti_1)
module_cells[3].filled_by_module_area.connect(mathe_1)
module_cells[4].filled_by_module_area.connect(schlüko_1)

# Semester 2
module_cells[5].filled_by_module_area.connect(aud)
module_cells[6].filled_by_module_area.connect(modellierung)
module_cells[7].filled_by_module_area.connect(ti_2)
module_cells[8].filled_by_module_area.connect(mathe_2)
module_cells[9].filled_by_module_area.connect(logik)
module_cells[10].filled_by_module_area.connect(schlüko_2)

# Semester 3
module_cells[11].filled_by_module_area.connect(i_s)
module_cells[12].filled_by_module_area.connect(itpm)
module_cells[13].filled_by_module_area.connect(wpf_ti)
module_cells[14].filled_by_module_area.connect(mathe_3)
module_cells[15].filled_by_module_area.connect(theo_inf_1)
module_cells[16].filled_by_module_area.connect(nebenfach1)
module_cells[17].filled_by_module_area.connect(trainingsmodul_smk)

# Semester 4
module_cells[18].filled_by_module_area.connect(sisi)
module_cells[19].filled_by_module_area.connect(pgp)
module_cells[20].filled_by_module_area.connect(se)
module_cells[21].filled_by_module_area.connect(theo_inf_2)
module_cells[22].filled_by_module_area.connect(nebenfach2)
module_cells[23].filled_by_module_area.connect(softwareproject)

# Semester 5
module_cells[24].filled_by_module_area.connect(wpf_inf_mat)
module_cells[25].filled_by_module_area.connect(wpf_inf)
module_cells[26].filled_by_module_area.connect(wpf_inf)
module_cells[27].filled_by_module_area.connect(wpf_inf)
module_cells[28].filled_by_module_area.connect(nebenfach3)
module_cells[29].filled_by_module_area.connect(wiss_seminar)

# Semester 6
module_cells[30].filled_by_module_area.connect(wpf_inf)
module_cells[31].filled_by_module_area.connect(wpf_inf)
module_cells[32].filled_by_module_area.connect(wpf_inf)
module_cells[33].filled_by_module_area.connect(wpf_inf)
module_cells[34].filled_by_module_area.connect(wpf_ti)
module_cells[35].filled_by_module_area.connect(wpf_fin_smk)

# Semester 7
module_cells[36].filled_by_module_area.connect(ba_praktikum)
