from uuid import uuid4

from neomodel import db

from modul_graph.DTOs import UpdateCPClusterDTO
from modul_graph.models.cp_cluster import CpCluster
from modul_graph.models.module import Module
from modul_graph.models.module_area import ModuleArea
from modul_graph.models.module_cell import ModuleCell
from modul_graph.models.semester import Semester


@db.transaction
def util_update_cp_cluster(cp_cluster: CpCluster, cp_cluster_update: UpdateCPClusterDTO) -> None:
    cp_cluster.cp_number_grade = cp_cluster_update.cp_note

    cells: list[ModuleCell] = cp_cluster.consists_of_module_cell.all()
    for _cell in cells:
        _cell.delete()

    for cell in cp_cluster_update.cells:
        semester: int = cell.sem
        semester = Semester.nodes.get_or_none(number=semester)

        if semester is None:
            continue

        module_cell: ModuleCell = ModuleCell(identifier=uuid4())
        module_cell.save()
        module_cell.is_in_semester.connect(semester)

        module_area: ModuleArea

        if cell.isWPF:
            module_area = ModuleArea.nodes.get_or_none(name=cell.name)

            if module_area is None:
                continue
        else:
            module: Module = Module.nodes.get_or_none(name=cell.name)

            if module is None:
                continue

            module_area = module.fills_module_area.single()

        module_cell.filled_by_module_area.connect(module_area)

        cp_cluster.consists_of_module_cell.connect(module_cell)
