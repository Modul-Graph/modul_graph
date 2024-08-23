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


@router.post("/")
async def create_module(module: ModuleDTO) -> Response:
    ModuleRouterService().create_module(module)
    return Response(status_code=201)


@router.delete("/{name}")
async def delete_module(name: str) -> Response:
    ModuleRouterService().delete_module(name)
    return Response(status_code=200)


@router.put("/{name}")  # old name (unique) as path param
async def update_module(name: str, module: ModuleDTO) -> Response:
    ModuleRouterService().update_module(name, module)
    return Response(status_code=200)

