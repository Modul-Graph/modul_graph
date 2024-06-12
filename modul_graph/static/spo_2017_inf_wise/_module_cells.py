import uuid

from modul_graph.models.module_cell import ModuleCell

module_cells: list[ModuleCell] = []

for i in range(37):
    module_cell = ModuleCell()
    module_cell.identifier = uuid.uuid4()
    module_cells.append(module_cell)

