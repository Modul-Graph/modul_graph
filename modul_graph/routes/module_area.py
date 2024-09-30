from fastapi import APIRouter, Response

from modul_graph.DTOs import ModuleAreaDTO
from modul_graph.utils.module_area_router_service import ModuleAreaRouterService  # type: ignore

router = APIRouter(
    prefix="/module_area",
)


@router.get("/{name}")
async def get_module_area(name: str) -> ModuleAreaDTO:
    return ModuleAreaRouterService().get_module_area(name)


@router.post("/")
async def create_module_area(mod_ar: ModuleAreaDTO) -> Response:
    ModuleAreaRouterService().create_module_area(mod_ar)
    return Response(status_code=201)


@router.delete("/{name}")
async def delete_module_area(name: str) -> Response:
    ModuleAreaRouterService().delete_module_area(name)  # type: ignore
    return Response(status_code=200)


@router.put("/{name}")  # old name (unique) as path param
async def update_module_area(name: str, mod_ar: ModuleAreaDTO) -> Response:
    ModuleAreaRouterService().update_module_area(name, mod_ar)  # type: ignore
    return Response(status_code=200)
