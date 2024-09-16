from fastapi import APIRouter, HTTPException

from modul_graph.DTOs import CellDTO
from modul_graph.models.module_area import ModuleArea
from modul_graph.models.module_cell import ModuleCell
from modul_graph.utils.module_area_router_service import ModuleAreaRouterService
from modul_graph.utils.module_router_service import ModuleRouterService

router = APIRouter(prefix="/cell")


@router.get("/{cell_id}")
def get_cell_data(cell_id: str) -> CellDTO:
    print(cell_id)
    cell: ModuleCell | None = ModuleCell.nodes.first_or_none(identifier=cell_id)
    print(ModuleCell.nodes.all())

    if cell is None:
        raise HTTPException(404, f"Cell with id {cell_id} not found")

    module_area: ModuleArea = cell.filled_by_module_area.single()

    if module_area.is_wpf:
        return CellDTO(contains_wpf=True, data=ModuleAreaRouterService().get_module_area(module_area.name))
    else:
        return CellDTO(contains_wpf=False,
                       data=ModuleRouterService().get_module(module_area.filled_by_module.single().name))


