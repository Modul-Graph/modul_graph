"""
This file contains all routes that get, create, edit or delete modules
"""
from fastapi import APIRouter, Response
from modul_graph.utils.module_router_service import ModuleRouterService
from modul_graph.DTOs import ModuleDTO

router = APIRouter(prefix="/module")


@router.get("/{name}")
async def get_module(name: str) -> ModuleDTO:
    return ModuleRouterService().get_module(name)


@router.get("/{name}/winter_summer_info")
async def get_module_winter_summer_info(name: str) -> tuple[bool, bool]:
    """
    Returns if the module is currently offered in winter and/or summer semester. This only applies to pflichtmodules
    WPF modules are always (False, False)
    :param name:
    :return: tuple of form (offered in winter, offered in summer)
    """
    return ModuleRouterService().get_winter_summer_info(name)


@router.post("/elective/")
async def create_elective_module(module: ModuleDTO) -> Response:
    ModuleRouterService().create_module(module)
    return Response(status_code=201)


@router.post("/required/")
async def create_required_module(module: ModuleDTO) -> Response:
    ModuleRouterService().create_required_module(module)  # type: ignore
    return Response(status_code=201)


@router.delete("/elective/{name}")
async def delete_elective_module(name: str) -> Response:
    ModuleRouterService().delete_module(name)
    return Response(status_code=200)


@router.delete("/required/{name}")
async def delete_required_module(name: str) -> Response:
    ModuleRouterService().delete_required_module(name)
    return Response(status_code=200)


@router.put("/{name}")  # old name (unique) as path param
async def update_module(name: str, module: ModuleDTO) -> Response:
    ModuleRouterService().update_module(name, module)
    return Response(status_code=200)
